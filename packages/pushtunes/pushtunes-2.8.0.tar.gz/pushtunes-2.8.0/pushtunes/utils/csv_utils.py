"""CSV utilities for importing and exporting song data.

This module now delegates to CsvManager for all operations.
"""

from .csv_manager import CsvManager

# Re-export all CsvManager methods for backward compatibility
export_albums_to_csv = CsvManager.export_albums
import_albums_from_csv = CsvManager.import_albums
export_tracks_to_csv = CsvManager.export_tracks
import_tracks_from_csv = CsvManager.import_tracks
export_playlist_to_csv = CsvManager.export_playlist
import_playlist_from_csv = CsvManager.import_playlist
export_album_results_to_csv = CsvManager.export_album_results
export_track_results_to_csv = CsvManager.export_track_results
export_album_results_to_mappings_csv = CsvManager.export_album_results_to_mappings
export_track_results_to_mappings_csv = CsvManager.export_track_results_to_mappings
