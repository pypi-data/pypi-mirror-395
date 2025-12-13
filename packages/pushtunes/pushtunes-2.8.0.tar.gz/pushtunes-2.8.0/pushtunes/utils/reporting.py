"""Utilities for generating reports from push results."""

from typing import Any

from rich.console import Console
from rich.table import Table


def print_album_results_table(results: list[Any], status_filter: str, title: str, use_color: bool = True) -> None:
    """Print a table of album results matching a specific status.

    Args:
        results: List of PushResult[Album] objects
        status_filter: Status value to filter by (e.g., 'not_found', 'filtered')
        title: Title for the table section
        use_color: Whether to use colored output
    """
    # Filter results by status
    filtered = [r for r in results if r.status.name == status_filter]

    if not filtered:
        return

    console = Console(no_color=not use_color, force_terminal=True)

    table = Table(
        title=f"{title} ({len(filtered)} albums)" if use_color else None,
        show_header=True,
        header_style="bold magenta" if use_color else "bold",
        expand=True,
    )

    # Print plain title when colors are disabled
    if not use_color:
        console.print(f"\n{title} ({len(filtered)} albums)")
    table.add_column("Artist", style="cyan" if use_color else None, no_wrap=False)
    table.add_column("Album", style="green" if use_color else None, no_wrap=False)
    table.add_column("Year", style="yellow" if use_color else None, justify="right")

    for result in filtered:
        artist = result.item.artist
        album_title = result.item.title
        year = str(result.item.year) if result.item.year else ""
        table.add_row(artist, album_title, year)

    console.print(table)


def print_track_results_table(results: list[Any], status_filter: str, title: str, use_color: bool = True) -> None:
    """Print a table of track results matching a specific status.

    Args:
        results: List of PushResult[Track] objects
        status_filter: Status value to filter by (e.g., 'not_found', 'filtered')
        title: Title for the table section
        use_color: Whether to use colored output
    """
    # Filter results by status
    filtered = [r for r in results if r.status.name == status_filter]

    if not filtered:
        return

    console = Console(no_color=not use_color, force_terminal=True)

    table = Table(
        title=f"{title} ({len(filtered)} tracks)" if use_color else None,
        show_header=True,
        header_style="bold magenta" if use_color else "bold",
        expand=True,
    )

    # Print plain title when colors are disabled
    if not use_color:
        console.print(f"\n{title} ({len(filtered)} tracks)")
    table.add_column("Artist", style="cyan" if use_color else None, no_wrap=False)
    table.add_column("Track", style="green" if use_color else None, no_wrap=False)
    table.add_column("Album", style="yellow" if use_color else None, no_wrap=False)

    for result in filtered:
        artist = result.item.artist
        track_title = result.item.title
        album = result.item.album or ""
        table.add_row(artist, track_title, album)

    console.print(table)


def print_playlist_track_results_table(results: list[Any], status_filter: str, title: str, use_color: bool = True) -> None:
    """Print a table of playlist track results matching a specific status.

    Args:
        results: List of PlaylistTrackResult objects
        status_filter: Status value to filter by (e.g., 'not_found', 'matched')
        title: Title for the table section
        use_color: Whether to use colored output
    """
    # Filter results by status
    filtered = [r for r in results if r.status.name == status_filter]

    if not filtered:
        return

    console = Console(no_color=not use_color, force_terminal=True)

    table = Table(
        title=f"{title} ({len(filtered)} tracks)" if use_color else None,
        show_header=True,
        header_style="bold magenta" if use_color else "bold",
        expand=True,
    )

    # Print plain title when colors are disabled
    if not use_color:
        console.print(f"\n{title} ({len(filtered)} tracks)")
    table.add_column("#", style="dim" if use_color else None, justify="right")
    table.add_column("Artist", style="cyan" if use_color else None, no_wrap=False)
    table.add_column("Track", style="green" if use_color else None, no_wrap=False)

    for i, result in enumerate(filtered, 1):
        artist = result.item.artist
        track_title = result.item.title
        table.add_row(str(i), artist, track_title)

    console.print(table)


def generate_report(results: list[Any], report_statuses: list[str], result_type: str = "album", use_color: bool = True) -> None:
    """Generate a report showing items matching requested statuses.

    Args:
        results: List of result objects (PushResult[Album], PushResult[Track], or PlaylistTrackResult)
        report_statuses: List of status names to include in report
        result_type: Type of results ('album', 'track', or 'playlist')
        use_color: Whether to use colored output
    """
    if not report_statuses or not results:
        return

    # Status name mapping for display
    status_titles = {
        "not_found": "Not found",
        "already_in_library": "Already in library",
        "filtered": "Filtered out",
        "error": "Errors",
        "added": "Added",
        "similarity_too_low": "Similarity too low",
        "matched": "Matched",
    }

    console = Console(no_color=not use_color, force_terminal=True)
    if use_color:
        console.print("\n[bold]Detailed Report[/bold]", style="bold white on blue")
    else:
        console.print("\nDetailed Report")

    # Print a table for each requested status
    for status in report_statuses:
        status_lower = status.lower()
        if status_lower not in status_titles:
            if use_color:
                console.print(f"\n[yellow]Warning: Unknown status '{status}' - skipping[/yellow]")
            else:
                console.print(f"\nWarning: Unknown status '{status}' - skipping")
            continue

        title = status_titles[status_lower]

        if result_type == "album":
            print_album_results_table(results, status_lower, title, use_color)
        elif result_type == "track":
            print_track_results_table(results, status_lower, title, use_color)
        elif result_type == "playlist":
            print_playlist_track_results_table(results, status_lower, title, use_color)
