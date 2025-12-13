"""Tests for the mappings manager."""

import unittest
import tempfile
import os
from pathlib import Path

from pushtunes.services.mappings_manager import MappingsManager, AlbumMapping, TrackMapping
from pushtunes.models.album import Album
from pushtunes.models.track import Track


class TestAlbumMapping(unittest.TestCase):
    """Test AlbumMapping dataclass."""

    def test_album_mapping_creation(self):
        """Test creating an album mapping."""
        mapping = AlbumMapping(
            source_artist="Artist A",
            source_title="Album A",
            spotify_id="123abc",
            spotify_artist="Artist A Remix",
            spotify_title="Album A Remastered"
        )
        self.assertEqual(mapping.source_artist, "Artist A")
        self.assertEqual(mapping.source_title, "Album A")
        self.assertEqual(mapping.spotify_id, "123abc")
        self.assertEqual(mapping.spotify_artist, "Artist A Remix")
        self.assertEqual(mapping.spotify_title, "Album A Remastered")

    def test_album_mapping_frozen(self):
        """Test that AlbumMapping is immutable."""
        mapping = AlbumMapping(
            source_artist="Artist A",
            source_title="Album A"
        )
        with self.assertRaises(AttributeError):
            mapping.source_artist = "Artist B"


class TestTrackMapping(unittest.TestCase):
    """Test TrackMapping dataclass."""

    def test_track_mapping_creation(self):
        """Test creating a track mapping."""
        mapping = TrackMapping(
            source_artist="Artist X",
            source_title="Track X",
            ytm_id="xyz789",
            ytm_artist="Artist X Live",
            ytm_title="Track X (Live Version)"
        )
        self.assertEqual(mapping.source_artist, "Artist X")
        self.assertEqual(mapping.source_title, "Track X")
        self.assertEqual(mapping.ytm_id, "xyz789")
        self.assertEqual(mapping.ytm_artist, "Artist X Live")
        self.assertEqual(mapping.ytm_title, "Track X (Live Version)")

    def test_track_mapping_frozen(self):
        """Test that TrackMapping is immutable."""
        mapping = TrackMapping(
            source_artist="Artist X",
            source_title="Track X"
        )
        with self.assertRaises(AttributeError):
            mapping.source_title = "Track Y"


class TestMappingsManagerInit(unittest.TestCase):
    """Test MappingsManager initialization."""

    def test_init_without_file(self):
        """Test creating manager without a file."""
        manager = MappingsManager()
        self.assertEqual(len(manager.album_mappings), 0)
        self.assertEqual(len(manager.track_mappings), 0)

    def test_init_with_nonexistent_file(self):
        """Test creating manager with nonexistent file (should log warning but not crash)."""
        manager = MappingsManager("/nonexistent/path/to/file.csv")
        self.assertEqual(len(manager.album_mappings), 0)
        self.assertEqual(len(manager.track_mappings), 0)

    def test_init_with_tilde_expansion(self):
        """Test that tilde (~) is expanded to home directory."""
        # Create a temp file in the home directory
        home_dir = os.path.expanduser("~")
        temp_file = tempfile.NamedTemporaryFile(
            mode='w', delete=False, suffix='.csv', dir=home_dir
        )
        temp_filename = os.path.basename(temp_file.name)

        # Write a simple mapping CSV
        temp_file.write("type,artist,title,spotify_id,ytm_id,spotify_artist,spotify_title,ytm_artist,ytm_title\n")
        temp_file.write("album,Test Artist,Test Album,test123,,,,,\n")
        temp_file.close()

        try:
            # Test with tilde path
            tilde_path = f"~/{temp_filename}"
            manager = MappingsManager(tilde_path)

            # Should successfully load the mapping
            self.assertEqual(len(manager.album_mappings), 1)

            # Verify the mapping was loaded correctly
            album = Album(artists=["Test Artist"], title="Test Album")
            target_album = manager.get_album_mapping(album, "spotify")
            self.assertIsNotNone(target_album)
            self.assertEqual(target_album.service_id, "test123")
        finally:
            # Clean up
            os.unlink(temp_file.name)


