from dataclasses import dataclass, field
from typing import Self, Any, override


@dataclass(eq=False)
class Album:
    """Represents an album with artist and title."""

    title: str
    artists: list[str] = field(default_factory=list)
    year: int | None = None
    service_id: str | None = None
    service_name: str | None = None
    extra_data: dict[str, Any] | None = None

    # @override
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Album):
            return False

        # For equality, artists should be the same, case- and order-independent
        artists_match = sorted(a.lower() for a in self.artists) == sorted(
            a.lower() for a in other.artists
        )

        if self.year and other.year:
            return (
                self.title.lower() == other.title.lower()
                and artists_match
                and self.year == other.year
            )
        else:
            return self.title.lower() == other.title.lower() and artists_match

    def __hash__(self):
        return hash(
            (self.title.lower(), tuple(sorted(a.lower() for a in self.artists)))
        )

    @classmethod
    def by_single_artist(cls, artist: str, /, **kw) -> Self:
        return cls(artists=[artist], **kw)

    @property
    def artist(self) -> str:
        """Human-readable concatenation of all artists."""
        match self.artists:
            case []:
                return ""
            case [a]:
                return a
            case [a, b]:
                return f"{a} & {b}"
            case _:
                # Alternative: Foo, Bar, Blarp & Baz
                # *init, last = self.artists
                # return ", ".join(init) + f" & {last}"
                return ", ".join(self.artists)

    def search_string(self, service_name: str | None):
        """A string that can be used to search for this album on a specific service"""
        match service_name:
            case "ytm":
                # For YTM, we just slap artists together willy-nilly because it's impossible
                # to predict how that thing performs searches.
                # YTM also gets confused if you add a year (sigh...) so let's not.
                search_query = f"{' '.join(self.artists)} {self.title}"
            case "spotify":
                # Limit to first 3 artists to avoid exceeding Spotify's 250 char query limit
                # Compilation albums with many artists would otherwise fail
                artists_to_use = self.artists[:3]
                artists_query = ""
                for artist in artists_to_use:
                    artists_query += f"artist:{artist} "
                search_query = f"{artists_query.rstrip()} album:{self.title}"
                if self.year:
                    search_query += f" year:{self.year}"
            case "tidal":
                # Tidal uses simple search queries
                search_query = f"{self.artist} {self.title}"
            case _:
                search_query = f"{self.artist} {self.title}"

        return search_query

    # def similarity_to(self, other: Self) -> float:
    #     from pushtunes.utils.similarity import similarity
    #
    #     artist_sim = similarity(self.artist, other.artist)
    #     title_sim = similarity(self.title, other.title)
    #     return artist_sim + title_sim / 2.0
