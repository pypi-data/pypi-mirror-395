"""Spotify music source for playlist retrieval."""

from .base import MusicSource
from ..models.album import Album
from ..models.track import Track
from ..models.playlist import Playlist
from ..services.spotify import SpotifyService
from ..utils.logging import get_logger


class SpotifySource(MusicSource):
    """Spotify source for retrieving playlists.

    This is a thin wrapper around SpotifyService that implements the MusicSource
    interface, allowing Spotify to be used as a source for playlist pushing.

    Caching is handled by the underlying SpotifyService, not by MusicSource.
    """

    def __init__(self, client_id: str | None = None, client_secret: str | None = None):
        """Initialize Spotify source.

        Args:
            client_id: Spotify client ID (or None to use SPOTIFY_CLIENT_ID env var)
            client_secret: Spotify client secret (or None to use SPOTIFY_CLIENT_SECRET env var)
        """
        self.log = get_logger(__name__)
        self.service = SpotifyService(client_id=client_id, client_secret=client_secret)
        self.service_name = "spotify"
        # Spotify uses service-level caching, so we don't call super().__init__()

    def _fetch_albums(self) -> list[Album]:
        """Not used for Spotify source (caching handled by SpotifyService)."""
        raise NotImplementedError("Spotify source uses service-level caching")

    def _fetch_tracks(self) -> list[Track]:
        """Not used for Spotify source (caching handled by SpotifyService)."""
        raise NotImplementedError("Spotify source uses service-level caching")

    def get_albums(self) -> list[Album]:
        """Get all albums from Spotify library.

        Uses cached data if available and not expired (1 hour TTL).

        Returns:
            List of Album objects from user's Spotify library
        """
        if len(self.service.cache.albums) == 0:
            self.service.cache.load_album_cache()
        return self.service.cache.albums

    def get_tracks(self) -> list[Track]:
        """Get all tracks from Spotify library.

        Uses cached data if available and not expired (1 hour TTL).

        Returns:
            List of Track objects from user's Spotify library
        """
        if len(self.service.cache.tracks) == 0:
            self.service.cache.load_track_cache()
        return self.service.cache.tracks

    def get_playlist(self, playlist_name: str, playlist_id: str | None = None) -> Playlist | None:
        """Get a specific playlist by name or ID from Spotify.

        Args:
            playlist_name: Name of the playlist to retrieve
            playlist_id: Optional Spotify playlist ID for direct lookup

        Returns:
            Playlist object if found, None otherwise
        """
        # If ID is provided, use it directly
        if playlist_id:
            self.log.info(f"Fetching Spotify playlist by ID: {playlist_id}")
            try:
                tracks = self.service.get_playlist_tracks(playlist_id)
                if tracks:
                    return Playlist(name=playlist_name, tracks=tracks)
                else:
                    self.log.error(f"Playlist with ID '{playlist_id}' not found or has no tracks")
                    return None
            except Exception as e:
                self.log.error(f"Error fetching playlist by ID: {e}")
                return None

        # Otherwise, search by name (case-insensitive)
        self.log.info(f"Searching for Spotify playlist by name: {playlist_name}")
        try:
            user_playlists = self.service.get_user_playlists()

            # Find playlist by name (case-insensitive)
            target_playlist = None
            for pl in user_playlists:
                if pl['name'].lower() == playlist_name.lower():
                    target_playlist = pl
                    break

            if not target_playlist:
                self.log.error(f"Playlist '{playlist_name}' not found in user's Spotify playlists")
                return None

            # Get tracks from the found playlist
            playlist_id = target_playlist['id']
            tracks = self.service.get_playlist_tracks(playlist_id)

            if not tracks:
                self.log.warning(f"Playlist '{playlist_name}' found but has no tracks")
                return Playlist(name=target_playlist['name'], tracks=[])

            self.log.info(f"Fetched playlist '{target_playlist['name']}' with {len(tracks)} tracks from Spotify")
            return Playlist(name=target_playlist['name'], tracks=tracks)

        except Exception as e:
            self.log.error(f"Error fetching playlist from Spotify: {e}")
            return None
