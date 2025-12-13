"""Tests for CSV music source."""

import unittest
import os
import csv
from pushtunes.sources.csv import CSVSource
from pushtunes.models.album import Album
from pushtunes.models.track import Track
from pushtunes.models.push_status import PushStatus
from pushtunes.utils.csv_utils import (
    import_tracks_from_csv, export_tracks_to_csv,
    export_album_results_to_csv, export_track_results_to_csv,
    export_album_results_to_mappings_csv, export_track_results_to_mappings_csv
)


class TestCSVSource(unittest.TestCase):
    def setUp(self):
        # Create a temporary CSV file for testing
        self.csv_file = "test_albums.csv"
        with open(self.csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["artist", "artist2", "artist3", "album", "year"])
            writer.writerow(["Artist A", "Artist B", "", "Album 1", "2023"])
            writer.writerow(["Artist C", "", "", "Album 2", "2024"])
            writer.writerow(["Artist D", "Artist E", "Artist F", "Album 3", "2025"])
            writer.writerow(["", "", "", "Album 4", "2026"])  # No artists
            writer.writerow(["Bohren & der Club of Gore", "", "", "Sunset Mission", "2000"])
            writer.writerow(["VV & The Void", "", "", "The Upper Room", "2010"])
            writer.writerow(["Black Hill", "Eensdenkend", "", "Black Turns Grey", "2015"])


    def tearDown(self):
        # Clean up the temporary CSV file
        if os.path.exists(self.csv_file):
            os.remove(self.csv_file)

    def test_import_albums_from_csv_multiple_artists(self):
        """Test importing albums from CSV with multiple artist columns."""
        csv_source = CSVSource(self.csv_file)
        albums = csv_source.get_albums()

        self.assertEqual(len(albums), 7) # Updated count

        # Album 1: Artist A, Artist B
        self.assertEqual(albums[0].artists, ["Artist A", "Artist B"])
        self.assertEqual(albums[0].title, "Album 1")
        self.assertEqual(albums[0].year, 2023)

        # Album 2: Artist C
        self.assertEqual(albums[1].artists, ["Artist C"])
        self.assertEqual(albums[1].title, "Album 2")
        self.assertEqual(albums[1].year, 2024)

        # Album 3: Artist D, Artist E, Artist F
        self.assertEqual(albums[2].artists, ["Artist D", "Artist E", "Artist F"])
        self.assertEqual(albums[2].title, "Album 3")
        self.assertEqual(albums[2].year, 2025)

        # Album 4: No artists
        self.assertEqual(albums[3].artists, [])
        self.assertEqual(albums[3].title, "Album 4")
        self.assertEqual(albums[3].year, 2026)

        # Album 5: Bohren & der Club of Gore
        self.assertEqual(albums[4].artists, ["Bohren", "der Club of Gore"])
        self.assertEqual(albums[4].title, "Sunset Mission")
        self.assertEqual(albums[4].year, 2000)

        # Album 6: VV & The Void
        self.assertEqual(albums[5].artists, ["VV", "The Void"])
        self.assertEqual(albums[5].title, "The Upper Room")
        self.assertEqual(albums[5].year, 2010)

        # Album 7: Black Hill, Eensdenkend
        self.assertEqual(albums[6].artists, ["Black Hill", "Eensdenkend"])
        self.assertEqual(albums[6].title, "Black Turns Grey")
        self.assertEqual(albums[6].year, 2015)


    def test_import_albums_from_csv_no_artists_column(self):
        """Test importing albums from CSV without any artist columns."""
        no_artist_csv_file = "test_no_artist.csv"
        with open(no_artist_csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["album", "year"]) # Changed "title" to "album"
            writer.writerow(["Album X", "2020"])

        csv_source = CSVSource(no_artist_csv_file)
        albums = csv_source.get_albums()

        self.assertEqual(len(albums), 1)
        self.assertEqual(albums[0].artists, [])
        self.assertEqual(albums[0].title, "Album X")
        self.assertEqual(albums[0].year, 2020)

        os.remove(no_artist_csv_file)


