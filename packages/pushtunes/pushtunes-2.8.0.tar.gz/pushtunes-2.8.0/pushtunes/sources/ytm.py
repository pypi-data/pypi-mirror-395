"""YouTube Music source for playlist retrieval."""

from .base import MusicSource
from ..models.album import Album
from ..models.track import Track
from ..models.playlist import Playlist
from ..services.ytm import YTMService
from ..utils.logging import get_logger


class YTMSource(MusicSource):
    """YouTube Music source for retrieving playlists.

    This is a thin wrapper around YTMService that implements the MusicSource
    interface, allowing YouTube Music to be used as a source for playlist pushing.

    Caching is handled by the underlying YTMService, not by MusicSource.
    """

    def __init__(self, auth_file: str = "browser.json"):
        """Initialize YouTube Music source.

        Args:
            auth_file: Path to ytmusicapi browser authentication file
        """
        self.log = get_logger(__name__)
        self.service = YTMService(auth_file=auth_file)
        self.service_name = "ytm"
        # YTM uses service-level caching, so we don't call super().__init__()

    def _fetch_albums(self) -> list[Album]:
        """Not used for YTM source (caching handled by YTMService)."""
        raise NotImplementedError("YTM source uses service-level caching")

    def _fetch_tracks(self) -> list[Track]:
        """Not used for YTM source (caching handled by YTMService)."""
        raise NotImplementedError("YTM source uses service-level caching")

    def get_albums(self) -> list[Album]:
        """Get all albums from YouTube Music library.

        Uses cached data if available and not expired (1 hour TTL).

        Returns:
            List of Album objects from user's YouTube Music library
        """
        if len(self.service.cache.albums) == 0:
            self.service.cache.load_album_cache()
        return self.service.cache.albums

    def get_tracks(self) -> list[Track]:
        """Get all tracks from YouTube Music library.

        Uses cached data if available and not expired (1 hour TTL).

        Returns:
            List of Track objects from user's YouTube Music library
        """
        if len(self.service.cache.tracks) == 0:
            self.service.cache.load_track_cache()
        return self.service.cache.tracks

    def get_playlist(self, playlist_name: str, playlist_id: str | None = None) -> Playlist | None:
        """Get a specific playlist by name or ID from YouTube Music.

        Args:
            playlist_name: Name of the playlist to retrieve
            playlist_id: Optional YTM playlist ID for direct lookup

        Returns:
            Playlist object if found, None otherwise
        """
        # If ID is provided, use it directly
        if playlist_id:
            self.log.info(f"Fetching YTM playlist by ID: {playlist_id}")
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
        self.log.info(f"Searching for YTM playlist by name: {playlist_name}")
        try:
            user_playlists = self.service.get_user_playlists()

            # Find playlist by name (case-insensitive)
            target_playlist = None
            for pl in user_playlists:
                if pl['title'].lower() == playlist_name.lower():
                    target_playlist = pl
                    break

            if not target_playlist:
                self.log.error(f"Playlist '{playlist_name}' not found in user's YTM playlists")
                return None

            # Get tracks from the found playlist
            playlist_id = target_playlist['playlistId']
            tracks = self.service.get_playlist_tracks(playlist_id)

            if not tracks:
                self.log.warning(f"Playlist '{playlist_name}' found but has no tracks")
                return Playlist(name=target_playlist['title'], tracks=[])

            self.log.info(f"Fetched playlist '{target_playlist['title']}' with {len(tracks)} tracks from YTM")
            return Playlist(name=target_playlist['title'], tracks=tracks)

        except Exception as e:
            self.log.error(f"Error fetching playlist from YTM: {e}")
            return None
