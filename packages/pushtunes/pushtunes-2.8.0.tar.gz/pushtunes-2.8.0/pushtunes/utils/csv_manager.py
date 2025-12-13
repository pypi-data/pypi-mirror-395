"""Centralized CSV manager for all CSV operations in pushtunes."""

import csv
import os
from typing import Callable

from ..models.album import Album
from ..models.track import Track
from ..models.playlist import Playlist
from .artist_utils import parse_artist_string


class CsvColumns:
    """Column definitions for all CSV formats (single source of truth)."""

    ALBUM_EXPORT = ["type", "artist", "album", "year", "spotify_id", "ytm_id", "tidal_id"]
    TRACK_EXPORT = ["type", "artist", "track", "album", "year", "spotify_id", "ytm_id", "tidal_id"]
    MAPPINGS = [
        "type",
        "artist",
        "title",
        "spotify_id",
        "ytm_id",
        "tidal_id",
        "spotify_artist",
        "spotify_title",
        "ytm_artist",
        "ytm_title",
        "tidal_artist",
        "tidal_title",
        "subsonic_artist",
        "subsonic_title",
        "subsonic_album",
        "jellyfin_artist",
        "jellyfin_title",
        "jellyfin_album",
    ]

    # Column names for unified format
    TYPE = "type"
    ARTIST = "artist"
    ALBUM = "album"
    TRACK = "track"
    TITLE = "title"
    YEAR = "year"
    SPOTIFY_ID = "spotify_id"
    YTM_ID = "ytm_id"
    TIDAL_ID = "tidal_id"

    # Column indices for mappings (used for validation)
    MAPPINGS_TYPE = "type"
    MAPPINGS_ARTIST = "artist"
    MAPPINGS_TITLE = "title"
    MAPPINGS_SPOTIFY_ID = "spotify_id"
    MAPPINGS_YTM_ID = "ytm_id"
    MAPPINGS_TIDAL_ID = "tidal_id"
    MAPPINGS_SPOTIFY_ARTIST = "spotify_artist"
    MAPPINGS_SPOTIFY_TITLE = "spotify_title"
    MAPPINGS_YTM_ARTIST = "ytm_artist"
    MAPPINGS_YTM_TITLE = "ytm_title"
    MAPPINGS_TIDAL_ARTIST = "tidal_artist"
    MAPPINGS_TIDAL_TITLE = "tidal_title"
    MAPPINGS_SUBSONIC_ARTIST = "subsonic_artist"
    MAPPINGS_SUBSONIC_TITLE = "subsonic_title"
    MAPPINGS_SUBSONIC_ALBUM = "subsonic_album"
    MAPPINGS_JELLYFIN_ARTIST = "jellyfin_artist"
    MAPPINGS_JELLYFIN_TITLE = "jellyfin_title"
    MAPPINGS_JELLYFIN_ALBUM = "jellyfin_album"


