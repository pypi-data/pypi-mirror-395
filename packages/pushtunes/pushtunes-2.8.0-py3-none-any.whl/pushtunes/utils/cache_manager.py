"""Cache manager for music libraries (albums and tracks).

This provides reusable caching infrastructure for both MusicSource and MusicService
classes, eliminating code duplication.
"""

import os
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from typing import Callable

import orjson
from platformdirs import PlatformDirs

from ..models.album import Album
from ..models.track import Track
from .logging import get_logger


class CacheManager:
    """Manages caching of album and track libraries.

    Uses platformdirs for cross-platform cache directory location with 1-hour TTL.
    """

    def __init__(
        self,
        service_name: str,
        fetch_albums_fn: Callable[[], list[Album]],
        fetch_tracks_fn: Callable[[], list[Track]],
    ):
        """Initialize cache manager.

        Args:
            service_name: Name of the service (e.g., 'spotify', 'subsonic')
            fetch_albums_fn: Function to call to fetch albums from source
            fetch_tracks_fn: Function to call to fetch tracks from source
        """
        self.service_name = service_name
        self.fetch_albums_fn = fetch_albums_fn
        self.fetch_tracks_fn = fetch_tracks_fn
        self.log = get_logger(__name__)

        self.albums: list[Album] = []
        self.tracks: list[Track] = []

        # Setup cache file paths
        self.dirs: PlatformDirs = PlatformDirs(appname="pushtunes", appauthor="psy-q")
        self.album_cache_file = os.path.join(
            self.dirs.user_cache_dir, f"{service_name}_albums.json"
        )
        self.track_cache_file = os.path.join(
            self.dirs.user_cache_dir, f"{service_name}_tracks.json"
        )

    # Album cache methods

    def _update_album_cache(self):
        """Update album cache by fetching fresh data."""
        if self._is_album_cache_expired():
            self.log.info("Album cache is expired or missing, fetching library albums")
            try:
                self.albums = self.fetch_albums_fn()
                # Save cache even if empty - having 0 albums is a valid state
                self._save_album_cache()
                if len(self.albums) == 0:
                    self.log.info("Saved empty album cache (0 albums in library)")
                else:
                    self.log.debug(f"Saved {len(self.albums)} albums to cache")
            except Exception as e:
                self.log.error(f"Failed to fetch library albums: {e}. Not saving cache.")
                # Re-raise so caller knows the operation failed
                raise

    def _save_album_cache(self):
        """Save albums to cache file."""
        os.makedirs(os.path.dirname(self.album_cache_file), exist_ok=True)
        with open(self.album_cache_file, "w+") as cache:
            albums_as_dicts = [asdict(album) for album in self.albums]
            _ = cache.write(
                orjson.dumps(albums_as_dicts, option=orjson.OPT_INDENT_2).decode()
            )

    def load_album_cache(self):
        """Load albums from cache, updating if expired.

        Load cached album data. It will automatically fetch fresh data if the
        cache is expired (>1 hour old).

        Raises:
            Exception: If cache update or loading fails
        """
        if self._is_album_cache_expired():
            try:
                self._update_album_cache()
            except Exception as e:
                self.log.error(f"Failed to update album cache: {e}")
                # Don't try to load from file if update failed - propagate the error
                raise
        try:
            with open(self.album_cache_file, "r") as cache:
                albums = [Album(**a) for a in orjson.loads(cache.read())]
                self.albums = albums
                self.log.debug(f"Loaded {len(self.albums)} albums from cache")
        except FileNotFoundError:
            self.log.error(
                f"Album cache file not found. Please ensure authentication is set up correctly."
            )
            raise
        except Exception as e:
            self.log.error(f"Error loading album cache: {e}")
            raise

    def _is_album_cache_expired(self, seconds: int = 3600):
        """Check if album cache is expired.

        Args:
            seconds: Cache lifetime in seconds (default: 3600 = 1 hour)

        Returns:
            True if cache is expired or doesn't exist
        """
        if not os.path.exists(self.album_cache_file):
            return True
        else:
            age = time.time() - os.path.getmtime(self.album_cache_file)
            return age > seconds

    # Track cache methods

    def _update_track_cache(self):
        """Update track cache by fetching fresh data."""
        if self._is_track_cache_expired():
            self.log.info("Track cache is expired or missing, fetching library tracks")
            try:
                self.tracks = self.fetch_tracks_fn()
                # Save cache even if empty - having 0 tracks is a valid state
                self._save_track_cache()
                if len(self.tracks) == 0:
                    self.log.info("Saved empty track cache (0 tracks in library)")
                else:
                    self.log.debug(f"Saved {len(self.tracks)} tracks to cache")
            except Exception as e:
                self.log.error(f"Failed to fetch library tracks: {e}. Not saving cache.")
                # Re-raise so caller knows the operation failed
                raise

    def _save_track_cache(self):
        """Save tracks to cache file."""
        os.makedirs(os.path.dirname(self.track_cache_file), exist_ok=True)
        with open(self.track_cache_file, "w+") as cache:
            tracks_as_dicts = [asdict(track) for track in self.tracks]
            _ = cache.write(
                orjson.dumps(tracks_as_dicts, option=orjson.OPT_INDENT_2).decode()
            )

    def load_track_cache(self):
        """Load tracks from cache, updating if expired.

        Load cached track data. It will automatically fetch fresh data if the
        cache is expired (>1 hour old).

        Raises:
            Exception: If cache update or loading fails
        """
        if self._is_track_cache_expired():
            try:
                self._update_track_cache()
            except Exception as e:
                self.log.error(f"Failed to update track cache: {e}")
                # Don't try to load from file if update failed - propagate the error
                raise
        try:
            with open(self.track_cache_file, "r") as cache:
                tracks = [Track(**t) for t in orjson.loads(cache.read())]
                self.tracks = tracks
                self.log.debug(f"Loaded {len(self.tracks)} tracks from cache")
        except FileNotFoundError:
            self.log.error(
                f"Track cache file not found. Please ensure authentication is set up correctly."
            )
            raise
        except Exception as e:
            self.log.error(f"Error loading track cache: {e}")
            raise

    def _is_track_cache_expired(self, seconds: int = 3600):
        """Check if track cache is expired.

        Args:
            seconds: Cache lifetime in seconds (default: 3600 = 1 hour)

        Returns:
            True if cache is expired or doesn't exist
        """
        if not os.path.exists(self.track_cache_file):
            return True
        else:
            age = time.time() - os.path.getmtime(self.track_cache_file)
            return age > seconds

    # Cache invalidation methods

    def invalidate_album_cache(self):
        """Invalidate album cache by removing the cache file.

        This forces the next load_album_cache() call to fetch fresh data.
        """
        if os.path.exists(self.album_cache_file):
            os.remove(self.album_cache_file)
            self.log.info("Album cache invalidated")
        else:
            self.log.debug("Album cache file doesn't exist, nothing to invalidate")

    def invalidate_track_cache(self):
        """Invalidate track cache by removing the cache file.

        This forces the next load_track_cache() call to fetch fresh data.
        """
        if os.path.exists(self.track_cache_file):
            os.remove(self.track_cache_file)
            self.log.info("Track cache invalidated")
        else:
            self.log.debug("Track cache file doesn't exist, nothing to invalidate")


