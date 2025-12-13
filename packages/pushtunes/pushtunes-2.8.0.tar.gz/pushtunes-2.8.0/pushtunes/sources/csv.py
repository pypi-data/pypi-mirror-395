"""CSV music source implementation."""

from pushtunes.sources.base import MusicSource
from pushtunes.models.album import Album
from pushtunes.models.track import Track
from pushtunes.models.playlist import Playlist
from pushtunes.utils.csv_manager import CsvManager
from pushtunes.utils.logging import get_logger


class CSVSource(MusicSource):
    """CSV music source implementation that reads from a CSV file.

    CSV sources don't use caching as they read from local files.
    """

    log = get_logger()

    def __init__(self, csv_file: str):
        """Initialize CSV source.

        Args:
            csv_file: Path to the CSV file containing music data
        """
        self.csv_file = csv_file
        # CSV sources don't need caching, so we don't call super().__init__()

    def _fetch_albums(self) -> list[Album]:
        """Not used for CSV source (no caching needed)."""
        raise NotImplementedError("CSV source does not use caching")

    def _fetch_tracks(self) -> list[Track]:
        """Not used for CSV source (no caching needed)."""
        raise NotImplementedError("CSV source does not use caching")

    def get_albums(self) -> list[Album]:
        """Get all albums from the CSV file.

        Returns:
            list of Album objects
        """
        albums = CsvManager.import_albums(self.csv_file)

        self.log.info(f"Fetched {len(albums)} albums from CSV file {self.csv_file}")
        return albums

    def get_tracks(self) -> list[Track]:
        """Get all tracks from the CSV file.

        Returns:
            list of Track objects
        """
        tracks = CsvManager.import_tracks(self.csv_file)

        self.log.info(f"Fetched {len(tracks)} tracks from CSV file {self.csv_file}")
        return tracks

    def get_playlist(self, playlist_name: str, playlist_id: str | None = None) -> Playlist | None:
        """Get a playlist from the CSV file.

        The CSV file contains tracks, and the playlist name is used to name the playlist.
        If playlist_name is not provided or doesn't match the filename, the filename
        (without extension) is used as the playlist name.

        Args:
            playlist_name: Name of the playlist (used to name the imported playlist)
            playlist_id: Not used for CSV (uses file-based lookup only)

        Returns:
            Playlist object or None if the file doesn't exist
        """
        try:
            playlist = CsvManager.import_playlist(self.csv_file, playlist_name)
            self.log.info(f"Fetched playlist '{playlist.name}' with {len(playlist.tracks)} tracks from CSV file {self.csv_file}")
            return playlist
        except FileNotFoundError:
            self.log.error(f"CSV file not found: {self.csv_file}")
            return None
