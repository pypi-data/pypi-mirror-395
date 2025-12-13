"""Artist-related utility functions."""

import re


def extract_featured_artists(title: str) -> list[str]:
    """Extract featured artists from track/album title.

    Handles patterns like:
    - "Song (feat. Artist)"
    - "Song (ft. Artist)"
    - "Song (featuring Artist)"
    - "Song feat. Artist"
    - "Song ft. Artist"

    Args:
        title: Track or album title

    Returns:
        List of featured artist names
    """
    # Patterns to match featured artists
    patterns = [
        r'\((?:feat\.|ft\.|featuring)\s+([^)]+)\)',
        r'\s+(?:feat\.|ft\.|featuring)\s+(.+?)(?:\s*-\s*|$)',
    ]

    featured = []
    for pattern in patterns:
        matches = re.findall(pattern, title, re.IGNORECASE)
        for match in matches:
            # Split multiple featured artists (e.g., "Artist1 & Artist2")
            artists = match.replace(" & ", ", ").replace(" and ", ", ")
            featured.extend([a.strip() for a in artists.split(",")])

    return featured


def parse_artist_string(artists: str) -> list[str]:
    """Parse a string of artists into a list of artists.

    Handles '&', '+', '/', 'feat.', 'ft.' and ',' as separators.

    Args:
        artists: A string containing one or more artist names.

    Returns:
        A list of artist names.
    """
    if not artists:
        return []
    # Replace separators with comma
    # Handle various "featuring" patterns
    artists_normalized = artists.replace(" feat. ", ", ").replace(" ft. ", ", ")
    artists_normalized = artists_normalized.replace(" feat ", ", ").replace(" ft ", ", ")
    artists_normalized = artists_normalized.replace(" featuring ", ", ")
    # Handle other separators
    artists_normalized = artists_normalized.replace(" & ", ", ").replace(" + ", ", ").replace("/", ", ")
    # Split by comma and strip whitespace
    return [artist.strip() for artist in artists_normalized.split(",")]
