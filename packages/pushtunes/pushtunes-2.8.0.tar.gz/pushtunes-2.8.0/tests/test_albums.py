import unittest
from pushtunes.models.album import Album


class TestSearchString(unittest.TestCase):
    def test_ytm_search_string(self):
        album = Album(artists=["Ott"], title="Blumenkraft", service_name="ytm")
        self.assertEqual(album.search_string(service_name="ytm"), "Ott Blumenkraft")

    def test_ytm_search_string_with_year(self):
        # YTM doesn't include year in search query because it gets confused by it
        album = Album(
            artists=["Ott"], title="Blumenkraft", year=2003, service_name="ytm"
        )
        self.assertEqual(
            album.search_string(service_name="ytm"), "Ott Blumenkraft"
        )

    def test_spotify(self):
        album = Album(artists=["Ott"], title="Blumenkraft", service_name="ytm")
        self.assertEqual(
            album.search_string(service_name="spotify"), "artist:Ott album:Blumenkraft"
        )

    def test_spotify_search_string_with_year(self):
        album = Album(
            artists=["Ott"], title="Blumenkraft", year=2003, service_name="ytm"
        )
        self.assertEqual(
            album.search_string(service_name="spotify"),
            "artist:Ott album:Blumenkraft year:2003",
        )


class TestArtistProperty(unittest.TestCase):
    def test_zero_artists(self):
        self.assertEqual(Album(artists=[], title="Empty").artist, "")

    def test_one_artist(self):
        self.assertEqual(
            Album(artists=["Pink Floyd"], title="The Wall").artist, "Pink Floyd"
        )

    def test_two_artists(self):
        self.assertEqual(
            Album(artists=["Simon", "Garfunkel"], title="Bookends").artist,
            "Simon & Garfunkel",
        )

    def test_four_artists(self):
        self.assertEqual(
            Album(artists=["A", "B", "C", "D"], title="Comp").artist, "A, B, C, D"
        )