class TestMappingsManagerCSVLoading(unittest.TestCase):
    """Test loading mappings from CSV."""

    def setUp(self):
        """Create a temporary CSV file for testing."""
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
        self.temp_file_path = self.temp_file.name

    def tearDown(self):
        """Clean up temporary file."""
        self.temp_file.close()
        if os.path.exists(self.temp_file_path):
            os.unlink(self.temp_file_path)

    def test_load_album_mapping_with_metadata(self):
        """Test loading album mapping with metadata."""
        csv_content = """type,artist,title,spotify_id,ytm_id,spotify_artist,spotify_title,ytm_artist,ytm_title
album,Volkor X,This Means War,,,Volkor X,This Really Means War (2025),,"""

        with open(self.temp_file_path, 'w') as f:
            f.write(csv_content)

        manager = MappingsManager(self.temp_file_path)
        self.assertEqual(len(manager.album_mappings), 1)

        key = ("volkor x", "this means war")
        self.assertIn(key, manager.album_mappings)

        mapping = manager.album_mappings[key]
        self.assertEqual(mapping.source_artist, "Volkor X")
        self.assertEqual(mapping.source_title, "This Means War")
        self.assertEqual(mapping.spotify_artist, "Volkor X")
        self.assertEqual(mapping.spotify_title, "This Really Means War (2025)")
        self.assertIsNone(mapping.spotify_id)

    def test_load_album_mapping_with_id(self):
        """Test loading album mapping with service ID."""
        csv_content = """type,artist,title,spotify_id,ytm_id,spotify_artist,spotify_title,ytm_artist,ytm_title
album,Lazerhawk,Redline,2fK9z3234fK9z3234fK9z3234,,,,,"""

        with open(self.temp_file_path, 'w') as f:
            f.write(csv_content)

        manager = MappingsManager(self.temp_file_path)
        self.assertEqual(len(manager.album_mappings), 1)

        key = ("lazerhawk", "redline")
        mapping = manager.album_mappings[key]
        self.assertEqual(mapping.spotify_id, "2fK9z3234fK9z3234fK9z3234")

    def test_load_track_mapping_with_metadata(self):
        """Test loading track mapping with metadata."""
        csv_content = """type,artist,title,spotify_id,ytm_id,spotify_artist,spotify_title,ytm_artist,ytm_title
track,Kavinsky,Nightcall,,,Kavinsky,Nightcall (Drive Original Movie Soundtrack),,"""

        with open(self.temp_file_path, 'w') as f:
            f.write(csv_content)

        manager = MappingsManager(self.temp_file_path)
        self.assertEqual(len(manager.track_mappings), 1)

        key = ("kavinsky", "nightcall")
        self.assertIn(key, manager.track_mappings)

        mapping = manager.track_mappings[key]
        self.assertEqual(mapping.source_artist, "Kavinsky")
        self.assertEqual(mapping.source_title, "Nightcall")
        self.assertEqual(mapping.spotify_title, "Nightcall (Drive Original Movie Soundtrack)")

    def test_load_track_mapping_with_id(self):
        """Test loading track mapping with service ID."""
        csv_content = """type,artist,title,spotify_id,ytm_id,spotify_artist,spotify_title,ytm_artist,ytm_title
track,Perturbator,Humans Are Such Easy Prey,,VK4Kx2pVK4Kx2pVK4Kx2p,,,,"""

        with open(self.temp_file_path, 'w') as f:
            f.write(csv_content)

        manager = MappingsManager(self.temp_file_path)
        self.assertEqual(len(manager.track_mappings), 1)

        mapping = manager.track_mappings[("perturbator", "humans are such easy prey")]
        self.assertEqual(mapping.ytm_id, "VK4Kx2pVK4Kx2pVK4Kx2p")

    def test_load_mixed_mappings(self):
        """Test loading both album and track mappings."""
        csv_content = """type,artist,title,spotify_id,ytm_id,spotify_artist,spotify_title,ytm_artist,ytm_title
album,Artist A,Album A,,,Artist A,Album A Remastered,,
track,Artist B,Track B,,,Artist B,Track B (Live),,"""

        with open(self.temp_file_path, 'w') as f:
            f.write(csv_content)

        manager = MappingsManager(self.temp_file_path)
        self.assertEqual(len(manager.album_mappings), 1)
        self.assertEqual(len(manager.track_mappings), 1)

    def test_load_without_type_column_defaults_to_album(self):
        """Test that rows without type column default to album."""
        csv_content = """artist,title,spotify_id,ytm_id,spotify_artist,spotify_title,ytm_artist,ytm_title
Artist C,Album C,,,Artist C,Album C (Deluxe),,"""

        with open(self.temp_file_path, 'w') as f:
            f.write(csv_content)

        manager = MappingsManager(self.temp_file_path)
        self.assertEqual(len(manager.album_mappings), 1)
        self.assertEqual(len(manager.track_mappings), 0)

    def test_skip_row_with_missing_artist_or_title(self):
        """Test that rows with missing artist or title are skipped."""
        csv_content = """type,artist,title,spotify_id,ytm_id,spotify_artist,spotify_title,ytm_artist,ytm_title
album,,Album A,,,Artist A,Album A Remastered,,
album,Artist B,,,,Artist B,Album B,,"""

        with open(self.temp_file_path, 'w') as f:
            f.write(csv_content)

        manager = MappingsManager(self.temp_file_path)
        self.assertEqual(len(manager.album_mappings), 0)

    def test_skip_row_with_no_target(self):
        """Test that rows with no target are skipped."""
        csv_content = """type,artist,title,spotify_id,ytm_id,spotify_artist,spotify_title,ytm_artist,ytm_title
album,Artist A,Album A,,,,,"""

        with open(self.temp_file_path, 'w') as f:
            f.write(csv_content)

        manager = MappingsManager(self.temp_file_path)
        self.assertEqual(len(manager.album_mappings), 0)

    def test_case_insensitive_keys(self):
        """Test that mapping keys are case insensitive (stored as lowercase)."""
        csv_content = """type,artist,title,spotify_id,ytm_id,spotify_artist,spotify_title,ytm_artist,ytm_title
album,Volkor X,This Means War,,,Volkor X,This Really Means War,,"""

        with open(self.temp_file_path, 'w') as f:
            f.write(csv_content)

        manager = MappingsManager(self.temp_file_path)

        # Keys are stored as lowercase tuples
        self.assertIn(("volkor x", "this means war"), manager.album_mappings)
        # Different cases should normalize to the same key
        self.assertIn(("VOLKOR X".lower(), "THIS MEANS WAR".lower()), manager.album_mappings)
        self.assertIn(("VoLkOr X".lower(), "ThIs MeAnS wAr".lower()), manager.album_mappings)


