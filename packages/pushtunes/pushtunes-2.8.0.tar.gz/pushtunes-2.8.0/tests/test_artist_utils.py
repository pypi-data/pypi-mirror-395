"""Tests for artist utilities."""

import unittest
from pushtunes.utils.artist_utils import parse_artist_string, extract_featured_artists


class TestParseArtistString(unittest.TestCase):
    """Test artist string parsing."""

    def test_single_artist(self):
        """Test parsing single artist."""
        result = parse_artist_string("Perturbator")
        self.assertEqual(result, ["Perturbator"])

    def test_ampersand_separator(self):
        """Test parsing with & separator."""
        result = parse_artist_string("Carbon Based Lifeforms & Ester Nannmark")
        self.assertEqual(result, ["Carbon Based Lifeforms", "Ester Nannmark"])

    def test_plus_separator(self):
        """Test parsing with + separator."""
        result = parse_artist_string("Artist A + Artist B")
        self.assertEqual(result, ["Artist A", "Artist B"])

    def test_slash_separator(self):
        """Test parsing with / separator."""
        result = parse_artist_string("Kashchei/Zebbler Encanti Experience")
        self.assertEqual(result, ["Kashchei", "Zebbler Encanti Experience"])

    def test_feat_separator(self):
        """Test parsing with feat. separator."""
        result = parse_artist_string("Carbon Based Lifeforms feat. Ester Nannmark")
        self.assertEqual(result, ["Carbon Based Lifeforms", "Ester Nannmark"])

    def test_ft_separator(self):
        """Test parsing with ft. separator."""
        result = parse_artist_string("Volkor X ft. Dimi Kaye")
        self.assertEqual(result, ["Volkor X", "Dimi Kaye"])

    def test_featuring_separator(self):
        """Test parsing with featuring separator."""
        result = parse_artist_string("Artist A featuring Artist B")
        self.assertEqual(result, ["Artist A", "Artist B"])

    def test_multiple_separators(self):
        """Test parsing with multiple separator types."""
        result = parse_artist_string("Carbon Based Lifeforms feat. Not Lars & Ester Nannmark")
        self.assertEqual(result, ["Carbon Based Lifeforms", "Not Lars", "Ester Nannmark"])

    def test_comma_separator(self):
        """Test parsing with comma separator."""
        result = parse_artist_string("Artist A, Artist B, Artist C")
        self.assertEqual(result, ["Artist A", "Artist B", "Artist C"])

    def test_empty_string(self):
        """Test parsing empty string."""
        result = parse_artist_string("")
        self.assertEqual(result, [])

    def test_whitespace_trimming(self):
        """Test that whitespace is properly trimmed."""
        result = parse_artist_string("  Artist A  &  Artist B  ")
        self.assertEqual(result, ["Artist A", "Artist B"])


class TestExtractFeaturedArtists(unittest.TestCase):
    """Test extracting featured artists from titles."""

    def test_feat_in_parentheses(self):
        """Test extracting (feat. Artist) pattern."""
        result = extract_featured_artists("Venger (feat. Greta Link)")
        self.assertEqual(result, ["Greta Link"])

    def test_ft_in_parentheses(self):
        """Test extracting (ft. Artist) pattern."""
        result = extract_featured_artists("Song Title (ft. Featured Artist)")
        self.assertEqual(result, ["Featured Artist"])

    def test_featuring_in_parentheses(self):
        """Test extracting (featuring Artist) pattern."""
        result = extract_featured_artists("Track (featuring Someone)")
        self.assertEqual(result, ["Someone"])

    def test_multiple_featured_artists(self):
        """Test extracting multiple featured artists."""
        result = extract_featured_artists("Song (feat. Artist A & Artist B)")
        self.assertEqual(result, ["Artist A", "Artist B"])

    def test_no_featured_artists(self):
        """Test when no featured artists present."""
        result = extract_featured_artists("Regular Track Title")
        self.assertEqual(result, [])

    def test_feat_without_parentheses(self):
        """Test extracting feat. without parentheses."""
        result = extract_featured_artists("Song feat. Artist Name")
        self.assertEqual(result, ["Artist Name"])


if __name__ == "__main__":
    unittest.main()
