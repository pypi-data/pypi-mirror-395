"""Tests for music service caching."""
import os
import time

from pushtunes.models.album import Album
from pushtunes.models.track import Track
from tests.test_doubles import MockMusicService


def test_album_caching(tmp_path):
    """Test that album caching saves and loads albums correctly."""
    cache_file = tmp_path / "mock_albums.json"

    original_albums = [
        Album(title="Album 1", artists=["Artist 1"], year=2023),
        Album(title="Album 2", artists=["Artist 2", "Artist 3"], year=2024),
    ]

    # 1. Create a service instance, set its albums, and save cache
    service = MockMusicService()
    service.cache.album_cache_file = str(cache_file)
    service.cache.albums = original_albums
    service.cache._save_album_cache()
    assert os.path.exists(cache_file)

    # 2. Load cache in a new service instance
    new_service = MockMusicService()
    new_service.cache.album_cache_file = str(cache_file)
    new_service.cache.load_album_cache()  # This will not trigger an update since cache is fresh

    # 3. Assert loaded albums are correct
    # Using set for comparison to be order-independent
    assert set(new_service.cache.albums) == set(original_albums)


def test_cache_expiration(tmp_path):
    """Test that the cache expiration logic works."""
    cache_file = tmp_path / "mock_albums.json"

    # 1. Create an old cache file with old data
    old_albums = [Album(title="Old Album", artists=["Old Artist"])]
    service = MockMusicService()
    service.cache.album_cache_file = str(cache_file)
    service.cache.albums = old_albums
    service.cache._save_album_cache()

    # Make the file seem old
    one_hour_ago = time.time() - 3601  # default expiry is 3600s
    os.utime(cache_file, (one_hour_ago, one_hour_ago))

    # 2. Create a new service instance with different "remote" albums
    new_remote_albums = [Album(title="New Album", artists=["New Artist"])]
    new_service = MockMusicService(library_albums=new_remote_albums)
    new_service.cache.album_cache_file = str(cache_file)

    # 3. Load cache, which should be expired and trigger an update
    # load_album_cache will call _update_album_cache, which calls get_library_albums
    new_service.cache.load_album_cache()

    # 4. Assert that the albums are the new ones, not the old ones
    assert new_service.cache.albums == new_remote_albums
    assert old_albums[0] not in new_service.cache.albums


def test_empty_album_library_creates_cache(tmp_path):
    """Test that cache is created even when library has 0 albums."""
    cache_file = tmp_path / "mock_albums.json"

    # Create a service with an empty library (0 albums)
    service = MockMusicService(library_albums=[])
    service.cache.album_cache_file = str(cache_file)

    # Force cache update
    service.cache._update_album_cache()

    # Cache file should exist even though library is empty
    assert os.path.exists(cache_file), "Cache file should be created for empty library"

    # Load the cache to verify it works
    new_service = MockMusicService()
    new_service.cache.album_cache_file = str(cache_file)
    new_service.cache.load_album_cache()

    # Should have 0 albums
    assert len(new_service.cache.albums) == 0


def test_empty_track_library_creates_cache(tmp_path):
    """Test that cache is created even when library has 0 tracks."""
    cache_file = tmp_path / "mock_tracks.json"

    # Create a service with an empty library (0 tracks)
    service = MockMusicService(library_tracks=[])
    service.cache.track_cache_file = str(cache_file)

    # Force cache update
    service.cache._update_track_cache()

    # Cache file should exist even though library is empty
    assert os.path.exists(cache_file), "Cache file should be created for empty library"

    # Load the cache to verify it works
    new_service = MockMusicService()
    new_service.cache.track_cache_file = str(cache_file)
    new_service.cache.load_track_cache()

    # Should have 0 tracks
    assert len(new_service.cache.tracks) == 0


def test_is_album_in_library_with_empty_cache(tmp_path):
    """Test that is_album_in_library works correctly with empty cache."""
    cache_file = tmp_path / "mock_albums.json"

    # Create a service with empty library
    service = MockMusicService(library_albums=[])
    service.cache.album_cache_file = str(cache_file)

    # Create and save empty cache
    service.cache._update_album_cache()

    # Try to check if an album is in library
    test_album = Album(title="Test Album", artists=["Test Artist"])
    result = service.is_album_in_library(test_album)

    # Should return False, not raise an error
    assert result is False


def test_is_track_in_library_with_empty_cache(tmp_path):
    """Test that is_track_in_library works correctly with empty cache."""
    cache_file = tmp_path / "mock_tracks.json"

    # Create a service with empty library
    service = MockMusicService(library_tracks=[])
    service.cache.track_cache_file = str(cache_file)

    # Create and save empty cache
    service.cache._update_track_cache()

    # Try to check if a track is in library
    test_track = Track(title="Test Track", artists=["Test Artist"])
    result = service.is_track_in_library(test_track)

    # Should return False, not raise an error
    assert result is False