# Cache utility functions for CLI commands

@dataclass
class CacheInfo:
    """Information about a cache file."""
    service_name: str
    content_type: str  # 'albums' or 'tracks'
    file_path: str
    exists: bool
    created_time: datetime | None = None
    expires_time: datetime | None = None
    size_bytes: int | None = None
    is_expired: bool = False


def list_all_caches(ttl_seconds: int = 3600) -> list[CacheInfo]:
    """List all cache files in the pushtunes cache directory.

    Args:
        ttl_seconds: Time-to-live for cache files in seconds (default: 3600 = 1 hour)

    Returns:
        List of CacheInfo objects for all found cache files
    """
    dirs = PlatformDirs(appname="pushtunes", appauthor="psy-q")
    cache_dir = dirs.user_cache_dir

    cache_infos = []

    if not os.path.exists(cache_dir):
        return cache_infos

    # Find all JSON cache files
    for filename in os.listdir(cache_dir):
        if not filename.endswith('.json'):
            continue

        file_path = os.path.join(cache_dir, filename)

        # Parse filename to extract service name and content type
        # Format: {service_name}_{content_type}.json
        # e.g., "spotify_albums.json", "subsonic_tracks.json"
        parts = filename.replace('.json', '').rsplit('_', 1)
        if len(parts) != 2:
            continue

        service_name, content_type = parts

        if content_type not in ['albums', 'tracks']:
            continue

        # Get file stats
        stat = os.stat(file_path)
        created_time = datetime.fromtimestamp(stat.st_mtime)
        expires_time = created_time + timedelta(seconds=ttl_seconds)
        is_expired = datetime.now() > expires_time

        cache_info = CacheInfo(
            service_name=service_name,
            content_type=content_type,
            file_path=file_path,
            exists=True,
            created_time=created_time,
            expires_time=expires_time,
            size_bytes=stat.st_size,
            is_expired=is_expired
        )

        cache_infos.append(cache_info)

    # Sort by service name, then content type
    cache_infos.sort(key=lambda c: (c.service_name, c.content_type))

    return cache_infos


def invalidate_cache_by_pattern(service_name: str | None = None, content_type: str | None = None) -> list[str]:
    """Invalidate cache files matching the given pattern.

    Args:
        service_name: Service name to filter by (e.g., 'spotify', 'subsonic'). None = all services.
        content_type: Content type to filter by ('albums' or 'tracks'). None = both types.

    Returns:
        List of invalidated cache file paths
    """
    log = get_logger(__name__)
    dirs = PlatformDirs(appname="pushtunes", appauthor="psy-q")
    cache_dir = dirs.user_cache_dir

    invalidated = []

    if not os.path.exists(cache_dir):
        return invalidated

    # Find all JSON cache files
    for filename in os.listdir(cache_dir):
        if not filename.endswith('.json'):
            continue

        file_path = os.path.join(cache_dir, filename)

        # Parse filename
        parts = filename.replace('.json', '').rsplit('_', 1)
        if len(parts) != 2:
            continue

        file_service_name, file_content_type = parts

        if file_content_type not in ['albums', 'tracks']:
            continue

        # Check if this file matches our filter criteria
        if service_name and file_service_name != service_name:
            continue

        if content_type and file_content_type != content_type:
            continue

        # Remove the cache file
        try:
            os.remove(file_path)
            log.info(f"Invalidated cache: {filename}")
            invalidated.append(file_path)
        except Exception as e:
            log.error(f"Failed to invalidate cache {filename}: {e}")

    return invalidated
