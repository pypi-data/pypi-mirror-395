"""Deleter for removing albums and tracks from music services with preview and backup."""

from pushtunes.models.track import Track
from pushtunes.models.album import Album
from pushtunes.models.push_status import PushStatus
from pushtunes.services.music_service import MusicService
from pushtunes.utils.logging import get_logger
from pushtunes.utils.deletion_manager import DeletionManager, DeletionPreview, DeletionCandidate
from dataclasses import dataclass
from typing import TypeVar, Generic, Literal


T = TypeVar('T', Album, Track)


@dataclass(frozen=True, slots=True)
class DeleteResult(Generic[T]):
    """Result of a delete operation."""
    item: T
    status: PushStatus  # deleted, error
    message: str = ""


@dataclass
class Deleter(Generic[T]):
    """Handles deletion of albums or tracks from a music service with backup and confirmation."""

    items_to_delete: list[T]
    service: MusicService
    item_type: Literal["album", "track"]
    backup_operation_name: str = "deletion"
    require_confirmation: bool = True
    color: bool = True

    def delete(self) -> list[DeleteResult[T]]:
        """Delete items from service with preview, backup, and confirmation.

        Returns:
            List of DeleteResult objects with status for each item
        """
        from pushtunes.utils.deletion_confirm import display_deletion_preview, confirm_deletion

        log = get_logger()

        if not self.items_to_delete:
            log.info("No items to delete")
            return []

        # Create a DeletionPreview object for display
        # All items are marked for deletion (no source comparison)
        deletion_candidates = [
            DeletionCandidate(
                item=item,
                source_match=None,
                similarity_score=0.0,
                will_be_deleted=True
            )
            for item in self.items_to_delete
        ]

        preview = DeletionPreview(
            total_target_items=len(self.items_to_delete),
            items_to_delete=deletion_candidates,
            items_preserved=[]
        )

        # Show preview using shared function (without total/preserved counts for standalone delete)
        display_deletion_preview(
            preview=preview,
            item_type=f"{self.item_type}s",
            min_similarity=0.0,  # Not applicable for standalone delete
            use_color=self.color,
            show_total=False  # Don't show total library counts for standalone delete
        )

        # Create backup
        deletion_manager = DeletionManager()
        if self.item_type == "album":
            backup_file = deletion_manager.backup_albums(self.items_to_delete, self.backup_operation_name)
        else:
            backup_file = deletion_manager.backup_tracks(self.items_to_delete, self.backup_operation_name)

        log.info(f"Backup saved to: {backup_file}")

        # Request confirmation using shared function
        if self.require_confirmation:
            if not confirm_deletion(preview, f"{self.item_type}s", backup_file, self.color):
                return []

        # Perform deletion
        return self._perform_deletion()

    def _perform_deletion(self) -> list[DeleteResult[T]]:
        """Perform the actual deletion.

        Returns:
            List of DeleteResult objects
        """
        from rich.console import Console
        from rich.progress import Progress, SpinnerColumn, TextColumn

        log = get_logger()
        results: list[DeleteResult[T]] = []
        console = Console(no_color=not self.color)

        delete_method = getattr(self.service, f"remove_{self.item_type}")

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task(
                f"Deleting {len(self.items_to_delete)} {self.item_type}s...",
                total=len(self.items_to_delete)
            )

            for item in self.items_to_delete:
                success = delete_method(item)
                if success:
                    results.append(DeleteResult(item=item, status=PushStatus.deleted))
                    log.info(f"Deleted: {item.artist} - {item.title}")
                else:
                    results.append(DeleteResult(
                        item=item,
                        status=PushStatus.error,
                        message="Failed to delete"
                    ))
                    log.error(f"Failed to delete: {item.artist} - {item.title}")

                progress.update(task, advance=1)

        return results


def print_delete_stats(results: list[DeleteResult], item_type: str = "albums", use_color: bool = True):
    """Print deletion statistics.

    Args:
        results: List of DeleteResult objects
        item_type: Type of items ("albums" or "tracks")
        use_color: Whether to use colored output
    """
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text

    console = Console(no_color=not use_color)

    deleted_count = sum(1 for r in results if r.status == PushStatus.deleted)
    error_count = sum(1 for r in results if r.status == PushStatus.error)

    stats_text = Text()
    stats_text.append("Successfully deleted: ", style="bold")
    stats_text.append(f"{deleted_count} {item_type}", style="bold green")
    if error_count > 0:
        stats_text.append("\nErrors: ", style="bold")
        stats_text.append(f"{error_count}", style="bold red")

    console.print()
    console.print(Panel(stats_text, title="Deletion Complete", border_style="green"))
