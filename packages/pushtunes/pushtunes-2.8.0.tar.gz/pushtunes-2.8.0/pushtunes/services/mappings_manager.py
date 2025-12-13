"""Manages mappings from source albums/tracks to specific target service IDs."""

import csv
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from pushtunes.models.album import Album
from pushtunes.models.track import Track
from pushtunes.utils.logging import get_logger
from pushtunes.utils.csv_manager import CsvColumns


@dataclass(frozen=True)
class AlbumMapping:
    """Maps a source album to a target album by service ID or metadata."""

    # Source album identifiers (from subsonic, csv, jellyfin)
    source_artist: str
    source_title: str

    # Target album identifiers (optional: use service ID if provided)
    spotify_id: str | None = None
    ytm_id: str | None = None
    tidal_id: str | None = None

    # Target album metadata (optional: use if service ID not provided)
    spotify_artist: str | None = None
    spotify_title: str | None = None
    ytm_artist: str | None = None
    ytm_title: str | None = None
    tidal_artist: str | None = None
    tidal_title: str | None = None
    subsonic_artist: str | None = None
    subsonic_title: str | None = None
    subsonic_album: str | None = None
    jellyfin_artist: str | None = None
    jellyfin_title: str | None = None
    jellyfin_album: str | None = None


@dataclass(frozen=True)
class TrackMapping:
    """Maps a source track to a target track by service ID or metadata."""

    # Source track identifiers
    source_artist: str
    source_title: str

    # Target track identifiers (optional: use service ID if provided)
    spotify_id: str | None = None
    ytm_id: str | None = None
    tidal_id: str | None = None

    # Target track metadata (optional: use if service ID not provided)
    spotify_artist: str | None = None
    spotify_title: str | None = None
    ytm_artist: str | None = None
    ytm_title: str | None = None
    tidal_artist: str | None = None
    tidal_title: str | None = None
    subsonic_artist: str | None = None
    subsonic_title: str | None = None
    subsonic_album: str | None = None
    jellyfin_artist: str | None = None
    jellyfin_title: str | None = None
    jellyfin_album: str | None = None


# Cache for Spotify ID type detection to minimize API calls
_spotify_id_type_cache: dict[str, Literal["album", "track"] | None] = {}


def normalize_mapping_key(text: str) -> str:
    """Normalize text for mapping lookup to handle sloppy CSVs.

    Makes lookups case-insensitive and handles whitespace/separator variations.

    Args:
        text: The text to normalize (artist or title)

    Returns:
        Normalized text for use as mapping key
    """
    # Convert to lowercase
    normalized = text.lower()

    # Normalize whitespace: replace multiple spaces/tabs with single space
    import re
    normalized = re.sub(r'\s+', ' ', normalized)

    # Normalize common separators to a standard form
    # Replace various separators with a normalized one
    normalized = re.sub(r'\s*[&,;/]\s*', ' & ', normalized)

    # Strip leading/trailing whitespace
    normalized = normalized.strip()

    return normalized


def detect_id_type_ytm(service_id: str) -> Literal["album", "track"] | None:
    """Detect if a YTM ID is for an album or track using heuristics.

    YTM uses distinguishable formats:
    - Track IDs (videoId): 11-character strings (standard YouTube video IDs)
    - Album IDs (playlistId): Longer strings, typically starting with "OLAK5uy_" or "MPREb_"

    Args:
        service_id: The YTM service ID

    Returns:
        "album", "track", or None if cannot determine
    """
    if not service_id:
        return None

    # Track: 11-character videoId (standard YouTube format)
    if len(service_id) == 11:
        return "track"

    # Album: Longer playlistId with specific prefixes
    if service_id.startswith(("OLAK5uy_", "MPREb_")):
        return "album"

    return None


