"""Subsonic music service implementation."""

import os
import sys

from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TaskProgressColumn

from pushtunes.models.album import Album
from pushtunes.models.track import Track
from pushtunes.services.music_service import MusicService
from pushtunes.clients.subsonic import SubsonicClient
from pushtunes.utils.artist_utils import parse_artist_string
from pushtunes.utils.logging import get_logger


class SubsonicService(MusicService):
    """Subsonic music service implementation."""

    def __init__(
        self,
        url: str | None = None,
        username: str | None = None,
        password: str | None = None,
        port: int = 443,
        min_similarity: float = 0.8,
    ):
        """Initialize Subsonic service.

        Args:
            url: Subsonic server URL (defaults to SUBSONIC_URL env var)
            username: Username (defaults to SUBSONIC_USER env var)
            password: Password (defaults to SUBSONIC_PASS env var)
            port: Server port (defaults to 443)
            min_similarity: Minimum similarity score for matching
        """
        self.service_name = "subsonic"
        self.url = url or os.getenv("SUBSONIC_URL")
        self.username = username or os.getenv("SUBSONIC_USER")
        self.password = password or os.getenv("SUBSONIC_PASS")
        self.port = port

        if not self.url or not (self.username and self.password):
            raise ValueError(
                "Subsonic credentials not found! Please set SUBSONIC_URL, "
                "SUBSONIC_USER, and SUBSONIC_PASS environment variables"
            )

        # Initialize Subsonic client
        self.client = SubsonicClient(self.url, self.username, self.password, self.port)
        super().__init__()
        self.min_similarity = min_similarity
        self.log = get_logger()

    def _subsonic_album_to_album(self, subsonic_album: dict) -> Album:
        """Convert a Subsonic album dictionary to an Album object."""
        artist_string = subsonic_album.get("artist", "")
        artist_list = parse_artist_string(artist_string)

        year_str = str(subsonic_album.get("year", ""))
        year = int(year_str) if year_str.isdigit() else None

        album = Album(
            artists=artist_list,
            title=subsonic_album.get("title", subsonic_album.get("name", "")),
            year=year,
            service_id=subsonic_album.get("id"),
            service_name=self.service_name,
        )
        return album

    def _subsonic_track_to_track(self, subsonic_track: dict) -> Track:
        """Convert a Subsonic track dictionary to a Track object."""
        artist_string = subsonic_track.get("artist", "")
        artist_list = parse_artist_string(artist_string)

        year_str = str(subsonic_track.get("year", ""))
        year = int(year_str) if year_str.isdigit() else None

        track = Track(
            artists=artist_list,
            title=subsonic_track.get("title", ""),
            album=subsonic_track.get("album"),
            year=year,
            service_id=subsonic_track.get("id"),
            service_name=self.service_name,
        )
        return track

    def get_library_albums(self) -> list[Album]:
        """Fetch library albums from Subsonic API.

        Raises:
            Exception: If API error occurs
        """
        try:
            # Clear the cache before fetching
            self.cache.albums = []

            # Check if we're running in a TTY (not piped)
            show_progress = sys.stdout.isatty()

            if show_progress:
                # Create progress bar - we don't know total upfront, so use indeterminate progress
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    TextColumn("[cyan]{task.completed} albums fetched"),
                ) as progress:
                    task = progress.add_task("[cyan]Fetching Subsonic albums...")

                    # Get albums from Subsonic with progress
                    raw_albums = self.client.get_albums(progress_bar=progress, progress_task=task)

                    # Convert to Album objects
                    for raw_album in raw_albums:
                        album = self._subsonic_album_to_album(raw_album)
                        self.cache.albums.append(album)
            else:
                # No progress bar
                raw_albums = self.client.get_albums()
                for raw_album in raw_albums:
                    album = self._subsonic_album_to_album(raw_album)
                    self.cache.albums.append(album)

            self.log.info(f"Fetched {len(self.cache.albums)} albums from Subsonic library")

            return self.cache.albums

        except Exception as e:
            self.log.error(
                f"Subsonic API error: {e}. Please check your authentication."
            )
            # Re-raise so the error propagates and we don't save empty cache
            raise

    def get_library_tracks(self) -> list[Track]:
        """Fetch library tracks from Subsonic API.

        Note: For better playlist matching, this fetches ALL tracks from the server,
        not just starred tracks. This may take time for large libraries.

        Raises:
            Exception: If API error occurs
        """
        try:
            # Clear the cache before fetching
            self.cache.tracks = []

            # Check if we're running in a TTY (not piped)
            show_progress = sys.stdout.isatty()

            if show_progress:
                # First, fetch the album list with a progress bar
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    TextColumn("[cyan]{task.completed} albums scanned"),
                ) as progress:
                    album_task = progress.add_task("[cyan]Fetching Subsonic album list...")
                    raw_albums = self.client.get_albums(progress_bar=progress, progress_task=album_task)

                # Now fetch tracks from each album with a progress bar
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    BarColumn(),
                    TaskProgressColumn(),
                    TextColumn("({task.completed}/{task.total} albums) - {task.fields[tracks]} tracks"),
                ) as progress:
                    task = progress.add_task(
                        "[cyan]Fetching tracks from albums...",
                        total=len(raw_albums),
                        tracks=0
                    )

                    for raw_album in raw_albums:
                        try:
                            # Get full album with tracks
                            album_id = raw_album.get("id")
                            if not album_id:
                                progress.update(task, advance=1)
                                continue

                            album_details = self.client.connection.getAlbum(album_id)
                            if "album" in album_details and "song" in album_details["album"]:
                                songs = album_details["album"]["song"]
                                if isinstance(songs, dict):
                                    songs = [songs]

                                for song in songs:
                                    track = self._subsonic_track_to_track(song)
                                    self.cache.tracks.append(track)

                            progress.update(task, advance=1, tracks=len(self.cache.tracks))

                        except Exception as e:
                            self.log.warning(f"Error fetching album tracks: {e}")
                            progress.update(task, advance=1)
                            continue

                # Also fetch any tracks that might not be in albums (singles, etc.)
                # Use search3 with wildcard to get all songs
                try:
                    with Progress(
                        SpinnerColumn(),
                        TextColumn("[progress.description]{task.description}"),
                    ) as progress:
                        progress.add_task("[cyan]Checking for tracks not in albums...")

                        # Get all songs via search (catches singles and orphaned tracks)
                        # We'll use a broad search and deduplicate based on track IDs
                        search_result = self.client.connection.search3(query='', songCount=10000)
                        if "searchResult3" in search_result and "song" in search_result["searchResult3"]:
                            all_songs = search_result["searchResult3"]["song"]
                            if isinstance(all_songs, dict):
                                all_songs = [all_songs]

                            # Track IDs we already have
                            existing_ids = {track.service_id for track in self.cache.tracks if track.service_id}

                            # Add any songs we don't already have
                            added_count = 0
                            for song in all_songs:
                                song_id = song.get("id")
                                if song_id and song_id not in existing_ids:
                                    track = self._subsonic_track_to_track(song)
                                    self.cache.tracks.append(track)
                                    existing_ids.add(song_id)
                                    added_count += 1

                            if added_count > 0:
                                self.log.info(f"Found {added_count} additional tracks not in albums")
                except Exception as e:
                    # Non-fatal - we still have tracks from albums
                    self.log.warning(f"Could not fetch standalone tracks: {e}")
            else:
                # No progress bar
                raw_albums = self.client.get_albums()
                for raw_album in raw_albums:
                    try:
                        album_id = raw_album.get("id")
                        if not album_id:
                            continue

                        album_details = self.client.connection.getAlbum(album_id)
                        if "album" in album_details and "song" in album_details["album"]:
                            songs = album_details["album"]["song"]
                            if isinstance(songs, dict):
                                songs = [songs]

                            for song in songs:
                                track = self._subsonic_track_to_track(song)
                                self.cache.tracks.append(track)

                    except Exception as e:
                        self.log.warning(f"Error fetching album tracks: {e}")
                        continue

                # Also fetch standalone tracks
                try:
                    search_result = self.client.connection.search3(query='', songCount=10000)
                    if "searchResult3" in search_result and "song" in search_result["searchResult3"]:
                        all_songs = search_result["searchResult3"]["song"]
                        if isinstance(all_songs, dict):
                            all_songs = [all_songs]

                        existing_ids = {track.service_id for track in self.cache.tracks if track.service_id}

                        added_count = 0
                        for song in all_songs:
                            song_id = song.get("id")
                            if song_id and song_id not in existing_ids:
                                track = self._subsonic_track_to_track(song)
                                self.cache.tracks.append(track)
                                existing_ids.add(song_id)
                                added_count += 1

                        if added_count > 0:
                            self.log.info(f"Found {added_count} additional tracks not in albums")
                except Exception as e:
                    self.log.warning(f"Could not fetch standalone tracks: {e}")

            self.log.info(f"Fetched {len(self.cache.tracks)} tracks from Subsonic library")

            return self.cache.tracks

        except Exception as e:
            self.log.error(
                f"Subsonic API error: {e}. Please check your authentication."
            )
            # Re-raise so the error propagates and we don't save empty cache
            raise

    def search_albums(self, album: Album) -> list[Album]:
        """Search for albums matching artist and title using in-memory fuzzy matching.

        Args:
            album: Album object with "artist" and "title" filled in

        Returns:
            List of matching Album objects
        """
        from pushtunes.utils.similarity import get_best_match

        # Load cache if needed
        if len(self.cache.albums) == 0:
            self.cache.load_album_cache()

        # Use fuzzy matching against cached albums
        best_match, score = get_best_match(album, self.cache.albums, self.min_similarity)

        if best_match:
            return [best_match]

        return []

    def search_tracks(self, track: Track) -> list[Track]:
        """Search for tracks matching artist and title using in-memory fuzzy matching.

        Args:
            track: Track object with "artist" and "title" filled in

        Returns:
            List of matching Track objects with service_id populated
        """
        from pushtunes.utils.similarity import get_best_match

        # Load cache if needed
        if len(self.cache.tracks) == 0:
            self.cache.load_track_cache()

        # Use fuzzy matching against cached tracks
        best_match, score = get_best_match(track, self.cache.tracks, self.min_similarity)

        if best_match:
            return [best_match]

        return []

    def is_album_in_library(self, album: Album) -> bool:
        """Check if an album is already in the library.

        Args:
            album: Album to check

        Returns:
            True if album is in library, False otherwise
        """
        from pushtunes.utils.similarity import get_best_match

        if len(self.cache.albums) == 0:
            self.cache.load_album_cache()

        # If the album has a service_id, check for exact ID match first
        if album.service_id:
            for cached_album in self.cache.albums:
                if cached_album.service_id == album.service_id:
                    return True

        # Use similarity matching
        best_match, _ = get_best_match(album, self.cache.albums, self.min_similarity)
        if best_match:
            return True
        return False

    def is_track_in_library(self, track: Track) -> bool:
        """Check if a track is already in the library.

        Args:
            track: Track to check

        Returns:
            True if track is in library, False otherwise
        """
        from pushtunes.utils.similarity import get_best_match

        if len(self.cache.tracks) == 0:
            self.cache.load_track_cache()

        # If the track has a service_id, check for exact ID match first
        if track.service_id:
            for cached_track in self.cache.tracks:
                if cached_track.service_id == track.service_id:
                    return True

        # Use similarity matching
        best_match, _ = get_best_match(track, self.cache.tracks, self.min_similarity)
        if best_match:
            return True
        return False

    def add_album(self, album: Album) -> bool:
        """Add an album to the library.

        Note: Subsonic doesn't support adding albums via API.

        Args:
            album: Album object to add

        Returns:
            False (not supported)
        """
        self.log.warning(
            "Adding albums to Subsonic library is not supported via API. "
            "Albums must be added by placing files on the server."
        )
        return False

    def add_track(self, track: Track) -> bool:
        """Add a track to the library.

        Note: Subsonic doesn't support adding tracks via API.

        Args:
            track: Track object to add

        Returns:
            False (not supported)
        """
        self.log.warning(
            "Adding tracks to Subsonic library is not supported via API. "
            "Tracks must be added by placing files on the server."
        )
        return False

    def remove_album(self, album: Album) -> bool:
        """Remove an album from the library.

        Note: Subsonic doesn't support removing albums via API.

        Args:
            album: Album to remove

        Returns:
            False (not supported)
        """
        self.log.warning(
            "Removing albums from Subsonic library is not supported via API."
        )
        return False

    def remove_track(self, track: Track) -> bool:
        """Remove a track from the library.

        Note: Subsonic doesn't support removing tracks via API.

        Args:
            track: Track to remove

        Returns:
            False (not supported)
        """
        self.log.warning(
            "Removing tracks from Subsonic library is not supported via API."
        )
        return False

    # Playlist methods

    def create_playlist(self, name: str, description: str = "") -> str | None:
        """Create a new playlist on Subsonic.

        Note: Subsonic doesn't support playlist descriptions.

        Args:
            name: Playlist name
            description: Playlist description (ignored for Subsonic)

        Returns:
            Playlist ID if successful, None otherwise
        """
        try:
            playlist_id = self.client.create_playlist(name)
            if playlist_id:
                self.log.info(f"Created playlist '{name}' with ID: {playlist_id}")
            return playlist_id
        except Exception as e:
            self.log.error(f"Error creating playlist '{name}': {e}")
            return None

    def get_user_playlists(self) -> list[dict]:
        """Get all playlists from Subsonic.

        Returns:
            List of playlist dictionaries with 'id', 'name', and 'track_count' keys
        """
        try:
            playlists = self.client.get_playlists()
            result = []
            for pl in playlists:
                result.append({
                    "id": pl.get("id"),
                    "name": pl.get("name"),
                    "track_count": pl.get("songCount", 0)
                })
            return result
        except Exception as e:
            self.log.error(f"Error fetching user playlists: {e}")
            return []

    def get_playlist_tracks(self, playlist_id: str) -> list[Track]:
        """Get all tracks from a playlist.

        Args:
            playlist_id: Subsonic playlist ID

        Returns:
            List of Track objects
        """
        try:
            raw_playlist = self.client.get_playlist(playlist_id)
            if not raw_playlist:
                return []

            tracks = []
            for entry in raw_playlist.get("entry", []):
                track = self._subsonic_track_to_track(entry)
                tracks.append(track)

            return tracks

        except Exception as e:
            self.log.error(f"Error fetching playlist tracks: {e}")
            return []

    def replace_playlist_tracks(self, playlist_id: str, track_ids: list[str]) -> bool:
        """Replace all tracks in a playlist.

        Args:
            playlist_id: ID of the playlist
            track_ids: List of Subsonic track IDs to replace with

        Returns:
            True if successful, False otherwise
        """
        try:
            success = self.client.update_playlist(playlist_id, track_ids)
            if success:
                self.log.info(f"Replaced playlist {playlist_id} with {len(track_ids)} tracks")
            return success
        except Exception as e:
            self.log.error(f"Error replacing playlist tracks: {e}")
            return False

    def remove_tracks_from_playlist(self, playlist_id: str, track_ids: list[str]) -> bool:
        """Remove tracks from a playlist.

        Args:
            playlist_id: ID of the playlist
            track_ids: List of Subsonic track IDs to remove

        Returns:
            True if successful, False otherwise
        """
        try:
            # Get current playlist to map IDs to indices
            current_tracks = self.get_playlist_tracks(playlist_id)

            # Find indices of tracks to remove
            indices_to_remove = []
            for i, track in enumerate(current_tracks):
                if track.service_id in track_ids:
                    indices_to_remove.append(i)

            if not indices_to_remove:
                return True  # Nothing to remove

            success = self.client.remove_from_playlist(playlist_id, indices_to_remove)
            if success:
                self.log.info(f"Removed {len(indices_to_remove)} tracks from playlist {playlist_id}")
            return success

        except Exception as e:
            self.log.error(f"Error removing tracks from playlist: {e}")
            return False

    def add_tracks_to_playlist(self, playlist_id: str, track_ids: list[str]) -> bool:
        """Add tracks to a Subsonic playlist.

        Args:
            playlist_id: ID of the playlist to add tracks to
            track_ids: List of Subsonic track IDs to add

        Returns:
            True if successful, False otherwise
        """
        try:
            success = self.client.add_to_playlist(playlist_id, track_ids)
            if success:
                self.log.info(f"Added {len(track_ids)} tracks to playlist {playlist_id}")
            return success
        except Exception as e:
            self.log.error(f"Error adding tracks to playlist {playlist_id}: {e}")
            return False
