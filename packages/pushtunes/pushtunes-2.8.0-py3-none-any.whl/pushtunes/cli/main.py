import typer
from typing_extensions import Annotated

from pushtunes.utils.cli.commands import push_albums, push_tracks, push_playlist
from pushtunes.utils.cli.commands import (
    compare_albums,
    compare_tracks,
    compare_playlist,
)
from pushtunes.utils.cli.commands import delete_albums, delete_tracks
from pushtunes.utils.cache_manager import list_all_caches, invalidate_cache_by_pattern

app = typer.Typer()
push_app = typer.Typer()
compare_app = typer.Typer()
delete_app = typer.Typer()
cache_app = typer.Typer()

app.add_typer(push_app, name="push")
app.add_typer(compare_app, name="compare")
app.add_typer(delete_app, name="delete")
app.add_typer(cache_app, name="cache")


@push_app.command("albums")
def push_albums_command(
    source: Annotated[
        str | None,
        typer.Option(
            "-f", "--from", help="Source ('subsonic', 'jellyfin', 'spotify', 'ytm', 'tidal' or 'csv')"
        ),
    ] = None,
    target: Annotated[
        str | None, typer.Option("-t", "--to", help="Target ('spotify', 'ytm', 'tidal' or 'csv')")
    ] = None,
    similarity: Annotated[
        float,
        typer.Option("-s", "--similarity", help="Minimum similarity threshold for matching (0.0-1.0)"),
    ] = 0.8,
    verbose: Annotated[
        bool, typer.Option("-v", "--verbose", help="Enable verbose output")
    ] = False,
    log_level: Annotated[
        str,
        typer.Option(
            "--log-level",
            help="Console log level: DEBUG, INFO, WARNING, ERROR, CRITICAL",
        ),
    ] = "INFO",
    ytm_auth: Annotated[
        str,
        typer.Option(help="Path to YouTube Music authentication file"),
    ] = "browser.json",
    include: Annotated[
        list[str] | None,
        typer.Option(
            "-i", "--include",
            help="Include pattern (can be specified multiple times). Use AND logic within pattern: \"artist:'Taylor Swift' album:'1989'\"",
        ),
    ] = None,
    exclude: Annotated[
        list[str] | None,
        typer.Option(
            "-e", "--exclude",
            help="Exclude pattern (can be specified multiple times). Use AND logic within pattern: \"artist:'Opeth' album:'Still Life'\"",
        ),
    ] = None,
    patterns_from: Annotated[
        str | None,
        typer.Option(
            "-p", "--patterns-from",
            help="File with +/- prefixed patterns (e.g., '+ artist:Taylor' or '- artist:Opeth album:Still'). Rules processed sequentially.",
        ),
    ] = None,
    csv_file: Annotated[
        str | None,
        typer.Option("-c", "--csv-file", help="Filename of the CSV file to write to or read from"),
    ] = None,
    report: Annotated[
        str | None,
        typer.Option(
            "--report",
            help="Generate detailed report for specific statuses (comma-separated: not_found,filtered,similarity_too_low,already_in_library,added,deleted,error)",
        ),
    ] = None,
    color: Annotated[
        bool,
        typer.Option(
            "--color/--no-color",
            help="Enable/disable colored output (default: enabled)",
        ),
    ] = True,
    mappings_file: Annotated[
        str | None,
        typer.Option(
            "-m", "--mappings-file",
            help="CSV file containing mappings for items that can't be matched automatically",
        ),
    ] = None,
    export_csv: Annotated[
        str | None,
        typer.Option(
            "--export-csv",
            help="Export results with specific statuses to CSV (comma-separated: not_found,filtered,similarity_too_low,already_in_library,added,deleted,error)",
        ),
    ] = None,
    export_csv_file: Annotated[
        str | None,
        typer.Option(
            "-C", "--export-csv-file",
            help="Filename for the exported CSV file (default: albums_export_<statuses>.csv)",
        ),
    ] = None,
    delete: Annotated[
        bool,
        typer.Option(
            "--delete",
            help="Delete albums from target that are not present in source (with confirmation and backup)",
        ),
    ] = False,
    profile: Annotated[
        str | None,
        typer.Option(
            "-P", "--profile",
            help="Load configuration from profile file (YAML, JSON, or TOML)",
        ),
    ] = None,
):
    """
    Push albums from a source to a target service.
    """
    push_albums(
        source=source,
        target=target,
        similarity=similarity,
        verbose=verbose,
        log_level=log_level,
        ytm_auth=ytm_auth,
        include=include,
        exclude=exclude,
        patterns_from=patterns_from,
        csv_file=csv_file,
        report=report,
        color=color,
        mappings_file=mappings_file,
        export_csv=export_csv,
        export_csv_file=export_csv_file,
        delete=delete,
        profile=profile,
    )


