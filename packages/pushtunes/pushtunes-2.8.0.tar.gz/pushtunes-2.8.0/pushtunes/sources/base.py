from abc import ABC, abstractmethod

from ..models.album import Album
from ..models.track import Track
from ..models.playlist import Playlist
from ..utils.logging import get_logger
from ..utils.cache_manager import CacheManager


class MusicSource(ABC):
    """Abstract base class for music sources (e.g., Subsonic).

    Provides caching infrastructure for album and track data to avoid
    repeated API calls to the source.
    """

    log = get_logger()

    def __init__(self):
        """Initialize cache infrastructure.

        Subclasses should call super().__init__() after setting self.service_name
        """
        self.cache = CacheManager(
            self.service_name,
            self._fetch_albums,
            self._fetch_tracks
        )

    @abstractmethod
    def get_albums(self) -> list[Album]:
        """Get all albums from the music source."""
        pass

    @abstractmethod
    def get_tracks(self) -> list[Track]:
        """Get all tracks from the music source."""
        pass

    @abstractmethod
    def get_playlist(self, playlist_name: str, playlist_id: str | None = None) -> Playlist | None:
        """Get a specific playlist by name or ID.

        Args:
            playlist_name: Name of the playlist to retrieve
            playlist_id: Optional ID for direct playlist lookup (streaming services only)

        Returns:
            Playlist object if found, None otherwise
        """
        pass

    @abstractmethod
    def _fetch_albums(self) -> list[Album]:
        """Fetch albums from the source API.

        This should be implemented by subclasses to fetch albums from
        the actual source (e.g., Subsonic server).

        Returns:
            List of Album objects
        """
        pass

    @abstractmethod
    def _fetch_tracks(self) -> list[Track]:
        """Fetch tracks from the source API.

        This should be implemented by subclasses to fetch tracks from
        the actual source (e.g., Subsonic server).

        Returns:
            List of Track objects
        """
        pass
