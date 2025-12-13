"""Tests for similarity matching utilities."""

import unittest
from pushtunes.utils.similarity import (
    similarity,
    get_best_match,
    normalized_similarity,
    has_remaster_info,
    parse_remaster_info,
    _calculate_artist_similarity,
)
from pushtunes.models.album import Album
from pushtunes.models.track import Track


class TestBasicSimilarity(unittest.TestCase):
    """Test basic similarity functions."""

    def test_similarity_identical(self):
        """Test similarity with identical strings."""
        self.assertEqual(similarity("Album Title", "Album Title"), 1.0)
        self.assertEqual(similarity("Artist Name", "Artist Name"), 1.0)

    def test_similarity_case_insensitive(self):
        """Test similarity is case insensitive."""
        self.assertEqual(similarity("Album Title", "album title"), 1.0)
        self.assertEqual(similarity("ARTIST NAME", "artist name"), 1.0)

    def test_get_best_match_basic(self):
        """Test basic good match functionality."""
        # Perfect matches
        source = Album(artists=["The Beatles"], title="Abbey Road")
        candidate = Album(artists=["The Beatles"], title="Abbey Road")
        match, score = get_best_match(source, [candidate])
        self.assertIsNotNone(match)

        # Case differences should still match
        source = Album(artists=["the beatles"], title="abbey road")
        candidate = Album(artists=["The Beatles"], title="Abbey Road")
        match, score = get_best_match(source, [candidate])
        self.assertIsNotNone(match)

        # Poor matches should fail
        source = Album(artists=["Metallica"], title="Master of Puppets")
        candidate = Album(artists=["The Beatles"], title="Abbey Road")
        match, score = get_best_match(source, [candidate])
        self.assertIsNone(match)



class TestRemasterMatching(unittest.TestCase):
    """Test remaster-aware matching logic."""

    def setUp(self):
        """Set up test albums."""
        self.artist = ["Test Artist"]
        self.title = "Album Title"
        self.remaster_title = "Album Title (2015 Remaster)"
        self.source_album = Album(artists=self.artist, title=self.title)
        self.source_remaster = Album(artists=self.artist, title=self.remaster_title)

        self.candidates = [
            Album(artists=self.artist, title=self.title),
            Album(artists=self.artist, title=self.remaster_title),
            Album(artists=self.artist, title="Album Title (2020 Remaster)"),
        ]

    def test_remaster_does_not_match_non_remaster(self):
        """Test that a remaster matches a non-remaster version with a penalty."""
        match, score = get_best_match(self.source_remaster, [self.candidates[0]])
        # Should match, but with reduced score due to remaster penalty
        self.assertIsNotNone(match)
        self.assertLess(score, 1.0)
        self.assertGreaterEqual(score, 0.8)  # Should still be above min threshold

    def test_non_remaster_does_not_match_remaster(self):
        """Test that a non-remaster matches a remaster version with a penalty."""
        match, score = get_best_match(self.source_album, [self.candidates[1]])
        # Should match, but with reduced score due to remaster penalty
        self.assertIsNotNone(match)
        self.assertLess(score, 1.0)
        self.assertGreaterEqual(score, 0.8)  # Should still be above min threshold

    def test_identical_versions_match(self):
        """Test that identical versions match."""
        match, score = get_best_match(self.source_album, [self.candidates[0]])
        self.assertIsNotNone(match)
        match, score = get_best_match(self.source_remaster, [self.candidates[1]])
        self.assertIsNotNone(match)

    def test_different_remasters_match(self):
        """Test that two different remasters of the same album are a match."""
        # The base titles are the same, and both are remasters.
        match, score = get_best_match(self.source_remaster, [self.candidates[2]])
        self.assertIsNotNone(match)


class TestHybridArtistSimilarity(unittest.TestCase):
    """Test the hybrid artist similarity logic."""

    def test_parsing_mismatch_with_ampersand_in_name(self):
        """
        Test that similarity is high when one artist string is incorrectly
        split.
        """
        album1 = Album(artists=["Bohren", "der Club of Gore"], title="Sunset Mission")
        album2 = Album(artists=["Bohren & der Club of Gore"], title="Sunset Mission")
        match, score = get_best_match(album1, [album2])
        self.assertIsNotNone(match)

    def test_multi_artist_order_and_separator_insensitivity(self):
        """
        Test that similarity is high for multi-artist albums regardless of
        order or separator.
        """
        album1 = Album(artists=["Foo", "Bar"], title="Some Album")
        album2 = Album(artists=["Bar", "Foo"], title="Some Album")
        match, score = get_best_match(album1, [album2])
        self.assertIsNotNone(match)

    def test_completely_different_artists(self):
        """Test that completely different artists have low similarity."""
        album1 = Album(artists=["Genesis", "Phil Collins"], title="Some Album")
        album2 = Album(artists=["Yes", "Jon Anderson"], title="Some Album")
        match, score = get_best_match(album1, [album2])
        self.assertIsNone(match)


