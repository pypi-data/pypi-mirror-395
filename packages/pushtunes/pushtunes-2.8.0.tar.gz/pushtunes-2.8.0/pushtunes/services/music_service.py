"""Abstract base classes for pushtunes services."""

from abc import ABC, abstractmethod

from pushtunes.models.album import Album
from pushtunes.models.track import Track
from pushtunes.utils.logging import get_logger
from pushtunes.utils.cache_manager import CacheManager


class MusicService(ABC):
    """Base class for music services (e.g., Spotify, YouTube Music)."""

    log = get_logger()

    def __init__(self):
        """Initialize service with cache manager.

        Subclasses should call super().__init__() after setting self.service_name
        """
        self.cache = CacheManager(
            self.service_name,
            self.get_library_albums,
            self.get_library_tracks
        )

    @abstractmethod
    def search_albums(self, album: Album) -> list[Album]:
        pass

    @abstractmethod
    def is_album_in_library(self, album: Album) -> bool:
        pass

    @abstractmethod
    def add_album(self, album: Album) -> bool:
        pass

    @abstractmethod
    def search_tracks(self, track: Track) -> list[Track]:
        pass

    @abstractmethod
    def is_track_in_library(self, track: Track) -> bool:
        pass

    @abstractmethod
    def add_track(self, track: Track) -> bool:
        pass

    @abstractmethod
    def remove_album(self, album: Album) -> bool:
        """Remove an album from the user's library.

        Args:
            album: Album to remove (must have service_id set)

        Returns:
            True if successful, False otherwise
        """
        pass

    @abstractmethod
    def remove_track(self, track: Track) -> bool:
        """Remove a track from the user's library.

        Args:
            track: Track to remove (must have service_id set)

        Returns:
            True if successful, False otherwise
        """
        pass