class TestGetAlbumMapping(unittest.TestCase):
    """Test get_album_mapping method."""

    def setUp(self):
        """Create a temporary CSV file with test data."""
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
        csv_content = """type,artist,title,spotify_id,ytm_id,spotify_artist,spotify_title,ytm_artist,ytm_title
album,Volkor X,This Means War,,,Volkor X,This Really Means War (2025),,
album,Lazerhawk,Redline,spotify123,,,,,
album,Mitch Murder,Current Events,,,Mitch Murder,Current Events (Remastered),Mitch Murder,Current Events (Deluxe)"""

        with open(self.temp_file.name, 'w') as f:
            f.write(csv_content)

        self.manager = MappingsManager(self.temp_file.name)
        self.temp_file_path = self.temp_file.name

    def tearDown(self):
        """Clean up temporary file."""
        self.temp_file.close()
        if os.path.exists(self.temp_file_path):
            os.unlink(self.temp_file_path)

    def test_get_album_mapping_spotify_metadata(self):
        """Test getting album mapping with Spotify metadata."""
        source = Album(title="This Means War", artists=["Volkor X"])
        mapped = self.manager.get_album_mapping(source, "spotify")

        self.assertIsNotNone(mapped)
        self.assertEqual(mapped.title, "This Really Means War (2025)")
        self.assertEqual(mapped.artists, ["Volkor X"])
        self.assertEqual(mapped.service_name, "spotify")
        self.assertIsNone(mapped.service_id)

    def test_get_album_mapping_spotify_id(self):
        """Test getting album mapping with Spotify ID."""
        source = Album(title="Redline", artists=["Lazerhawk"])
        mapped = self.manager.get_album_mapping(source, "spotify")

        self.assertIsNotNone(mapped)
        self.assertEqual(mapped.service_id, "spotify123")
        self.assertEqual(mapped.service_name, "spotify")

    def test_get_album_mapping_ytm_metadata(self):
        """Test getting album mapping with YTM metadata."""
        source = Album(title="Current Events", artists=["Mitch Murder"])
        mapped = self.manager.get_album_mapping(source, "ytm")

        self.assertIsNotNone(mapped)
        self.assertEqual(mapped.title, "Current Events (Deluxe)")
        self.assertEqual(mapped.artists, ["Mitch Murder"])
        self.assertEqual(mapped.service_name, "ytm")

    def test_get_album_mapping_not_found(self):
        """Test getting album mapping for non-existent album."""
        source = Album(title="Non-existent Album", artists=["Unknown Artist"])
        mapped = self.manager.get_album_mapping(source, "spotify")

        self.assertIsNone(mapped)

    def test_get_album_mapping_case_insensitive(self):
        """Test that album mapping lookup is case insensitive."""
        source = Album(title="this means war", artists=["volkor x"])
        mapped = self.manager.get_album_mapping(source, "spotify")

        self.assertIsNotNone(mapped)
        self.assertEqual(mapped.title, "This Really Means War (2025)")

    def test_get_album_mapping_no_mapping_for_service(self):
        """Test getting album mapping when no mapping exists for the target service."""
        source = Album(title="This Means War", artists=["Volkor X"])
        mapped = self.manager.get_album_mapping(source, "ytm")

        # This album has no YTM mapping, only Spotify
        self.assertIsNone(mapped)


