"""Tidal music service implementation."""

import os
import sys

import tidalapi
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TaskProgressColumn

from pushtunes.models.album import Album
from pushtunes.models.track import Track
from pushtunes.models.playlist import Playlist
from pushtunes.services.music_service import MusicService
from pushtunes.utils.logging import get_logger


class TidalService(MusicService):
    """Tidal music service implementation."""

    def __init__(
        self,
        min_similarity: float = 0.8,
        client_id: str | None = None,
        client_secret: str | None = None,
        session_file: str = "tidal-session.json",
    ):
        """Initialize Tidal service.
        Args:
            min_similarity: Minimum similarity score for matching albums
            client_id: Tidal client ID (defaults to TIDAL_CLIENT_ID env var)
            client_secret: Tidal client secret (defaults to TIDAL_CLIENT_SECRET env var)
            session_file: Path to Tidal session file (defaults to tidal-session.json)
        """
        self.service_name = "tidal"
        self.session_file = session_file

        # Initialize Tidal client
        self._init_tidal_client()
        super().__init__()
        self.min_similarity = min_similarity
        self.log = get_logger()

    def _init_tidal_client(self):
        """Initialize the Tidal client with authentication."""
        try:
            self.session = tidalapi.Session()

            # Try to use session file authentication (creates file on first login)
            from pathlib import Path
            session_path = Path(self.session_file)

            if not self.session.login_session_file(session_path):
                raise RuntimeError("Tidal authentication failed. Please ensure you complete the OAuth flow.")

            if not self.session.check_login():
                raise RuntimeError("Tidal authentication failed")

        except Exception as e:
            raise RuntimeError(f"Error initializing Tidal: {e}")

    def _tidal_album_to_album(self, tidal_album) -> Album:
        """Convert a Tidal album object to an Album object."""
        # Handle both tidalapi Album objects and dict responses
        if isinstance(tidal_album, dict):
            artist_names = [artist.get("name", "") for artist in tidal_album.get("artists", [])]
            title = tidal_album.get("title", "Unknown")
            service_id = str(tidal_album.get("id"))
            year = tidal_album.get("year")
            extra_data = tidal_album
        else:
            # tidalapi Album object
            artist_names = [artist.name for artist in tidal_album.artists] if hasattr(tidal_album, 'artists') else []
            title = tidal_album.name if hasattr(tidal_album, 'name') else "Unknown"
            service_id = str(tidal_album.id) if hasattr(tidal_album, 'id') else None
            year = tidal_album.year if hasattr(tidal_album, 'year') else None
            extra_data = {"tidal_object": str(tidal_album)}

        album = Album(
            artists=artist_names if artist_names else ["Unknown"],
            title=title,
            year=year,
            service_id=service_id,
            service_name=self.service_name,
            extra_data=extra_data,
        )
        return album

    def get_library_albums(self) -> list[Album]:
        """Fetch library albums from Tidal API.

        Raises:
            Exception: If API error occurs
        """
        try:
            # Clear the cache before fetching
            self.cache.albums = []

            # Check if we're running in a TTY (not piped)
            show_progress = sys.stdout.isatty()

            if show_progress:
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                ) as progress:
                    task = progress.add_task("[cyan]Fetching Tidal albums...", total=None)

                    # Get favorite albums
                    tidal_albums = self.session.user.favorites.albums()

                    progress.update(task, total=len(tidal_albums), completed=len(tidal_albums))
            else:
                # No progress bar, simple fetch
                tidal_albums = self.session.user.favorites.albums()

            # Convert Tidal albums to Album objects
            for tidal_album in tidal_albums:
                album = self._tidal_album_to_album(tidal_album)
                self.cache.albums.append(album)

            self.log.info(f"Fetched {len(self.cache.albums)} albums from Tidal library")

            return self.cache.albums

        except Exception as e:
            self.log.error(
                f"Tidal API error: {e}. Please check your authentication."
            )
            # Re-raise so the error propagates and we don't save empty cache
            raise

    def search_albums(self, album: Album) -> list[Album]:
        """Search for albums matching artist and title.
        Args:
            album: Album object with "artist" and "title" filled in
        Returns:
            List of matching Album objects
        """
        try:
            search_query = album.search_string(service_name=self.service_name)

            search_results = self.session.search(search_query, models=[tidalapi.Album])

            albums = []
            if search_results and "albums" in search_results:
                for item in search_results["albums"][:5]:  # Limit to 5 results
                    found_album = self._tidal_album_to_album(item)
                    albums.append(found_album)

            return albums

        except Exception as e:
            self.log.error(f"Error searching for {album.artist} - {album.title}: {e}")
            return []

    def add_album(self, album: Album) -> bool:
        """Add an album to the user's Tidal library.
        Args:
            album: Album object to add
        Returns:
            True if successfully added, False otherwise
        """
        try:
            if not album.service_id:
                self.log.error(
                    f"Cannot add album without ID: {album.artist} - {album.title}"
                )
                return False

            # Add to favorites using album ID
            self.session.user.favorites.add_album(album.service_id)
            return True
        except Exception as e:
            self.log.error(f"Error adding album {album.artist} - {album.title}: {e}")
            return False

    def remove_album(self, album: Album) -> bool:
        """Remove an album from the user's Tidal library.
        Args:
            album: Album object to remove (must have service_id set)
        Returns:
            True if successfully removed, False otherwise
        """
        try:
            if not album.service_id:
                self.log.error(
                    f"Cannot remove album without ID: {album.artist} - {album.title}"
                )
                return False

            # Remove from favorites using album ID
            self.session.user.favorites.remove_album(album.service_id)
            return True
        except Exception as e:
            self.log.error(f"Error removing album {album.artist} - {album.title}: {e}")
            return False

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

    def _tidal_track_to_track(self, tidal_track) -> Track:
        """Convert a Tidal track object to a Track object."""
        # Handle both tidalapi Track objects and dict responses
        if isinstance(tidal_track, dict):
            artist_names = [artist.get("name", "") for artist in tidal_track.get("artists", [])]
            title = tidal_track.get("title", "Unknown")
            service_id = str(tidal_track.get("id"))
            album_name = tidal_track.get("album", {}).get("title") if "album" in tidal_track else None
            year = tidal_track.get("year")
            extra_data = tidal_track
        else:
            # tidalapi Track object
            artist_names = [artist.name for artist in tidal_track.artists] if hasattr(tidal_track, 'artists') else []
            title = tidal_track.name if hasattr(tidal_track, 'name') else "Unknown"
            service_id = str(tidal_track.id) if hasattr(tidal_track, 'id') else None
            album_name = tidal_track.album.name if hasattr(tidal_track, 'album') and tidal_track.album else None
            year = tidal_track.year if hasattr(tidal_track, 'year') else None
            extra_data = {"tidal_object": str(tidal_track)}

        track = Track(
            artists=artist_names if artist_names else ["Unknown"],
            title=title,
            album=album_name,
            year=year,
            service_id=service_id,
            service_name=self.service_name,
            extra_data=extra_data,
        )
        return track

    def get_library_tracks(self) -> list[Track]:
        """Fetch library tracks from Tidal API.

        Raises:
            Exception: If API error occurs
        """
        try:
            # Clear the cache before fetching
            self.cache.tracks = []

            # Check if we're running in a TTY (not piped)
            show_progress = sys.stdout.isatty()

            if show_progress:
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                ) as progress:
                    task = progress.add_task("[cyan]Fetching Tidal tracks...", total=None)

                    # Get favorite tracks
                    tidal_tracks = self.session.user.favorites.tracks()

                    progress.update(task, total=len(tidal_tracks), completed=len(tidal_tracks))
            else:
                # No progress bar, simple fetch
                tidal_tracks = self.session.user.favorites.tracks()

            # Convert Tidal tracks to Track objects
            for tidal_track in tidal_tracks:
                track = self._tidal_track_to_track(tidal_track)
                self.cache.tracks.append(track)

            self.log.info(f"Fetched {len(self.cache.tracks)} tracks from Tidal library")

            return self.cache.tracks

        except Exception as e:
            self.log.error(
                f"Tidal API error: {e}. Please check your authentication."
            )
            # Re-raise so the error propagates and we don't save empty cache
            raise

    def search_tracks(self, track: Track) -> list[Track]:
        """Search for tracks matching artist and title.
        Args:
            track: Track object with "artist" and "title" filled in
        Returns:
            List of matching Track objects
        """
        try:
            search_query = track.search_string(service_name=self.service_name)

            search_results = self.session.search(search_query, models=[tidalapi.Track])

            tracks = []
            if search_results and "tracks" in search_results:
                for item in search_results["tracks"][:5]:  # Limit to 5 results
                    found_track = self._tidal_track_to_track(item)
                    tracks.append(found_track)

            return tracks

        except Exception as e:
            self.log.error(f"Error searching for {track.artist} - {track.title}: {e}")
            return []

    def add_track(self, track: Track) -> bool:
        """Add a track to the user's Tidal library.
        Args:
            track: Track object to add
        Returns:
            True if successfully added, False otherwise
        """
        try:
            if not track.service_id:
                self.log.error(
                    f"Cannot add track without ID: {track.artist} - {track.title}"
                )
                return False

            # Add to favorites using track ID
            self.session.user.favorites.add_track(track.service_id)
            return True
        except Exception as e:
            self.log.error(f"Error adding track {track.artist} - {track.title}: {e}")
            return False

    def remove_track(self, track: Track) -> bool:
        """Remove a track from the user's Tidal library.
        Args:
            track: Track object to remove (must have service_id set)
        Returns:
            True if successfully removed, False otherwise
        """
        try:
            if not track.service_id:
                self.log.error(
                    f"Cannot remove track without ID: {track.artist} - {track.title}"
                )
                return False

            # Remove from favorites using track ID
            self.session.user.favorites.remove_track(track.service_id)
            return True
        except Exception as e:
            self.log.error(f"Error removing track {track.artist} - {track.title}: {e}")
            return False

    def is_track_in_library(self, track: Track) -> bool:
        """Check if a track is already in the user's library.

        This uses the similarity matching logic to account for discrepancies
        between how different services structure artist names.

        Args:
            track: Track to check

        Returns:
            True if track is in library, False otherwise

        Raises:
            Exception: If cache loading fails (e.g., authentication issues)
        """
        from pushtunes.utils.similarity import get_best_match

        if len(self.cache.tracks) == 0:
            # If this raises an exception (e.g., auth failure), let it propagate
            self.cache.load_track_cache()

        # If the track has a service_id, check for exact ID match first
        if track.service_id:
            for cached_track in self.cache.tracks:
                if cached_track.service_id == track.service_id:
                    return True

        # Use similarity matching against the cache instead of a direct `in` check,
        # as the __eq__ method would fail on artist parsing discrepancies.
        best_match, _ = get_best_match(track, self.cache.tracks, self.min_similarity)
        if best_match:
            return True
        return False

    def create_playlist(self, name: str, description: str = "") -> str | None:
        """Create a new playlist on Tidal.

        Args:
            name: Playlist name
            description: Playlist description (optional)

        Returns:
            Playlist ID if successful, None otherwise
        """
        try:
            playlist = self.session.user.create_playlist(name, description)

            self.log.info(f"Created playlist '{name}' with ID: {playlist.id}")
            return str(playlist.id)

        except Exception as e:
            self.log.error(f"Error creating playlist '{name}': {e}")
            return None

    def get_user_playlists(self) -> list[dict]:
        """Get all playlists owned by the current user.

        Returns:
            List of playlist dictionaries with 'id' and 'name' keys
        """
        try:
            playlists_raw = self.session.user.playlists()

            playlists = []
            for pl in playlists_raw:
                playlists.append({
                    "id": str(pl.id),
                    "name": pl.name,
                    "track_count": pl.num_tracks if hasattr(pl, 'num_tracks') else 0
                })

            return playlists

        except Exception as e:
            self.log.error(f"Error fetching user playlists: {e}")
            return []

    def get_playlist_tracks(self, playlist_id: str) -> list[Track]:
        """Get all tracks from a playlist.

        Args:
            playlist_id: Tidal playlist ID

        Returns:
            List of Track objects
        """
        try:
            playlist = self.session.playlist(playlist_id)
            tracks_raw = playlist.tracks()

            tracks = []
            for track_data in tracks_raw:
                track = self._tidal_track_to_track(track_data)
                tracks.append(track)

            return tracks

        except Exception as e:
            self.log.error(f"Error fetching playlist tracks: {e}")
            return []

    def replace_playlist_tracks(self, playlist_id: str, track_ids: list[str]) -> bool:
        """Replace all tracks in a playlist.

        Args:
            playlist_id: ID of the playlist
            track_ids: List of Tidal track IDs to replace with

        Returns:
            True if successful, False otherwise
        """
        try:
            playlist = self.session.playlist(playlist_id)

            # Remove all existing tracks
            existing_tracks = playlist.tracks()
            if existing_tracks:
                for track in existing_tracks:
                    playlist.remove_by_id(track.id)

            # Add new tracks
            if track_ids:
                playlist.add(track_ids)

            self.log.info(f"Replaced playlist {playlist_id} with {len(track_ids)} tracks")
            return True

        except Exception as e:
            self.log.error(f"Error replacing playlist tracks: {e}")
            return False

    def remove_tracks_from_playlist(self, playlist_id: str, track_ids: list[str]) -> bool:
        """Remove tracks from a playlist.

        Args:
            playlist_id: ID of the playlist
            track_ids: List of Tidal track IDs to remove

        Returns:
            True if successful, False otherwise
        """
        try:
            playlist = self.session.playlist(playlist_id)

            # Remove specified tracks
            for track_id in track_ids:
                playlist.remove_by_id(int(track_id))

            self.log.info(f"Removed {len(track_ids)} tracks from playlist {playlist_id}")
            return True

        except Exception as e:
            self.log.error(f"Error removing tracks from playlist: {e}")
            return False

    def add_tracks_to_playlist(self, playlist_id: str, track_ids: list[str]) -> bool:
        """Add tracks to a Tidal playlist.

        Args:
            playlist_id: ID of the playlist to add tracks to
            track_ids: List of Tidal track IDs to add

        Returns:
            True if successful, False otherwise
        """
        try:
            playlist = self.session.playlist(playlist_id)
            playlist.add(track_ids)

            self.log.info(f"Added {len(track_ids)} tracks to playlist {playlist_id}")
            return True

        except Exception as e:
            self.log.error(f"Error adding tracks to playlist {playlist_id}: {e}")
            return False