@push_app.command("tracks")
def push_tracks_command(
    source: Annotated[
        str | None, typer.Option("-f", "--from", help="Source ('subsonic', 'jellyfin', or 'csv')")
    ] = None,
    target: Annotated[str | None, typer.Option("-t", "--to", help="Target ('spotify', 'tidal' or 'csv')")] = None,
    similarity: Annotated[
        float,
        typer.Option("-s", "--similarity", help="Minimum similarity threshold for matching (0.0-1.0)"),
    ] = 0.8,
    verbose: Annotated[
        bool, typer.Option("-v", "--verbose", help="Enable verbose output")
    ] = False,
    log_level: Annotated[
        str,
        typer.Option(
            "--log-level",
            help="Console log level: DEBUG, INFO, WARNING, ERROR, CRITICAL",
        ),
    ] = "INFO",
    include: Annotated[
        list[str] | None,
        typer.Option(
            "-i", "--include",
            help="Include pattern (can be specified multiple times). Use AND logic within pattern: \"artist:'Taylor Swift' track:'Shake It Off'\"",
        ),
    ] = None,
    exclude: Annotated[
        list[str] | None,
        typer.Option(
            "-e", "--exclude",
            help="Exclude pattern (can be specified multiple times). Use AND logic within pattern: \"artist:'Opeth' track:'Deliverance'\"",
        ),
    ] = None,
    patterns_from: Annotated[
        str | None,
        typer.Option(
            "-p", "--patterns-from",
            help="File with +/- prefixed patterns (e.g., '+ artist:Taylor' or '- artist:Opeth track:Deliverance'). Rules processed sequentially.",
        ),
    ] = None,
    csv_file: Annotated[
        str | None,
        typer.Option("-c", "--csv-file", help="Filename of the CSV file to write to or read from"),
    ] = None,
    report: Annotated[
        str | None,
        typer.Option(
            "--report",
            help="Generate detailed report for specific statuses (comma-separated: not_found,filtered,similarity_too_low,already_in_library,added,deleted,error)",
        ),
    ] = None,
    color: Annotated[
        bool,
        typer.Option(
            "--color/--no-color",
            help="Enable/disable colored output (default: enabled)",
        ),
    ] = True,
    mappings_file: Annotated[
        str | None,
        typer.Option(
            "-m", "--mappings-file",
            help="CSV file containing mappings for tracks that can't be matched automatically",
        ),
    ] = None,
    export_csv: Annotated[
        str | None,
        typer.Option(
            "--export-csv",
            help="Export results with specific statuses to CSV (comma-separated: not_found,filtered,similarity_too_low,already_in_library,added,deleted,error)",
        ),
    ] = None,
    export_csv_file: Annotated[
        str | None,
        typer.Option(
            "-C", "--export-csv-file",
            help="Filename for the exported CSV file (default: tracks_export_<statuses>.csv)",
        ),
    ] = None,
    delete: Annotated[
        bool,
        typer.Option(
            "--delete",
            help="Delete tracks from target that are not present in source (with confirmation and backup)",
        ),
    ] = False,
    profile: Annotated[
        str | None,
        typer.Option(
            "-P", "--profile",
            help="Load configuration from profile file (YAML, JSON, or TOML)",
        ),
    ] = None,
):
    """
    Push tracks from a source to a target service.
    """
    push_tracks(
        source=source,
        target=target,
        similarity=similarity,
        verbose=verbose,
        log_level=log_level,
        include=include,
        exclude=exclude,
        patterns_from=patterns_from,
        csv_file=csv_file,
        report=report,
        color=color,
        mappings_file=mappings_file,
        export_csv=export_csv,
        export_csv_file=export_csv_file,
        delete=delete,
        profile=profile,
    )