def detect_id_type_spotify(service_id: str, spotify_client=None) -> Literal["album", "track"] | None:
    """Detect if a Spotify ID is for an album or track using API query.

    Spotify album and track IDs have identical formats (22-character Base62 strings),
    so we need to query the API to determine the type. Results are cached to minimize API calls.

    Args:
        service_id: The Spotify service ID
        spotify_client: Optional Spotipy client instance for API queries

    Returns:
        "album", "track", or None if cannot determine
    """
    if not service_id:
        return None

    # Check cache first
    if service_id in _spotify_id_type_cache:
        return _spotify_id_type_cache[service_id]

    # If no client provided, cannot detect (would need API access)
    if spotify_client is None:
        return None

    try:
        # Try album endpoint first
        try:
            spotify_client.album(service_id)
            _spotify_id_type_cache[service_id] = "album"
            return "album"
        except Exception:
            pass

        # Try track endpoint
        try:
            spotify_client.track(service_id)
            _spotify_id_type_cache[service_id] = "track"
            return "track"
        except Exception:
            pass

        # Neither worked
        _spotify_id_type_cache[service_id] = None
        return None

    except Exception:
        return None


def detect_id_type_tidal(service_id: str) -> Literal["album", "track"] | None:
    """Detect if a Tidal ID is for an album or track using heuristics.

    Tidal IDs are numeric strings. Album and track IDs have the same format,
    so we cannot reliably distinguish them without an API call. For now,
    we assume album unless proven otherwise.

    Args:
        service_id: The Tidal service ID

    Returns:
        None (cannot determine without API call)
    """
    # Tidal album and track IDs are both numeric strings
    # Cannot distinguish without API call, so return None
    return None


def detect_id_type(service_id: str, service_name: str, service_client=None) -> Literal["album", "track"] | None:
    """Detect if a service ID is for an album or track.

    Args:
        service_id: The service ID to detect
        service_name: The service name ("spotify", "ytm", or "tidal")
        service_client: Optional service client for API queries (Spotify only)

    Returns:
        "album", "track", or None if cannot determine
    """
    if service_name == "ytm":
        return detect_id_type_ytm(service_id)
    elif service_name == "spotify":
        return detect_id_type_spotify(service_id, service_client)
    elif service_name == "tidal":
        return detect_id_type_tidal(service_id)

    return None


