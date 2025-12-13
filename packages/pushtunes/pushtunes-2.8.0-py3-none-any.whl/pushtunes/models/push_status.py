"""Shared status enum for push operations (albums, tracks, playlists)."""

from enum import Enum, auto


class PushStatus(Enum):
    """Status of a push operation for an album, track, or playlist item."""

    # Common to all push operations
    not_found = auto()
    similarity_too_low = auto()
    error = auto()
    mapped = auto()

    # Used by album and track pushers
    already_in_library = auto()
    filtered = auto()
    added = auto()
    deleted = auto()

    # Used by playlist pusher
    matched = auto()