@push_app.command("playlist")
def push_playlist_command(
    source: Annotated[
        str | None,
        typer.Option(
            "-f", "--from", help="Source ('subsonic', 'jellyfin', 'spotify', 'ytm', 'tidal', or 'csv')"
        ),
    ] = None,
    target: Annotated[
        str | None, typer.Option("-t", "--to", help="Target ('spotify', 'ytm', 'tidal', or 'csv')")
    ] = None,
    playlist_name: Annotated[
        str | None,
        typer.Option("--playlist-name", help="Name of the playlist to push (required)"),
    ] = None,
    source_playlist_id: Annotated[
        str | None,
        typer.Option(
            "--source-playlist-id",
            help="ID of source playlist (Spotify/YTM only, for direct lookup)",
        ),
    ] = None,
    playlist_id: Annotated[
        str | None,
        typer.Option(
            "--playlist-id",
            help="ID of existing playlist on target (Spotify only, for conflict resolution)",
        ),
    ] = None,
    similarity: Annotated[
        float,
        typer.Option("-s", "--similarity", help="Minimum similarity threshold for matching tracks (0.0-1.0)"),
    ] = 0.8,
    require_all_tracks: Annotated[
        bool,
        typer.Option(
            "--require-all-tracks",
            help="Require all tracks to match (fail if any track can't be matched)",
        ),
    ] = False,
    verbose: Annotated[
        bool, typer.Option("-v", "--verbose", help="Enable verbose output")
    ] = False,
    log_level: Annotated[
        str,
        typer.Option(
            "--log-level",
            help="Console log level: DEBUG, INFO, WARNING, ERROR, CRITICAL",
        ),
    ] = "INFO",
    ytm_auth: Annotated[
        str,
        typer.Option(help="Path to YouTube Music authentication file"),
    ] = "browser.json",
    csv_file: Annotated[
        str | None,
        typer.Option("-c", "--csv-file", help="Filename of the CSV file to write to or read from"),
    ] = None,
    on_conflict: Annotated[
        str,
        typer.Option(
            "--on-conflict",
            help="How to handle conflicts: 'abort' (show differences), 'replace' (replace entire playlist), 'append' (add missing tracks), 'sync' (add missing, remove extras)",
        ),
    ] = "abort",
    report: Annotated[
        str | None,
        typer.Option(
            "--report",
            help="Generate detailed report for specific statuses (comma-separated: not_found,matched,similarity_too_low)",
        ),
    ] = None,
    color: Annotated[
        bool,
        typer.Option(
            "--color/--no-color",
            help="Enable/disable colored output (default: enabled)",
        ),
    ] = True,
    mappings_file: Annotated[
        str | None,
        typer.Option(
            "-m", "--mappings-file",
            help="CSV file containing mappings for tracks that can't be matched automatically",
        ),
    ] = None,
    profile: Annotated[
        str | None,
        typer.Option(
            "-P", "--profile",
            help="Load configuration from profile file (YAML, JSON, or TOML)",
        ),
    ] = None,
):
    """
    Push a playlist from a source to a target service, preserving track order.
    """
    push_playlist(
        source=source,
        target=target,
        playlist_name=playlist_name,
        source_playlist_id=source_playlist_id,
        playlist_id=playlist_id,
        similarity=similarity,
        require_all_tracks=require_all_tracks,
        verbose=verbose,
        log_level=log_level,
        ytm_auth=ytm_auth,
        csv_file=csv_file,
        on_conflict=on_conflict,
        report=report,
        color=color,
        mappings_file=mappings_file,
        profile=profile,
    )