class TestGetTrackMapping(unittest.TestCase):
    """Test get_track_mapping method."""

    def setUp(self):
        """Create a temporary CSV file with test data."""
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
        csv_content = """type,artist,title,spotify_id,ytm_id,spotify_artist,spotify_title,ytm_artist,ytm_title
track,Kavinsky,Nightcall,,,Kavinsky,Nightcall (Drive Original Movie Soundtrack),,
track,Perturbator,Humans Are Such Easy Prey,,ytm456,,,,
track,Lazerhawk,Electric Groove,spotify789,,Lazerhawk,Electric Groove (Remastered),Lazerhawk,Electric Groove (Live)"""

        with open(self.temp_file.name, 'w') as f:
            f.write(csv_content)

        self.manager = MappingsManager(self.temp_file.name)
        self.temp_file_path = self.temp_file.name

    def tearDown(self):
        """Clean up temporary file."""
        self.temp_file.close()
        if os.path.exists(self.temp_file_path):
            os.unlink(self.temp_file_path)

    def test_get_track_mapping_spotify_metadata(self):
        """Test getting track mapping with Spotify metadata."""
        source = Track(title="Nightcall", artists=["Kavinsky"])
        mapped = self.manager.get_track_mapping(source, "spotify")

        self.assertIsNotNone(mapped)
        self.assertEqual(mapped.title, "Nightcall (Drive Original Movie Soundtrack)")
        self.assertEqual(mapped.artists, ["Kavinsky"])
        self.assertEqual(mapped.service_name, "spotify")
        self.assertIsNone(mapped.service_id)

    def test_get_track_mapping_ytm_id(self):
        """Test getting track mapping with YTM ID."""
        source = Track(title="Humans Are Such Easy Prey", artists=["Perturbator"])
        mapped = self.manager.get_track_mapping(source, "ytm")

        self.assertIsNotNone(mapped)
        self.assertEqual(mapped.service_id, "ytm456")
        self.assertEqual(mapped.service_name, "ytm")

    def test_get_track_mapping_service_specific(self):
        """Test getting track mapping for specific services."""
        source = Track(title="Electric Groove", artists=["Lazerhawk"])

        # Test Spotify mapping
        spotify_mapped = self.manager.get_track_mapping(source, "spotify")
        self.assertIsNotNone(spotify_mapped)
        self.assertEqual(spotify_mapped.service_id, "spotify789")

        # Test YTM mapping
        ytm_mapped = self.manager.get_track_mapping(source, "ytm")
        self.assertIsNotNone(ytm_mapped)
        self.assertEqual(ytm_mapped.title, "Electric Groove (Live)")

    def test_get_track_mapping_not_found(self):
        """Test getting track mapping for non-existent track."""
        source = Track(title="Non-existent Track", artists=["Unknown Artist"])
        mapped = self.manager.get_track_mapping(source, "spotify")

        self.assertIsNone(mapped)

    def test_get_track_mapping_case_insensitive(self):
        """Test that track mapping lookup is case insensitive."""
        source = Track(title="NIGHTCALL", artists=["KAVINSKY"])
        mapped = self.manager.get_track_mapping(source, "spotify")

        self.assertIsNotNone(mapped)
        self.assertEqual(mapped.title, "Nightcall (Drive Original Movie Soundtrack)")


