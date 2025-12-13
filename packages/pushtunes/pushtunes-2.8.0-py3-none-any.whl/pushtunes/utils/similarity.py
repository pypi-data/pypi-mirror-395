"""Similarity matching utilities for album and artist names."""

from difflib import SequenceMatcher
from functools import lru_cache
from pushtunes.models.album import Album
from pushtunes.models.track import Track


def similarity(a: str, b: str) -> float:
    """Calculate similarity between two strings using SequenceMatcher.

    Args:
        a: First string
        b: Second string

    Returns:
        Similarity ratio between 0.0 and 1.0
    """
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def _calculate_artist_similarity(artists1: list[str], artists2: list[str]) -> float:
    """
    Calculates artist similarity using a hybrid approach to handle parsing
    discrepancies.
    """
    set1 = {a.lower() for a in artists1}
    set2 = {a.lower() for a in artists2}

    # 1. Direct Jaccard similarity on the sets of artists
    if not set1 and not set2:
        jaccard_sim = 1.0
    elif not set1 or not set2:
        jaccard_sim = 0.0
    else:
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        jaccard_sim = float(intersection) / union

    if jaccard_sim > 0.99:
        return 1.0

    # 2. Check for parsing mismatch by splitting single-artist strings
    if len(set1) == 1 and len(set2) > 1:
        single_artist_str = list(set1)[0]
        # Use the same parsing logic as in subsonic.py
        split_str = single_artist_str.replace(" & ", ", ").replace(" + ", ", ")
        split_set = {a.strip() for a in split_str.split(",")}
        if split_set == set2:
            return 1.0

    if len(set2) == 1 and len(set1) > 1:
        single_artist_str = list(set2)[0]
        split_str = single_artist_str.replace(" & ", ", ").replace(" + ", ", ")
        split_set = {a.strip() for a in split_str.split(",")}
        if split_set == set1:
            return 1.0

    # 3. Check if one is a subset of the other (for featured artist handling)
    # This handles cases where one service lists featured artists separately
    # and another includes them in the title
    if set1.issubset(set2) or set2.issubset(set1):
        # If one is a subset, give high similarity but not perfect
        # to prefer exact matches when available
        return 0.95

    # 4. Fallback to SequenceMatcher on sorted, concatenated strings
    sorted_artists1 = sorted(list(set1))
    sorted_artists2 = sorted(list(set2))
    sequence_sim = similarity(", ".join(sorted_artists1), ", ".join(sorted_artists2))

    return max(jaccard_sim, sequence_sim)


def get_best_match(
    source: Album | Track,
    candidates: list[Album | Track],
    min_similarity: float = 0.8,
) -> tuple[Album | Track | None, float]:
    """
    Find the best matching album or track from a list of candidates, with
    remaster-aware logic.

    Returns:
        Tuple of (best_match, similarity_score)
        - best_match: The best matching album/track or None if no match found
        - similarity_score: The similarity score of the best match (0.0 if no match)
    """
    best_match = None
    best_score = 0.0

    source_base_title, _, source_remaster = parse_remaster_info(source.title)

    for candidate in candidates:
        artist_sim = _calculate_artist_similarity(source.artists, candidate.artists)

        candidate_base_title, _, candidate_remaster = parse_remaster_info(
            candidate.title
        )

        # Calculate title similarity based on base titles
        title_sim = similarity(source_base_title, candidate_base_title)

        # Apply remaster penalty if one has remaster info and the other doesn't
        remaster_penalty = 0.0
        if bool(source_remaster) != bool(candidate_remaster):
            # Soundtracks: no penalty - one version might not have "(Original Soundtrack)" suffix
            if source_remaster == "soundtrack" or candidate_remaster == "soundtrack":
                pass
            else:
                # Non-soundtrack remaster mismatch: apply penalty instead of skipping
                # This allows matching when only remastered version is available,
                # but prefers exact remaster state matches when available
                remaster_penalty = 0.15

        if artist_sim >= min_similarity and title_sim >= min_similarity:
            combined_score = (artist_sim + title_sim) / 2
            # Apply remaster penalty after combining scores
            combined_score -= remaster_penalty

            if combined_score > best_score:
                best_score = combined_score
                best_match = candidate

                # Early exit optimization: if we found a perfect match, no need to continue
                if combined_score == 1.0:
                    break

    return best_match, best_score


def normalize_string(s: str) -> str:
    """Normalize a string for better matching.

    Args:
        s: String to normalize

    Returns:
        Normalized string
    """
    import re

    # Convert to lowercase
    s = s.lower()

    # Remove special characters and extra whitespace
    s = re.sub(r"[^\w\s]", "", s)
    s = re.sub(r"\s+", " ", s).strip()

    return s


def normalized_similarity(a: str, b: str) -> float:
    """Calculate similarity between two strings after normalization.

    Args:
        a: First string
        b: Second string

    Returns:
        Similarity ratio between 0.0 and 1.0
    """
    return similarity(normalize_string(a), normalize_string(b))


def has_remaster_info(title: str) -> bool:
    """Check if a title contains remaster-related information.

    Args:
        title: Album title to check

    Returns:
        True if title contains remaster keywords
    """
    import re

    # Pattern to match remaster-related keywords
    remaster_pattern = r"\b(remaster|remastered|edition|deluxe|expanded|extended|revised|reissue|re-issue|anniversary)\b"
    return bool(re.search(remaster_pattern, title.lower()))


@lru_cache(maxsize=2048)
def parse_remaster_info(title: str) -> tuple[str, str | None, str]:
    """Parse remaster information from an album title.

    Args:
        title: Album title to parse

    Returns:
        Tuple of (base_title, year, remaster_type)
        - base_title: Title without remaster suffixes
        - year: Year if found (e.g., "2015"), None otherwise
        - remaster_type: Type of remaster (e.g., "remaster", "edition")
    """
    import re

    # Pattern to match various remaster/soundtrack formats with optional years
    # Check soundtrack patterns first (they don't capture groups)
    soundtrack_patterns = [
        r"\s*\((?:original\s+)?(?:game\s+)?soundtrack\)",
        r"\s*\((?:original\s+)?(?:motion\s+picture\s+)?soundtrack\)",
        r"\s*\((?:ost|o\.s\.t\.)\)",
    ]

    for pattern in soundtrack_patterns:
        match = re.search(pattern, title, re.IGNORECASE)
        if match:
            base_title = title[: match.start()].strip()
            return base_title, None, "soundtrack"

    # Check remaster patterns
    remaster_patterns = [
        r"\s*\([^)]*?(\d{4})?\s*(remaster|remastered|edition|deluxe|expanded|extended|revised|reissue|re-issue|anniversary)[^)]*\)",
        r"\s*-\s*(\d{4})?\s*(remaster|remastered|edition|deluxe|expanded|extended|revised|reissue|re-issue|anniversary).*",
        r"\s+(\d{4})?\s*(remaster|remastered|edition|deluxe|expanded|extended|revised|reissue|re-issue|anniversary).*$",
    ]

    base_title = title
    year = None
    remaster_type = ""

    for pattern in remaster_patterns:
        match = re.search(pattern, title, re.IGNORECASE)
        if match:
            # Remove the matched remaster part from title
            base_title = title[: match.start()].strip()
            year = match.group(1) if match.group(1) else None
            remaster_type = match.group(2).lower()
            break

    return base_title, year, remaster_type