class TestTrackCSVImportExport(unittest.TestCase):
    """Test CSV import/export for tracks."""

    def setUp(self):
        """Create temporary CSV file for testing."""
        self.csv_file = "test_tracks.csv"

    def tearDown(self):
        """Clean up temporary files."""
        if os.path.exists(self.csv_file):
            os.remove(self.csv_file)

    def test_import_tracks_basic(self):
        """Test importing tracks from CSV."""
        with open(self.csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["artist", "track", "album", "year"])
            writer.writerow(["Dire Straits", "Sultans of Swing", "Dire Straits", "1978"])
            writer.writerow(["Thy Catafalque", "Molekuláris Gépezetek", "Róka Hasa Rádió", "2009"])

        tracks = import_tracks_from_csv(self.csv_file)

        self.assertEqual(len(tracks), 2)

        # Track 1
        self.assertEqual(tracks[0].artists, ["Dire Straits"])
        self.assertEqual(tracks[0].title, "Sultans of Swing")
        self.assertEqual(tracks[0].album, "Dire Straits")
        self.assertEqual(tracks[0].year, 1978)

        # Track 2
        self.assertEqual(tracks[1].artists, ["Thy Catafalque"])
        self.assertEqual(tracks[1].title, "Molekuláris Gépezetek")
        self.assertEqual(tracks[1].album, "Róka Hasa Rádió")
        self.assertEqual(tracks[1].year, 2009)

    def test_import_tracks_optional_fields(self):
        """Test importing tracks with optional album and year fields."""
        with open(self.csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["artist", "track", "album", "year"])
            writer.writerow(["Artist A", "Track 1", "", ""])
            writer.writerow(["Artist B", "Track 2", "Album B", ""])
            writer.writerow(["Artist C", "Track 3", "", "2020"])

        tracks = import_tracks_from_csv(self.csv_file)

        self.assertEqual(len(tracks), 3)

        # Track without album or year
        self.assertIsNone(tracks[0].album)
        self.assertIsNone(tracks[0].year)

        # Track with album but no year
        self.assertEqual(tracks[1].album, "Album B")
        self.assertIsNone(tracks[1].year)

        # Track with year but no album
        self.assertIsNone(tracks[2].album)
        self.assertEqual(tracks[2].year, 2020)

    def test_import_tracks_title_fallback(self):
        """Test that 'title' column works as fallback for 'track'."""
        with open(self.csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["artist", "title", "album", "year"])
            writer.writerow(["Artist", "Track Title", "Album", "2020"])

        tracks = import_tracks_from_csv(self.csv_file)

        self.assertEqual(len(tracks), 1)
        self.assertEqual(tracks[0].title, "Track Title")

    def test_export_tracks(self):
        """Test exporting tracks to CSV."""
        tracks = [
            Track(artists=["Artist A"], title="Track 1", album="Album A", year=2020),
            Track(artists=["Artist B"], title="Track 2", album=None, year=2021),
            Track(artists=["Artist C", "Artist D"], title="Track 3", album="Album C", year=None),
        ]

        export_tracks_to_csv(tracks, self.csv_file)

        # Verify the exported CSV
        with open(self.csv_file, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        self.assertEqual(len(rows), 3)

        # Check first row
        self.assertEqual(rows[0]["artist"], "Artist A")
        self.assertEqual(rows[0]["track"], "Track 1")
        self.assertEqual(rows[0]["album"], "Album A")
        self.assertEqual(rows[0]["year"], "2020")
        self.assertEqual(rows[0]["spotify_id"], "")
        self.assertEqual(rows[0]["ytm_id"], "")

        # Check row with no album
        self.assertEqual(rows[1]["album"], "")

        # Check multi-artist (should use & format)
        self.assertEqual(rows[2]["artist"], "Artist C & Artist D")

    def test_csv_source_get_tracks(self):
        """Test CSVSource get_tracks method."""
        with open(self.csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["artist", "track", "album", "year"])
            writer.writerow(["Test Artist", "Test Track", "Test Album", "2023"])

        csv_source = CSVSource(self.csv_file)
        tracks = csv_source.get_tracks()

        self.assertEqual(len(tracks), 1)
        self.assertEqual(tracks[0].artists, ["Test Artist"])
        self.assertEqual(tracks[0].title, "Test Track")


class TestExportResultsToCSV(unittest.TestCase):
    """Test exporting push results to CSV."""

    def setUp(self):
        """Create temporary CSV file for testing."""
        self.csv_file = "test_export.csv"

    def tearDown(self):
        """Clean up temporary files."""
        if os.path.exists(self.csv_file):
            os.remove(self.csv_file)

    def test_export_album_results_to_csv(self):
        """Test exporting album results to CSV."""
        from dataclasses import dataclass

        @dataclass
        class AlbumResult:
            item: Album
            status: PushStatus
            message: str = ""

        # Create mock results
        results = [
            AlbumResult(
                item=Album(artists=["Artist A"], title="Album 1", year=2020),
                status=PushStatus.not_found,
                message="Not found"
            ),
            AlbumResult(
                item=Album(artists=["Artist B"], title="Album 2", year=2021),
                status=PushStatus.similarity_too_low,
                message="Low similarity"
            ),
            AlbumResult(
                item=Album(artists=["Artist C"], title="Album 3", year=2022),
                status=PushStatus.added,
                message="Added"
            ),
            AlbumResult(
                item=Album(artists=["Artist D"], title="Album 4", year=2023),
                status=PushStatus.not_found,
                message="Not found"
            ),
        ]

        # Export only not_found and similarity_too_low
        exported_count = export_album_results_to_csv(
            results, ["not_found", "similarity_too_low"], self.csv_file
        )

        self.assertEqual(exported_count, 3)

        # Verify the exported CSV
        with open(self.csv_file, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0]["artist"], "Artist A")
        self.assertEqual(rows[0]["album"], "Album 1")
        self.assertEqual(rows[0]["year"], "2020")

        self.assertEqual(rows[1]["artist"], "Artist B")
        self.assertEqual(rows[1]["album"], "Album 2")

    def test_export_track_results_to_csv(self):
        """Test exporting track results to CSV."""
        from dataclasses import dataclass

        @dataclass
        class TrackResult:
            item: Track
            status: PushStatus
            message: str = ""

        # Create mock results
        results = [
            TrackResult(
                item=Track(artists=["Artist A"], title="Track 1", album="Album A", year=2020),
                status=PushStatus.not_found,
                message="Not found"
            ),
            TrackResult(
                item=Track(artists=["Artist B"], title="Track 2", album="Album B", year=2021),
                status=PushStatus.filtered,
                message="Filtered"
            ),
            TrackResult(
                item=Track(artists=["Artist C"], title="Track 3", album="Album C", year=2022),
                status=PushStatus.added,
                message="Added"
            ),
        ]

        # Export only filtered tracks
        exported_count = export_track_results_to_csv(
            results, ["filtered"], self.csv_file
        )

        self.assertEqual(exported_count, 1)

        # Verify the exported CSV
        with open(self.csv_file, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["artist"], "Artist B")
        self.assertEqual(rows[0]["track"], "Track 2")
        self.assertEqual(rows[0]["album"], "Album B")

    def test_export_no_matching_results(self):
        """Test exporting when no results match the filter."""
        from dataclasses import dataclass

        @dataclass
        class AlbumResult:
            item: Album
            status: PushStatus
            message: str = ""

        results = [
            AlbumResult(
                item=Album(artists=["Artist A"], title="Album 1", year=2020),
                status=PushStatus.added,
                message="Added"
            ),
        ]

        # Export only not_found (which doesn't exist in results)
        exported_count = export_album_results_to_csv(
            results, ["not_found"], self.csv_file
        )

        self.assertEqual(exported_count, 0)
        # CSV file should not be created if no results
        self.assertFalse(os.path.exists(self.csv_file))

    def test_export_album_results_to_mappings_csv(self):
        """Test exporting album results to mappings CSV format."""
        from dataclasses import dataclass

        @dataclass
        class AlbumResult:
            item: Album
            status: PushStatus
            message: str = ""

        # Create mock results
        results = [
            AlbumResult(
                item=Album(artists=["Artist A"], title="Album 1", year=2020),
                status=PushStatus.not_found,
                message="Not found"
            ),
            AlbumResult(
                item=Album(artists=["Artist B"], title="Album 2", year=2021),
                status=PushStatus.similarity_too_low,
                message="Similarity too low"
            ),
            AlbumResult(
                item=Album(artists=["Artist C"], title="Album 3", year=2022),
                status=PushStatus.added,
                message="Added"
            ),
            AlbumResult(
                item=Album(artists=["Artist D"], title="Album 4", year=2023),
                status=PushStatus.not_found,
                message="Not found"
            ),
        ]

        # Export not_found and similarity_too_low items to mappings format
        new_count, unmapped_count = export_album_results_to_mappings_csv(
            results, ["not_found", "similarity_too_low"], self.csv_file
        )

        self.assertEqual(new_count, 3)
        self.assertEqual(unmapped_count, 0)

        # Verify the exported mappings CSV
        with open(self.csv_file, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        self.assertEqual(len(rows), 3)

        # Check header columns
        with open(self.csv_file, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
            self.assertEqual(headers, [
                "type", "artist", "title",
                "spotify_id", "ytm_id", "tidal_id",
                "spotify_artist", "spotify_title",
                "ytm_artist", "ytm_title",
                "tidal_artist", "tidal_title",
                "subsonic_artist", "subsonic_title", "subsonic_album",
                "jellyfin_artist", "jellyfin_title", "jellyfin_album"
            ])

        # Check first row (not_found)
        self.assertEqual(rows[0]["type"], "album")
        self.assertEqual(rows[0]["artist"], "Artist A")
        self.assertEqual(rows[0]["title"], "Album 1")
        self.assertEqual(rows[0]["spotify_id"], "")
        self.assertEqual(rows[0]["ytm_id"], "")
        self.assertEqual(rows[0]["spotify_artist"], "")
        self.assertEqual(rows[0]["spotify_title"], "")
        self.assertEqual(rows[0]["ytm_artist"], "")
        self.assertEqual(rows[0]["ytm_title"], "")

        # Check second row (similarity_too_low)
        self.assertEqual(rows[1]["type"], "album")
        self.assertEqual(rows[1]["artist"], "Artist B")
        self.assertEqual(rows[1]["title"], "Album 2")

    def test_export_track_results_to_mappings_csv(self):
        """Test exporting track results to mappings CSV format."""
        from dataclasses import dataclass

        @dataclass
        class TrackResult:
            item: Track
            status: PushStatus
            message: str = ""

        # Create mock results
        results = [
            TrackResult(
                item=Track(artists=["Artist A"], title="Track 1", album="Album A", year=2020),
                status=PushStatus.not_found,
                message="Not found"
            ),
            TrackResult(
                item=Track(artists=["Artist B"], title="Track 2", album="Album B", year=2021),
                status=PushStatus.similarity_too_low,
                message="Low similarity"
            ),
            TrackResult(
                item=Track(artists=["Artist C"], title="Track 3", album="Album C", year=2022),
                status=PushStatus.added,
                message="Added"
            ),
        ]

        # Export not_found and similarity_too_low items to mappings format
        new_count, unmapped_count = export_track_results_to_mappings_csv(
            results, ["not_found", "similarity_too_low"], self.csv_file
        )

        self.assertEqual(new_count, 2)
        self.assertEqual(unmapped_count, 0)

        # Verify the exported mappings CSV
        with open(self.csv_file, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        self.assertEqual(len(rows), 2)

        # Check header columns
        with open(self.csv_file, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
            self.assertEqual(headers, [
                "type", "artist", "title",
                "spotify_id", "ytm_id", "tidal_id",
                "spotify_artist", "spotify_title",
                "ytm_artist", "ytm_title",
                "tidal_artist", "tidal_title",
                "subsonic_artist", "subsonic_title", "subsonic_album",
                "jellyfin_artist", "jellyfin_title", "jellyfin_album"
            ])

        # Check first row (not_found)
        self.assertEqual(rows[0]["type"], "track")
        self.assertEqual(rows[0]["artist"], "Artist A")
        self.assertEqual(rows[0]["title"], "Track 1")
        # All target fields should be empty
        self.assertEqual(rows[0]["spotify_id"], "")
        self.assertEqual(rows[0]["ytm_id"], "")

        # Check second row (similarity_too_low)
        self.assertEqual(rows[1]["type"], "track")
        self.assertEqual(rows[1]["artist"], "Artist B")
        self.assertEqual(rows[1]["title"], "Track 2")

    def test_incremental_export_album_mappings(self):
        """Test that mappings export is incremental and preserves existing data."""
        from dataclasses import dataclass

        @dataclass
        class AlbumResult:
            item: Album
            status: PushStatus
            message: str = ""

        # First export - 2 albums
        first_results = [
            AlbumResult(
                item=Album(artists=["Artist A"], title="Album 1", year=2020),
                status=PushStatus.not_found,
                message="Not found"
            ),
            AlbumResult(
                item=Album(artists=["Artist B"], title="Album 2", year=2021),
                status=PushStatus.not_found,
                message="Not found"
            ),
        ]

        # Export first batch
        new_count1, unmapped_count1 = export_album_results_to_mappings_csv(
            first_results, ["not_found"], self.csv_file
        )
        self.assertEqual(new_count1, 2)
        self.assertEqual(unmapped_count1, 0)

        # Manually edit the CSV to add spotify_id for Album 1
        with open(self.csv_file, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)

        # Modify the first data row (index 1, after header) to add spotify_id
        rows[1][3] = "spotify123"  # spotify_id column (index 3)
        rows[1][6] = "Modified Artist A"  # spotify_artist column (index 6, after adding tidal_id at 5)

        with open(self.csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerows(rows)

        # Second export - includes 1 duplicate and 2 new albums
        second_results = [
            AlbumResult(
                item=Album(artists=["Artist A"], title="Album 1", year=2020),
                status=PushStatus.not_found,
                message="Not found"  # Duplicate - should be skipped
            ),
            AlbumResult(
                item=Album(artists=["Artist C"], title="Album 3", year=2022),
                status=PushStatus.not_found,
                message="Not found"  # New
            ),
            AlbumResult(
                item=Album(artists=["Artist D"], title="Album 4", year=2023),
                status=PushStatus.not_found,
                message="Not found"  # New
            ),
        ]

        # Export second batch to SAME file
        new_count2, unmapped_count2 = export_album_results_to_mappings_csv(
            second_results, ["not_found"], self.csv_file
        )

        # Should only add 2 new albums (not the duplicate)
        self.assertEqual(new_count2, 2)
        self.assertEqual(unmapped_count2, 0)  # Album 1 has mapping, so skipped completely

        # Verify the final CSV
        with open(self.csv_file, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        # Should have 4 total rows (2 original + 2 new)
        self.assertEqual(len(rows), 4)

        # Verify first row still has manual edits preserved
        self.assertEqual(rows[0]["artist"], "Artist A")
        self.assertEqual(rows[0]["title"], "Album 1")
        self.assertEqual(rows[0]["spotify_id"], "spotify123")  # Preserved!
        self.assertEqual(rows[0]["spotify_artist"], "Modified Artist A")  # Preserved!

        # Verify second row is unchanged
        self.assertEqual(rows[1]["artist"], "Artist B")
        self.assertEqual(rows[1]["title"], "Album 2")

        # Verify third row is new Album 3
        self.assertEqual(rows[2]["artist"], "Artist C")
        self.assertEqual(rows[2]["title"], "Album 3")
        self.assertEqual(rows[2]["spotify_id"], "")  # Empty for new row

        # Verify fourth row is new Album 4
        self.assertEqual(rows[3]["artist"], "Artist D")
        self.assertEqual(rows[3]["title"], "Album 4")

    def test_incremental_export_track_mappings(self):
        """Test that track mappings export is incremental and preserves existing data."""
        from dataclasses import dataclass

        @dataclass
        class TrackResult:
            item: Track
            status: PushStatus
            message: str = ""

        # First export - 1 track
        first_results = [
            TrackResult(
                item=Track(artists=["Artist A"], title="Track 1", album="Album A"),
                status=PushStatus.not_found,
                message="Not found"
            ),
        ]

        new_count1, unmapped_count1 = export_track_results_to_mappings_csv(
            first_results, ["not_found"], self.csv_file
        )
        self.assertEqual(new_count1, 1)
        self.assertEqual(unmapped_count1, 0)

        # Manually edit to add ytm_id
        with open(self.csv_file, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)

        rows[1][4] = "ytm456"  # ytm_id column

        with open(self.csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerows(rows)

        # Second export - 1 duplicate (case-insensitive) + 1 new
        second_results = [
            TrackResult(
                item=Track(artists=["artist a"], title="track 1", album="Album A"),
                status=PushStatus.not_found,
                message="Not found"  # Duplicate (case-insensitive) - should be skipped
            ),
            TrackResult(
                item=Track(artists=["Artist B"], title="Track 2", album="Album B"),
                status=PushStatus.not_found,
                message="Not found"  # New
            ),
        ]

        new_count2, unmapped_count2 = export_track_results_to_mappings_csv(
            second_results, ["not_found"], self.csv_file
        )

        # Should only add 1 new track
        self.assertEqual(new_count2, 1)
        self.assertEqual(unmapped_count2, 0)  # Track 1 has ytm_id, so skipped completely

        # Verify final CSV
        with open(self.csv_file, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        # Should have 2 total rows
        self.assertEqual(len(rows), 2)

        # Verify first row preserved manual edit
        self.assertEqual(rows[0]["ytm_id"], "ytm456")

        # Verify second row is new
        self.assertEqual(rows[1]["artist"], "Artist B")
        self.assertEqual(rows[1]["title"], "Track 2")

    def test_export_unmapped_items_already_in_file(self):
        """Test that items already in file with empty target fields are reported as unmapped."""
        from dataclasses import dataclass

        @dataclass
        class AlbumResult:
            item: Album
            status: PushStatus
            message: str = ""

        # First export - 3 albums that failed
        first_results = [
            AlbumResult(
                item=Album(artists=["Artist A"], title="Album 1", year=2020),
                status=PushStatus.not_found,
                message="Not found"
            ),
            AlbumResult(
                item=Album(artists=["Artist B"], title="Album 2", year=2021),
                status=PushStatus.not_found,
                message="Not found"
            ),
            AlbumResult(
                item=Album(artists=["Artist C"], title="Album 3", year=2022),
                status=PushStatus.similarity_too_low,
                message="Similarity too low"
            ),
        ]

        # Export first batch
        new_count1, unmapped_count1 = export_album_results_to_mappings_csv(
            first_results, ["not_found", "similarity_too_low"], self.csv_file
        )
        self.assertEqual(new_count1, 3)
        self.assertEqual(unmapped_count1, 0)

        # User manually fills in mappings for Album 1 only (fills spotify_id)
        with open(self.csv_file, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)

        rows[1][3] = "spotify123"  # Album 1 gets spotify_id - successfully mapped

        with open(self.csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerows(rows)

        # User runs push again with --mappings-file and --export-csv mappings-file
        # Albums 2 and 3 still fail (empty target fields), Album 1 is skipped
        # Plus one new failure (Album 4)
        second_results = [
            AlbumResult(
                item=Album(artists=["Artist B"], title="Album 2", year=2021),
                status=PushStatus.not_found,
                message="Not found"  # Still failing, already in file with empty fields
            ),
            AlbumResult(
                item=Album(artists=["Artist C"], title="Album 3", year=2022),
                status=PushStatus.similarity_too_low,
                message="Similarity too low"  # Still failing, already in file with empty fields
            ),
            AlbumResult(
                item=Album(artists=["Artist D"], title="Album 4", year=2023),
                status=PushStatus.not_found,
                message="Not found"  # New failure
            ),
        ]

        # Export second batch
        new_count2, unmapped_count2 = export_album_results_to_mappings_csv(
            second_results, ["not_found", "similarity_too_low"], self.csv_file
        )

        # Should add 1 new album (Album 4)
        self.assertEqual(new_count2, 1)
        # Should report 2 unmapped items (Albums 2 and 3 still failing with empty fields)
        self.assertEqual(unmapped_count2, 2)

        # Verify the final CSV still has 4 rows total
        with open(self.csv_file, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        self.assertEqual(len(rows), 4)

        # Verify Album 1 still has its mapping
        self.assertEqual(rows[0]["spotify_id"], "spotify123")


class TestCSVServiceIDSupport(unittest.TestCase):
    """Test CSV import/export with service IDs (spotify_id, ytm_id)."""

    def setUp(self):
        """Create temporary CSV file for testing."""
        self.csv_file = "test_service_ids.csv"

    def tearDown(self):
        """Clean up temporary files."""
        if os.path.exists(self.csv_file):
            os.remove(self.csv_file)

    def test_export_albums_with_spotify_id(self):
        """Test exporting albums with Spotify service ID."""
        from pushtunes.utils.csv_utils import export_albums_to_csv, import_albums_from_csv

        albums = [
            Album(
                artists=["The Beatles"],
                title="Abbey Road",
                year=1969,
                service_id="3o2dn2O0FCVsKnXJy48T3d",
                service_name="spotify"
            ),
            Album(
                artists=["Pink Floyd"],
                title="Dark Side",
                year=1973,
                service_id="4LH4d3cOWNNsVw41Gqt2kv",
                service_name="spotify"
            ),
        ]

        export_albums_to_csv(albums, self.csv_file)

        # Verify exported CSV has IDs in spotify_id column
        with open(self.csv_file, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["spotify_id"], "3o2dn2O0FCVsKnXJy48T3d")
        self.assertEqual(rows[0]["ytm_id"], "")
        self.assertEqual(rows[1]["spotify_id"], "4LH4d3cOWNNsVw41Gqt2kv")
        self.assertEqual(rows[1]["ytm_id"], "")

    def test_export_albums_with_ytm_id(self):
        """Test exporting albums with YTM service ID."""
        from pushtunes.utils.csv_utils import export_albums_to_csv

        albums = [
            Album(
                artists=["Queen"],
                title="Greatest Hits",
                year=1981,
                service_id="MPREb_C8AonwnkvCk",
                service_name="ytm"
            ),
        ]

        export_albums_to_csv(albums, self.csv_file)

        # Verify exported CSV has ID in ytm_id column
        with open(self.csv_file, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["spotify_id"], "")
        self.assertEqual(rows[0]["ytm_id"], "MPREb_C8AonwnkvCk")

    def test_import_albums_with_service_ids(self):
        """Test importing albums with service IDs from CSV."""
        from pushtunes.utils.csv_utils import import_albums_from_csv

        # Create CSV with both spotify_id and ytm_id
        with open(self.csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["artist", "album", "year", "spotify_id", "ytm_id"])
            writer.writerow(["The Beatles", "Abbey Road", "1969", "spotify123", ""])
            writer.writerow(["Pink Floyd", "Dark Side", "1973", "", "ytm456"])
            writer.writerow(["Led Zeppelin", "IV", "1971", "spot789", "ytm999"])
            writer.writerow(["Queen", "Greatest", "1981", "", ""])

        albums = import_albums_from_csv(self.csv_file)

        self.assertEqual(len(albums), 4)

        # Album 1: Has spotify_id only
        self.assertEqual(albums[0].title, "Abbey Road")
        self.assertIsNotNone(albums[0].extra_data)
        self.assertEqual(albums[0].extra_data.get("spotify_id"), "spotify123")
        self.assertIsNone(albums[0].extra_data.get("ytm_id"))

        # Album 2: Has ytm_id only
        self.assertEqual(albums[1].title, "Dark Side")
        self.assertIsNotNone(albums[1].extra_data)
        self.assertIsNone(albums[1].extra_data.get("spotify_id"))
        self.assertEqual(albums[1].extra_data.get("ytm_id"), "ytm456")

        # Album 3: Has both IDs
        self.assertEqual(albums[2].title, "IV")
        self.assertIsNotNone(albums[2].extra_data)
        self.assertEqual(albums[2].extra_data.get("spotify_id"), "spot789")
        self.assertEqual(albums[2].extra_data.get("ytm_id"), "ytm999")

        # Album 4: Has no IDs
        self.assertEqual(albums[3].title, "Greatest")
        self.assertIsNone(albums[3].extra_data)

    def test_export_tracks_with_service_ids(self):
        """Test exporting tracks with service IDs."""
        from pushtunes.utils.csv_utils import export_tracks_to_csv

        tracks = [
            Track(
                artists=["Queen"],
                title="Bohemian Rhapsody",
                album="A Night at the Opera",
                year=1975,
                service_id="spot789",
                service_name="spotify"
            ),
            Track(
                artists=["AC/DC"],
                title="Back in Black",
                album="Back in Black",
                year=1980,
                service_id="ytm999",
                service_name="ytm"
            ),
        ]

        export_tracks_to_csv(tracks, self.csv_file)

        # Verify exported CSV
        with open(self.csv_file, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["spotify_id"], "spot789")
        self.assertEqual(rows[0]["ytm_id"], "")
        self.assertEqual(rows[1]["spotify_id"], "")
        self.assertEqual(rows[1]["ytm_id"], "ytm999")

    def test_import_tracks_with_service_ids(self):
        """Test importing tracks with service IDs from CSV."""
        from pushtunes.utils.csv_utils import import_tracks_from_csv

        # Create CSV with service IDs
        with open(self.csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["artist", "track", "album", "year", "spotify_id", "ytm_id"])
            writer.writerow(["Queen", "Bohemian Rhapsody", "Opera", "1975", "spot123", ""])
            writer.writerow(["AC/DC", "Back in Black", "BiB", "1980", "", "ytm456"])
            writer.writerow(["Beatles", "Hey Jude", "", "", "", ""])

        tracks = import_tracks_from_csv(self.csv_file)

        self.assertEqual(len(tracks), 3)

        # Track 1: Has spotify_id
        self.assertEqual(tracks[0].title, "Bohemian Rhapsody")
        self.assertIsNotNone(tracks[0].extra_data)
        self.assertEqual(tracks[0].extra_data.get("spotify_id"), "spot123")

        # Track 2: Has ytm_id
        self.assertEqual(tracks[1].title, "Back in Black")
        self.assertIsNotNone(tracks[1].extra_data)
        self.assertEqual(tracks[1].extra_data.get("ytm_id"), "ytm456")

        # Track 3: No IDs
        self.assertEqual(tracks[2].title, "Hey Jude")
        self.assertIsNone(tracks[2].extra_data)

    def test_roundtrip_albums_with_service_ids(self):
        """Test that albums with service IDs can be exported and imported correctly."""
        from pushtunes.utils.csv_utils import export_albums_to_csv, import_albums_from_csv

        original_albums = [
            Album(
                artists=["The Beatles"],
                title="Abbey Road",
                year=1969,
                service_id="spotify123",
                service_name="spotify"
            ),
            Album(
                artists=["Pink Floyd"],
                title="Dark Side",
                year=1973,
                service_id="ytm456",
                service_name="ytm"
            ),
        ]

        # Export
        export_albums_to_csv(original_albums, self.csv_file)

        # Import
        imported_albums = import_albums_from_csv(self.csv_file)

        self.assertEqual(len(imported_albums), 2)

        # Verify first album
        self.assertEqual(imported_albums[0].title, "Abbey Road")
        self.assertEqual(imported_albums[0].extra_data.get("spotify_id"), "spotify123")

        # Verify second album
        self.assertEqual(imported_albums[1].title, "Dark Side")
        self.assertEqual(imported_albums[1].extra_data.get("ytm_id"), "ytm456")

    def test_roundtrip_tracks_with_service_ids(self):
        """Test that tracks with service IDs can be exported and imported correctly."""
        from pushtunes.utils.csv_utils import export_tracks_to_csv, import_tracks_from_csv

        original_tracks = [
            Track(
                artists=["Queen"],
                title="Bohemian Rhapsody",
                album="Opera",
                year=1975,
                service_id="spot789",
                service_name="spotify"
            ),
        ]

        # Export
        export_tracks_to_csv(original_tracks, self.csv_file)

        # Import
        imported_tracks = import_tracks_from_csv(self.csv_file)

        self.assertEqual(len(imported_tracks), 1)
        self.assertEqual(imported_tracks[0].title, "Bohemian Rhapsody")
        self.assertEqual(imported_tracks[0].extra_data.get("spotify_id"), "spot789")