class TestMappingsManagerIntegration(unittest.TestCase):
    """Integration tests for MappingsManager."""

    def test_full_workflow(self):
        """Test a complete workflow with both albums and tracks."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
        csv_content = """type,artist,title,spotify_id,ytm_id,spotify_artist,spotify_title,ytm_artist,ytm_title
album,Artist 1,Album 1,,,Artist 1,Album 1 (Remastered),,
track,Artist 2,Track 2,track123,,,,,
album,Artist 3,Album 3,,,Artist 3,Album 3 (Deluxe),Artist 3,Album 3 (Extended)
track,Artist 4,Track 4,,,Artist 4,Track 4 (Radio Edit),Artist 4,Track 4 (Extended Mix)"""

        try:
            with open(temp_file.name, 'w') as f:
                f.write(csv_content)

            manager = MappingsManager(temp_file.name)

            # Verify counts
            self.assertEqual(len(manager.album_mappings), 2)
            self.assertEqual(len(manager.track_mappings), 2)

            # Test album mapping
            album1 = Album(title="Album 1", artists=["Artist 1"])
            mapped_album1 = manager.get_album_mapping(album1, "spotify")
            self.assertIsNotNone(mapped_album1)
            self.assertEqual(mapped_album1.title, "Album 1 (Remastered)")

            # Test track mapping with ID
            track2 = Track(title="Track 2", artists=["Artist 2"])
            mapped_track2 = manager.get_track_mapping(track2, "spotify")
            self.assertIsNotNone(mapped_track2)
            self.assertEqual(mapped_track2.service_id, "track123")

            # Test service-specific mapping
            album3 = Album(title="Album 3", artists=["Artist 3"])
            spotify_album3 = manager.get_album_mapping(album3, "spotify")
            ytm_album3 = manager.get_album_mapping(album3, "ytm")
            self.assertEqual(spotify_album3.title, "Album 3 (Deluxe)")
            self.assertEqual(ytm_album3.title, "Album 3 (Extended)")

        finally:
            temp_file.close()
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)


class TestSloppyCSVNormalization(unittest.TestCase):
    """Test that mapping lookups handle sloppy CSV formatting."""

    def test_case_insensitive_artist(self):
        """Test that artist matching is case-insensitive."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
        try:
            # CSV has lowercase artist
            temp_file.write("type,artist,title,spotify_id,ytm_id,spotify_artist,spotify_title,ytm_artist,ytm_title\n")
            temp_file.write("album,the beatles,Abbey Road,spotify123,,,,,\n")
            temp_file.flush()
            temp_file.close()

            manager = MappingsManager(temp_file.name)

            # Source has title case
            album = Album(artists=["The Beatles"], title="Abbey Road", year=1969)
            result = manager.get_album_mapping(album, "spotify")

            self.assertIsNotNone(result)
            self.assertEqual(result.service_id, "spotify123")

        finally:
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)

    def test_case_insensitive_title(self):
        """Test that title matching is case-insensitive."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
        try:
            # CSV has UPPERCASE title
            temp_file.write("type,artist,title,spotify_id,ytm_id,spotify_artist,spotify_title,ytm_artist,ytm_title\n")
            temp_file.write("album,Pink Floyd,DARK SIDE OF THE MOON,spotify456,,,,,\n")
            temp_file.flush()
            temp_file.close()

            manager = MappingsManager(temp_file.name)

            # Source has title case
            album = Album(artists=["Pink Floyd"], title="Dark Side of the Moon", year=1973)
            result = manager.get_album_mapping(album, "spotify")

            self.assertIsNotNone(result)
            self.assertEqual(result.service_id, "spotify456")

        finally:
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)

    def test_whitespace_normalization(self):
        """Test that extra whitespace is normalized."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
        try:
            # CSV has extra spaces
            temp_file.write("type,artist,title,spotify_id,ytm_id,spotify_artist,spotify_title,ytm_artist,ytm_title\n")
            temp_file.write("album,Led  Zeppelin,Led Zeppelin  IV,spotify789,,,,,\n")
            temp_file.flush()
            temp_file.close()

            manager = MappingsManager(temp_file.name)

            # Source has normal spacing
            album = Album(artists=["Led Zeppelin"], title="Led Zeppelin IV", year=1971)
            result = manager.get_album_mapping(album, "spotify")

            self.assertIsNotNone(result)
            self.assertEqual(result.service_id, "spotify789")

        finally:
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)

    def test_separator_normalization_ampersand(self):
        """Test that different separators are normalized (& vs ,)."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
        try:
            # CSV uses ampersand
            temp_file.write("type,artist,title,spotify_id,ytm_id,spotify_artist,spotify_title,ytm_artist,ytm_title\n")
            temp_file.write("album,Simon & Garfunkel,Bridge Over Troubled Water,spotifyABC,,,,,\n")
            temp_file.flush()
            temp_file.close()

            manager = MappingsManager(temp_file.name)

            # Source also uses ampersand (should match)
            album = Album(artists=["Simon", "Garfunkel"], title="Bridge Over Troubled Water", year=1970)
            result = manager.get_album_mapping(album, "spotify")

            self.assertIsNotNone(result)
            self.assertEqual(result.service_id, "spotifyABC")

        finally:
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)

    def test_separator_normalization_comma(self):
        """Test that comma separator is normalized to &."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
        try:
            # CSV uses comma (quoted to escape the comma in CSV format)
            temp_file.write("type,artist,title,spotify_id,ytm_id,spotify_artist,spotify_title,ytm_artist,ytm_title\n")
            temp_file.write('album,"Hall, Oates",Private Eyes,spotifyDEF,,,,,\n')
            temp_file.flush()
            temp_file.close()

            manager = MappingsManager(temp_file.name)

            # Source uses ampersand (Album.artist property uses &)
            album = Album(artists=["Hall", "Oates"], title="Private Eyes", year=1981)
            result = manager.get_album_mapping(album, "spotify")

            self.assertIsNotNone(result)
            self.assertEqual(result.service_id, "spotifyDEF")

        finally:
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)

    def test_separator_without_spaces(self):
        """Test that separators without spaces still match."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
        try:
            # CSV has no spaces around ampersand
            temp_file.write("type,artist,title,spotify_id,ytm_id,spotify_artist,spotify_title,ytm_artist,ytm_title\n")
            temp_file.write("album,Crosby&Nash,Another Album,spotifyGHI,,,,,\n")
            temp_file.flush()
            temp_file.close()

            manager = MappingsManager(temp_file.name)

            # Source has spaces (Album.artist property uses " & ")
            album = Album(artists=["Crosby", "Nash"], title="Another Album", year=1972)
            result = manager.get_album_mapping(album, "spotify")

            self.assertIsNotNone(result)
            self.assertEqual(result.service_id, "spotifyGHI")

        finally:
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)

    def test_combined_sloppy_formatting(self):
        """Test multiple formatting issues at once."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
        try:
            # CSV has multiple issues: lowercase, extra spaces, no spaces in separator
            temp_file.write("type,artist,title,spotify_id,ytm_id,spotify_artist,spotify_title,ytm_artist,ytm_title\n")
            temp_file.write("track,artist one&artist  two,the  TRACK  title,spotifyJKL,,,,,\n")
            temp_file.flush()
            temp_file.close()

            manager = MappingsManager(temp_file.name)

            # Source has proper formatting
            track = Track(artists=["Artist One", "Artist Two"], title="The Track Title", album=None, year=2020)
            result = manager.get_track_mapping(track, "spotify")

            self.assertIsNotNone(result)
            self.assertEqual(result.service_id, "spotifyJKL")

        finally:
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)


