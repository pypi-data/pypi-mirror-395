"""CLI command implementations organized by function."""

# Import push commands
from pushtunes.utils.cli.commands.push import (
    push_albums,
    push_tracks,
    push_playlist,
)

# Import compare commands
from pushtunes.utils.cli.commands.compare import (
    compare_albums,
    compare_tracks,
    compare_playlist,
)

# Import delete commands
from pushtunes.utils.cli.commands.delete import (
    delete_albums,
    delete_tracks,
)

# Export all commands
__all__ = [
    "push_albums",
    "push_tracks",
    "push_playlist",
    "compare_albums",
    "compare_tracks",
    "compare_playlist",
    "delete_albums",
    "delete_tracks",
]
