"""Delete commands for removing albums and tracks from music services."""

import sys
from typing import Optional

import typer

from pushtunes.models.album import Album
from pushtunes.models.track import Track
from pushtunes.models.push_status import PushStatus
from pushtunes.utils.filters import AlbumFilter, TrackFilter, FilterAction
from pushtunes.utils.logging import get_logger, set_console_log_level
from pushtunes.services.deleter import Deleter, print_delete_stats
from pushtunes.utils.cli.commands.shared import create_service


def delete_albums(
    service: str = typer.Option(..., "--from", help="Service to delete from ('spotify' or 'ytm')"),
    verbose: bool = typer.Option(False, "-v", "--verbose", help="Enable verbose output"),
    log_level: str = typer.Option(
        "INFO",
        "--log-level",
        help="Console log level: DEBUG, INFO, WARNING, ERROR, CRITICAL (default: INFO)",
    ),
    ytm_auth: str = typer.Option(
        "browser.json",
        help="Path to YouTube Music authentication file (default: browser.json)",
    ),
    include: Optional[list[str]] = None,
    exclude: Optional[list[str]] = None,
    patterns_from: Optional[str] = None,
    color: bool = typer.Option(
        True,
        "--color/--no-color",
        help="Enable/disable colored output (default: enabled)",
    ),
):
    """
    Delete albums from a music service based on filter criteria.

    This command requires a filter to specify which albums to delete.
    It fetches all albums from the service, applies the filter, shows a preview,
    creates a backup, and then deletes matching albums after confirmation.

    Examples:
        # Delete all albums by specific artist
        pushtunes delete albums --from spotify --include="artist:'Volkor X'"

        # Delete all live albums
        pushtunes delete albums --from spotify --exclude="album:'.*Live.*'"

        # Use patterns file
        pushtunes delete albums --from spotify --patterns-from=filters.txt
    """
    # Set console log level
    try:
        set_console_log_level(log_level)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Create configuration
    config = {
        "ytm_auth_file": ytm_auth,
    }

    log = get_logger()
    try:
        # Validate service
        if service not in ["spotify", "ytm"]:
            log.error("--from must be 'spotify' or 'ytm'")
            sys.exit(1)

        # Create filter
        album_filter = None
        if include or exclude or patterns_from:
            try:
                if patterns_from:
                    album_filter = AlbumFilter.from_patterns_file(patterns_from)
                    log.info(f"Loaded filter from {patterns_from} with {len(album_filter)} patterns")
                else:
                    album_filter = AlbumFilter()
                    if include:
                        for pattern in include:
                            album_filter.add_pattern(pattern, FilterAction.INCLUDE)
                    if exclude:
                        for pattern in exclude:
                            album_filter.add_pattern(pattern, FilterAction.EXCLUDE)
                    log.info(f"Created filter with {len(album_filter)} patterns")

                if album_filter:
                    log.info(f"Filter summary: {album_filter.get_summary()}")
            except (ValueError, FileNotFoundError) as e:
                log.error(f"Error creating filter: {e}")
                sys.exit(1)

        # Require filter for standalone delete
        if not album_filter:
            log.error("Filter is required when using 'delete albums' command")
            log.error("Use --include, --exclude, or --patterns-from to specify which albums to delete")
            log.error("")
            log.error("Examples:")
            log.error("  pushtunes delete albums --from spotify --include=\"artist:'Volkor X'\"")
            log.error("  pushtunes delete albums --from spotify --exclude=\"album:'.*Live.*'\"")
            log.error("  pushtunes delete albums --from spotify --patterns-from=filters.txt")
            sys.exit(1)

        # Create service
        log.info(f"Initializing {service} service...")
        service_obj = create_service(service, config)

        # Get all albums from service (load cache which auto-refreshes if expired)
        log.info(f"Fetching all albums from {service}...")
        service_obj.cache.load_album_cache()
        all_albums = service_obj.cache.albums
        log.info(f"Found {len(all_albums)} albums in {service} library")

        # Apply filter to get albums to delete
        albums_to_delete = [a for a in all_albums if not album_filter.should_filter_out(a)]
        log.info(f"After applying filter: {len(albums_to_delete)} albums match deletion criteria")

        if not albums_to_delete:
            print("\nNo albums match the specified filter criteria.")
            print("Nothing to delete.")
            return

        # Use Deleter to handle the deletion
        deleter = Deleter[Album](
            items_to_delete=albums_to_delete,
            service=service_obj,
            item_type="album",
            backup_operation_name="filter_delete",
            require_confirmation=True,
            color=color,
        )

        results = deleter.delete()

        # Print statistics
        if results:
            print_delete_stats(results, "albums", use_color=color)

            # Exit with error if any deletions failed
            error_count = sum(1 for r in results if r.status == PushStatus.error)
            if error_count > 0:
                sys.exit(1)

    except KeyboardInterrupt:
        print("\nDeletion interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def delete_tracks(
    service: str = typer.Option(..., "--from", help="Service to delete from ('spotify' or 'ytm')"),
    verbose: bool = typer.Option(False, "-v", "--verbose", help="Enable verbose output"),
    log_level: str = typer.Option(
        "INFO",
        "--log-level",
        help="Console log level: DEBUG, INFO, WARNING, ERROR, CRITICAL (default: INFO)",
    ),
    ytm_auth: str = typer.Option(
        "browser.json",
        help="Path to YouTube Music authentication file (default: browser.json)",
    ),
    include: Optional[list[str]] = None,
    exclude: Optional[list[str]] = None,
    patterns_from: Optional[str] = None,
    color: bool = typer.Option(
        True,
        "--color/--no-color",
        help="Enable/disable colored output (default: enabled)",
    ),
):
    """
    Delete tracks from a music service based on filter criteria.

    This command requires a filter to specify which tracks to delete.
    It fetches all tracks from the service, applies the filter, shows a preview,
    creates a backup, and then deletes matching tracks after confirmation.

    Examples:
        # Delete all tracks by specific artist
        pushtunes delete tracks --from spotify --include="artist:'Volkor X'"

        # Delete all live tracks
        pushtunes delete tracks --from spotify --include="track:'.*Live.*'"

        # Use patterns file
        pushtunes delete tracks --from spotify --patterns-from=filters.txt
    """
    # Set console log level
    try:
        set_console_log_level(log_level)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Create configuration
    config = {
        "ytm_auth_file": ytm_auth,
    }

    log = get_logger()
    try:
        # Validate service
        if service not in ["spotify", "ytm"]:
            log.error("--from must be 'spotify' or 'ytm'")
            sys.exit(1)

        # Create filter
        track_filter = None
        if include or exclude or patterns_from:
            try:
                if patterns_from:
                    track_filter = TrackFilter.from_patterns_file(patterns_from)
                    log.info(f"Loaded filter from {patterns_from} with {len(track_filter)} patterns")
                else:
                    track_filter = TrackFilter()
                    if include:
                        for pattern in include:
                            track_filter.add_pattern(pattern, FilterAction.INCLUDE)
                    if exclude:
                        for pattern in exclude:
                            track_filter.add_pattern(pattern, FilterAction.EXCLUDE)
                    log.info(f"Created filter with {len(track_filter)} patterns")

                if track_filter:
                    log.info(f"Filter summary: {track_filter.get_summary()}")
            except (ValueError, FileNotFoundError) as e:
                log.error(f"Error creating filter: {e}")
                sys.exit(1)

        # Require filter for standalone delete
        if not track_filter:
            log.error("Filter is required when using 'delete tracks' command")
            log.error("Use --include, --exclude, or --patterns-from to specify which tracks to delete")
            log.error("")
            log.error("Examples:")
            log.error("  pushtunes delete tracks --from spotify --include=\"artist:'Volkor X'\"")
            log.error("  pushtunes delete tracks --from spotify --include=\"track:'.*Live.*'\"")
            log.error("  pushtunes delete tracks --from spotify --patterns-from=filters.txt")
            sys.exit(1)

        # Create service
        log.info(f"Initializing {service} service...")
        service_obj = create_service(service, config)

        # Get all tracks from service (load cache which auto-refreshes if expired)
        log.info(f"Fetching all tracks from {service}...")
        service_obj.cache.load_track_cache()
        all_tracks = service_obj.cache.tracks
        log.info(f"Found {len(all_tracks)} tracks in {service} library")

        # Apply filter to get tracks to delete
        tracks_to_delete = [t for t in all_tracks if not track_filter.should_filter_out(t)]
        log.info(f"After applying filter: {len(tracks_to_delete)} tracks match deletion criteria")

        if not tracks_to_delete:
            print("\nNo tracks match the specified filter criteria.")
            print("Nothing to delete.")
            return

        # Use Deleter to handle the deletion
        deleter = Deleter[Track](
            items_to_delete=tracks_to_delete,
            service=service_obj,
            item_type="track",
            backup_operation_name="filter_delete",
            require_confirmation=True,
            color=color,
        )

        results = deleter.delete()

        # Print statistics
        if results:
            print_delete_stats(results, "tracks", use_color=color)

            # Exit with error if any deletions failed
            error_count = sum(1 for r in results if r.status == PushStatus.error)
            if error_count > 0:
                sys.exit(1)

    except KeyboardInterrupt:
        print("\nDeletion interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)