class TestCrossTypeMappingIDDetection(unittest.TestCase):
    """Test ID type detection for cross-type mappings."""

    def test_detect_ytm_track_id(self):
        """Test YTM track ID detection (11-char videoId)."""
        from pushtunes.services.mappings_manager import detect_id_type_ytm

        # 11-character videoId should be detected as track
        track_id = "dQw4w9WgXcQ"
        self.assertEqual(detect_id_type_ytm(track_id), "track")

    def test_detect_ytm_album_id_olak(self):
        """Test YTM album ID detection (OLAK5uy_ prefix)."""
        from pushtunes.services.mappings_manager import detect_id_type_ytm

        # Album ID with OLAK5uy_ prefix
        album_id = "OLAK5uy_lXqjXfK9z3234fK9z3234"
        self.assertEqual(detect_id_type_ytm(album_id), "album")

    def test_detect_ytm_album_id_mpreb(self):
        """Test YTM album ID detection (MPREb_ prefix)."""
        from pushtunes.services.mappings_manager import detect_id_type_ytm

        # Album ID with MPREb_ prefix
        album_id = "MPREb_1234567890abcdef"
        self.assertEqual(detect_id_type_ytm(album_id), "album")

    def test_detect_ytm_id_unknown_format(self):
        """Test YTM ID with unknown format returns None."""
        from pushtunes.services.mappings_manager import detect_id_type_ytm

        # Unknown format
        unknown_id = "UNKNOWN123456"
        self.assertIsNone(detect_id_type_ytm(unknown_id))

    def test_detect_spotify_id_no_client(self):
        """Test Spotify ID detection without client returns None."""
        from pushtunes.services.mappings_manager import detect_id_type_spotify

        # Without client, cannot detect
        spotify_id = "3GU4cxkfdc5NIfxVRcaTqT"
        self.assertIsNone(detect_id_type_spotify(spotify_id, None))


