"""Spotify music service implementation."""

import os
import sys

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TaskProgressColumn
from rich.live import Live
from rich.panel import Panel
from rich.console import Console, Group
from rich.text import Text

from pushtunes.models.album import Album
from pushtunes.models.track import Track
from pushtunes.models.playlist import Playlist
from pushtunes.services.music_service import MusicService
from pushtunes.utils.logging import get_logger


class SpotifyService(MusicService):
    """Spotify music service implementation."""

    def __init__(
        self,
        min_similarity: float = 0.8,
        client_id: str | None = None,
        client_secret: str | None = None,
        redirect_uri: str | None = None,
    ):
        """Initialize Spotify service.
        Args:
            min_similarity: Minimum similarity score for matching albums
            client_id: Spotify client ID (defaults to SPOTIFY_CLIENT_ID env var)
            client_secret: Spotify client secret (defaults to SPOTIFY_CLIENT_SECRET env var)
            redirect_uri: Spotify redirect URI (defaults to SPOTIFY_REDIRECT_URI env var)
        """
        self.service_name = "spotify"
        self.client_id = client_id or os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("SPOTIFY_CLIENT_SECRET")
        self.redirect_uri = redirect_uri or os.getenv(
            "SPOTIFY_REDIRECT_URI", "http://127.0.0.1:8080"
        )

        if not self.client_id or not self.client_secret:
            raise ValueError(
                "Spotify credentials not found! Please set SPOTIFY_CLIENT_ID and "
                + "SPOTIFY_CLIENT_SECRET environment variables"
            )

        # Initialize Spotify client
        self._init_spotify_client()
        super().__init__()
        self.min_similarity = min_similarity
        self.log = get_logger()

    def _init_spotify_client(self):
        """Initialize the Spotify client with authentication."""
        try:
            scope = "user-library-modify,user-library-read,playlist-modify-public,playlist-modify-private"
            sp_oauth = SpotifyOAuth(
                client_id=self.client_id,
                client_secret=self.client_secret,
                redirect_uri=self.redirect_uri,
                scope=scope,
            )
            self.sp = spotipy.Spotify(auth_manager=sp_oauth)
        except Exception as e:
            raise RuntimeError(f"Error initializing Spotify: {e}")

    def _spotify_album_to_album(self, spotify_album: dict) -> Album:
        """Convert a Spotify album dictionary to an Album object."""
        artist_names = [artist["name"] for artist in spotify_album.get("artists", [])]
        title = spotify_album.get("name", "Unknown")
        service_id = spotify_album.get("id")

        year = None
        release_date = spotify_album.get("release_date")
        if release_date:
            try:
                year = int(release_date.split("-")[0])
            except (ValueError, IndexError):
                year = None
        if "tracks" in spotify_album:
            del spotify_album["tracks"]

        album = Album(
            artists=artist_names,
            title=title,
            year=year,
            service_id=service_id,
            service_name=self.service_name,
            extra_data=spotify_album,
        )
        return album

    def get_library_albums(self) -> list[Album]:
        """Fetch library albums from Spotify API.

        Raises:
            spotipy.exceptions.SpotifyException: If API error occurs
            Exception: For other unexpected errors
        """
        try:
            # Clear the cache before fetching
            self.cache.albums = []

            # Get library albums with high limit to get all
            spotify_albums = []
            offset = 0
            limit = 50

            # Check if we're running in a TTY (not piped)
            show_progress = sys.stdout.isatty()

            if show_progress:
                # Get total count from first API call
                results = self.sp.current_user_saved_albums(limit=limit, offset=offset)
                total = results.get("total", 0)

                if results and results.get("items"):
                    spotify_albums.extend(results["items"])
                    offset += limit

                # Track last 5 albums for display
                recent_albums = []

                # Create progress bar
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    BarColumn(),
                    TaskProgressColumn(),
                    TextColumn("({task.completed}/{task.total})"),
                ) as progress:
                    task = progress.add_task("[cyan]Fetching Spotify albums...", total=total)

                    # Update for first batch
                    progress.update(task, advance=len(spotify_albums))

                    # Continue fetching remaining batches
                    while len(spotify_albums) < total and results.get("items") and len(results["items"]) == limit:
                        results = self.sp.current_user_saved_albums(limit=limit, offset=offset)
                        if not results or not results.get("items"):
                            break
                        spotify_albums.extend(results["items"])
                        progress.update(task, advance=len(results["items"]))
                        offset += limit
            else:
                # No progress bar, simple fetch
                while True:
                    results = self.sp.current_user_saved_albums(limit=limit, offset=offset)
                    if not results or not results.get("items"):
                        break
                    spotify_albums.extend(results["items"])
                    if len(results["items"]) < limit:
                        break
                    offset += limit

            # Convert Spotify albums to Album objects
            for item in spotify_albums:
                # Validate item structure
                if not item:
                    self.log.warning("Skipping None item in saved albums")
                    continue
                if "album" not in item:
                    self.log.warning(f"Skipping item without 'album' key: {list(item.keys()) if isinstance(item, dict) else type(item)}")
                    continue

                album = self._spotify_album_to_album(item["album"])
                self.cache.albums.append(album)

            self.log.info(f"Fetched {len(self.cache.albums)} albums from Spotify library")

            return self.cache.albums

        except Exception as e:
            self.log.error(
                f"Spotify API error: {e}. Please check your authentication."
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

            # Check if query might be too long (Spotify limit is 250 chars)
            if len(search_query) > 240:
                self.log.debug(
                    f"Search query too long ({len(search_query)} chars) for "
                    f"{album.artist} - {album.title}, truncating artists"
                )
                # Fallback: just use album title and first artist
                search_query = f"artist:{album.artists[0]} album:{album.title}" if album.artists else f"album:{album.title}"

            search_results = self.sp.search(q=search_query, type="album", limit=5)

            albums = []
            if search_results and search_results["albums"]:
                for item in search_results["albums"]["items"]:
                    found_album = self._spotify_album_to_album(item)
                    albums.append(found_album)

            return albums

        except spotipy.exceptions.SpotifyException as e:
            # 400 errors are usually query-related (too long, invalid chars, etc.)
            # Log as debug since this is expected for some albums
            if e.http_status == 400:
                self.log.debug(
                    f"Spotify query error for {album.artist} - {album.title}: {e.msg}"
                )
            else:
                self.log.error(f"Spotify API error searching for {album.artist} - {album.title}: {e}")
            return []
        except Exception as e:
            self.log.error(f"Error searching for {album.artist} - {album.title}: {e}")
            return []

    def add_album(self, album: Album) -> bool:
        """Add an album to the user's Spotify library.
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
            self.sp.current_user_saved_albums_add([album.service_id])
            return True
        except Exception as e:
            self.log.error(f"Error adding album {album.artist} - {album.title}: {e}")
            return False

    def remove_album(self, album: Album) -> bool:
        """Remove an album from the user's Spotify library.
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
            self.sp.current_user_saved_albums_delete([album.service_id])
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

    def _spotify_track_to_track(self, spotify_track: dict) -> Track:
        """Convert a Spotify track dictionary to a Track object."""
        artist_names = [artist["name"] for artist in spotify_track.get("artists", [])]
        title = spotify_track.get("name", "Unknown")
        service_id = spotify_track.get("id")

        album_name = None
        if "album" in spotify_track and spotify_track["album"]:
            album_name = spotify_track["album"].get("name")

        year = None
        if "album" in spotify_track and spotify_track["album"]:
            release_date = spotify_track["album"].get("release_date")
            if release_date:
                try:
                    year = int(release_date.split("-")[0])
                except (ValueError, IndexError):
                    year = None

        track = Track(
            artists=artist_names,
            title=title,
            album=album_name,
            year=year,
            service_id=service_id,
            service_name=self.service_name,
            extra_data=spotify_track,
        )
        return track

    def get_library_tracks(self) -> list[Track]:
        """Fetch library tracks from Spotify API.

        Raises:
            spotipy.exceptions.SpotifyException: If API error occurs
            Exception: For other unexpected errors
        """
        try:
            # Clear the cache before fetching
            self.cache.tracks = []

            # Get library tracks with pagination
            spotify_tracks = []
            offset = 0
            limit = 50

            # Check if we're running in a TTY (not piped)
            show_progress = sys.stdout.isatty()

            if show_progress:
                # Get total count from first API call
                results = self.sp.current_user_saved_tracks(limit=limit, offset=offset)
                total = results.get("total", 0)

                if results and results.get("items"):
                    spotify_tracks.extend(results["items"])
                    offset += limit

                # Create progress bar
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    BarColumn(),
                    TaskProgressColumn(),
                    TextColumn("({task.completed}/{task.total})"),
                ) as progress:
                    task = progress.add_task("[cyan]Fetching Spotify tracks...", total=total)

                    # Update for first batch
                    progress.update(task, advance=len(spotify_tracks))

                    # Continue fetching remaining batches
                    while len(spotify_tracks) < total and results.get("items") and len(results["items"]) == limit:
                        results = self.sp.current_user_saved_tracks(limit=limit, offset=offset)
                        if not results or not results.get("items"):
                            break
                        spotify_tracks.extend(results["items"])
                        progress.update(task, advance=len(results["items"]))
                        offset += limit
            else:
                # No progress bar, simple fetch
                while True:
                    results = self.sp.current_user_saved_tracks(limit=limit, offset=offset)
                    if not results or not results["items"]:
                        break
                    spotify_tracks.extend(results["items"])
                    if len(results["items"]) < limit:
                        break
                    offset += limit

            # Convert Spotify tracks to Track objects
            for item in spotify_tracks:
                track = self._spotify_track_to_track(item["track"])
                self.cache.tracks.append(track)

            self.log.info(f"Fetched {len(self.cache.tracks)} tracks from Spotify library")

            return self.cache.tracks

        except Exception as e:
            self.log.error(
                f"Spotify API error: {e}. Please check your authentication."
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

            # Check if query might be too long (Spotify limit is 250 chars)
            if len(search_query) > 240:
                self.log.debug(
                    f"Search query too long ({len(search_query)} chars) for "
                    f"{track.artist} - {track.title}, truncating artists"
                )
                # Fallback: just use track title and first artist
                search_query = f"artist:{track.artists[0]} track:{track.title}" if track.artists else f"track:{track.title}"

            search_results = self.sp.search(q=search_query, type="track", limit=5)

            tracks = []
            if search_results and search_results["tracks"]:
                for item in search_results["tracks"]["items"]:
                    found_track = self._spotify_track_to_track(item)
                    tracks.append(found_track)

            return tracks

        except spotipy.exceptions.SpotifyException as e:
            # 400 errors are usually query-related (too long, invalid chars, etc.)
            # Log as debug since this is expected for some tracks
            if e.http_status == 400:
                self.log.debug(
                    f"Spotify query error for {track.artist} - {track.title}: {e.msg}"
                )
            else:
                self.log.error(f"Spotify API error searching for {track.artist} - {track.title}: {e}")
            return []
        except Exception as e:
            self.log.error(f"Error searching for {track.artist} - {track.title}: {e}")
            return []

    def add_track(self, track: Track) -> bool:
        """Add a track to the user's Spotify library.
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
            self.sp.current_user_saved_tracks_add([track.service_id])
            return True
        except Exception as e:
            self.log.error(f"Error adding track {track.artist} - {track.title}: {e}")
            return False

    def remove_track(self, track: Track) -> bool:
        """Remove a track from the user's Spotify library.
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
            self.sp.current_user_saved_tracks_delete([track.service_id])
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
        """Create a new playlist on Spotify.

        Args:
            name: Playlist name
            description: Playlist description (optional)

        Returns:
            Playlist ID if successful, None otherwise
        """
        try:
            user = self.sp.current_user()
            user_id = user["id"]

            playlist = self.sp.user_playlist_create(
                user=user_id,
                name=name,
                public=False,
                description=description
            )

            self.log.info(f"Created playlist '{name}' with ID: {playlist['id']}")
            return playlist["id"]

        except Exception as e:
            self.log.error(f"Error creating playlist '{name}': {e}")
            return None

    def get_user_playlists(self) -> list[dict]:
        """Get all playlists owned by the current user.

        Returns:
            List of playlist dictionaries with 'id' and 'name' keys
        """
        try:
            playlists = []
            offset = 0
            limit = 50

            user = self.sp.current_user()
            user_id = user["id"]

            while True:
                results = self.sp.current_user_playlists(limit=limit, offset=offset)
                if not results or not results["items"]:
                    break

                # Only include playlists owned by the user
                for pl in results["items"]:
                    if pl["owner"]["id"] == user_id:
                        playlists.append({
                            "id": pl["id"],
                            "name": pl["name"],
                            "track_count": pl["tracks"]["total"]
                        })

                if len(results["items"]) < limit:
                    break
                offset += limit

            return playlists

        except Exception as e:
            self.log.error(f"Error fetching user playlists: {e}")
            return []

    def get_playlist_tracks(self, playlist_id: str) -> list[Track]:
        """Get all tracks from a playlist.

        Args:
            playlist_id: Spotify playlist ID

        Returns:
            List of Track objects
        """
        try:
            tracks = []
            offset = 0
            limit = 100

            while True:
                results = self.sp.playlist_items(playlist_id, limit=limit, offset=offset)
                if not results or not results["items"]:
                    break

                for item in results["items"]:
                    if item["track"] and item["track"]["id"]:
                        track = self._spotify_track_to_track(item["track"])
                        tracks.append(track)

                if len(results["items"]) < limit:
                    break
                offset += limit

            return tracks

        except Exception as e:
            self.log.error(f"Error fetching playlist tracks: {e}")
            return []

    def replace_playlist_tracks(self, playlist_id: str, track_ids: list[str]) -> bool:
        """Replace all tracks in a playlist.

        Args:
            playlist_id: ID of the playlist
            track_ids: List of Spotify track IDs to replace with

        Returns:
            True if successful, False otherwise
        """
        try:
            # Spotify API allows max 100 tracks in replace
            if len(track_ids) <= 100:
                self.sp.playlist_replace_items(playlist_id, track_ids)
            else:
                # Replace first 100, then add the rest
                self.sp.playlist_replace_items(playlist_id, track_ids[:100])
                for i in range(100, len(track_ids), 100):
                    batch = track_ids[i:i + 100]
                    self.sp.playlist_add_items(playlist_id, batch)

            self.log.info(f"Replaced playlist {playlist_id} with {len(track_ids)} tracks")
            return True

        except Exception as e:
            self.log.error(f"Error replacing playlist tracks: {e}")
            return False

    def remove_tracks_from_playlist(self, playlist_id: str, track_ids: list[str]) -> bool:
        """Remove tracks from a playlist.

        Args:
            playlist_id: ID of the playlist
            track_ids: List of Spotify track IDs to remove

        Returns:
            True if successful, False otherwise
        """
        try:
            # Spotify API allows max 100 tracks per request
            for i in range(0, len(track_ids), 100):
                batch = track_ids[i:i + 100]
                self.sp.playlist_remove_all_occurrences_of_items(playlist_id, batch)

            self.log.info(f"Removed {len(track_ids)} tracks from playlist {playlist_id}")
            return True

        except Exception as e:
            self.log.error(f"Error removing tracks from playlist: {e}")
            return False

    def add_tracks_to_playlist(self, playlist_id: str, track_ids: list[str]) -> bool:
        """Add tracks to a Spotify playlist.

        Args:
            playlist_id: ID of the playlist to add tracks to
            track_ids: List of Spotify track IDs to add

        Returns:
            True if successful, False otherwise
        """
        try:
            # Spotify API allows max 100 tracks per request
            batch_size = 100
            for i in range(0, len(track_ids), batch_size):
                batch = track_ids[i:i + batch_size]
                self.sp.playlist_add_items(playlist_id, batch)

            self.log.info(f"Added {len(track_ids)} tracks to playlist {playlist_id}")
            return True

        except Exception as e:
            self.log.error(f"Error adding tracks to playlist {playlist_id}: {e}")
            return False
