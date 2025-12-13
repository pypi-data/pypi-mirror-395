"""Tidal music source for playlist retrieval."""

from .base import MusicSource
from ..models.album import Album
from ..models.track import Track
from ..models.playlist import Playlist
from ..services.tidal import TidalService
from ..utils.logging import get_logger


class TidalSource(MusicSource):
    """Tidal source for retrieving playlists.

    This is a thin wrapper around TidalService that implements the MusicSource
    interface, allowing Tidal to be used as a source for playlist pushing.

    Caching is handled by the underlying TidalService, not by MusicSource.
    """

    def __init__(
        self,
        client_id: str | None = None,
        client_secret: str | None = None,
        session_file: str = "tidal-session.json"
    ):
        """Initialize Tidal source.

        Args:
            client_id: Tidal client ID (or None to use TIDAL_CLIENT_ID env var)
            client_secret: Tidal client secret (or None to use TIDAL_CLIENT_SECRET env var)
            session_file: Path to Tidal session file (defaults to tidal-session.json)
        """
        self.log = get_logger(__name__)
        self.service = TidalService(
            client_id=client_id,
            client_secret=client_secret,
            session_file=session_file
        )
        self.service_name = "tidal"
        # Tidal uses service-level caching, so we don't call super().__init__()

    def _fetch_albums(self) -> list[Album]:
        """Not used for Tidal source (caching handled by TidalService)."""
        raise NotImplementedError("Tidal source uses service-level caching")

    def _fetch_tracks(self) -> list[Track]:
        """Not used for Tidal source (caching handled by TidalService)."""
        raise NotImplementedError("Tidal source uses service-level caching")

    def get_albums(self) -> list[Album]:
        """Get all albums from Tidal library.

        Uses cached data if available and not expired (1 hour TTL).

        Returns:
            List of Album objects from user's Tidal library
        """
        if len(self.service.cache.albums) == 0:
            self.service.cache.load_album_cache()
        return self.service.cache.albums

    def get_tracks(self) -> list[Track]:
        """Get all tracks from Tidal library.

        Uses cached data if available and not expired (1 hour TTL).

        Returns:
            List of Track objects from user's Tidal library
        """
        if len(self.service.cache.tracks) == 0:
            self.service.cache.load_track_cache()
        return self.service.cache.tracks

    def get_playlist(self, playlist_name: str, playlist_id: str | None = None) -> Playlist | None:
        """Get a specific playlist by name or ID from Tidal.

        Args:
            playlist_name: Name of the playlist to retrieve
            playlist_id: Optional Tidal playlist ID for direct lookup

        Returns:
            Playlist object if found, None otherwise
        """
        # If ID is provided, use it directly
        if playlist_id:
            self.log.info(f"Fetching Tidal playlist by ID: {playlist_id}")
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
        self.log.info(f"Searching for Tidal playlist by name: {playlist_name}")
        try:
            user_playlists = self.service.get_user_playlists()

            # Find playlist by name (case-insensitive)
            target_playlist = None
            for pl in user_playlists:
                if pl['name'].lower() == playlist_name.lower():
                    target_playlist = pl
                    break

            if not target_playlist:
                self.log.error(f"Playlist '{playlist_name}' not found in user's Tidal playlists")
                return None

            # Get tracks from the found playlist
            playlist_id = target_playlist['id']
            tracks = self.service.get_playlist_tracks(playlist_id)

            if not tracks:
                self.log.warning(f"Playlist '{playlist_name}' found but has no tracks")
                return Playlist(name=target_playlist['name'], tracks=[])

            self.log.info(f"Fetched playlist '{target_playlist['name']}' with {len(tracks)} tracks from Tidal")
            return Playlist(name=target_playlist['name'], tracks=tracks)

        except Exception as e:
            self.log.error(f"Error fetching playlist from Tidal: {e}")
            return None
