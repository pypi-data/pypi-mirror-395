"""Compare commands for comparing libraries and playlists between music services."""

import sys
from typing import Optional

import typer

from pushtunes.models.compare_status import CompareStatus
from pushtunes.services.album_comparer import AlbumComparer, AlbumCompareResult
from pushtunes.services.track_comparer import TrackComparer, TrackCompareResult
from pushtunes.services.playlist_comparer import PlaylistComparer, PlaylistCompareResult
from pushtunes.utils.filters import AlbumFilter, TrackFilter, FilterAction
from pushtunes.utils.logging import get_logger, set_console_log_level
from pushtunes.utils.cli.commands.shared import create_source_or_service, print_compare_stats


def compare_albums(
    source: str = typer.Option(
        ...,
        "--from",
        help="Source ('subsonic', 'jellyfin', 'csv', 'spotify', or 'ytm')",
    ),
    target: str = typer.Option(
        ..., "--to", help="Target ('subsonic', 'jellyfin', 'csv', 'spotify', or 'ytm')"
    ),
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
    csv_file: Optional[str] = typer.Option(
        None, help="Filename of the CSV file to read from (for CSV source/target)"
    ),
    mappings_file: Optional[str] = typer.Option(
        None,
        "--mappings-file",
        help="CSV file containing mappings for albums that can't be matched automatically",
    ),
    color: bool = typer.Option(
        True,
        "--color/--no-color",
        help="Enable/disable colored output (default: enabled)",
    ),
):
    """
    Compare albums between two sources/services.
    """
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

        # Create source and target
        log.info(f"Initializing {source} source...")
        source_obj = create_source_or_service(source, config)

        log.info(f"Initializing {target} target...")
        target_obj = create_source_or_service(target, config)

        # Get albums from both source and target
        log.info(f"Fetching albums from {source}...")
        albums_source = source_obj.get_albums()
        log.info(f"Fetched {len(albums_source)} albums from {source}")

        log.info(f"Fetching albums from {target}...")
        albums_target = target_obj.get_albums()
        log.info(f"Fetched {len(albums_target)} albums from {target}")

        # Load mappings if provided
        mappings = None
        if mappings_file:
            from pushtunes.services.mappings_manager import MappingsManager

            mappings = MappingsManager(mappings_file)

        # Perform comparison
        log.info(f"Starting album comparison between {source} and {target}...")
        comparer = AlbumComparer(
            albums_source=albums_source,
            albums_target=albums_target,
            filter=album_filter,
            min_similarity=similarity,
            mappings=mappings,
        )
        results: list[AlbumCompareResult] = comparer.compare_albums()

        # Calculate statistics
        stats = {
            "total": len(results),
            "in_both": sum(1 for r in results if r.status == CompareStatus.in_both),
            "only_in_source": sum(
                1 for r in results if r.status == CompareStatus.only_in_source
            ),
            "only_in_target": sum(
                1 for r in results if r.status == CompareStatus.only_in_target
            ),
            "filtered": sum(1 for r in results if r.status == CompareStatus.filtered),
            "errors": sum(1 for r in results if r.status == CompareStatus.error),
        }

        print_compare_stats(stats, "albums")

        # Print detailed results grouped by status
        print("\n" + "=" * 50)
        print("Detailed Results")
        print("=" * 50)

        # Only in source
        only_in_source = [
            r for r in results if r.status == CompareStatus.only_in_source
        ]
        if only_in_source:
            print(f"\nAlbums only in {source} ({len(only_in_source)}):")
            for result in only_in_source:
                print(f"  - {result.album.artist} - {result.album.title}")

        # Only in target
        only_in_target = [
            r for r in results if r.status == CompareStatus.only_in_target
        ]
        if only_in_target:
            print(f"\nAlbums only in {target} ({len(only_in_target)}):")
            for result in only_in_target:
                print(f"  - {result.album.artist} - {result.album.title}")

        # In both (optionally show if verbose)
        if verbose:
            in_both = [r for r in results if r.status == CompareStatus.in_both]
            if in_both:
                print(f"\nAlbums in both ({len(in_both)}):")
                for result in in_both:
                    print(f"  - {result.album.artist} - {result.album.title}")

        print("\nComparison completed successfully")

    except KeyboardInterrupt:
        print("\nComparison interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        if verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


def compare_tracks(
    source: str = typer.Option(
        ...,
        "--from",
        help="Source ('subsonic', 'jellyfin', 'csv', 'spotify', or 'ytm')",
    ),
    target: str = typer.Option(
        ..., "--to", help="Target ('subsonic', 'jellyfin', 'csv', 'spotify', or 'ytm')"
    ),
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
    csv_file: Optional[str] = typer.Option(
        None, help="Filename of the CSV file to read from (for CSV source/target)"
    ),
    mappings_file: Optional[str] = typer.Option(
        None,
        "--mappings-file",
        help="CSV file containing mappings for tracks that can't be matched automatically",
    ),
    color: bool = typer.Option(
        True,
        "--color/--no-color",
        help="Enable/disable colored output (default: enabled)",
    ),
):
    """
    Compare tracks between two sources/services.
    """
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
        track_filter = None

        # Create source and target
        log.info(f"Initializing {source} source...")
        source_obj = create_source_or_service(source, config)

        log.info(f"Initializing {target} target...")
        target_obj = create_source_or_service(target, config)

        # Get tracks from both source and target
        log.info(f"Fetching tracks from {source}...")
        tracks_source = source_obj.get_tracks()
        log.info(f"Fetched {len(tracks_source)} tracks from {source}")

        log.info(f"Fetching tracks from {target}...")
        tracks_target = target_obj.get_tracks()
        log.info(f"Fetched {len(tracks_target)} tracks from {target}")

        # Load mappings if provided
        mappings = None
        if mappings_file:
            from pushtunes.services.mappings_manager import MappingsManager

            mappings = MappingsManager(mappings_file)

        # Perform comparison
        log.info(f"Starting track comparison between {source} and {target}...")
        comparer = TrackComparer(
            tracks_source=tracks_source,
            tracks_target=tracks_target,
            filter=track_filter,
            min_similarity=similarity,
            mappings=mappings,
        )
        results: list[TrackCompareResult] = comparer.compare_tracks()

        # Calculate statistics
        stats = {
            "total": len(results),
            "in_both": sum(1 for r in results if r.status == CompareStatus.in_both),
            "only_in_source": sum(
                1 for r in results if r.status == CompareStatus.only_in_source
            ),
            "only_in_target": sum(
                1 for r in results if r.status == CompareStatus.only_in_target
            ),
            "filtered": sum(1 for r in results if r.status == CompareStatus.filtered),
            "errors": sum(1 for r in results if r.status == CompareStatus.error),
        }

        print_compare_stats(stats, "tracks")

        # Print detailed results grouped by status
        print("\n" + "=" * 50)
        print("Detailed Results")
        print("=" * 50)

        # Only in source
        only_in_source = [
            r for r in results if r.status == CompareStatus.only_in_source
        ]
        if only_in_source:
            print(f"\nTracks only in {source} ({len(only_in_source)}):")
            for result in only_in_source:
                print(f"  - {result.track.artist} - {result.track.title}")

        # Only in target
        only_in_target = [
            r for r in results if r.status == CompareStatus.only_in_target
        ]
        if only_in_target:
            print(f"\nTracks only in {target} ({len(only_in_target)}):")
            for result in only_in_target:
                print(f"  - {result.track.artist} - {result.track.title}")

        # In both (optionally show if verbose)
        if verbose:
            in_both = [r for r in results if r.status == CompareStatus.in_both]
            if in_both:
                print(f"\nTracks in both ({len(in_both)}):")
                for result in in_both:
                    print(f"  - {result.track.artist} - {result.track.title}")

        print("\nComparison completed successfully")

    except KeyboardInterrupt:
        print("\nComparison interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        if verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


def compare_playlist(
    source: str = typer.Option(
        ..., "--from", help="Source ('subsonic', 'jellyfin', 'spotify', or 'ytm')"
    ),
    target: str = typer.Option(
        ..., "--to", help="Target ('subsonic', 'jellyfin', 'spotify', or 'ytm')"
    ),
    playlist_name_source: str = typer.Option(
        ..., "--playlist-name", help="Name of the playlist in the source"
    ),
    playlist_name_target: Optional[str] = typer.Option(
        None,
        "--playlist-name-target",
        help="Name of the playlist in the target (defaults to same as source)",
    ),
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
):
    """
    Compare a playlist between two sources/services.
    """
    # Set console log level
    try:
        set_console_log_level(log_level)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Default target playlist name to source playlist name if not specified
    if not playlist_name_target:
        playlist_name_target = playlist_name_source

    # Create configuration
    config = {
        "similarity": similarity,
        "ytm_auth_file": ytm_auth,
    }

    log = get_logger()
    try:
        # Create source and target
        log.info(f"Initializing {source} source...")
        source_obj = create_source_or_service(source, config)

        log.info(f"Initializing {target} target...")
        target_obj = create_source_or_service(target, config)

        # Get playlists from both source and target
        log.info(f"Fetching playlist '{playlist_name_source}' from {source}...")
        playlist_source = source_obj.get_playlist(playlist_name_source)
        if not playlist_source:
            print(f"Error: Playlist '{playlist_name_source}' not found in {source}")
            sys.exit(1)
        log.info(
            f"Fetched playlist with {len(playlist_source.tracks)} tracks from {source}"
        )

        log.info(f"Fetching playlist '{playlist_name_target}' from {target}...")
        playlist_target = target_obj.get_playlist(playlist_name_target)
        if not playlist_target:
            print(f"Error: Playlist '{playlist_name_target}' not found in {target}")
            sys.exit(1)
        log.info(
            f"Fetched playlist with {len(playlist_target.tracks)} tracks from {target}"
        )

        # Perform comparison
        log.info(f"Comparing playlists...")
        comparer = PlaylistComparer(
            playlist_source=playlist_source,
            playlist_target=playlist_target,
            min_similarity=similarity,
        )
        result: PlaylistCompareResult = comparer.compare_playlists()

        # Print results
        print("\n" + "=" * 50)
        print("Playlist Comparison Results")
        print("=" * 50)
        print(f"Playlist: {result.playlist_name}")
        print(f"Source ({source}): {result.source_track_count} tracks")
        print(f"Target ({target}): {result.target_track_count} tracks")
        print(f"Tracks in both: {len(result.tracks_in_both)}")
        print(f"Only in source: {len(result.tracks_only_in_source)}")
        print(f"Only in target: {len(result.tracks_only_in_target)}")
        print("=" * 50)

        # Print detailed results
        if result.tracks_only_in_source:
            print(f"\nTracks only in {source} ({len(result.tracks_only_in_source)}):")
            for track in result.tracks_only_in_source:
                print(f"  - {track.artist} - {track.title}")

        if result.tracks_only_in_target:
            print(f"\nTracks only in {target} ({len(result.tracks_only_in_target)}):")
            for track in result.tracks_only_in_target:
                print(f"  - {track.artist} - {track.title}")

        # Show matched tracks if verbose
        if verbose and result.tracks_in_both:
            print(f"\nTracks in both ({len(result.tracks_in_both)}):")
            for source_track, target_track in result.tracks_in_both:
                print(
                    f"  - {source_track.artist} - {source_track.title} <-> {target_track.artist} - {target_track.title}"
                )

        print("\nComparison completed successfully")

    except KeyboardInterrupt:
        print("\nComparison interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        if verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)
