"""YouTube Music service implementation."""

import sys

from ytmusicapi import YTMusic
from ytmusicapi.models.content.enums import LikeStatus
from rich.progress import Progress, SpinnerColumn, TextColumn

from pushtunes.models.album import Album
from pushtunes.models.track import Track
from pushtunes.services.music_service import MusicService
from pushtunes.utils.logging import get_logger


class YTMService(MusicService):
    """YouTube Music service implementation."""

    def __init__(
        self,
        min_similarity: float = 0.8,
        auth_file: str = "browser.json",
    ):
        """Initialize YouTube Music service.

        Args:
            min_similarity: Minimum similarity score for matching albums
            auth_file: Path to YTMusic authentication file
        """
        try:
            self.yt: YTMusic = YTMusic(auth_file)
            self.service_name: str = "ytm"
        except Exception as e:
            raise RuntimeError(f"Error initializing YouTube Music: {e}")
        super().__init__()
        self.min_similarity = min_similarity
        self.log = get_logger()

    def search_albums(self, album: Album) -> list[Album]:
        """Search for albums matching artist and title.

        Args:
            album: Album object with "artist" and "title" filled in

        Returns:
            List of matching Album objects
        """
        try:
            search_query = album.search_string(service_name=self.service_name)
            search_results = self.yt.search(
                search_query, ignore_spelling=False, filter="albums"
            )

            albums = []
            for result in search_results:
                album = self._ytm_album_to_album(result)
                albums.append(album)

            return albums

        except Exception as e:
            self.log.error(f"Error searching for {album.artist} - {album.title}: {e}")
            return []

    def add_album(self, album: Album) -> bool:
        """Add an album to the user's YouTube Music library.

        Args:
            album: Album object to add

        Returns:
            True if successfully added, False otherwise
        """
        try:
            if not album.service_id:
                self.log.error(
                    f"Cannot add album without playlist ID: {album.artist} - {album.title}"
                )
                return False

            # In YTM, adding an album means rating its playlist as LIKE
            _ = self.yt.rate_playlist(album.service_id, rating=LikeStatus.LIKE)
            return True

        except Exception as e:
            self.log.error(f"Error adding album {album.artist} - {album.title}: {e}")
            return False

    def remove_album(self, album: Album) -> bool:
        """Remove an album from the user's YouTube Music library.

        Args:
            album: Album object to remove (must have service_id set)

        Returns:
            True if successfully removed, False otherwise
        """
        try:
            if not album.service_id:
                self.log.error(
                    f"Cannot remove album without playlist ID: {album.artist} - {album.title}"
                )
                return False

            # In YTM, removing an album means rating its playlist as INDIFFERENT
            _ = self.yt.rate_playlist(album.service_id, rating=LikeStatus.INDIFFERENT)
            return True

        except Exception as e:
            self.log.error(f"Error removing album {album.artist} - {album.title}: {e}")
            return False

    def _ytm_album_to_album(self, ytm_album: dict[str, str]):
        # YTM albums have artists as a list
        artist_names: list[str] = []
        for artist in ytm_album.get("artists", []):
            if isinstance(artist, dict):
                artist_names.append(artist.get("name", ""))
            else:
                artist_names.append(str(artist))

        title: str = ytm_album.get("title", "Unknown")
        year: int = ytm_album.get("year")
        ytm_id: str = ytm_album.get("playlistId")

        album = Album(
            artists=artist_names if artist_names else ["Unknown"],
            title=title,
            year=year,
            service_name="ytm",
            service_id=ytm_id,  # YTM uses playlistId for albums
            extra_data=ytm_album,
        )
        return album

    def get_library_albums(self) -> list[Album]:
        """Fetch library albums from YTM API or local JSON cache file.

        Raises:
            ytmusicapi.exceptions.YTMusicUserError: If authentication fails
            ytmusicapi.exceptions.YTMusicServerError: If server error occurs
            ytmusicapi.exceptions.YTMusicError: For other API errors
        """
        from ytmusicapi.exceptions import YTMusicError

        try:
            # Check if we're running in a TTY (not piped)
            show_progress = sys.stdout.isatty()

            if show_progress:
                # Show spinner while fetching (YTM doesn't provide total count)
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                ) as progress:
                    task = progress.add_task("[cyan]Fetching YTM albums...", total=None)
                    ytm_albums = self.yt.get_library_albums(limit=20000)
                    progress.update(task, total=len(ytm_albums), completed=len(ytm_albums))
            else:
                # No progress indicator, simple fetch
                ytm_albums = self.yt.get_library_albums(limit=20000)

            for ytm_album in ytm_albums:
                album = self._ytm_album_to_album(ytm_album)
                self.cache.albums.append(album)

            self.log.info(
                f"Fetched {len(self.cache.albums)} albums from YouTube Music library"
            )

            return self.cache.albums

        except YTMusicError as e:
            self.log.error(
                f"YouTube Music API error: {e}. Please check your authentication."
            )
            # Re-raise so the error propagates and we don't save empty cache
            raise
        except Exception as e:
            self.log.error(f"Unexpected error getting YouTube Music albums: {e}")
            raise

    def is_album_in_library(self, album: Album) -> bool:
        """Check if an album is already in the user's library.

        This uses the similarity matching logic to account for discrepancies
        between how different services structure artist names.

        Args:
            album: Album to check

        Returns:
            True if album is in library, False otherwise

        Raises:
            Exception: If cache loading fails (e.g., authentication issues)
        """
        from pushtunes.utils.similarity import get_best_match

        if len(self.cache.albums) == 0:
            # If this raises an exception (e.g., auth failure), let it propagate
            self.cache.load_album_cache()

        # If the album has a service_id, check for exact ID match first
        if album.service_id:
            for cached_album in self.cache.albums:
                if cached_album.service_id == album.service_id:
                    return True

        # Use similarity matching against the cache instead of a direct `in` check,
        # as the __eq__ method would fail on artist parsing discrepancies.
        best_match, _ = get_best_match(album, self.cache.albums, self.min_similarity)
        if best_match:
            return True
        return False

    def _ytm_track_to_track(self, ytm_track: dict) -> Track:
        """Convert a YTM track dictionary to a Track object."""
        artist_names: list[str] = []
        for artist in ytm_track.get("artists", []):
            if isinstance(artist, dict):
                artist_names.append(artist.get("name", ""))
            else:
                artist_names.append(str(artist))

        title: str = ytm_track.get("title", "Unknown")
        video_id: str = ytm_track.get("videoId")

        album_name = None
        if "album" in ytm_track and ytm_track["album"]:
            if isinstance(ytm_track["album"], dict):
                album_name = ytm_track["album"].get("name")
            else:
                album_name = str(ytm_track["album"])

        year = ytm_track.get("year")

        track = Track(
            artists=artist_names if artist_names else ["Unknown"],
            title=title,
            album=album_name,
            year=year,
            service_name="ytm",
            service_id=video_id,
            extra_data=ytm_track,
        )
        return track

    def get_library_tracks(self) -> list[Track]:
        """Fetch library tracks from YTM API.

        Note: YTM doesn't have a direct "liked tracks" concept like Spotify.
        This fetches tracks from the user's liked songs playlist.

        Raises:
            ytmusicapi.exceptions.YTMusicError: For API errors
        """
        from ytmusicapi.exceptions import YTMusicError

        try:
            # Check if we're running in a TTY (not piped)
            show_progress = sys.stdout.isatty()

            if show_progress:
                # Show spinner while fetching (YTM doesn't provide total count)
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                ) as progress:
                    task = progress.add_task("[cyan]Fetching YTM tracks...", total=None)
                    ytm_tracks = self.yt.get_liked_songs(limit=10000)

                    if "tracks" in ytm_tracks:
                        progress.update(task, total=len(ytm_tracks["tracks"]), completed=len(ytm_tracks["tracks"]))
            else:
                # No progress indicator, simple fetch
                ytm_tracks = self.yt.get_liked_songs(limit=10000)

            if "tracks" in ytm_tracks:
                for ytm_track in ytm_tracks["tracks"]:
                    track = self._ytm_track_to_track(ytm_track)
                    self.cache.tracks.append(track)

            self.log.info(
                f"Fetched {len(self.cache.tracks)} tracks from YouTube Music library"
            )

            return self.cache.tracks

        except YTMusicError as e:
            self.log.error(
                f"YouTube Music API error: {e}. Please check your authentication."
            )
            raise
        except Exception as e:
            self.log.error(f"Unexpected error getting YouTube Music tracks: {e}")
            raise

    def search_tracks(self, track: Track) -> list[Track]:
        """Search for tracks matching artist and title.

        Args:
            track: Track object with artist and title

        Returns:
            List of matching Track objects
        """
        try:
            search_query = track.search_string(service_name=self.service_name)
            search_results = self.yt.search(
                search_query, filter="songs", limit=5
            )

            tracks = []
            for result in search_results:
                found_track = self._ytm_track_to_track(result)
                tracks.append(found_track)

            return tracks

        except Exception as e:
            self.log.error(f"Error searching for {track.artist} - {track.title}: {e}")
            return []

    def add_track(self, track: Track) -> bool:
        """Add a track to the user's YouTube Music library.

        Args:
            track: Track object to add

        Returns:
            True if successfully added, False otherwise
        """
        try:
            if not track.service_id:
                self.log.error(
                    f"Cannot add track without video ID: {track.artist} - {track.title}"
                )
                return False

            # In YTM, adding a track means rating it as LIKE
            _ = self.yt.rate_song(track.service_id, rating=LikeStatus.LIKE)
            return True

        except Exception as e:
            self.log.error(f"Error adding track {track.artist} - {track.title}: {e}")
            return False

    def remove_track(self, track: Track) -> bool:
        """Remove a track from the user's YouTube Music library.

        Args:
            track: Track object to remove (must have service_id set)

        Returns:
            True if successfully removed, False otherwise
        """
        try:
            if not track.service_id:
                self.log.error(
                    f"Cannot remove track without video ID: {track.artist} - {track.title}"
                )
                return False

            # In YTM, removing a track means rating it as INDIFFERENT
            _ = self.yt.rate_song(track.service_id, rating=LikeStatus.INDIFFERENT)
            return True

        except Exception as e:
            self.log.error(f"Error removing track {track.artist} - {track.title}: {e}")
            return False

    def is_track_in_library(self, track: Track) -> bool:
        """Check if a track is already in the user's library.

        Args:
            track: Track to check

        Returns:
            True if track is in library, False otherwise

        Raises:
            Exception: If cache loading fails
        """
        from pushtunes.utils.similarity import get_best_match

        if len(self.cache.tracks) == 0:
            self.cache.load_track_cache()

        # If the track has a service_id, check for exact ID match first
        if track.service_id:
            for cached_track in self.cache.tracks:
                if cached_track.service_id == track.service_id:
                    return True

        best_match, _ = get_best_match(track, self.cache.tracks, self.min_similarity)
        if best_match:
            return True
        return False

    def create_playlist(self, name: str, description: str = "") -> str | None:
        """Create a new playlist on YouTube Music.

        Args:
            name: Playlist name
            description: Playlist description (optional)

        Returns:
            Playlist ID if successful, None otherwise
        """
        try:
            playlist_id = self.yt.create_playlist(
                title=name,
                description=description,
                privacy_status="PRIVATE"
            )

            self.log.info(f"Created playlist '{name}' with ID: {playlist_id}")
            return playlist_id

        except Exception as e:
            self.log.error(f"Error creating playlist '{name}': {e}")
            return None

    def get_user_playlists(self) -> list[dict]:
        """Get all playlists owned by the current user.

        Returns:
            List of playlist dictionaries with 'id' and 'name' keys
        """
        try:
            playlists_raw = self.yt.get_library_playlists(limit=None)

            playlists = []
            for pl in playlists_raw:
                playlists.append({
                    "id": pl["playlistId"],
                    "name": pl["title"],
                    "track_count": pl.get("count", 0)
                })

            return playlists

        except Exception as e:
            self.log.error(f"Error fetching user playlists: {e}")
            return []

    def get_playlist_tracks(self, playlist_id: str) -> list[Track]:
        """Get all tracks from a playlist.

        Args:
            playlist_id: YTM playlist ID

        Returns:
            List of Track objects
        """
        try:
            playlist_data = self.yt.get_playlist(playlist_id, limit=None)

            tracks = []
            if "tracks" in playlist_data:
                for track_data in playlist_data["tracks"]:
                    track = self._ytm_track_to_track(track_data)
                    # Store setVideoId for removal operations
                    if "setVideoId" in track_data:
                        if not track.extra_data:
                            track.extra_data = {}
                        track.extra_data["setVideoId"] = track_data["setVideoId"]
                    tracks.append(track)

            return tracks

        except Exception as e:
            self.log.error(f"Error fetching playlist tracks: {e}")
            return []

    def replace_playlist_tracks(self, playlist_id: str, track_ids: list[str]) -> bool:
        """Replace all tracks in a playlist.

        Args:
            playlist_id: ID of the playlist
            track_ids: List of YTM video IDs to replace with

        Returns:
            True if successful, False otherwise
        """
        try:
            # Get existing tracks to remove them
            existing_tracks = self.get_playlist_tracks(playlist_id)

            # Remove all existing tracks
            if existing_tracks:
                videos_to_remove = []
                for track in existing_tracks:
                    if track.extra_data and "setVideoId" in track.extra_data:
                        videos_to_remove.append({
                            "videoId": track.service_id,
                            "setVideoId": track.extra_data["setVideoId"]
                        })

                if videos_to_remove:
                    self.yt.remove_playlist_items(playlist_id, videos_to_remove)

            # Add new tracks
            if track_ids:
                self.yt.add_playlist_items(playlist_id, videoIds=track_ids)

            self.log.info(f"Replaced playlist {playlist_id} with {len(track_ids)} tracks")
            return True

        except Exception as e:
            self.log.error(f"Error replacing playlist tracks: {e}")
            return False

    def remove_tracks_from_playlist(self, playlist_id: str, track_ids: list[str]) -> bool:
        """Remove tracks from a playlist.

        Args:
            playlist_id: ID of the playlist
            track_ids: List of YTM video IDs to remove

        Returns:
            True if successful, False otherwise
        """
        try:
            # Get all tracks to find setVideoIds
            existing_tracks = self.get_playlist_tracks(playlist_id)

            # Build removal list
            videos_to_remove = []
            for track in existing_tracks:
                if track.service_id in track_ids:
                    if track.extra_data and "setVideoId" in track.extra_data:
                        videos_to_remove.append({
                            "videoId": track.service_id,
                            "setVideoId": track.extra_data["setVideoId"]
                        })

            if videos_to_remove:
                self.yt.remove_playlist_items(playlist_id, videos_to_remove)
                self.log.info(f"Removed {len(videos_to_remove)} tracks from playlist {playlist_id}")
                return True
            else:
                self.log.warning(f"No tracks found to remove from playlist {playlist_id}")
                return True

        except Exception as e:
            self.log.error(f"Error removing tracks from playlist: {e}")
            return False

    def add_tracks_to_playlist(self, playlist_id: str, track_ids: list[str]) -> bool:
        """Add tracks to a YouTube Music playlist.

        Args:
            playlist_id: ID of the playlist to add tracks to
            track_ids: List of YouTube Music video IDs to add

        Returns:
            True if successful, False otherwise
        """
        try:
            # YTM API can handle multiple tracks at once
            self.yt.add_playlist_items(playlist_id, videoIds=track_ids)

            self.log.info(f"Added {len(track_ids)} tracks to playlist {playlist_id}")
            return True

        except Exception as e:
            self.log.error(f"Error adding tracks to playlist {playlist_id}: {e}")
            return False
