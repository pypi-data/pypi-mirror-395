import unittest
from pushtunes.models.track import Track


class TestTrackModel(unittest.TestCase):
    """Test Track model functionality."""

    def test_by_single_artist(self):
        """Test creating track with single artist."""
        track = Track.by_single_artist("Dire Straits", title="Sultans of Swing")
        self.assertEqual(track.artists, ["Dire Straits"])
        self.assertEqual(track.title, "Sultans of Swing")

    def test_artist_property_single(self):
        """Test artist property with single artist."""
        track = Track(artists=["The Beatles"], title="Hey Jude")
        self.assertEqual(track.artist, "The Beatles")

    def test_artist_property_two_artists(self):
        """Test artist property with two artists."""
        track = Track(artists=["Artist A", "Artist B"], title="Song")
        self.assertEqual(track.artist, "Artist A & Artist B")

    def test_artist_property_multiple_artists(self):
        """Test artist property with multiple artists."""
        track = Track(artists=["A", "B", "C"], title="Song")
        self.assertEqual(track.artist, "A, B, C")

    def test_equality_case_insensitive(self):
        """Test track equality is case insensitive."""
        track1 = Track(artists=["The Beatles"], title="Hey Jude")
        track2 = Track(artists=["the beatles"], title="hey jude")
        self.assertEqual(track1, track2)

    def test_equality_artist_order_independent(self):
        """Test track equality is artist order independent."""
        track1 = Track(artists=["A", "B"], title="Song")
        track2 = Track(artists=["B", "A"], title="Song")
        self.assertEqual(track1, track2)

    def test_hash_consistent(self):
        """Test track hashing is consistent."""
        track1 = Track(artists=["Artist"], title="Title")
        track2 = Track(artists=["Artist"], title="Title")
        self.assertEqual(hash(track1), hash(track2))


class TestSearchString(unittest.TestCase):
    def test_ytm_search_string(self):
        track = Track.by_single_artist("Ott", title="Blumenkraft", service_name="ytm")
        self.assertEqual(track.search_string(service_name="ytm"), "Ott Blumenkraft")

    def test_ytm_search_string_with_year(self):
        track = Track.by_single_artist(
            "Ott", title="Blumenkraft", year=2003, service_name="ytm"
        )
        self.assertEqual(
            track.search_string(service_name="ytm"), "Ott Blumenkraft (2003)"
        )

    def test_spotify(self):
        track = Track.by_single_artist("Ott", title="Blumenkraft", service_name="ytm")
        self.assertEqual(
            track.search_string(service_name="spotify"), "artist:Ott track:Blumenkraft"
        )

    def test_spotify_search_string_with_year(self):
        # Year is only added if album is not present
        track = Track.by_single_artist(
            "Ott", title="Blumenkraft", year=2003, service_name="ytm"
        )
        self.assertEqual(
            track.search_string(service_name="spotify"),
            "artist:Ott track:Blumenkraft year:2003",
        )

        # When album is present, year is ignored in favor of album
        track_with_album = Track.by_single_artist(
            "Ott", title="Blumenkraft", album="Skylon", year=2003, service_name="ytm"
        )
        self.assertEqual(
            track_with_album.search_string(service_name="spotify"),
            "artist:Ott track:Blumenkraft album:Skylon",
        )