# Compare commands
@compare_app.command("albums")
def compare_albums_command(
    source: Annotated[
        str,
        typer.Option(
            "-f", "--from", help="Source ('subsonic', 'jellyfin', 'csv', 'spotify', 'ytm', or 'tidal')"
        ),
    ],
    target: Annotated[
        str,
        typer.Option(
            "-t", "--to", help="Target ('subsonic', 'jellyfin', 'csv', 'spotify', 'ytm', or 'tidal')"
        ),
    ],
    similarity: Annotated[
        float,
        typer.Option("-s", "--similarity", help="Minimum similarity threshold for matching (0.0-1.0)"),
    ] = 0.8,
    verbose: Annotated[
        bool, typer.Option("-v", "--verbose", help="Enable verbose output")
    ] = False,
    log_level: Annotated[
        str,
        typer.Option(
            "--log-level",
            help="Console log level: DEBUG, INFO, WARNING, ERROR, CRITICAL",
        ),
    ] = "INFO",
    ytm_auth: Annotated[
        str,
        typer.Option(help="Path to YouTube Music authentication file"),
    ] = "browser.json",
    csv_file: Annotated[
        str | None,
        typer.Option(
            "-c", "--csv-file",
            help="Filename of the CSV file to read from (for CSV source/target)"
        ),
    ] = None,
    mappings_file: Annotated[
        str | None,
        typer.Option(
            "-m", "--mappings-file",
            help="CSV file containing mappings for items that can't be matched automatically",
        ),
    ] = None,
    color: Annotated[
        bool,
        typer.Option(
            "--color/--no-color",
            help="Enable/disable colored output (default: enabled)",
        ),
    ] = True,
):
    """
    Compare albums between two sources/services.
    """
    compare_albums(
        source=source,
        target=target,
        similarity=similarity,
        verbose=verbose,
        log_level=log_level,
        ytm_auth=ytm_auth,
        csv_file=csv_file,
        mappings_file=mappings_file,
        color=color,
    )


@compare_app.command("tracks")
def compare_tracks_command(
    source: Annotated[
        str,
        typer.Option(
            "-f", "--from", help="Source ('subsonic', 'jellyfin', 'csv', 'spotify', 'ytm', or 'tidal')"
        ),
    ],
    target: Annotated[
        str,
        typer.Option(
            "-t", "--to", help="Target ('subsonic', 'jellyfin', 'csv', 'spotify', 'ytm', or 'tidal')"
        ),
    ],
    similarity: Annotated[
        float,
        typer.Option("-s", "--similarity", help="Minimum similarity threshold for matching (0.0-1.0)"),
    ] = 0.8,
    verbose: Annotated[
        bool, typer.Option("-v", "--verbose", help="Enable verbose output")
    ] = False,
    log_level: Annotated[
        str,
        typer.Option(
            "--log-level",
            help="Console log level: DEBUG, INFO, WARNING, ERROR, CRITICAL",
        ),
    ] = "INFO",
    ytm_auth: Annotated[
        str,
        typer.Option(help="Path to YouTube Music authentication file"),
    ] = "browser.json",
    csv_file: Annotated[
        str | None,
        typer.Option(
            "-c", "--csv-file",
            help="Filename of the CSV file to read from (for CSV source/target)"
        ),
    ] = None,
    mappings_file: Annotated[
        str | None,
        typer.Option(
            "-m", "--mappings-file",
            help="CSV file containing mappings for tracks that can't be matched automatically",
        ),
    ] = None,
    color: Annotated[
        bool,
        typer.Option(
            "--color/--no-color",
            help="Enable/disable colored output (default: enabled)",
        ),
    ] = True,
):
    """
    Compare tracks between two sources/services.
    """
    compare_tracks(
        source=source,
        target=target,
        similarity=similarity,
        verbose=verbose,
        log_level=log_level,
        ytm_auth=ytm_auth,
        csv_file=csv_file,
        mappings_file=mappings_file,
        color=color,
    )