class TestSubsetMatching(unittest.TestCase):
    """Test subset matching for featured artists."""

    def test_subset_matching_single_to_multi_artist(self):
        """Test that single artist matches multi-artist when it's a subset."""
        # Case: Subsonic has "Perturbator", Spotify has "Perturbator, Greta Link"
        album1 = Album(artists=["Perturbator"], title="Venger (feat. Greta Link)")
        album2 = Album(artists=["Perturbator", "Greta Link"], title="Venger (feat. Greta Link)")

        # Should match with high similarity (0.95)
        match, score = get_best_match(album1, [album2], min_similarity=0.8)
        self.assertIsNotNone(match)

        # Test artist similarity directly
        sim = _calculate_artist_similarity(album1.artists, album2.artists)
        self.assertAlmostEqual(sim, 0.95, places=2)

    def test_subset_matching_reverse(self):
        """Test subset matching works in reverse (multi to single)."""
        album1 = Album(artists=["Carbon Based Lifeforms", "Ester Nannmark"], title="...and On")
        album2 = Album(artists=["Carbon Based Lifeforms"], title="...and On")

        match, score = get_best_match(album1, [album2], min_similarity=0.8)
        self.assertIsNotNone(match)

    def test_no_subset_no_match(self):
        """Test that non-overlapping artists don't match via subset logic."""
        album1 = Album(artists=["Artist A"], title="Song")
        album2 = Album(artists=["Artist B", "Artist C"], title="Song")

        match, score = get_best_match(album1, [album2], min_similarity=0.8)
        self.assertIsNone(match)


class TestSoundtrackMatching(unittest.TestCase):
    """Test soundtrack suffix handling."""

    def test_parse_original_game_soundtrack(self):
        """Test parsing (Original Game Soundtrack) suffix."""
        base, year, rtype = parse_remaster_info("Shift Quantum, Vol. 2 (Original Game Soundtrack)")
        self.assertEqual(base, "Shift Quantum, Vol. 2")
        self.assertIsNone(year)
        self.assertEqual(rtype, "soundtrack")

    def test_parse_original_soundtrack(self):
        """Test parsing (Original Soundtrack) suffix."""
        base, year, rtype = parse_remaster_info("Drive (Original Soundtrack)")
        self.assertEqual(base, "Drive")
        self.assertIsNone(year)
        self.assertEqual(rtype, "soundtrack")

    def test_parse_motion_picture_soundtrack(self):
        """Test parsing (Original Motion Picture Soundtrack) suffix."""
        base, year, rtype = parse_remaster_info("The Social Network (Original Motion Picture Soundtrack)")
        self.assertEqual(base, "The Social Network")
        self.assertIsNone(year)
        self.assertEqual(rtype, "soundtrack")

    def test_parse_ost(self):
        """Test parsing (OST) suffix."""
        base, year, rtype = parse_remaster_info("Skyrim (OST)")
        self.assertEqual(base, "Skyrim")
        self.assertIsNone(year)
        self.assertEqual(rtype, "soundtrack")

    def test_soundtrack_matches_non_soundtrack(self):
        """Test that soundtrack version matches non-soundtrack version."""
        source = Album(artists=["Volkor X"], title="Shift Quantum, Vol. 2")
        candidate = Album(artists=["Volkor X"], title="Shift Quantum, Vol. 2 (Original Game Soundtrack)")

        match, score = get_best_match(source, [candidate], min_similarity=0.8)
        self.assertIsNotNone(match)

    def test_non_soundtrack_matches_soundtrack(self):
        """Test that non-soundtrack version matches soundtrack version (reverse)."""
        source = Album(artists=["Volkor X"], title="Shift Quantum, Vol. 2 (Original Soundtrack)")
        candidate = Album(artists=["Volkor X"], title="Shift Quantum, Vol. 2")

        match, score = get_best_match(source, [candidate], min_similarity=0.8)
        self.assertIsNotNone(match)

    def test_remaster_still_strict(self):
        """Test that remaster matching remains strict (prefers non-remaster)."""
        source = Album(artists=["Bluetech"], title="Wilderness")
        candidates = [
            Album(artists=["Bluetech"], title="Wilderness - 2020 Remastered"),
            Album(artists=["Bluetech"], title="Wilderness"),
        ]

        match, score = get_best_match(source, candidates, min_similarity=0.8)
        self.assertIsNotNone(match)
        # Should prefer the non-remastered version
        self.assertEqual(match.title, "Wilderness")


class TestTrackSimilarity(unittest.TestCase):
    """Test similarity matching for tracks."""

    def test_track_basic_match(self):
        """Test basic track matching."""
        source = Track(artists=["Dire Straits"], title="Sultans of Swing")
        candidate = Track(artists=["Dire Straits"], title="Sultans of Swing")

        match, score = get_best_match(source, [candidate], min_similarity=0.8)
        self.assertIsNotNone(match)

    def test_track_featured_artist_subset(self):
        """Test track matching with featured artists as subset."""
        source = Track(artists=["Perturbator"], title="Venger (feat. Greta Link)")
        candidate = Track(artists=["Perturbator", "Greta Link"], title="Venger (feat. Greta Link)")

        match, score = get_best_match(source, [candidate], min_similarity=0.8)
        self.assertIsNotNone(match)

    def test_track_case_insensitive(self):
        """Test track matching is case insensitive."""
        source = Track(artists=["the beatles"], title="hey jude")
        candidate = Track(artists=["The Beatles"], title="Hey Jude")

        match, score = get_best_match(source, [candidate], min_similarity=0.8)
        self.assertIsNotNone(match)


if __name__ == "__main__":
    unittest.main()