class MappingsManager:
    """Manages mappings from source albums/tracks to target service albums/tracks."""

    def __init__(self, mappings_file: str | Path | None = None):
        """Initialize the mappings manager.

        Args:
            mappings_file: Path to CSV file containing mappings (supports ~ for home directory)
        """
        self.log = get_logger(__name__)
        self.album_mappings: dict[tuple[str, str], AlbumMapping] = {}
        self.track_mappings: dict[tuple[str, str], TrackMapping] = {}

        if mappings_file:
            # Expand ~ to home directory
            expanded_path = os.path.expanduser(str(mappings_file))
            self._load_from_csv(Path(expanded_path))

    def _load_from_csv(self, csv_file: Path) -> None:
        """Load mappings from CSV file.

        CSV format:
        type,artist,title,spotify_id,ytm_id,spotify_artist,spotify_title,ytm_artist,ytm_title

        Where type is 'album' or 'track'.
        """
        if not csv_file.exists():
            self.log.warning(f"Mappings file not found: {csv_file}")
            return

        try:
            with open(csv_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)

                # Check if the CSV has a 'type' column, otherwise assume albums
                has_type_column = CsvColumns.MAPPINGS_TYPE in reader.fieldnames if reader.fieldnames else False

                for row_num, row in enumerate(reader, start=2):  # Start at 2 (header is line 1)
                    try:
                        # Determine the type of mapping
                        mapping_type = row.get(CsvColumns.MAPPINGS_TYPE, "album").strip().lower()

                        artist = row.get(CsvColumns.MAPPINGS_ARTIST, "").strip()
                        title = row.get(CsvColumns.MAPPINGS_TITLE, "").strip()

                        if not artist or not title:
                            self.log.warning(
                                f"Skipping row {row_num}: missing artist or title"
                            )
                            continue

                        # Extract target service IDs
                        spotify_id = row.get(CsvColumns.MAPPINGS_SPOTIFY_ID, "").strip() or None
                        ytm_id = row.get(CsvColumns.MAPPINGS_YTM_ID, "").strip() or None
                        tidal_id = row.get(CsvColumns.MAPPINGS_TIDAL_ID, "").strip() or None

                        # Extract target metadata
                        spotify_artist = row.get(CsvColumns.MAPPINGS_SPOTIFY_ARTIST, "").strip() or None
                        spotify_title = row.get(CsvColumns.MAPPINGS_SPOTIFY_TITLE, "").strip() or None
                        ytm_artist = row.get(CsvColumns.MAPPINGS_YTM_ARTIST, "").strip() or None
                        ytm_title = row.get(CsvColumns.MAPPINGS_YTM_TITLE, "").strip() or None
                        tidal_artist = row.get(CsvColumns.MAPPINGS_TIDAL_ARTIST, "").strip() or None
                        tidal_title = row.get(CsvColumns.MAPPINGS_TIDAL_TITLE, "").strip() or None
                        subsonic_artist = row.get(CsvColumns.MAPPINGS_SUBSONIC_ARTIST, "").strip() or None
                        subsonic_title = row.get(CsvColumns.MAPPINGS_SUBSONIC_TITLE, "").strip() or None
                        subsonic_album = row.get(CsvColumns.MAPPINGS_SUBSONIC_ALBUM, "").strip() or None
                        jellyfin_artist = row.get(CsvColumns.MAPPINGS_JELLYFIN_ARTIST, "").strip() or None
                        jellyfin_title = row.get(CsvColumns.MAPPINGS_JELLYFIN_TITLE, "").strip() or None
                        jellyfin_album = row.get(CsvColumns.MAPPINGS_JELLYFIN_ALBUM, "").strip() or None

                        # At least one target must be specified
                        has_spotify = spotify_id or (spotify_artist and spotify_title)
                        has_ytm = ytm_id or (ytm_artist and ytm_title)
                        has_tidal = tidal_id or (tidal_artist and tidal_title)
                        has_subsonic = subsonic_artist and subsonic_title
                        has_jellyfin = jellyfin_artist and jellyfin_title

                        if not has_spotify and not has_ytm and not has_tidal and not has_subsonic and not has_jellyfin:
                            self.log.warning(
                                f"Skipping row {row_num}: no target specified for {artist} - {title}"
                            )
                            continue

                        # Create the appropriate mapping
                        if mapping_type == "track":
                            mapping = TrackMapping(
                                source_artist=artist,
                                source_title=title,
                                spotify_id=spotify_id,
                                ytm_id=ytm_id,
                                tidal_id=tidal_id,
                                spotify_artist=spotify_artist,
                                spotify_title=spotify_title,
                                ytm_artist=ytm_artist,
                                ytm_title=ytm_title,
                                tidal_artist=tidal_artist,
                                tidal_title=tidal_title,
                                subsonic_artist=subsonic_artist,
                                subsonic_title=subsonic_title,
                                subsonic_album=subsonic_album,
                                jellyfin_artist=jellyfin_artist,
                                jellyfin_title=jellyfin_title,
                                jellyfin_album=jellyfin_album,
                            )
                            key = (normalize_mapping_key(artist), normalize_mapping_key(title))
                            self.track_mappings[key] = mapping
                            self.log.debug(f"Loaded track mapping: {artist} - {title}")
                        else:  # Default to album
                            mapping = AlbumMapping(
                                source_artist=artist,
                                source_title=title,
                                spotify_id=spotify_id,
                                ytm_id=ytm_id,
                                tidal_id=tidal_id,
                                spotify_artist=spotify_artist,
                                spotify_title=spotify_title,
                                ytm_artist=ytm_artist,
                                ytm_title=ytm_title,
                                tidal_artist=tidal_artist,
                                tidal_title=tidal_title,
                                subsonic_artist=subsonic_artist,
                                subsonic_title=subsonic_title,
                                subsonic_album=subsonic_album,
                                jellyfin_artist=jellyfin_artist,
                                jellyfin_title=jellyfin_title,
                                jellyfin_album=jellyfin_album,
                            )
                            key = (normalize_mapping_key(artist), normalize_mapping_key(title))
                            self.album_mappings[key] = mapping
                            self.log.debug(f"Loaded album mapping: {artist} - {title}")

                    except Exception as e:
                        self.log.error(f"Error parsing row {row_num}: {e}")
                        continue

            self.log.info(
                f"Loaded {len(self.album_mappings)} album mappings and "
                f"{len(self.track_mappings)} track mappings from {csv_file}"
            )

        except Exception as e:
            self.log.error(f"Failed to load mappings from {csv_file}: {e}")

    def get_album_mapping(
        self, source_album: Album, service_name: str, service_client=None
    ) -> Album | Track | None:
        """Get the target album or track for a source album on a specific service.

        Supports cross-type mapping (album→track) for cases like audiobooks, DJ mixes, etc.

        Args:
            source_album: The source album to map
            service_name: The target service name ('spotify' or 'ytm')
            service_client: Optional service client for Spotify ID type detection

        Returns:
            Album or Track object with service_id or metadata for the target, or None if no mapping
        """
        # Look up mapping by artist and title (normalized for sloppy CSVs)
        key = (normalize_mapping_key(source_album.artist), normalize_mapping_key(source_album.title))
        mapping = self.album_mappings.get(key)

        if not mapping:
            return None

        # Create the target based on the service
        if service_name == "spotify":
            if mapping.spotify_id:
                # Detect ID type for cross-type mapping support
                detected_type = detect_id_type(mapping.spotify_id, "spotify", service_client)

                if detected_type == "track":
                    # Cross-type mapping: album→track
                    self.log.warning(
                        f"Cross-type mapping: album '{source_album.artist} - {source_album.title}' "
                        f"mapped to Spotify track ID {mapping.spotify_id}"
                    )
                    return Track(
                        title=source_album.title,
                        artists=source_album.artists,
                        album=None,  # No album context
                        year=source_album.year,
                        service_id=mapping.spotify_id,
                        service_name="spotify",
                    )
                else:
                    # Normal album mapping (or undetectable, assume album)
                    return Album(
                        title=source_album.title,
                        artists=source_album.artists,
                        year=source_album.year,
                        service_id=mapping.spotify_id,
                        service_name="spotify",
                    )
            elif mapping.spotify_artist and mapping.spotify_title:
                # Use metadata for search (ID-based cross-type only for now)
                return Album(
                    title=mapping.spotify_title,
                    artists=[mapping.spotify_artist],
                    year=source_album.year,
                    service_name="spotify",
                )
        elif service_name == "ytm":
            if mapping.ytm_id:
                # Detect ID type for cross-type mapping support
                detected_type = detect_id_type_ytm(mapping.ytm_id)

                if detected_type == "track":
                    # Cross-type mapping: album→track
                    self.log.warning(
                        f"Cross-type mapping: album '{source_album.artist} - {source_album.title}' "
                        f"mapped to YTM track ID {mapping.ytm_id}"
                    )
                    return Track(
                        title=source_album.title,
                        artists=source_album.artists,
                        album=None,  # No album context
                        year=source_album.year,
                        service_id=mapping.ytm_id,
                        service_name="ytm",
                    )
                else:
                    # Normal album mapping (or undetectable, assume album)
                    return Album(
                        title=source_album.title,
                        artists=source_album.artists,
                        year=source_album.year,
                        service_id=mapping.ytm_id,
                        service_name="ytm",
                    )
            elif mapping.ytm_artist and mapping.ytm_title:
                # Use metadata for search (ID-based cross-type only for now)
                return Album(
                    title=mapping.ytm_title,
                    artists=[mapping.ytm_artist],
                    year=source_album.year,
                    service_name="ytm",
                )
        elif service_name == "tidal":
            if mapping.tidal_id:
                # Tidal IDs cannot be reliably detected as album vs track without API call
                # Assume album mapping (since we're in get_album_mapping)
                return Album(
                    title=source_album.title,
                    artists=source_album.artists,
                    year=source_album.year,
                    service_id=mapping.tidal_id,
                    service_name="tidal",
                )
            elif mapping.tidal_artist and mapping.tidal_title:
                # Use metadata for search
                return Album(
                    title=mapping.tidal_title,
                    artists=[mapping.tidal_artist],
                    year=source_album.year,
                    service_name="tidal",
                )
        elif service_name == "subsonic":
            if mapping.subsonic_artist and mapping.subsonic_title:
                return Album(
                    title=mapping.subsonic_title,
                    artists=[mapping.subsonic_artist],
                    year=source_album.year,
                    service_name="subsonic",
                )
        elif service_name == "jellyfin":
            if mapping.jellyfin_artist and mapping.jellyfin_title:
                return Album(
                    title=mapping.jellyfin_title,
                    artists=[mapping.jellyfin_artist],
                    year=source_album.year,
                    service_name="jellyfin",
                )

        return None

    def get_track_mapping(
        self, source_track: Track, service_name: str, service_client=None
    ) -> Track | Album | None:
        """Get the target track or album for a source track on a specific service.

        Supports cross-type mapping (track→album) though less common than album→track.

        Args:
            source_track: The source track to map
            service_name: The target service name ('spotify' or 'ytm')
            service_client: Optional service client for Spotify ID type detection

        Returns:
            Track or Album object with service_id or metadata for the target, or None if no mapping
        """
        # Look up mapping by artist and title (normalized for sloppy CSVs)
        key = (normalize_mapping_key(source_track.artist), normalize_mapping_key(source_track.title))
        mapping = self.track_mappings.get(key)

        if not mapping:
            return None

        # Create the target based on the service
        if service_name == "spotify":
            if mapping.spotify_id:
                # Detect ID type for cross-type mapping support
                detected_type = detect_id_type(mapping.spotify_id, "spotify", service_client)

                if detected_type == "album":
                    # Cross-type mapping: track→album
                    self.log.warning(
                        f"Cross-type mapping: track '{source_track.artist} - {source_track.title}' "
                        f"mapped to Spotify album ID {mapping.spotify_id}"
                    )
                    return Album(
                        title=source_track.title,
                        artists=source_track.artists,
                        year=source_track.year,
                        service_id=mapping.spotify_id,
                        service_name="spotify",
                    )
                else:
                    # Normal track mapping (or undetectable, assume track)
                    return Track(
                        title=source_track.title,
                        artists=source_track.artists,
                        album=source_track.album,
                        year=source_track.year,
                        service_id=mapping.spotify_id,
                        service_name="spotify",
                    )
            elif mapping.spotify_artist and mapping.spotify_title:
                # Use metadata for search (ID-based cross-type only for now)
                return Track(
                    title=mapping.spotify_title,
                    artists=[mapping.spotify_artist],
                    album=source_track.album,
                    year=source_track.year,
                    service_name="spotify",
                )
        elif service_name == "ytm":
            if mapping.ytm_id:
                # Detect ID type for cross-type mapping support
                detected_type = detect_id_type_ytm(mapping.ytm_id)

                if detected_type == "album":
                    # Cross-type mapping: track→album
                    self.log.warning(
                        f"Cross-type mapping: track '{source_track.artist} - {source_track.title}' "
                        f"mapped to YTM album ID {mapping.ytm_id}"
                    )
                    return Album(
                        title=source_track.title,
                        artists=source_track.artists,
                        year=source_track.year,
                        service_id=mapping.ytm_id,
                        service_name="ytm",
                    )
                else:
                    # Normal track mapping (or undetectable, assume track)
                    return Track(
                        title=source_track.title,
                        artists=source_track.artists,
                        album=source_track.album,
                        year=source_track.year,
                        service_id=mapping.ytm_id,
                        service_name="ytm",
                    )
            elif mapping.ytm_artist and mapping.ytm_title:
                # Use metadata for search (ID-based cross-type only for now)
                return Track(
                    title=mapping.ytm_title,
                    artists=[mapping.ytm_artist],
                    album=source_track.album,
                    year=source_track.year,
                    service_name="ytm",
                )
        elif service_name == "tidal":
            if mapping.tidal_id:
                # Tidal IDs cannot be reliably detected as album vs track without API call
                # Assume track mapping (since we're in get_track_mapping)
                return Track(
                    title=source_track.title,
                    artists=source_track.artists,
                    album=source_track.album,
                    year=source_track.year,
                    service_id=mapping.tidal_id,
                    service_name="tidal",
                )
            elif mapping.tidal_artist and mapping.tidal_title:
                # Use metadata for search
                return Track(
                    title=mapping.tidal_title,
                    artists=[mapping.tidal_artist],
                    album=source_track.album,
                    year=source_track.year,
                    service_name="tidal",
                )
        elif service_name == "subsonic":
            if mapping.subsonic_artist and mapping.subsonic_title:
                return Track(
                    title=mapping.subsonic_title,
                    artists=[mapping.subsonic_artist],
                    album=mapping.subsonic_album,
                    year=source_track.year,
                    service_name="subsonic",
                )
        elif service_name == "jellyfin":
            if mapping.jellyfin_artist and mapping.jellyfin_title:
                return Track(
                    title=mapping.jellyfin_title,
                    artists=[mapping.jellyfin_artist],
                    album=mapping.jellyfin_album,
                    year=source_track.year,
                    service_name="jellyfin",
                )

        return None