class TestCrossTypeMapping(unittest.TestCase):
    """Test cross-type mappings (album→track, track→album)."""

    def test_album_to_track_mapping_ytm(self):
        """Test album mapped to YTM track ID (11-char videoId)."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
        try:
            # Create mappings CSV with album→track mapping
            temp_file.write("type,artist,title,spotify_id,ytm_id,spotify_artist,spotify_title,ytm_artist,ytm_title\n")
            temp_file.write("album,Audiobook Author,Long Audiobook,,dQw4w9WgXcQ,,,,,\n")
            temp_file.flush()
            temp_file.close()

            manager = MappingsManager(temp_file.name)

            # Create source album
            album = Album(
                artists=["Audiobook Author"],
                title="Long Audiobook",
                year=2023
            )

            # Get mapping - should return Track, not Album
            result = manager.get_album_mapping(album, "ytm")

            # Verify it returns a Track object
            self.assertIsInstance(result, Track)
            self.assertEqual(result.title, "Long Audiobook")
            self.assertEqual(result.artists, ["Audiobook Author"])
            self.assertEqual(result.service_id, "dQw4w9WgXcQ")
            self.assertEqual(result.service_name, "ytm")

        finally:
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)

    def test_album_to_track_mapping_with_olak_id_returns_album(self):
        """Test album mapped to YTM album ID (OLAK prefix) returns Album."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
        try:
            # Create mappings CSV with album→album mapping (OLAK ID)
            temp_file.write("type,artist,title,spotify_id,ytm_id,spotify_artist,spotify_title,ytm_artist,ytm_title\n")
            temp_file.write("album,Artist Name,Album Title,,OLAK5uy_lXqjXfK9z3234fK9z3234,,,,,\n")
            temp_file.flush()
            temp_file.close()

            manager = MappingsManager(temp_file.name)

            album = Album(
                artists=["Artist Name"],
                title="Album Title",
                year=2020
            )

            # Get mapping - should return Album (OLAK is album ID)
            result = manager.get_album_mapping(album, "ytm")

            self.assertIsInstance(result, Album)
            self.assertEqual(result.service_id, "OLAK5uy_lXqjXfK9z3234fK9z3234")

        finally:
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)

    def test_track_to_album_mapping_ytm(self):
        """Test track mapped to YTM album ID (OLAK prefix)."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
        try:
            # Create mappings CSV with track→album mapping
            temp_file.write("type,artist,title,spotify_id,ytm_id,spotify_artist,spotify_title,ytm_artist,ytm_title\n")
            temp_file.write("track,Artist Name,Single Track,,OLAK5uy_lXqjXfK9z3234fK9z3234,,,,,\n")
            temp_file.flush()
            temp_file.close()

            manager = MappingsManager(temp_file.name)

            # Create source track
            track = Track(
                artists=["Artist Name"],
                title="Single Track",
                album=None,
                year=2022
            )

            # Get mapping - should return Album, not Track
            result = manager.get_track_mapping(track, "ytm")

            # Verify it returns an Album object
            self.assertIsInstance(result, Album)
            self.assertEqual(result.title, "Single Track")
            self.assertEqual(result.artists, ["Artist Name"])
            self.assertEqual(result.service_id, "OLAK5uy_lXqjXfK9z3234fK9z3234")
            self.assertEqual(result.service_name, "ytm")

        finally:
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)

    def test_track_to_track_mapping_with_videoid_returns_track(self):
        """Test track mapped to YTM track ID (11-char videoId) returns Track."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
        try:
            # Create mappings CSV with track→track mapping (videoId)
            temp_file.write("type,artist,title,spotify_id,ytm_id,spotify_artist,spotify_title,ytm_artist,ytm_title\n")
            temp_file.write("track,Artist Name,Track Title,,dQw4w9WgXcQ,,,,,\n")
            temp_file.flush()
            temp_file.close()

            manager = MappingsManager(temp_file.name)

            track = Track(
                artists=["Artist Name"],
                title="Track Title",
                album=None,
                year=2021
            )

            # Get mapping - should return Track (videoId is track ID)
            result = manager.get_track_mapping(track, "ytm")

            self.assertIsInstance(result, Track)
            self.assertEqual(result.service_id, "dQw4w9WgXcQ")

        finally:
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)

    def test_album_mapping_metadata_only_returns_album(self):
        """Test album mapping with metadata (no ID) returns Album."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
        try:
            # Create mappings CSV with metadata-based mapping
            temp_file.write("type,artist,title,spotify_id,ytm_id,spotify_artist,spotify_title,ytm_artist,ytm_title\n")
            temp_file.write("album,Original Artist,Original Album,,,Mapped Artist,Mapped Album,,,\n")
            temp_file.flush()
            temp_file.close()

            manager = MappingsManager(temp_file.name)

            album = Album(
                artists=["Original Artist"],
                title="Original Album",
                year=2020
            )

            # Get mapping - metadata-based, should return Album (search-based, no cross-type)
            result = manager.get_album_mapping(album, "spotify")

            self.assertIsInstance(result, Album)
            self.assertEqual(result.title, "Mapped Album")
            self.assertEqual(result.artists, ["Mapped Artist"])
            self.assertIsNone(result.service_id)  # No ID, just metadata

        finally:
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)

    def test_multiple_cross_type_mappings_in_same_file(self):
        """Test CSV file with both normal and cross-type mappings."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
        try:
            temp_file.write("type,artist,title,spotify_id,ytm_id,spotify_artist,spotify_title,ytm_artist,ytm_title\n")
            temp_file.write("album,Normal Artist,Normal Album,,OLAK5uy_normalalbum123,,,,,\n")
            temp_file.write("album,Audiobook Author,Audiobook Title,,dQw4w9WgXcQ,,,,,\n")  # Cross-type
            temp_file.write("track,Track Artist,Track Title,,OLAK5uy_tracktoalbum456,,,,,\n")  # Cross-type
            temp_file.flush()
            temp_file.close()

            manager = MappingsManager(temp_file.name)

            # Normal album mapping
            normal_album = Album(artists=["Normal Artist"], title="Normal Album", year=2020)
            result1 = manager.get_album_mapping(normal_album, "ytm")
            self.assertIsInstance(result1, Album)

            # Album→Track cross-type mapping
            audiobook = Album(artists=["Audiobook Author"], title="Audiobook Title", year=2021)
            result2 = manager.get_album_mapping(audiobook, "ytm")
            self.assertIsInstance(result2, Track)

            # Track→Album cross-type mapping
            track = Track(artists=["Track Artist"], title="Track Title", album=None, year=2022)
            result3 = manager.get_track_mapping(track, "ytm")
            self.assertIsInstance(result3, Album)

        finally:
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)

    def test_album_mapping_preserves_metadata(self):
        """Test that cross-type mapping preserves important metadata."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
        try:
            temp_file.write("type,artist,title,spotify_id,ytm_id,spotify_artist,spotify_title,ytm_artist,ytm_title\n")
            temp_file.write("album,Artist One & Artist Two,Joint Album,,dQw4w9WgXcQ,,,,,\n")
            temp_file.flush()
            temp_file.close()

            manager = MappingsManager(temp_file.name)

            # Album with multiple artists parsed from & separator and year
            album = Album(
                artists=["Artist One", "Artist Two"],
                title="Joint Album",
                year=2023
            )

            result = manager.get_album_mapping(album, "ytm")

            # Verify metadata preserved in Track
            self.assertIsInstance(result, Track)
            self.assertEqual(result.artists, ["Artist One", "Artist Two"])
            self.assertEqual(result.year, 2023)
            self.assertEqual(result.title, "Joint Album")

        finally:
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)


if __name__ == "__main__":
    unittest.main()
