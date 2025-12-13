"""Shared utilities for CLI commands."""

from typing import Any

from pushtunes.sources.csv import CSVSource
from pushtunes.sources.spotify import SpotifySource
from pushtunes.sources.ytm import YTMSource
from pushtunes.sources.tidal import TidalSource
from pushtunes.services.spotify import SpotifyService
from pushtunes.services.ytm import YTMService
from pushtunes.services.tidal import TidalService
from pushtunes.services.csv import CSVService
from pushtunes.services.subsonic import SubsonicService
from pushtunes.services.jellyfin import JellyfinService
from pushtunes.sources.subsonic import SubsonicSource
from pushtunes.sources.jellyfin import JellyfinSource


def create_source(source_type: str, config: dict[str, Any]):
    """Create a music source based on type and configuration."""
    if source_type == "subsonic":
        return SubsonicSource(
            url=config.get("subsonic_url"),
            username=config.get("subsonic_username"),
            password=config.get("subsonic_password"),
            port=config.get("subsonic_port", 443),
        )
    elif source_type == "jellyfin":
        return JellyfinSource(
            url=config.get("jellyfin_url"),
            username=config.get("jellyfin_username"),
            password=config.get("jellyfin_password"),
        )
    elif source_type == "spotify":
        return SpotifySource(
            client_id=config.get("spotify_client_id"),
            client_secret=config.get("spotify_client_secret"),
        )
    elif source_type == "ytm":
        return YTMSource(auth_file=config.get("ytm_auth", "browser.json"))
    elif source_type == "tidal":
        return TidalSource(
            client_id=config.get("tidal_client_id"),
            client_secret=config.get("tidal_client_secret"),
            session_file=config.get("tidal_session_file", "tidal-session.json"),
        )
    elif source_type == "csv":
        return CSVSource(csv_file=config.get("csv_file"))
    else:
        raise ValueError(f"Unsupported source type: {source_type}")


def create_service(service_type: str, config: dict[str, Any]):
    """Create a music service based on type and configuration."""
    if service_type == "spotify":
        return SpotifyService(
            min_similarity=config.get("similarity", 0.8),
            client_id=config.get("spotify_client_id"),
            client_secret=config.get("spotify_client_secret"),
            redirect_uri=config.get("spotify_redirect_uri"),
        )
    elif service_type == "ytm":
        return YTMService(
            min_similarity=config.get("similarity", 0.8),
            auth_file=config.get("ytm_auth_file", "browser.json"),
        )
    elif service_type == "tidal":
        return TidalService(
            min_similarity=config.get("similarity", 0.8),
            client_id=config.get("tidal_client_id"),
            client_secret=config.get("tidal_client_secret"),
            session_file=config.get("tidal_session_file", "tidal-session.json"),
        )
    elif service_type == "subsonic":
        return SubsonicService(
            url=config.get("subsonic_url"),
            username=config.get("subsonic_username"),
            password=config.get("subsonic_password"),
            port=config.get("subsonic_port", 443),
            min_similarity=config.get("similarity", 0.8),
        )
    elif service_type == "jellyfin":
        return JellyfinService(
            url=config.get("jellyfin_url"),
            username=config.get("jellyfin_username"),
            password=config.get("jellyfin_password"),
            min_similarity=config.get("similarity", 0.8),
        )
    elif service_type == "csv":
        csv_file = config.get("csv_file")
        if not csv_file:
            raise ValueError("CSV file path is required when using CSV as a target")
        return CSVService(csv_file=csv_file)
    else:
        raise ValueError(f"Unsupported service type: {service_type}")


def create_source_or_service(source_type: str, config: dict[str, Any]):
    """Create a music source or service based on type and configuration.

    This is used for compare commands where both --from and --to can be
    either sources (subsonic, jellyfin, csv) or services (spotify, ytm, tidal).
    """
    # Try to create as a source first
    if source_type in ["subsonic", "jellyfin", "csv", "spotify", "ytm", "tidal"]:
        if source_type in ["subsonic", "jellyfin", "csv"]:
            return create_source(source_type, config)
        elif source_type in ["spotify", "ytm", "tidal"]:
            # These can be both sources and services
            # For compare, we want to get their library, so create as sources
            return create_source(source_type, config)

    raise ValueError(f"Unsupported source/service type: {source_type}")


def print_stats(stats: dict[str, int], content_type: str = "albums"):
    """Print sync statistics."""
    print("\n" + "=" * 50)
    print("Statistics")
    print("=" * 50)
    print(f"Total {content_type} processed: {stats['total']}")
    if stats.get("skipped_filtered", 0) > 0:
        print(f"Skipped (filtered out): {stats['skipped_filtered']}")
    print(f"Successfully added: {stats['added']}")
    if stats.get("mapped", 0) > 0:
        print(f"Added via mappings: {stats['mapped']}")
    if stats.get("deleted", 0) > 0:
        print(f"Deleted from target: {stats['deleted']}")
    print(f"Skipped (already in library): {stats['skipped_existing']}")
    print(f"Skipped (not found): {stats['skipped_not_found']}")
    print(f"Skipped (low similarity): {stats['skipped_low_similarity']}")
    print(f"Errors: {stats['errors']}")
    print("=" * 50)


def print_compare_stats(stats: dict[str, int], content_type: str = "albums"):
    """Print comparison statistics."""
    print("\n" + "=" * 50)
    print("Comparison Results")
    print("=" * 50)
    print(f"Total {content_type} compared: {stats['total']}")
    print(f"In both: {stats['in_both']}")
    print(f"Only in source: {stats['only_in_source']}")
    print(f"Only in target: {stats['only_in_target']}")
    if stats.get("filtered", 0) > 0:
        print(f"Filtered out: {stats['filtered']}")
    if stats.get("errors", 0) > 0:
        print(f"Errors: {stats['errors']}")
    print("=" * 50)
