"""Playlist model."""

from dataclasses import dataclass, field
from typing import Any
from pushtunes.models.track import Track


@dataclass
class Playlist:
    """Represents a playlist with name and ordered tracks."""

    name: str
    tracks: list[Track] = field(default_factory=list)
    service_id: str | None = None
    service_name: str | None = None
    description: str | None = None
    extra_data: dict[str, Any] | None = None

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Playlist):
            return False

        return self.name.lower() == other.name.lower()

    def __hash__(self):
        return hash(self.name.lower())
