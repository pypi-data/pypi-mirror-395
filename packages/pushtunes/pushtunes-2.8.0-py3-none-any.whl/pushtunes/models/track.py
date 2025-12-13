from dataclasses import dataclass, field
from typing import Any, Self


@dataclass(eq=False)
class Track:
    """Represents a track with artist, title and optional album and year."""

    title: str
    artists: list[str] = field(default_factory=list)
    album: str | None = None
    year: int | None = None
    service_id: str | None = None
    service_name: str | None = None
    extra_data: dict[str, Any] | None = None

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Track):
            return False

        # For equality, artists should be the same, case- and order-independent
        artists_match = sorted(a.lower() for a in self.artists) == sorted(
            a.lower() for a in other.artists
        )

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
        """A string that can be used to search for this track on a specific service"""
        match service_name:
            case "ytm":
                search_query = f"{self.artist} {self.title}"
                if self.year:
                    search_query = f"{search_query} ({self.year})"
            case "spotify":
                # Limit to first 3 artists to avoid exceeding Spotify's 250 char query limit
                artists_to_use = self.artists[:3]
                artists_query = ""
                for artist in artists_to_use:
                    artists_query += f"artist:{artist} "
                search_query = f"{artists_query.rstrip()} track:{self.title}"
                # Add album if present (more specific than year)
                if self.album:
                    search_query = f"{search_query} album:{self.album}"
                # Only add year if album is not present (to avoid over-constraining)
                elif self.year:
                    search_query = f"{search_query} year:{self.year}"
            case "tidal":
                # Tidal uses simple search queries
                search_query = f"{self.artist} {self.title}"
            case _:
                search_query = f"{self.artist} {self.title}"

        return search_query
