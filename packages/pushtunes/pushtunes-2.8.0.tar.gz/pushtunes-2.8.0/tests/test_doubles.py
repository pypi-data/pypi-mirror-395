"""Test doubles for pushtunes tests."""

from pushtunes.models.album import Album
from pushtunes.models.track import Track
from pushtunes.services.music_service import MusicService


class MockMusicService(MusicService):
    """A mock music service for testing."""

    def __init__(self, library_albums: list[Album] | None = None, library_tracks: list[Track] | None = None):
        self.service_name = "mock"
        self._library_albums = library_albums or []
        self._library_tracks = library_tracks or []
        super().__init__()

    def search_albums(self, album: Album) -> list[Album]:
        """Mock search_albums."""
        return []

    def is_album_in_library(self, album: Album) -> bool:
        """Mock is_album_in_library."""
        return album in self.cache.albums

    def add_album(self, album: Album) -> bool:
        """Mock add_album."""
        self.cache.albums.append(album)
        return True

    def remove_album(self, album: Album) -> bool:
        """Mock remove_album."""
        if album in self.cache.albums:
            self.cache.albums.remove(album)
            return True
        return False

    def get_library_albums(self) -> list[Album]:
        """Mock get_library_albums."""
        self.cache.albums = self._library_albums
        return self.cache.albums

    def search_tracks(self, track: Track) -> list[Track]:
        """Mock search_tracks."""
        return []

    def is_track_in_library(self, track: Track) -> bool:
        """Mock is_track_in_library."""
        return track in self.cache.tracks

    def add_track(self, track: Track) -> bool:
        """Mock add_track."""
        self.cache.tracks.append(track)
        return True

    def remove_track(self, track: Track) -> bool:
        """Mock remove_track."""
        if track in self.cache.tracks:
            self.cache.tracks.remove(track)
            return True
        return False

    def get_library_tracks(self) -> list[Track]:
        """Mock get_library_tracks."""
        self.cache.tracks = self._library_tracks
        return self.cache.tracks
