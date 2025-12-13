"""Utilities for deletion confirmation and preview display."""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from pushtunes.models.album import Album
from pushtunes.models.track import Track
from pushtunes.utils.deletion_manager import DeletionPreview


def display_deletion_preview(
    preview: DeletionPreview,
    item_type: str,
    min_similarity: float,
    use_color: bool = True,
    show_total: bool = True,
) -> None:
    """Display a preview of items that will be deleted.

    Args:
        preview: DeletionPreview object with deletion analysis
        item_type: "albums" or "tracks"
        min_similarity: Similarity threshold being used
        use_color: Whether to use colored output
        show_total: Whether to show total items in target library (only relevant for push --delete)
    """
    console = Console(no_color=not use_color)

    # Summary panel
    summary_text = Text()

    # Only show total and preserved counts for push --delete (when comparing source vs target)
    if show_total:
        summary_text.append(f"Total {item_type} in target library: ", style="bold")
        summary_text.append(f"{preview.total_target_items}\n", style="bold cyan")

    summary_text.append(f"{item_type.capitalize()} that will be ", style="bold")
    summary_text.append("DELETED", style="bold red")
    summary_text.append(": ", style="bold")
    summary_text.append(f"{len(preview.items_to_delete)}", style="bold red")

    if show_total:
        summary_text.append("\n", style="bold")
        summary_text.append(f"{item_type.capitalize()} that will be ", style="bold")
        summary_text.append("PRESERVED", style="bold green")
        summary_text.append(": ", style="bold")
        summary_text.append(f"{len(preview.items_preserved)}", style="bold green")

    console.print(Panel(summary_text, title="Deletion Preview", border_style="yellow"))

    # Show items that will be deleted
    if preview.items_to_delete:
        console.print()
        if show_total:
            # For push --delete: mention source comparison
            console.print(
                f"[bold red]Items that will be DELETED[/bold red] (not found in source with similarity >= {min_similarity}):"
            )
        else:
            # For standalone delete: just list items
            console.print(f"[bold red]Items that will be DELETED:[/bold red]")
        console.print()

        table = Table(show_header=True, header_style="bold red")
        table.add_column("Artist")
        table.add_column("Title")
        if item_type == "tracks":
            table.add_column("Album")

        # Show up to 50 items
        for candidate in preview.items_to_delete[:50]:
            item = candidate.item
            if isinstance(item, Album):
                table.add_row(item.artist, item.title)
            else:  # Track
                table.add_row(item.artist, item.title, item.album or "N/A")

        console.print(table)

        if len(preview.items_to_delete) > 50:
            console.print(f"... and {len(preview.items_to_delete) - 50} more items")

    console.print()


def confirm_deletion(
    preview: DeletionPreview, item_type: str, backup_file: str, use_color: bool = True
) -> bool:
    """Ask user to confirm deletion.

    Args:
        preview: DeletionPreview object
        item_type: "albums" or "tracks"
        backup_file: Path to the backup file
        use_color: Whether to use colored output

    Returns:
        True if user confirms, False otherwise
    """
    console = Console(no_color=not use_color)

    if not preview.items_to_delete:
        console.print(
            "[bold green]No items to delete. Target is already in sync with source.[/bold green]"
        )
        return False

    console.print()
    console.print(f"[bold]Backup saved to:[/bold] {backup_file}")
    console.print(
        "You can restore deleted items using: pushtunes push {item_type} --from=csv --csv-file={backup_file}".format(
            item_type=item_type, backup_file=backup_file
        )
    )
    console.print()

    # Ask for confirmation
    console.print(
        f"[bold yellow]Are you sure you want to delete {len(preview.items_to_delete)} {item_type}?[/bold yellow]"
    )
    console.print("This action will remove them from your target library.")
    console.print()

    response = (
        input("Type 'yes' to confirm deletion, or anything else to cancel: ")
        .strip()
        .lower()
    )

    if response == "yes":
        console.print("[bold green]Proceeding with deletion...[/bold green]")
        return True
    else:
        console.print("[bold red]Deletion cancelled.[/bold red]")
        return False


def display_item_details(item: Album | Track, item_type: str) -> str:
    """Format item details for display.

    Args:
        item: Album or Track object
        item_type: "album" or "track"

    Returns:
        Formatted string
    """
    if isinstance(item, Album):
        return f"{item.artist} - {item.title}"
    else:  # Track
        if item.album:
            return f"{item.artist} - {item.title} (from {item.album})"
        else:
            return f"{item.artist} - {item.title}"