@compare_app.command("playlist")
def compare_playlist_command(
    source: Annotated[
        str,
        typer.Option(
            "-f", "--from", help="Source ('subsonic', 'jellyfin', 'spotify', 'ytm', or 'tidal')"
        ),
    ],
    target: Annotated[
        str,
        typer.Option(
            "-t", "--to", help="Target ('subsonic', 'jellyfin', 'spotify', 'ytm', or 'tidal')"
        ),
    ],
    playlist_name_source: Annotated[
        str,
        typer.Option("--playlist-name", help="Name of the playlist in the source"),
    ],
    playlist_name_target: Annotated[
        str | None,
        typer.Option(
            "--playlist-name-target",
            help="Name of the playlist in the target (defaults to same as source)",
        ),
    ] = None,
    similarity: Annotated[
        float,
        typer.Option("-s", "--similarity", help="Minimum similarity threshold for matching (0.0-1.0)"),
    ] = 0.8,
    verbose: Annotated[
        bool, typer.Option("-v", "--verbose", help="Enable verbose output")
    ] = False,
    log_level: Annotated[
        str,
        typer.Option(
            "--log-level",
            help="Console log level: DEBUG, INFO, WARNING, ERROR, CRITICAL",
        ),
    ] = "INFO",
    ytm_auth: Annotated[
        str,
        typer.Option(help="Path to YouTube Music authentication file"),
    ] = "browser.json",
):
    """
    Compare a playlist between two sources/services.
    """
    compare_playlist(
        source=source,
        target=target,
        playlist_name_source=playlist_name_source,
        playlist_name_target=playlist_name_target,
        similarity=similarity,
        verbose=verbose,
        log_level=log_level,
        ytm_auth=ytm_auth,
    )


# Delete commands
@delete_app.command("albums")
def delete_albums_command(
    service: Annotated[
        str,
        typer.Option("-f", "--from", help="Service to delete from ('spotify', 'ytm', or 'tidal')"),
    ],
    verbose: Annotated[
        bool, typer.Option("-v", "--verbose", help="Enable verbose output")
    ] = False,
    log_level: Annotated[
        str,
        typer.Option(
            "--log-level",
            help="Console log level: DEBUG, INFO, WARNING, ERROR, CRITICAL",
        ),
    ] = "INFO",
    ytm_auth: Annotated[
        str,
        typer.Option(help="Path to YouTube Music authentication file"),
    ] = "browser.json",
    include: Annotated[
        list[str] | None,
        typer.Option(
            "-i", "--include",
            help="Include pattern (can be specified multiple times). Use AND logic within pattern",
        ),
    ] = None,
    exclude: Annotated[
        list[str] | None,
        typer.Option(
            "-e", "--exclude",
            help="Exclude pattern (can be specified multiple times). Use AND logic within pattern",
        ),
    ] = None,
    patterns_from: Annotated[
        str | None,
        typer.Option(
            "-p", "--patterns-from",
            help="File with +/- prefixed patterns",
        ),
    ] = None,
    color: Annotated[
        bool,
        typer.Option(
            "--color/--no-color",
            help="Enable/disable colored output (default: enabled)",
        ),
    ] = True,
):
    """
    Delete albums from a music service based on filter criteria.
    """
    delete_albums(
        service=service,
        verbose=verbose,
        log_level=log_level,
        ytm_auth=ytm_auth,
        include=include,
        exclude=exclude,
        patterns_from=patterns_from,
        color=color,
    )


