"""Subsonic music source implementation."""

import os

from pushtunes.sources.base import MusicSource
from pushtunes.models.album import Album
from pushtunes.models.track import Track
from pushtunes.models.playlist import Playlist
from pushtunes.clients.subsonic import SubsonicClient
from pushtunes.utils.artist_utils import parse_artist_string
from pushtunes.utils.logging import get_logger


class SubsonicSource(MusicSource):
    """Subsonic music source implementation with caching."""

    def __init__(self, url=None, username=None, password=None, port=443):
        """Initialize Subsonic source.

        Args:
            url: Subsonic server URL (defaults to SUBSONIC_URL env var)
            username: Username (defaults to SUBSONIC_USER env var)
            password: Password (defaults to SUBSONIC_PASS env var)
            port: Server port (defaults to 443)
        """
        self.url = url or os.getenv("SUBSONIC_URL")
        self.username = username or os.getenv("SUBSONIC_USER")
        self.password = password or os.getenv("SUBSONIC_PASS")

        if not self.url or not (self.username or self.password):
            raise ValueError(
                "Subsonic credentials not found. Please set "
                + "SUBSONIC_URL, SUBSONIC_USER, "
                + "SUBSONIC_PASS"
            )

        self.client = SubsonicClient(self.url, self.username, self.password, port)
        self.service_name = "subsonic"
        super().__init__()
        self.log = get_logger(__name__)

    def get_albums(self) -> list[Album]:
        """Get all albums from the Subsonic server.

        Uses cached data if available and not expired (1 hour TTL).

        Returns:
            List of Album objects
        """
        if len(self.cache.albums) == 0:
            self.cache.load_album_cache()
        return self.cache.albums

    def get_tracks(self) -> list[Track]:
        """Get all starred/favorite tracks from the Subsonic server.

        Uses cached data if available and not expired (1 hour TTL).

        Returns:
            List of Track objects
        """
        if len(self.cache.tracks) == 0:
            self.cache.load_track_cache()
        return self.cache.tracks

    def _fetch_albums(self) -> list[Album]:
        """Fetch albums from Subsonic server.

        Returns:
            List of Album objects
        """
        raw_albums = self.client.get_albums()

        albums: list[Album] = []
        for raw_album in raw_albums:
            artist_string = raw_album.get("artist", "")
            artist_list = parse_artist_string(artist_string)

            year_str = str(raw_album.get("year", ""))
            year = int(year_str) if year_str.isdigit() else None

            album = Album(
                artists=artist_list, title=raw_album.get("title", ""), year=year
            )
            albums.append(album)

        self.log.info(f"Fetched {len(albums)} albums from Subsonic server")
        return albums

    def _fetch_tracks(self) -> list[Track]:
        """Fetch tracks from Subsonic server.

        Returns:
            List of Track objects
        """
        raw_tracks = self.client.get_tracks()

        tracks: list[Track] = []
        for raw_track in raw_tracks:
            artist_string = raw_track.get("artist", "")
            artist_list = parse_artist_string(artist_string)

            year_str = str(raw_track.get("year", ""))
            year = int(year_str) if year_str.isdigit() else None

            track = Track(
                artists=artist_list,
                title=raw_track.get("title", ""),
                album=raw_track.get("album"),
                year=year
            )
            tracks.append(track)

        self.log.info(f"Fetched {len(tracks)} tracks from Subsonic server")
        return tracks

    def get_playlist(self, playlist_name: str, playlist_id: str | None = None) -> Playlist | None:
        """Get a specific playlist by name from the Subsonic server.

        Args:
            playlist_name: Name of the playlist to fetch
            playlist_id: Not used for Subsonic (uses name-based lookup only)

        Returns:
            Playlist object or None if not found
        """
        # First, get all playlists to find the ID
        raw_playlists = self.client.get_playlists()

        playlist_id = None
        for pl in raw_playlists:
            if pl["name"].lower() == playlist_name.lower():
                playlist_id = pl["id"]
                break

        if not playlist_id:
            print(f"Playlist '{playlist_name}' not found")
            return None

        # Now fetch the full playlist with tracks
        raw_playlist = self.client.get_playlist(playlist_id)
        if not raw_playlist:
            return None

        # Convert entries to Track objects
        tracks: list[Track] = []
        for entry in raw_playlist.get("entry", []):
            artist_string = entry.get("artist", "")
            artist_list = parse_artist_string(artist_string)

            year_str = str(entry.get("year", ""))
            year = int(year_str) if year_str.isdigit() else None

            track = Track(
                artists=artist_list,
                title=entry.get("title", ""),
                album=entry.get("album"),
                year=year
            )
            tracks.append(track)

        playlist = Playlist(
            name=raw_playlist.get("name", playlist_name),
            tracks=tracks
        )

        print(f"Fetched playlist '{playlist.name}' with {len(tracks)} tracks from Subsonic server")
        return playlist
