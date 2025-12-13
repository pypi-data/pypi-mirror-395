"""Shared status enum for compare operations (albums, tracks, playlists)."""

from enum import Enum, auto


class CompareStatus(Enum):
    """Status of a compare operation for an album, track, or playlist item."""

    only_in_source = auto()  # Item exists only in source
    only_in_target = auto()  # Item exists only in target
    in_both = auto()  # Item exists in both source and target
    filtered = auto()  # Item was filtered out
    error = auto()  # Error occurred during comparison