@delete_app.command("tracks")
def delete_tracks_command(
    service: Annotated[
        str,
        typer.Option("-f", "--from", help="Service to delete from ('spotify', 'ytm', or 'tidal')"),
    ],
    verbose: Annotated[
        bool, typer.Option("-v", "--verbose", help="Enable verbose output")
    ] = False,
    log_level: Annotated[
        str,
        typer.Option(
            "--log-level",
            help="Console log level: DEBUG, INFO, WARNING, ERROR, CRITICAL",
        ),
    ] = "INFO",
    ytm_auth: Annotated[
        str,
        typer.Option(help="Path to YouTube Music authentication file"),
    ] = "browser.json",
    include: Annotated[
        list[str] | None,
        typer.Option(
            "-i", "--include",
            help="Include pattern (can be specified multiple times). Use AND logic within pattern",
        ),
    ] = None,
    exclude: Annotated[
        list[str] | None,
        typer.Option(
            "-e", "--exclude",
            help="Exclude pattern (can be specified multiple times). Use AND logic within pattern",
        ),
    ] = None,
    patterns_from: Annotated[
        str | None,
        typer.Option(
            "-p", "--patterns-from",
            help="File with +/- prefixed patterns",
        ),
    ] = None,
    color: Annotated[
        bool,
        typer.Option(
            "--color/--no-color",
            help="Enable/disable colored output (default: enabled)",
        ),
    ] = True,
):
    """
    Delete tracks from a music service based on filter criteria.
    """
    delete_tracks(
        service=service,
        verbose=verbose,
        log_level=log_level,
        ytm_auth=ytm_auth,
        include=include,
        exclude=exclude,
        patterns_from=patterns_from,
        color=color,
    )


# Cache commands
@cache_app.command("list")
def cache_list_command():
    """
    List all cache files with creation and expiration times.
    """
    caches = list_all_caches()

    if not caches:
        print("No cache files found.")
        return

    print("\n" + "=" * 80)
    print("Cache Files")
    print("=" * 80)

    for cache in caches:
        status = "EXPIRED" if cache.is_expired else "VALID"
        size_kb = cache.size_bytes / 1024 if cache.size_bytes else 0

        print(f"\nService: {cache.service_name}")
        print(f"  Type: {cache.content_type}")
        print(f"  Status: {status}")
        if cache.created_time:
            print(f"  Created: {cache.created_time.strftime('%Y-%m-%d %H:%M:%S')}")
        if cache.expires_time:
            print(f"  Expires: {cache.expires_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  Size: {size_kb:.2f} KB")
        print(f"  Path: {cache.file_path}")

    print("\n" + "=" * 80)
    print(f"Total cache files: {len(caches)}")
    expired_count = sum(1 for c in caches if c.is_expired)
    if expired_count > 0:
        print(f"Expired: {expired_count}")
    print("=" * 80)


@cache_app.command("invalidate")
def cache_invalidate_command(
    all: Annotated[
        bool, typer.Option("--all", help="Invalidate all cache files")
    ] = False,
    service: Annotated[
        str | None,
        typer.Option(
            "--service", help="Service name to invalidate (e.g., 'spotify', 'subsonic')"
        ),
    ] = None,
    content_type: Annotated[
        str | None,
        typer.Option(
            "--type", help="Content type to invalidate ('albums' or 'tracks')"
        ),
    ] = None,
):
    """
    Invalidate cache files.

    Examples:
      pushtunes cache invalidate --all                    # Invalidate all caches
      pushtunes cache invalidate --service spotify        # Invalidate all Spotify caches
      pushtunes cache invalidate --type albums            # Invalidate all album caches
      pushtunes cache invalidate --service spotify --type albums  # Invalidate Spotify album cache
    """
    if not all and not service and not content_type:
        print("Error: You must specify --all, --service, or --type")
        print("\nExamples:")
        print("  pushtunes cache invalidate --all")
        print("  pushtunes cache invalidate --service spotify")
        print("  pushtunes cache invalidate --type albums")
        print("  pushtunes cache invalidate --service spotify --type albums")
        return

    # Validate content_type if provided
    if content_type and content_type not in ["albums", "tracks"]:
        print(
            f"Error: Invalid content type '{content_type}'. Must be 'albums' or 'tracks'."
        )
        return

    # If --all is specified, ignore service and content_type
    if all:
        service_filter = None
        type_filter = None
    else:
        service_filter = service
        type_filter = content_type

    invalidated = invalidate_cache_by_pattern(
        service_name=service_filter, content_type=type_filter
    )

    if invalidated:
        print(f"\nInvalidated {len(invalidated)} cache file(s):")
        for path in invalidated:
            filename = path.split("/")[-1]
            print(f"  - {filename}")
        print(f"\nTotal: {len(invalidated)} cache file(s) invalidated")
    else:
        print("\nNo cache files matched the specified criteria.")


if __name__ == "__main__":
    app()
