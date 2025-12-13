"""Jellyfin music source implementation."""

import os

from pushtunes.sources.base import MusicSource
from pushtunes.models.album import Album
from pushtunes.models.track import Track
from pushtunes.models.playlist import Playlist
from pushtunes.clients.jellyfin import JellyfinClient
from pushtunes.utils.artist_utils import parse_artist_string
from pushtunes.utils.logging import get_logger


class JellyfinSource(MusicSource):
    """Jellyfin music source implementation with caching."""

    def __init__(self, url=None, username=None, password=None):
        """Initialize Jellyfin source.

        Args:
            url: Jellyfin server URL (defaults to JELLYFIN_URL env var)
            username: Username (defaults to JELLYFIN_USER env var)
            password: Password (defaults to JELLYFIN_PASS env var)
        """
        self.url = url or os.getenv("JELLYFIN_URL")
        self.username = username or os.getenv("JELLYFIN_USER")
        self.password = password or os.getenv("JELLYFIN_PASS")

        if not self.url or not (self.username or self.password):
            raise ValueError(
                "Jellyfin credentials not found. Please set "
                + "JELLYFIN_URL, JELLYFIN_USER, "
                + "JELLYFIN_PASS"
            )

        self.client = JellyfinClient(self.url, self.username, self.password)
        self.service_name = "jellyfin"
        super().__init__()
        self.log = get_logger(__name__)

    def get_albums(self) -> list[Album]:
        """Get all albums from the Jellyfin server.

        Uses cached data if available and not expired (1 hour TTL).

        Returns:
            List of Album objects
        """
        if len(self.cache.albums) == 0:
            self.cache.load_album_cache()
        return self.cache.albums

    def get_tracks(self) -> list[Track]:
        """Get all starred/favorite tracks from the Jellyfin server.

        Uses cached data if available and not expired (1 hour TTL).

        Returns:
            List of Track objects
        """
        if len(self.cache.tracks) == 0:
            self.cache.load_track_cache()
        return self.cache.tracks

    def _fetch_albums(self) -> list[Album]:
        """Fetch albums from Jellyfin server.

        Returns:
            List of Album objects
        """
        raw_albums = self.client.get_albums()

        albums: list[Album] = []
        for raw_album in raw_albums:
            # Prefer AlbumArtist for better search results, especially for compilations
            # AlbumArtist is the "album artist" (compiler, label, or main artist)
            # Artists contains individual track artists which can be overwhelming for compilations
            album_artist = raw_album.get("AlbumArtist")

            if album_artist:
                # Use AlbumArtist - this handles compilations ("Various Artists", labels)
                # and regular albums (the main artist) correctly
                artists = [album_artist]
            else:
                # Fallback to Artists array if no AlbumArtist
                artists = raw_album.get("Artists", [])
                if not artists:
                    artists = []

            year = raw_album.get("ProductionYear")

            album = Album(
                artists=artists,
                title=raw_album.get("Name", ""),
                year=year,
            )
            albums.append(album)

        self.log.info(f"Fetched {len(albums)} albums from Jellyfin server")
        return albums

    def _fetch_tracks(self) -> list[Track]:
        """Fetch tracks from Jellyfin server.

        Returns:
            List of Track objects
        """
        raw_tracks = self.client.get_tracks()

        tracks: list[Track] = []
        for raw_track in raw_tracks:
            # Get artists
            artists = raw_track.get("Artists", [])
            if not artists:
                artist = raw_track.get("AlbumArtist")
                if artist:
                    artists = parse_artist_string(artist)

            year = raw_track.get("ProductionYear")

            track = Track(
                artists=artists,
                title=raw_track.get("Name", ""),
                album=raw_track.get("Album"),
                year=year,
            )
            tracks.append(track)

        self.log.info(f"Fetched {len(tracks)} tracks from Jellyfin server")
        return tracks

    def get_playlist(self, playlist_name: str, playlist_id: str | None = None) -> Playlist | None:
        """Get a specific playlist by name or ID from the Jellyfin server.

        Args:
            playlist_name: Name of the playlist to fetch (used for display if ID provided)
            playlist_id: Optional Jellyfin playlist ID for direct lookup

        Returns:
            Playlist object or None if not found
        """
        # If ID is provided, use it directly
        if playlist_id:
            self.log.info(f"Fetching Jellyfin playlist by ID: {playlist_id}")
            try:
                raw_tracks = self.client.get_playlist_items(playlist_id)
                # Use the provided playlist_name for display
                actual_playlist_name = playlist_name
            except Exception as e:
                self.log.error(f"Error fetching playlist by ID: {e}")
                return None
        else:
            # Otherwise, search by name (case-insensitive)
            self.log.info(f"Searching for Jellyfin playlist by name: {playlist_name}")
            raw_playlists = self.client.get_playlists()

            # Find the playlist by name (case-insensitive)
            target_playlist = None
            for pl in raw_playlists:
                if pl.get("Name", "").lower() == playlist_name.lower():
                    target_playlist = pl
                    break

            if not target_playlist:
                print(f"Playlist '{playlist_name}' not found on Jellyfin server")
                return None

            # Get tracks from the playlist
            playlist_id = target_playlist.get("Id")
            actual_playlist_name = target_playlist.get("Name", playlist_name)
            raw_tracks = self.client.get_playlist_items(playlist_id)

        tracks: list[Track] = []
        for raw_track in raw_tracks:
            # Get artists
            artists = raw_track.get("Artists", [])
            if not artists:
                artist = raw_track.get("AlbumArtist")
                if artist:
                    artists = parse_artist_string(artist)

            year = raw_track.get("ProductionYear")

            track = Track(
                artists=artists,
                title=raw_track.get("Name", ""),
                album=raw_track.get("Album"),
                year=year,
            )
            tracks.append(track)

        playlist = Playlist(name=actual_playlist_name, tracks=tracks)
        print(f"Fetched playlist '{playlist.name}' with {len(playlist.tracks)} tracks from Jellyfin server")
        return playlist
