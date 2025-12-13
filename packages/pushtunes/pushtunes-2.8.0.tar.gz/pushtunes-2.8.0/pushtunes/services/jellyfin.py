"""Jellyfin music service implementation."""

import os
import sys

from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TaskProgressColumn

from pushtunes.models.album import Album
from pushtunes.models.track import Track
from pushtunes.services.music_service import MusicService
from pushtunes.clients.jellyfin import JellyfinClient
from pushtunes.utils.artist_utils import parse_artist_string
from pushtunes.utils.logging import get_logger


class JellyfinService(MusicService):
    """Jellyfin music service implementation."""

    def __init__(
        self,
        url: str | None = None,
        username: str | None = None,
        password: str | None = None,
        min_similarity: float = 0.8,
    ):
        """Initialize Jellyfin service.

        Args:
            url: Jellyfin server URL (defaults to JELLYFIN_URL env var)
            username: Username (defaults to JELLYFIN_USER env var)
            password: Password (defaults to JELLYFIN_PASS env var)
            min_similarity: Minimum similarity score for matching
        """
        self.service_name = "jellyfin"
        self.url = url or os.getenv("JELLYFIN_URL")
        self.username = username or os.getenv("JELLYFIN_USER")
        self.password = password or os.getenv("JELLYFIN_PASS")

        if not self.url or not (self.username and self.password):
            raise ValueError(
                "Jellyfin credentials not found! Please set JELLYFIN_URL, "
                "JELLYFIN_USER, and JELLYFIN_PASS environment variables"
            )

        # Initialize Jellyfin client
        self.client = JellyfinClient(self.url, self.username, self.password)
        super().__init__()
        self.min_similarity = min_similarity
        self.log = get_logger()

    def _jellyfin_album_to_album(self, jellyfin_album: dict) -> Album:
        """Convert a Jellyfin album dictionary to an Album object."""
        # Jellyfin stores artists as a list under 'AlbumArtists'
        artists = []
        if "AlbumArtists" in jellyfin_album:
            artists = [artist["Name"] for artist in jellyfin_album["AlbumArtists"]]
        elif "Artists" in jellyfin_album:
            artists = jellyfin_album["Artists"]

        year = None
        if "ProductionYear" in jellyfin_album:
            year = jellyfin_album["ProductionYear"]

        album = Album(
            artists=artists if artists else ["Unknown Artist"],
            title=jellyfin_album.get("Name", ""),
            year=year,
            service_id=jellyfin_album.get("Id"),
            service_name=self.service_name,
        )
        return album

    def _jellyfin_track_to_track(self, jellyfin_track: dict) -> Track:
        """Convert a Jellyfin track dictionary to a Track object."""
        # Jellyfin stores artists as a list
        artists = jellyfin_track.get("Artists", [])
        if not artists:
            artists = ["Unknown Artist"]

        year = None
        if "ProductionYear" in jellyfin_track:
            year = jellyfin_track["ProductionYear"]

        track = Track(
            artists=artists,
            title=jellyfin_track.get("Name", ""),
            album=jellyfin_track.get("Album"),
            year=year,
            service_id=jellyfin_track.get("Id"),
            service_name=self.service_name,
        )
        return track

    def get_library_albums(self) -> list[Album]:
        """Fetch library albums from Jellyfin API.

        Raises:
            Exception: If API error occurs
        """
        try:
            # Clear the cache before fetching
            self.cache.albums = []

            # Get albums from Jellyfin
            raw_albums = self.client.get_albums()

            # Check if we're running in a TTY (not piped)
            show_progress = sys.stdout.isatty()

            if show_progress and len(raw_albums) > 50:
                # Create progress bar for large libraries
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    BarColumn(),
                    TaskProgressColumn(),
                    TextColumn("({task.completed}/{task.total})"),
                ) as progress:
                    task = progress.add_task(
                        "[cyan]Processing Jellyfin albums...", total=len(raw_albums)
                    )

                    for raw_album in raw_albums:
                        album = self._jellyfin_album_to_album(raw_album)
                        self.cache.albums.append(album)
                        progress.update(task, advance=1)
            else:
                # No progress bar
                for raw_album in raw_albums:
                    album = self._jellyfin_album_to_album(raw_album)
                    self.cache.albums.append(album)

            self.log.info(f"Fetched {len(self.cache.albums)} albums from Jellyfin library")

            return self.cache.albums

        except Exception as e:
            self.log.error(
                f"Jellyfin API error: {e}. Please check your authentication."
            )
            # Re-raise so the error propagates and we don't save empty cache
            raise

    def get_library_tracks(self) -> list[Track]:
        """Fetch library tracks from Jellyfin API.

        Note: For better playlist matching, this fetches ALL tracks from the server
        by iterating through all albums. This may take time for large libraries.

        Raises:
            Exception: If API error occurs
        """
        try:
            # Clear the cache before fetching
            self.cache.tracks = []

            # Check if we're running in a TTY (not piped)
            show_progress = sys.stdout.isatty()

            if show_progress:
                # First, fetch the album list
                raw_albums = self.client.get_albums()

                # Now fetch tracks from each album with a progress bar
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    BarColumn(),
                    TaskProgressColumn(),
                    TextColumn("({task.completed}/{task.total} albums) - {task.fields[tracks]} tracks"),
                ) as progress:
                    task = progress.add_task(
                        "[cyan]Fetching tracks from Jellyfin albums...",
                        total=len(raw_albums),
                        tracks=0
                    )

                    for album in raw_albums:
                        try:
                            album_id = album.get("Id")
                            if not album_id:
                                progress.update(task, advance=1)
                                continue

                            # Get all tracks (Audio items) from this album
                            response = self.client.client.jellyfin.get_items({
                                "ParentId": album_id,
                                "IncludeItemTypes": "Audio",
                                "Recursive": False,
                            })

                            for item in response.get("Items", []):
                                track = self._jellyfin_track_to_track(item)
                                self.cache.tracks.append(track)

                            progress.update(task, advance=1, tracks=len(self.cache.tracks))

                        except Exception as e:
                            self.log.warning(f"Error fetching tracks from album: {e}")
                            progress.update(task, advance=1)
                            continue

                # Also fetch any tracks that might not be in albums (singles, etc.)
                try:
                    with Progress(
                        SpinnerColumn(),
                        TextColumn("[progress.description]{task.description}"),
                    ) as progress:
                        progress.add_task("[cyan]Checking for tracks not in albums...")

                        # Get all audio items that might not be in albums
                        # IMPORTANT: Must specify ParentId to limit to music library only
                        response = self.client.client.jellyfin.user_items(params={
                            "ParentId": self.client.music_library_id,
                            "IncludeItemTypes": "Audio",
                            "Recursive": True,
                            "Limit": 10000,
                        })

                        if "Items" in response:
                            # Track IDs we already have
                            existing_ids = {track.service_id for track in self.cache.tracks if track.service_id}

                            # Add any tracks we don't already have
                            added_count = 0
                            for item in response["Items"]:
                                item_id = item.get("Id")
                                if item_id and item_id not in existing_ids:
                                    track = self._jellyfin_track_to_track(item)
                                    self.cache.tracks.append(track)
                                    existing_ids.add(item_id)
                                    added_count += 1

                            if added_count > 0:
                                self.log.info(f"Found {added_count} additional tracks not in albums")
                except Exception as e:
                    # Non-fatal - we still have tracks from albums
                    self.log.warning(f"Could not fetch standalone tracks: {e}")
            else:
                # No progress bar
                raw_albums = self.client.get_albums()

                for album in raw_albums:
                    try:
                        album_id = album.get("Id")
                        if not album_id:
                            continue

                        # Get all tracks (Audio items) from this album
                        response = self.client.client.jellyfin.get_items({
                            "ParentId": album_id,
                            "IncludeItemTypes": "Audio",
                            "Recursive": False,
                        })

                        for item in response.get("Items", []):
                            track = self._jellyfin_track_to_track(item)
                            self.cache.tracks.append(track)

                    except Exception as e:
                        self.log.warning(f"Error fetching tracks from album: {e}")
                        continue

                # Also fetch standalone tracks
                try:
                    # IMPORTANT: Must specify ParentId to limit to music library only
                    response = self.client.client.jellyfin.user_items(params={
                        "ParentId": self.client.music_library_id,
                        "IncludeItemTypes": "Audio",
                        "Recursive": True,
                        "Limit": 10000,
                    })

                    if "Items" in response:
                        existing_ids = {track.service_id for track in self.cache.tracks if track.service_id}

                        added_count = 0
                        for item in response["Items"]:
                            item_id = item.get("Id")
                            if item_id and item_id not in existing_ids:
                                track = self._jellyfin_track_to_track(item)
                                self.cache.tracks.append(track)
                                existing_ids.add(item_id)
                                added_count += 1

                        if added_count > 0:
                            self.log.info(f"Found {added_count} additional tracks not in albums")
                except Exception as e:
                    self.log.warning(f"Could not fetch standalone tracks: {e}")

            self.log.info(f"Fetched {len(self.cache.tracks)} tracks from Jellyfin library")

            return self.cache.tracks

        except Exception as e:
            self.log.error(
                f"Jellyfin API error: {e}. Please check your authentication."
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

        Note: Jellyfin doesn't support adding albums via API.

        Args:
            album: Album object to add

        Returns:
            False (not supported)
        """
        self.log.warning(
            "Adding albums to Jellyfin library is not supported via API. "
            "Albums must be added by placing files on the server."
        )
        return False

    def add_track(self, track: Track) -> bool:
        """Add a track to the library.

        Note: Jellyfin doesn't support adding tracks via API.

        Args:
            track: Track object to add

        Returns:
            False (not supported)
        """
        self.log.warning(
            "Adding tracks to Jellyfin library is not supported via API. "
            "Tracks must be added by placing files on the server."
        )
        return False

    def remove_album(self, album: Album) -> bool:
        """Remove an album from the library.

        Note: Jellyfin doesn't support removing albums via API.

        Args:
            album: Album to remove

        Returns:
            False (not supported)
        """
        self.log.warning(
            "Removing albums from Jellyfin library is not supported via API."
        )
        return False

    def remove_track(self, track: Track) -> bool:
        """Remove a track from the library.

        Note: Jellyfin doesn't support removing tracks via API.

        Args:
            track: Track to remove

        Returns:
            False (not supported)
        """
        self.log.warning(
            "Removing tracks from Jellyfin library is not supported via API."
        )
        return False

    # Playlist methods

    def create_playlist(self, name: str, description: str = "") -> str | None:
        """Create a new playlist on Jellyfin.

        Note: Jellyfin doesn't support playlist descriptions via this API.

        Args:
            name: Playlist name
            description: Playlist description (ignored for Jellyfin)

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
        """Get all playlists from Jellyfin.

        Returns:
            List of playlist dictionaries with 'id', 'name', and 'track_count' keys
        """
        try:
            playlists = self.client.get_playlists()
            result = []
            for pl in playlists:
                # Get playlist items to count tracks
                items = self.client.get_playlist_items(pl.get("Id"))
                result.append({
                    "id": pl.get("Id"),
                    "name": pl.get("Name"),
                    "track_count": len(items)
                })
            return result
        except Exception as e:
            self.log.error(f"Error fetching user playlists: {e}")
            return []

    def get_playlist_tracks(self, playlist_id: str) -> list[Track]:
        """Get all tracks from a playlist.

        Args:
            playlist_id: Jellyfin playlist ID

        Returns:
            List of Track objects
        """
        try:
            raw_items = self.client.get_playlist_items(playlist_id)
            tracks = []
            for item in raw_items:
                track = self._jellyfin_track_to_track(item)
                tracks.append(track)

            return tracks

        except Exception as e:
            self.log.error(f"Error fetching playlist tracks: {e}")
            return []

    def replace_playlist_tracks(self, playlist_id: str, track_ids: list[str]) -> bool:
        """Replace all tracks in a playlist.

        Args:
            playlist_id: ID of the playlist
            track_ids: List of Jellyfin track IDs to replace with

        Returns:
            True if successful, False otherwise
        """
        try:
            # Remove all existing tracks first
            current_tracks = self.get_playlist_tracks(playlist_id)
            if current_tracks:
                current_ids = [track.service_id for track in current_tracks if track.service_id]
                if current_ids:
                    self.client.remove_from_playlist(playlist_id, current_ids)

            # Add new tracks
            if track_ids:
                success = self.client.add_items_to_playlist(playlist_id, track_ids)
                if success:
                    self.log.info(f"Replaced playlist {playlist_id} with {len(track_ids)} tracks")
                return success

            return True

        except Exception as e:
            self.log.error(f"Error replacing playlist tracks: {e}")
            return False

    def remove_tracks_from_playlist(self, playlist_id: str, track_ids: list[str]) -> bool:
        """Remove tracks from a playlist.

        Args:
            playlist_id: ID of the playlist
            track_ids: List of Jellyfin track IDs to remove

        Returns:
            True if successful, False otherwise
        """
        try:
            if not track_ids:
                return True  # Nothing to remove

            success = self.client.remove_from_playlist(playlist_id, track_ids)
            if success:
                self.log.info(f"Removed {len(track_ids)} tracks from playlist {playlist_id}")
            return success

        except Exception as e:
            self.log.error(f"Error removing tracks from playlist: {e}")
            return False

    def add_tracks_to_playlist(self, playlist_id: str, track_ids: list[str]) -> bool:
        """Add tracks to a Jellyfin playlist.

        Args:
            playlist_id: ID of the playlist to add tracks to
            track_ids: List of Jellyfin track IDs to add

        Returns:
            True if successful, False otherwise
        """
        try:
            success = self.client.add_items_to_playlist(playlist_id, track_ids)
            if success:
                self.log.info(f"Added {len(track_ids)} tracks to playlist {playlist_id}")
            return success
        except Exception as e:
            self.log.error(f"Error adding tracks to playlist {playlist_id}: {e}")
            return False
