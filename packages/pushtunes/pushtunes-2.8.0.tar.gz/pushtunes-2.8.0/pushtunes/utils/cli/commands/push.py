"""Push commands for syncing albums, tracks, and playlists to music services."""

import os
import sys
from typing import Optional

import typer

from pushtunes.models.push_status import PushStatus
from pushtunes.services.pusher import Pusher, PushResult
from pushtunes.models.album import Album
from pushtunes.models.track import Track
from pushtunes.services.csv import CSVService
from pushtunes.utils.filters import AlbumFilter, TrackFilter, FilterAction
from pushtunes.utils.logging import get_logger, set_console_log_level
from pushtunes.utils.cli.commands.shared import create_source, create_service, print_stats
from pushtunes.services.playlist_pusher import (
    PlaylistPusher,
    PlaylistResult,
    ConflictMode,
    pretty_print_track_result,
)


def push_albums(
    source: Optional[str] = None,
    target: Optional[str] = None,
    similarity: float = typer.Option(
        0.8, help="Minimum similarity threshold for matching (0.0-1.0, default: 0.8)"
    ),
    verbose: bool = typer.Option(
        False, "-v", "--verbose", help="Enable verbose output"
    ),
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
    csv_file: Optional[str] = typer.Option(
        None, help="Filename of the CSV file to write to or read from"
    ),
    report: Optional[str] = typer.Option(
        None,
        help="Generate detailed report for specific statuses (comma-separated: not_found,filtered,similarity_too_low,already_in_library,added,deleted,error)",
    ),
    color: bool = typer.Option(
        True,
        "--color/--no-color",
        help="Enable/disable colored output (default: enabled)",
    ),
    mappings_file: Optional[str] = typer.Option(
        None,
        "--mappings-file",
        help="CSV file containing mappings for albums that can't be matched automatically",
    ),
    export_csv: Optional[str] = typer.Option(
        None,
        "--export-csv",
        help="Export results with specific statuses to CSV (comma-separated: not_found,filtered,similarity_too_low,already_in_library,already_in_library_cache,added,deleted,error)",
    ),
    export_csv_file: Optional[str] = typer.Option(
        None,
        "--export-csv-file",
        help="Filename for the exported CSV file (default: albums_export_<statuses>.csv)",
    ),
    delete: bool = typer.Option(
        False,
        "--delete",
        help="Delete albums from target that are not present in source (with confirmation and backup)",
    ),
    profile: Optional[str] = None,
):
    """
    Push albums from a source to a target service.
    """
    # Load profile if specified
    if profile:
        from pushtunes.utils.profile_manager import load_profile, merge_with_cli_args

        try:
            profile_config = load_profile(profile, "albums")
            # Build dict of CLI arguments
            cli_args = {
                "from": source,
                "to": target,
                "similarity": similarity,
                "verbose": verbose,
                "log-level": log_level,
                "ytm-auth": ytm_auth,
                "include": include,
                "exclude": exclude,
                "patterns-from": patterns_from,
                "csv-file": csv_file,
                "report": report,
                "color": color,
                "mappings-file": mappings_file,
                "export-csv": export_csv,
                "export-csv-file": export_csv_file,
                "delete": delete,
            }
            # Merge profile with CLI args (CLI takes precedence)
            merged = merge_with_cli_args(profile_config, cli_args)

            # Apply merged values (use profile values if CLI value is default/None)
            source = merged.get("from", source)
            target = merged.get("to", target)
            similarity = merged.get("similarity", similarity)
            verbose = merged.get("verbose", verbose)
            log_level = merged.get("log-level", log_level)
            ytm_auth = merged.get("ytm-auth", ytm_auth)
            include = merged.get("include", include)
            exclude = merged.get("exclude", exclude)
            patterns_from = merged.get("patterns-from", patterns_from)
            csv_file = merged.get("csv-file", csv_file)
            report = merged.get("report", report)
            color = merged.get("color", color)
            mappings_file = merged.get("mappings-file", mappings_file)
            export_csv = merged.get("export-csv", export_csv)
            export_csv_file = merged.get("export-csv-file", export_csv_file)
            delete = merged.get("delete", delete)
        except (FileNotFoundError, ValueError) as e:
            print(f"Error loading profile: {e}")
            sys.exit(1)

    # Validate that source and target are provided
    if source is None:
        print("Error: --from is required (either via command line or profile)")
        sys.exit(1)
    if target is None:
        print("Error: --to is required (either via command line or profile)")
        sys.exit(1)

    # Set console log level
    try:
        set_console_log_level(log_level)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Create configuration
    config = {
        "similarity": similarity,
        "ytm_auth_file": ytm_auth,
        "csv_file": csv_file,
    }

    log = get_logger()
    try:
        album_filter = None
        # Handle filter options
        if include or exclude or patterns_from:
            try:
                from pushtunes.utils.filters import FilterAction

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

        # Create source and target services
        log.info(f"Initializing {source} source...")
        source_obj = create_source(source, config)

        log.info(f"Initializing {target} service...")
        service = create_service(target, config)

        # Get albums from source (invalidate cache first if using --delete)
        if delete:
            log.info("Invalidating source cache for fresh comparison...")
            source_obj.cache.invalidate_album_cache()
        albums = source_obj.get_albums()

        # If target is CSV, write directly to file (no matching needed)
        if target == "csv" and isinstance(service, CSVService):
            log.info(f"Exporting {len(albums)} albums to CSV file {csv_file}...")

            # Apply filter if present
            if album_filter:
                filtered_albums = [a for a in albums if not album_filter.should_filter_out(a)]
                log.info(f"After filtering: {len(filtered_albums)} albums")
                albums = filtered_albums

            from pushtunes.utils.csv_manager import CsvManager

            CsvManager.export_albums(albums, csv_file)
            print(f"\nSuccessfully exported {len(albums)} albums to {csv_file}")
            return

        # Perform sync
        log.info(f"Starting albums sync from {source} to {target}...")

        # Load mappings if provided
        mappings = None
        if mappings_file:
            from pushtunes.services.mappings_manager import MappingsManager

            mappings = MappingsManager(mappings_file)

        pusher = Pusher[Album](
            items=albums,
            service=service,
            item_type="album",
            filter=album_filter,
            min_similarity=similarity,
            mappings=mappings,
        )
        results: list[PushResult[Album]] = pusher.push()

        stats = {
            "total": len(results),
            "added": sum(1 for r in results if r.status == PushStatus.added),
            "mapped": sum(1 for r in results if r.status == PushStatus.mapped),
            "skipped_existing": sum(
                1 for r in results if r.status == PushStatus.already_in_library
            ),
            "skipped_not_found": sum(
                1 for r in results if r.status == PushStatus.not_found
            ),
            "skipped_low_similarity": sum(
                1 for r in results if r.status == PushStatus.similarity_too_low
            ),
            "skipped_filtered": sum(
                1 for r in results if r.status == PushStatus.filtered
            ),
            "errors": sum(1 for r in results if r.status == PushStatus.error),
            "deleted": 0,
        }

        print_stats(stats, "albums")

        # Handle deletion if requested
        if delete:
            if target == "csv":
                log.error("--delete option is not supported when target is CSV")
                sys.exit(1)

            log.info("Processing deletion of albums not present in source...")

            from pushtunes.utils.deletion_manager import DeletionManager
            from pushtunes.utils.deletion_confirm import (
                display_deletion_preview,
                confirm_deletion,
            )

            # Initialize deletion manager
            deletion_manager = DeletionManager()

            # Get target library from cache (already fresh from the push operation)
            log.info("Getting target library from cache...")
            target_albums = service.cache.albums
            log.info(f"Found {len(target_albums)} albums in target library")

            # Apply filter to source albums for deletion comparison
            # Filters should be applied BEFORE mappings during deletion
            filtered_source_albums = albums
            if album_filter:
                filtered_source_albums = [a for a in albums if not album_filter.should_filter_out(a)]
                log.info(f"After filtering: {len(filtered_source_albums)} albums will be considered from source (out of {len(albums)} total)")
                log.info(f"Filtered out {len(albums) - len(filtered_source_albums)} albums - these will be completely ignored for deletion matching")

            # Generate deletion preview
            log.info("Analyzing which albums would be deleted...")
            preview = deletion_manager.generate_deletion_preview(
                target_items=target_albums,
                source_items=filtered_source_albums,
                min_similarity=similarity,
                mappings=mappings,
                service_name=target,
            )

            # Display preview
            display_deletion_preview(preview, "albums", similarity, color)

            # If there are items to delete, use Deleter to handle backup, confirmation, and deletion
            if preview.items_to_delete:
                from pushtunes.services.deleter import Deleter

                albums_to_delete = [c.item for c in preview.items_to_delete]

                deleter = Deleter[Album](
                    items_to_delete=albums_to_delete,
                    service=service,
                    item_type="album",
                    backup_operation_name="deletion",
                    require_confirmation=True,
                    color=color,
                )

                deletion_results = deleter.delete()

                if deletion_results:
                    # Update stats
                    stats["deleted"] = sum(
                        1 for r in deletion_results if r.status == PushStatus.deleted
                    )
                    stats["errors"] += sum(
                        1 for r in deletion_results if r.status == PushStatus.error
                    )

                    # Add deletion results to main results
                    results.extend(deletion_results)

                    print(f"\nDeleted {stats['deleted']} albums from target library")
            else:
                print("\nNo albums to delete. Target library is in sync with source.")

        # Generate detailed report if requested
        if report:
            from pushtunes.utils.reporting import generate_report

            report_statuses = [s.strip() for s in report.split(",")]
            generate_report(
                results, report_statuses, result_type="album", use_color=color
            )

        # Export results to CSV if requested
        if export_csv:
            export_statuses = [s.strip() for s in export_csv.split(",")]

            # Check if user wants mappings file format
            if "mappings-file" in export_statuses:
                from pushtunes.utils.csv_manager import CsvManager

                # Generate default filename if not provided
                if not export_csv_file:
                    export_filename = "albums_mappings_template.csv"
                else:
                    export_filename = os.path.expanduser(export_csv_file)

                # Export not_found and similarity_too_low items in mappings format
                new_count, unmapped_count = CsvManager.export_album_results_to_mappings(
                    results, ["not_found", "similarity_too_low"], export_filename
                )

                if new_count > 0 or unmapped_count > 0:
                    if new_count > 0:
                        print(
                            f"\nExported {new_count} NEW albums to mappings template: {export_filename}"
                        )
                    if unmapped_count > 0:
                        print(
                            f"  {unmapped_count} failed albums already in {export_filename} with empty target fields"
                        )
                        print(
                            f"  These items are still failing - fill in their target fields to fix them"
                        )
                    if new_count > 0:
                        print(
                            f"  Fill in the target fields and use with --mappings-file={export_filename}"
                        )
                else:
                    print(
                        f"\nNo albums with status 'not_found' or 'similarity_too_low' to export"
                    )
            else:
                from pushtunes.utils.csv_manager import CsvManager

                # Generate default filename if not provided
                if not export_csv_file:
                    statuses_str = "_".join(export_statuses)
                    export_filename = f"albums_export_{statuses_str}.csv"
                else:
                    export_filename = os.path.expanduser(export_csv_file)

                exported_count = CsvManager.export_album_results(
                    results, export_statuses, export_filename
                )
                if exported_count > 0:
                    print(f"\nExported {exported_count} albums to {export_filename}")
                else:
                    print(f"\nNo albums matched the specified statuses for export")

        # Exit with appropriate code
        if stats["errors"] > 0:
            print("\nWarning: Some errors occurred during sync")
            sys.exit(1)
        else:
            print("\nSync completed successfully")

    except KeyboardInterrupt:
        print("\nSync interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        if verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


from pushtunes.services.playlist_pusher import (
    PlaylistPusher,
    PlaylistResult,
    ConflictMode,
    pretty_print_track_result,
)


def push_tracks(
    source: Optional[str] = None,
    target: Optional[str] = None,
    similarity: float = typer.Option(
        0.8, help="Minimum similarity threshold for matching (0.0-1.0, default: 0.8)"
    ),
    verbose: bool = typer.Option(
        False, "-v", "--verbose", help="Enable verbose output"
    ),
    log_level: str = typer.Option(
        "INFO",
        "--log-level",
        help="Console log level: DEBUG, INFO, WARNING, ERROR, CRITICAL (default: INFO)",
    ),
    include: Optional[list[str]] = None,
    exclude: Optional[list[str]] = None,
    patterns_from: Optional[str] = None,
    csv_file: Optional[str] = typer.Option(
        None, help="Filename of the CSV file to write to or read from"
    ),
    report: Optional[str] = typer.Option(
        None,
        help="Generate detailed report for specific statuses (comma-separated: not_found,filtered,similarity_too_low,already_in_library,added,deleted,error)",
    ),
    color: bool = typer.Option(
        True,
        "--color/--no-color",
        help="Enable/disable colored output (default: enabled)",
    ),
    mappings_file: Optional[str] = typer.Option(
        None,
        "--mappings-file",
        help="CSV file containing mappings for tracks that can't be matched automatically",
    ),
    export_csv: Optional[str] = typer.Option(
        None,
        "--export-csv",
        help="Export results with specific statuses to CSV (comma-separated: not_found,filtered,similarity_too_low,already_in_library,already_in_library_cache,added,deleted,error)",
    ),
    export_csv_file: Optional[str] = typer.Option(
        None,
        "--export-csv-file",
        help="Filename for the exported CSV file (default: tracks_export_<statuses>.csv)",
    ),
    delete: bool = typer.Option(
        False,
        "--delete",
        help="Delete tracks from target that are not present in source (with confirmation and backup)",
    ),
    profile: Optional[str] = None,
):
    """
    Push tracks from a source to a target service.
    """
    # Load profile if specified
    if profile:
        from pushtunes.utils.profile_manager import load_profile, merge_with_cli_args

        try:
            profile_config = load_profile(profile, "tracks")
            # Build dict of CLI arguments
            cli_args = {
                "from": source,
                "to": target,
                "similarity": similarity,
                "verbose": verbose,
                "log-level": log_level,
                "include": include,
                "exclude": exclude,
                "patterns-from": patterns_from,
                "csv-file": csv_file,
                "report": report,
                "color": color,
                "mappings-file": mappings_file,
                "export-csv": export_csv,
                "export-csv-file": export_csv_file,
                "delete": delete,
            }
            # Merge profile with CLI args (CLI takes precedence)
            merged = merge_with_cli_args(profile_config, cli_args)

            # Apply merged values (use profile values if CLI value is default/None)
            source = merged.get("from", source)
            target = merged.get("to", target)
            similarity = merged.get("similarity", similarity)
            verbose = merged.get("verbose", verbose)
            log_level = merged.get("log-level", log_level)
            include = merged.get("include", include)
            exclude = merged.get("exclude", exclude)
            patterns_from = merged.get("patterns-from", patterns_from)
            csv_file = merged.get("csv-file", csv_file)
            report = merged.get("report", report)
            color = merged.get("color", color)
            mappings_file = merged.get("mappings-file", mappings_file)
            export_csv = merged.get("export-csv", export_csv)
            export_csv_file = merged.get("export-csv-file", export_csv_file)
            delete = merged.get("delete", delete)
        except (FileNotFoundError, ValueError) as e:
            print(f"Error loading profile: {e}")
            sys.exit(1)

    # Validate that source and target are provided
    if source is None:
        print("Error: --from is required (either via command line or profile)")
        sys.exit(1)
    if target is None:
        print("Error: --to is required (either via command line or profile)")
        sys.exit(1)

    # Set console log level
    try:
        set_console_log_level(log_level)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Create configuration
    config = {
        "similarity": similarity,
        "csv_file": csv_file,
    }

    log = get_logger()
    try:
        track_filter = None
        # Handle filter options
        if include or exclude or patterns_from:
            try:
                from pushtunes.utils.filters import FilterAction

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

        # Create source and target services
        log.info(f"Initializing {source} source...")
        source_obj = create_source(source, config)

        log.info(f"Initializing {target} service...")
        service = create_service(target, config)

        # Get tracks from source (invalidate cache first if using --delete)
        if delete:
            log.info("Invalidating source cache for fresh comparison...")
            source_obj.cache.invalidate_track_cache()
        tracks = source_obj.get_tracks()

        # If target is CSV, write directly to file (no matching needed)
        if target == "csv" and isinstance(service, CSVService):
            log.info(f"Exporting {len(tracks)} tracks to CSV file {csv_file}...")

            # Apply filter if present
            if track_filter:
                filtered_tracks = [t for t in tracks if not track_filter.should_filter_out(t)]
                log.info(f"After filtering: {len(filtered_tracks)} tracks")
                tracks = filtered_tracks

            from pushtunes.utils.csv_manager import CsvManager

            CsvManager.export_tracks(tracks, csv_file)
            print(f"\nSuccessfully exported {len(tracks)} tracks to {csv_file}")
            return

        # Perform sync
        log.info(f"Starting tracks sync from {source} to {target}...")

        # Load mappings if provided
        mappings = None
        if mappings_file:
            from pushtunes.services.mappings_manager import MappingsManager

            mappings = MappingsManager(mappings_file)

        pusher = Pusher[Track](
            items=tracks,
            service=service,
            item_type="track",
            filter=track_filter,
            min_similarity=similarity,
            mappings=mappings,
        )
        results: list[PushResult[Track]] = pusher.push()

        stats = {
            "total": len(results),
            "added": sum(1 for r in results if r.status == PushStatus.added),
            "mapped": sum(1 for r in results if r.status == PushStatus.mapped),
            "skipped_existing": sum(
                1 for r in results if r.status == PushStatus.already_in_library
            ),
            "skipped_not_found": sum(
                1 for r in results if r.status == PushStatus.not_found
            ),
            "skipped_low_similarity": sum(
                1 for r in results if r.status == PushStatus.similarity_too_low
            ),
            "skipped_filtered": sum(
                1 for r in results if r.status == PushStatus.filtered
            ),
            "errors": sum(1 for r in results if r.status == PushStatus.error),
            "deleted": 0,
        }

        print_stats(stats, "tracks")

        # Handle deletion if requested
        if delete:
            if target == "csv":
                log.error("--delete option is not supported when target is CSV")
                sys.exit(1)

            log.info("Processing deletion of tracks not present in source...")

            from pushtunes.utils.deletion_manager import DeletionManager
            from pushtunes.utils.deletion_confirm import (
                display_deletion_preview,
                confirm_deletion,
            )

            # Initialize deletion manager
            deletion_manager = DeletionManager()

            # Get target library from cache (already fresh from the push operation)
            log.info("Getting target library from cache...")
            target_tracks = service.cache.tracks
            log.info(f"Found {len(target_tracks)} tracks in target library")

            # Apply filter to source tracks for deletion comparison
            # Filters should be applied BEFORE mappings during deletion
            filtered_source_tracks = tracks
            if track_filter:
                filtered_source_tracks = [t for t in tracks if not track_filter.should_filter_out(t)]
                log.info(f"After filtering: {len(filtered_source_tracks)} tracks will be considered from source (out of {len(tracks)} total)")
                log.info(f"Filtered out {len(tracks) - len(filtered_source_tracks)} tracks - these will be completely ignored for deletion matching")

            # Generate deletion preview
            log.info("Analyzing which tracks would be deleted...")
            preview = deletion_manager.generate_deletion_preview(
                target_items=target_tracks,
                source_items=filtered_source_tracks,
                min_similarity=similarity,
                mappings=mappings,
                service_name=target,
            )

            # Display preview
            display_deletion_preview(preview, "tracks", similarity, color)

            # If there are items to delete, use Deleter to handle backup, confirmation, and deletion
            if preview.items_to_delete:
                from pushtunes.services.deleter import Deleter

                tracks_to_delete = [c.item for c in preview.items_to_delete]

                deleter = Deleter[Track](
                    items_to_delete=tracks_to_delete,
                    service=service,
                    item_type="track",
                    backup_operation_name="deletion",
                    require_confirmation=True,
                    color=color,
                )

                deletion_results = deleter.delete()

                if deletion_results:
                    # Update stats
                    stats["deleted"] = sum(
                        1 for r in deletion_results if r.status == PushStatus.deleted
                    )
                    stats["errors"] += sum(
                        1 for r in deletion_results if r.status == PushStatus.error
                    )

                    # Add deletion results to main results
                    results.extend(deletion_results)

                    print(f"\nDeleted {stats['deleted']} tracks from target library")
            else:
                print("\nNo tracks to delete. Target library is in sync with source.")

        # Generate detailed report if requested
        if report:
            from pushtunes.utils.reporting import generate_report

            report_statuses = [s.strip() for s in report.split(",")]
            generate_report(
                results, report_statuses, result_type="track", use_color=color
            )

        # Export results to CSV if requested
        if export_csv:
            export_statuses = [s.strip() for s in export_csv.split(",")]

            # Check if user wants mappings file format
            if "mappings-file" in export_statuses:
                from pushtunes.utils.csv_manager import CsvManager

                # Generate default filename if not provided
                if not export_csv_file:
                    export_filename = "tracks_mappings_template.csv"
                else:
                    export_filename = os.path.expanduser(export_csv_file)

                # Export not_found and similarity_too_low items in mappings format
                new_count, unmapped_count = CsvManager.export_track_results_to_mappings(
                    results, ["not_found", "similarity_too_low"], export_filename
                )

                if new_count > 0 or unmapped_count > 0:
                    if new_count > 0:
                        print(
                            f"\nExported {new_count} NEW tracks to mappings template: {export_filename}"
                        )
                        print(
                            f"  Fill in the target fields and use with --mappings-file={export_filename}"
                        )
                    if unmapped_count > 0:
                        print(
                            f"  {unmapped_count} failed tracks already in {export_filename} with empty target fields"
                        )
                        print(
                            f"  These items are still failing - fill in their target fields to fix them"
                        )
                else:
                    print(
                        f"\nNo tracks with status 'not_found' or 'similarity_too_low' to export"
                    )
            else:
                from pushtunes.utils.csv_manager import CsvManager

                # Generate default filename if not provided
                if not export_csv_file:
                    statuses_str = "_".join(export_statuses)
                    export_filename = f"tracks_export_{statuses_str}.csv"
                else:
                    export_filename = os.path.expanduser(export_csv_file)

                exported_count = CsvManager.export_track_results(
                    results, export_statuses, export_filename
                )
                if exported_count > 0:
                    print(f"\nExported {exported_count} tracks to {export_filename}")
                else:
                    print(f"\nNo tracks matched the specified statuses for export")

        # Exit with appropriate code
        if stats["errors"] > 0:
            print("\nWarning: Some errors occurred during sync")
            sys.exit(1)
        else:
            print("\nSync completed successfully")

    except KeyboardInterrupt:
        print("\nSync interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        if verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


def push_playlist(
    source: Optional[str] = None,
    target: Optional[str] = None,
    playlist_name: Optional[str] = typer.Option(
        None, "--playlist-name", help="Name of the playlist to push (required)"
    ),
    source_playlist_id: Optional[str] = typer.Option(
        None,
        "--source-playlist-id",
        help="ID of source playlist (Spotify/YTM only, for direct lookup)",
    ),
    playlist_id: Optional[str] = typer.Option(
        None,
        "--playlist-id",
        help="ID of existing playlist on target (Spotify/Jellyfin, for conflict resolution)",
    ),
    similarity: float = typer.Option(
        0.8,
        help="Minimum similarity threshold for matching tracks (0.0-1.0, default: 0.8)",
    ),
    require_all_tracks: bool = typer.Option(
        False,
        "--require-all-tracks",
        help="Require all tracks to match (fail if any track can't be matched)",
    ),
    verbose: bool = typer.Option(
        False, "-v", "--verbose", help="Enable verbose output"
    ),
    log_level: str = typer.Option(
        "INFO",
        "--log-level",
        help="Console log level: DEBUG, INFO, WARNING, ERROR, CRITICAL (default: INFO)",
    ),
    ytm_auth: str = typer.Option(
        "browser.json", help="Path to YouTube Music authentication file"
    ),
    csv_file: Optional[str] = typer.Option(
        None, help="Filename of the CSV file to write to or read from"
    ),
    report: Optional[str] = typer.Option(
        None,
        help="Generate detailed report for specific statuses (comma-separated: not_found,matched,similarity_too_low)",
    ),
    color: bool = typer.Option(
        True,
        "--color/--no-color",
        help="Enable/disable colored output (default: enabled)",
    ),
    on_conflict: str = typer.Option(
        "abort",
        "--on-conflict",
        help="How to handle conflicts: 'abort' (show differences), 'replace' (replace entire playlist), 'append' (add missing tracks), 'sync' (add missing, remove extras)",
    ),
    mappings_file: Optional[str] = typer.Option(
        None,
        "--mappings-file",
        help="CSV file containing mappings for tracks that can't be matched automatically",
    ),
    profile: Optional[str] = None,
):
    """
    Push a playlist from a source to a target service, preserving track order.
    """
    # Load profile if specified
    if profile:
        from pushtunes.utils.profile_manager import load_profile, merge_with_cli_args

        try:
            profile_config = load_profile(profile, "playlist")
            # Build dict of CLI arguments
            cli_args = {
                "from": source,
                "to": target,
                "playlist-name": playlist_name,
                "source-playlist-id": source_playlist_id,
                "playlist-id": playlist_id,
                "similarity": similarity,
                "require-all-tracks": require_all_tracks,
                "verbose": verbose,
                "log-level": log_level,
                "ytm-auth": ytm_auth,
                "csv-file": csv_file,
                "report": report,
                "color": color,
                "on-conflict": on_conflict,
                "mappings-file": mappings_file,
            }
            # Merge profile with CLI args (CLI takes precedence)
            merged = merge_with_cli_args(profile_config, cli_args)

            # Apply merged values (use profile values if CLI value is default/None)
            source = merged.get("from", source)
            target = merged.get("to", target)
            playlist_name = merged.get("playlist-name", playlist_name)
            source_playlist_id = merged.get("source-playlist-id", source_playlist_id)
            playlist_id = merged.get("playlist-id", playlist_id)
            similarity = merged.get("similarity", similarity)
            require_all_tracks = merged.get("require-all-tracks", require_all_tracks)
            verbose = merged.get("verbose", verbose)
            log_level = merged.get("log-level", log_level)
            ytm_auth = merged.get("ytm-auth", ytm_auth)
            csv_file = merged.get("csv-file", csv_file)
            report = merged.get("report", report)
            color = merged.get("color", color)
            on_conflict = merged.get("on-conflict", on_conflict)
            mappings_file = merged.get("mappings-file", mappings_file)
        except (FileNotFoundError, ValueError) as e:
            print(f"Error loading profile: {e}")
            sys.exit(1)

    # Validate that source and target are provided
    if source is None:
        print("Error: --from is required (either via command line or profile)")
        sys.exit(1)
    if target is None:
        print("Error: --to is required (either via command line or profile)")
        sys.exit(1)

    # Set console log level
    try:
        set_console_log_level(log_level)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Create configuration
    config = {
        "similarity": similarity,
        "ytm_auth_file": ytm_auth,
        "csv_file": csv_file,
    }

    log = get_logger()
    try:
        # Validate inputs based on source service
        if source in ("spotify", "jellyfin"):
            # Spotify and Jellyfin require playlist ID because multiple playlists can have the same name
            if not source_playlist_id:
                print(f"Error: --source-playlist-id is required when using --from {source}")
                print(f"  ({source.capitalize()} allows duplicate playlist names, so ID is needed for precision)")
                sys.exit(1)
            # playlist_name is still used for display/target naming, but default to "Playlist" if not provided
            if not playlist_name:
                playlist_name = "Playlist"
        else:
            # Other sources require playlist name
            if not playlist_name:
                print("Error: --playlist-name is required")
                sys.exit(1)

        # Parse conflict mode
        try:
            conflict_mode = ConflictMode[on_conflict]
        except KeyError:
            print(
                f"Error: Invalid conflict mode '{on_conflict}'. Valid options: abort, replace, append, sync"
            )
            sys.exit(1)

        # Create source and target services
        log.info(f"Initializing {source} source...")
        source_obj = create_source(source, config)

        log.info(f"Initializing {target} service...")
        service = create_service(target, config)

        # Get playlist from source
        log.info(f"Fetching playlist '{playlist_name}' from {source}...")
        playlist = source_obj.get_playlist(
            playlist_name, playlist_id=source_playlist_id
        )

        if not playlist:
            print(f"Error: Playlist '{playlist_name}' not found on {source}")
            sys.exit(1)

        # If target is CSV, write directly to file (no matching needed)
        if target == "csv" and isinstance(service, CSVService):
            log.info(
                f"Exporting playlist '{playlist.name}' with {len(playlist.tracks)} tracks to CSV file {csv_file}..."
            )
            from pushtunes.utils.csv_manager import CsvManager

            CsvManager.export_playlist(playlist, csv_file)
            print(
                f"\nSuccessfully exported playlist '{playlist.name}' with {len(playlist.tracks)} tracks to {csv_file}"
            )
            return

        # Push playlist to target
        log.info(f"Pushing playlist '{playlist.name}' to {target}...")

        # Load mappings if provided
        mappings = None
        if mappings_file:
            from pushtunes.services.mappings_manager import MappingsManager

            mappings = MappingsManager(mappings_file)

        pusher = PlaylistPusher(
            playlist=playlist,
            service=service,
            min_similarity=similarity,
            conflict_mode=conflict_mode,
            target_playlist_id=playlist_id,  # Pass the specific ID if provided
            mappings=mappings,
            require_all_tracks=require_all_tracks,
        )
        result: PlaylistResult = pusher.push_playlist()

        # Print detailed results
        print(f"\n{'=' * 60}")
        print(f"Playlist: {playlist.name}")
        print(f"{'=' * 60}")

        # Count statuses
        stats = {
            "total": len(result.track_results),
            "matched": sum(
                1 for r in result.track_results if r.status == PushStatus.matched
            ),
            "not_found": sum(
                1 for r in result.track_results if r.status == PushStatus.not_found
            ),
            "similarity_too_low": sum(
                1
                for r in result.track_results
                if r.status == PushStatus.similarity_too_low
            ),
        }

        print(f"\nTrack Matching Results:")
        print(f"  Total tracks:          {stats['total']}")
        print(f"  Successfully matched:  {stats['matched']}")
        print(f"  Not found:             {stats['not_found']}")
        print(f"  Similarity too low:    {stats['similarity_too_low']}")

        # Show failed matches if verbose
        if verbose:
            print("\nDetailed track results:")
            for track_result in result.track_results:
                print(f"  {pretty_print_track_result(track_result)}")

        # Show conflict information if present
        if result.conflict:
            print(f"\nPlaylist Conflict:")
            print(f"  Existing tracks:   {result.conflict.existing_track_count}")
            print(f"  Source tracks:     {result.conflict.source_track_count}")
            print(f"  Tracks in common:  {len(result.conflict.tracks_in_common)}")
            print(f"  Tracks to add:     {len(result.conflict.tracks_to_add)}")
            print(f"  Tracks to remove:  {len(result.conflict.tracks_to_remove)}")

            if verbose and result.conflict.tracks_to_add:
                print("\nTracks to add:")
                for track in result.conflict.tracks_to_add:
                    print(f"  + {track.artist} - {track.title}")

            if verbose and result.conflict.tracks_to_remove:
                print("\nTracks to remove:")
                for track in result.conflict.tracks_to_remove:
                    print(f"  - {track.artist} - {track.title}")

        # Generate detailed report if requested
        if report:
            from pushtunes.utils.reporting import generate_report

            report_statuses = [s.strip() for s in report.split(",")]
            generate_report(
                result.track_results,
                report_statuses,
                result_type="playlist",
                use_color=color,
            )

        # Show final status
        print(f"\n{'=' * 60}")
        if result.success:
            if result.conflict:
                print(f"{result.message}")
            else:
                print(f"Successfully created playlist on {target}")
            print(f"  Playlist ID: {result.playlist_id}")
            print(f"  Tracks: {stats['matched']}/{stats['total']}")
        else:
            print(f"Error: {result.message}")
            if result.conflict and conflict_mode == ConflictMode.abort:
                print(f"\nTo resolve this conflict, use one of:")
                print(f"  --on-conflict=replace  # Replace entire playlist")
                print(f"  --on-conflict=append    # Add missing tracks only")
                print(f"  --on-conflict=sync     # Add missing, remove extras")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\nPlaylist push interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        if verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


# ============================================================================
# Compare Commands
# ============================================================================


