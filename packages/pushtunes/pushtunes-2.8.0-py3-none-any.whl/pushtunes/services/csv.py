"""CSV service implementation for exporting music to CSV files."""

from pushtunes.services.music_service import MusicService
from pushtunes.models.album import Album
from pushtunes.models.track import Track
from pushtunes.models.playlist import Playlist
from pushtunes.utils.csv_manager import CsvManager
from pushtunes.utils.logging import get_logger


class CSVService(MusicService):
    """CSV service that writes albums, tracks, or playlists to CSV files."""

    service_name = "csv"
    log = get_logger()

    def __init__(self, csv_file: str):
        """Initialize CSV service.

        Args:
            csv_file: Path to the output CSV file
        """
        # Don't call super().__init__() because we don't need cache files
        self.csv_file = csv_file
        self.collected_albums: list[Album] = []
        self.collected_tracks: list[Track] = []
        self.collected_playlist: Playlist | None = None

    def search_albums(self, album: Album) -> list[Album]:
        """CSV doesn't search - just return the album itself."""
        return [album]

    def is_album_in_library(self, album: Album) -> bool:
        """CSV always returns False so everything gets added."""
        return False

    def add_album(self, album: Album) -> bool:
        """Add album to collection for later CSV export."""
        self.collected_albums.append(album)
        return True

    def search_tracks(self, track: Track) -> list[Track]:
        """CSV doesn't search - just return the track itself."""
        return [track]

    def is_track_in_library(self, track: Track) -> bool:
        """CSV always returns False so everything gets added."""
        return False

    def add_track(self, track: Track) -> bool:
        """Add track to collection for later CSV export."""
        self.collected_tracks.append(track)
        return True

    def remove_album(self, album: Album) -> bool:
        """CSV service doesn't support deletion."""
        self.log.warning("CSV service does not support removing albums")
        return False

    def remove_track(self, track: Track) -> bool:
        """CSV service doesn't support deletion."""
        self.log.warning("CSV service does not support removing tracks")
        return False

    def create_playlist(self, name: str, description: str = "") -> str:
        """Create a playlist (just stores the name)."""
        self.collected_playlist = Playlist(name=name, tracks=[])
        return name  # Return the name as a fake ID

    def add_tracks_to_playlist(self, playlist_id: str, track_ids: list[str]) -> bool:
        """Add tracks to the playlist being collected."""
        # track_ids are actually Track objects stored as service_ids
        # We'll handle this specially in the playlist pusher
        return True

    def get_user_playlists(self) -> list[dict]:
        """CSV doesn't have existing playlists."""
        return []

    def get_playlist_tracks(self, playlist_id: str) -> list[Track]:
        """CSV doesn't have existing playlists."""
        return []

    def replace_playlist_tracks(self, playlist_id: str, track_ids: list[str]) -> bool:
        """Replace tracks in playlist."""
        return True

    def remove_tracks_from_playlist(self, playlist_id: str, track_ids: list[str]) -> bool:
        """Remove tracks from playlist."""
        return True

    def write_albums_to_csv(self) -> None:
        """Write collected albums to CSV file."""
        if self.collected_albums:
            CsvManager.export_albums(self.collected_albums, self.csv_file)
            self.log.info(f"Wrote {len(self.collected_albums)} albums to {self.csv_file}")
        else:
            self.log.warning("No albums to write to CSV")

    def write_tracks_to_csv(self) -> None:
        """Write collected tracks to CSV file."""
        if self.collected_tracks:
            CsvManager.export_tracks(self.collected_tracks, self.csv_file)
            self.log.info(f"Wrote {len(self.collected_tracks)} tracks to {self.csv_file}")
        else:
            self.log.warning("No tracks to write to CSV")

    def write_playlist_to_csv(self, playlist: Playlist) -> None:
        """Write a playlist to CSV file.

        Args:
            playlist: Playlist object with tracks to export
        """
        if playlist and playlist.tracks:
            CsvManager.export_playlist(playlist, self.csv_file)
            self.log.info(f"Wrote playlist '{playlist.name}' with {len(playlist.tracks)} tracks to {self.csv_file}")
        else:
            self.log.warning("No playlist or tracks to write to CSV")