class CsvManager:
    """Centralized manager for all CSV operations."""

    # Standard CSV settings
    ENCODING = "utf-8"
    QUOTING = csv.QUOTE_ALL

    @staticmethod
    def _open_for_write(csv_file: str):
        """Standard file opening for CSV writes."""
        return open(csv_file, "w", newline="", encoding=CsvManager.ENCODING)

    @staticmethod
    def _open_for_read(csv_file: str):
        """Standard file opening for CSV reads."""
        return open(csv_file, "r", newline="", encoding=CsvManager.ENCODING)

    @staticmethod
    def _extract_service_ids(item: Album | Track) -> tuple[str, str, str]:
        """Extract spotify_id, ytm_id, and tidal_id from an item.

        Args:
            item: Album or Track object

        Returns:
            Tuple of (spotify_id, ytm_id, tidal_id)
        """
        spotify_id = item.service_id if item.service_name == "spotify" else ""
        ytm_id = item.service_id if item.service_name == "ytm" else ""
        tidal_id = item.service_id if item.service_name == "tidal" else ""
        return spotify_id, ytm_id, tidal_id

    @staticmethod
    def export_albums(albums: list[Album], csv_file: str) -> None:
        """Export a list of albums to a CSV file.

        Args:
            albums: list of Album objects to export
            csv_file: Path to the output CSV file
        """
        with CsvManager._open_for_write(csv_file) as f:
            writer = csv.writer(f, quoting=CsvManager.QUOTING)
            writer.writerow(CsvColumns.ALBUM_EXPORT)

            for album in albums:
                spotify_id, ytm_id, tidal_id = CsvManager._extract_service_ids(album)
                writer.writerow(
                    ["album", album.artist, album.title, album.year or "", spotify_id, ytm_id, tidal_id]
                )

    @staticmethod
    def import_albums(csv_file: str) -> list[Album]:
        """Import albums from a CSV file with 'artist', 'album' fields.
        Supports multiple artist columns: 'artist', 'artist2', ..., 'artist10'.
        Also supports service IDs: 'spotify_id' and 'ytm_id' columns.
        Supports optional 'type' column for unified CSV format (backward compatible).

        Args:
            csv_file: Path to the input CSV file

        Returns:
            list of Album objects
        """
        albums = []
        with CsvManager._open_for_read(csv_file) as f:
            reader = csv.DictReader(f)

            # Check if CSV has type column (unified format)
            has_type_column = CsvColumns.TYPE in reader.fieldnames if reader.fieldnames else False

            for row in reader:
                # If unified CSV, filter by type
                if has_type_column:
                    row_type = row.get(CsvColumns.TYPE, "").strip().lower()
                    if row_type and row_type != "album":
                        continue  # Skip non-album rows

                artist_names = []
                # Check for artist2, artist3 etc. first
                for i in range(2, 11):
                    additional_artist = row.get(f"artist{i}")
                    if additional_artist:
                        artist_names.append(additional_artist)

                primary_artist = row.get("artist")
                if primary_artist:
                    # If there were additional artist columns, we assume the user has
                    # already split the artists and we just prepend the primary artist.
                    # If not, we parse the primary artist string for separators.
                    if artist_names:
                        artist_names.insert(0, primary_artist)
                    else:
                        artist_names.extend(parse_artist_string(primary_artist))

                year_str = row.get("year")
                year = int(year_str) if year_str else None

                # Store both service IDs in extra_data
                extra_data = {}
                spotify_id = row.get("spotify_id", "").strip()
                ytm_id = row.get("ytm_id", "").strip()

                if spotify_id:
                    extra_data["spotify_id"] = spotify_id
                if ytm_id:
                    extra_data["ytm_id"] = ytm_id

                album = Album(
                    artists=artist_names,
                    title=row.get("album", ""),
                    year=year,
                    extra_data=extra_data if extra_data else None,
                )
                albums.append(album)
        return albums

    @staticmethod
    def export_tracks(tracks: list[Track], csv_file: str) -> None:
        """Export a list of tracks to a CSV file.

        Args:
            tracks: list of Track objects to export
            csv_file: Path to the output CSV file
        """
        with CsvManager._open_for_write(csv_file) as f:
            writer = csv.writer(f, quoting=CsvManager.QUOTING)
            writer.writerow(CsvColumns.TRACK_EXPORT)

            for track in tracks:
                spotify_id, ytm_id, tidal_id = CsvManager._extract_service_ids(track)
                writer.writerow(
                    [
                        "track",
                        track.artist,
                        track.title,
                        track.album or "",
                        track.year or "",
                        spotify_id,
                        ytm_id,
                        tidal_id,
                    ]
                )

    @staticmethod
    def import_tracks(csv_file: str) -> list[Track]:
        """Import tracks from a CSV file with 'artist' and 'track' fields.
        Supports single artist per track (as per requirements).
        Also supports service IDs: 'spotify_id' and 'ytm_id' columns.
        Supports optional 'type' column for unified CSV format (backward compatible).

        Args:
            csv_file: Path to the input CSV file

        Returns:
            list of Track objects
        """
        tracks = []
        with CsvManager._open_for_read(csv_file) as f:
            reader = csv.DictReader(f)

            # Check if CSV has type column (unified format)
            has_type_column = CsvColumns.TYPE in reader.fieldnames if reader.fieldnames else False

            for row in reader:
                # If unified CSV, filter by type
                if has_type_column:
                    row_type = row.get(CsvColumns.TYPE, "").strip().lower()
                    if row_type and row_type != "track":
                        continue  # Skip non-track rows

                artist = row.get("artist", "")
                artist_list = [artist] if artist else []

                year_str = row.get("year")
                year = int(year_str) if year_str and year_str.isdigit() else None

                # Store both service IDs in extra_data
                extra_data = {}
                spotify_id = row.get("spotify_id", "").strip()
                ytm_id = row.get("ytm_id", "").strip()

                if spotify_id:
                    extra_data["spotify_id"] = spotify_id
                if ytm_id:
                    extra_data["ytm_id"] = ytm_id

                track = Track(
                    artists=artist_list,
                    title=row.get("track", "") or row.get("title", ""),
                    album=row.get("album") or None,
                    year=year,
                    extra_data=extra_data if extra_data else None,
                )
                tracks.append(track)
        return tracks

    @staticmethod
    def export_playlist(playlist: Playlist, csv_file: str) -> None:
        """Export a playlist to a CSV file.

        Uses the same format as tracks (artist, track, album, year).

        Args:
            playlist: Playlist object to export
            csv_file: Path to the output CSV file
        """
        CsvManager.export_tracks(playlist.tracks, csv_file)

    @staticmethod
    def import_playlist(csv_file: str, playlist_name: str | None = None) -> Playlist:
        """Import a playlist from a CSV file.

        Uses the same format as tracks (artist, track, album, year).

        Args:
            csv_file: Path to the input CSV file
            playlist_name: Name for the playlist (defaults to filename without extension)

        Returns:
            Playlist object
        """
        tracks = CsvManager.import_tracks(csv_file)

        # Use filename (without extension) as playlist name if not provided
        if not playlist_name:
            playlist_name = os.path.splitext(os.path.basename(csv_file))[0]

        return Playlist(name=playlist_name, tracks=tracks)

    @staticmethod
    def export_album_results(
        results: list, status_filter: list[str], csv_file: str
    ) -> int:
        """Export album results matching specified statuses to a CSV file.

        Args:
            results: List of PushResult[Album] objects
            status_filter: List of status names to include (e.g., ['not_found', 'similarity_too_low'])
            csv_file: Path to the output CSV file

        Returns:
            Number of albums exported
        """
        # Filter results by status
        filtered = [r for r in results if r.status.name in status_filter]

        if not filtered:
            return 0

        # Extract albums from results
        albums = [r.item for r in filtered]

        # Export using existing function
        CsvManager.export_albums(albums, csv_file)

        return len(albums)

    @staticmethod
    def export_track_results(
        results: list, status_filter: list[str], csv_file: str
    ) -> int:
        """Export track results matching specified statuses to a CSV file.

        Args:
            results: List of PushResult[Track] objects
            status_filter: List of status names to include (e.g., ['not_found', 'similarity_too_low'])
            csv_file: Path to the output CSV file

        Returns:
            Number of tracks exported
        """
        # Filter results by status
        filtered = [r for r in results if r.status.name in status_filter]

        if not filtered:
            return 0

        # Extract tracks from results
        tracks = [r.item for r in filtered]

        # Export using existing function
        CsvManager.export_tracks(tracks, csv_file)

        return len(tracks)

    @staticmethod
    def _read_existing_mappings(
        csv_file: str,
    ) -> tuple[dict[tuple, dict], list[dict], set[tuple]]:
        """Read existing mappings CSV file and return existing rows preserving all data.

        Uses DictReader instead of index-based access for robustness.

        Args:
            csv_file: Path to the existing CSV file

        Returns:
            Tuple of (existing_mappings_dict, existing_rows_list, mapped_items_set)
            - existing_mappings_dict: Maps (type, artist_lower, title_lower) -> full row dict
            - existing_rows_list: List of all existing rows (as dicts) to preserve order
            - mapped_items_set: Set of keys for items that have at least one target field filled
        """
        existing_mappings = {}
        existing_rows = []
        mapped_items = set()

        if not os.path.exists(csv_file):
            return existing_mappings, existing_rows, mapped_items

        with CsvManager._open_for_read(csv_file) as f:
            reader = csv.DictReader(f)

            # Verify required columns exist
            if not reader.fieldnames:
                return existing_mappings, existing_rows, mapped_items

            for row in reader:
                # Need at minimum type, artist, title
                if not all(
                    k in row
                    for k in [
                        CsvColumns.MAPPINGS_TYPE,
                        CsvColumns.MAPPINGS_ARTIST,
                        CsvColumns.MAPPINGS_TITLE,
                    ]
                ):
                    continue

                item_type = row[CsvColumns.MAPPINGS_TYPE].lower()
                artist = row[CsvColumns.MAPPINGS_ARTIST]
                title = row[CsvColumns.MAPPINGS_TITLE]

                # Create lookup key (case-insensitive)
                key = (item_type, artist.lower(), title.lower())
                existing_mappings[key] = row
                existing_rows.append(row)

                # Check if this item has any target fields filled in
                target_fields = [
                    CsvColumns.MAPPINGS_SPOTIFY_ID,
                    CsvColumns.MAPPINGS_YTM_ID,
                    CsvColumns.MAPPINGS_SPOTIFY_ARTIST,
                    CsvColumns.MAPPINGS_SPOTIFY_TITLE,
                    CsvColumns.MAPPINGS_YTM_ARTIST,
                    CsvColumns.MAPPINGS_YTM_TITLE,
                    CsvColumns.MAPPINGS_SUBSONIC_ARTIST,
                    CsvColumns.MAPPINGS_SUBSONIC_TITLE,
                    CsvColumns.MAPPINGS_SUBSONIC_ALBUM,
                    CsvColumns.MAPPINGS_JELLYFIN_ARTIST,
                    CsvColumns.MAPPINGS_JELLYFIN_TITLE,
                    CsvColumns.MAPPINGS_JELLYFIN_ALBUM,
                ]
                has_mapping = any(row.get(field, "").strip() for field in target_fields)
                if has_mapping:
                    mapped_items.add(key)

        return existing_mappings, existing_rows, mapped_items

    @staticmethod
    def _export_results_to_mappings(
        results: list,
        item_type: str,
        status_filter: list[str],
        csv_file: str,
        get_artist: Callable,
        get_title: Callable,
    ) -> tuple[int, int]:
        """Generic mappings export function (consolidates album and track versions).

        Creates a CSV file in the mappings format with empty target fields that the user can fill in.

        This function operates incrementally: if the target file already exists, it will:
        - Preserve all existing rows and their data (especially user-filled IDs and titles)
        - Only add NEW items that aren't already in the file
        - Never delete or modify existing mappings

        This allows users to run export multiple times and gradually build up a mappings file
        without losing manual edits.

        Args:
            results: List of PushResult objects (PushResult[Album] or PushResult[Track])
            item_type: Type of item ("album" or "track")
            status_filter: List of status names to include (e.g., ['not_found'])
            csv_file: Path to the output CSV file
            get_artist: Function to extract artist from result
            get_title: Function to extract title from result

        Returns:
            Tuple of (new_count, already_unmapped_count):
            - new_count: Number of NEW items added to the file
            - already_unmapped_count: Number of failed items already in file with empty target fields
        """
        # Filter results by status
        filtered = [r for r in results if r.status.name in status_filter]

        # Read existing mappings to preserve user data
        (
            existing_mappings,
            existing_rows,
            mapped_items,
        ) = CsvManager._read_existing_mappings(csv_file)

        # Collect new rows to add and count items already in file
        new_rows = []
        already_in_file_unmapped = 0

        for result in filtered:
            artist = get_artist(result)
            title = get_title(result)

            # Create lookup key (case-insensitive)
            key = (item_type, artist.lower(), title.lower())

            if key in mapped_items:
                # Already in file with filled target fields - skip completely
                continue
            elif key in existing_mappings:
                # In file but with empty target fields - count it but don't add duplicate
                already_in_file_unmapped += 1
            else:
                # Brand new item - add it
                new_rows.append(
                    {
                        CsvColumns.MAPPINGS_TYPE: item_type,
                        CsvColumns.MAPPINGS_ARTIST: artist,
                        CsvColumns.MAPPINGS_TITLE: title,
                        CsvColumns.MAPPINGS_SPOTIFY_ID: "",
                        CsvColumns.MAPPINGS_YTM_ID: "",
                        CsvColumns.MAPPINGS_SPOTIFY_ARTIST: "",
                        CsvColumns.MAPPINGS_SPOTIFY_TITLE: "",
                        CsvColumns.MAPPINGS_YTM_ARTIST: "",
                        CsvColumns.MAPPINGS_YTM_TITLE: "",
                        CsvColumns.MAPPINGS_SUBSONIC_ARTIST: "",
                        CsvColumns.MAPPINGS_SUBSONIC_TITLE: "",
                        CsvColumns.MAPPINGS_SUBSONIC_ALBUM: "",
                        CsvColumns.MAPPINGS_JELLYFIN_ARTIST: "",
                        CsvColumns.MAPPINGS_JELLYFIN_TITLE: "",
                        CsvColumns.MAPPINGS_JELLYFIN_ALBUM: "",
                    }
                )

        # If no existing rows and no new rows, nothing to write
        if not existing_rows and not new_rows:
            return (0, already_in_file_unmapped)

        # Write all rows (existing + new) to file
        with CsvManager._open_for_write(csv_file) as f:
            writer = csv.DictWriter(f, fieldnames=CsvColumns.MAPPINGS, quoting=CsvManager.QUOTING)
            writer.writeheader()

            # Write existing rows first (preserving user data)
            for row in existing_rows:
                writer.writerow(row)

            # Write new rows
            for row in new_rows:
                writer.writerow(row)

        return (len(new_rows), already_in_file_unmapped)

    @staticmethod
    def export_album_results_to_mappings(
        results: list, status_filter: list[str], csv_file: str
    ) -> tuple[int, int]:
        """Export album results matching specified statuses to a mappings CSV file.

        Args:
            results: List of PushResult[Album] objects
            status_filter: List of status names to include (e.g., ['not_found'])
            csv_file: Path to the output CSV file

        Returns:
            Tuple of (new_count, already_unmapped_count)
        """
        return CsvManager._export_results_to_mappings(
            results=results,
            item_type="album",
            status_filter=status_filter,
            csv_file=csv_file,
            get_artist=lambda r: r.item.artist,
            get_title=lambda r: r.item.title,
        )

    @staticmethod
    def export_track_results_to_mappings(
        results: list, status_filter: list[str], csv_file: str
    ) -> tuple[int, int]:
        """Export track results matching specified statuses to a mappings CSV file.

        Args:
            results: List of PushResult[Track] objects
            status_filter: List of status names to include (e.g., ['not_found'])
            csv_file: Path to the output CSV file

        Returns:
            Tuple of (new_count, already_unmapped_count)
        """
        return CsvManager._export_results_to_mappings(
            results=results,
            item_type="track",
            status_filter=status_filter,
            csv_file=csv_file,
            get_artist=lambda r: r.item.artist,
            get_title=lambda r: r.item.title,
        )
