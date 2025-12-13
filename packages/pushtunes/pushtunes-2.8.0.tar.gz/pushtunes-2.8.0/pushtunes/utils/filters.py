"""Filtering utilities for pushtunes sync operations."""

import re
import os
from dataclasses import dataclass
from enum import Enum
from pushtunes.models.album import Album
from pushtunes.models.track import Track


class FilterAction(Enum):
    """Action to take when pattern matches."""

    INCLUDE = "include"
    EXCLUDE = "exclude"


@dataclass
class FilterPattern:
    """Represents a single filter pattern.

    Multiple fields within a pattern use AND logic (all must match).
    Multiple patterns use the include-first logic (see filter classes).
    """

    fields: dict[str, re.Pattern]  # field name -> compiled regex
    action: FilterAction  # include or exclude

    @property
    def pattern_str(self) -> str:
        """Get a string representation of the pattern for display."""
        parts = [f"{field}:'{regex.pattern}'" for field, regex in self.fields.items()]
        return " ".join(parts)


class AlbumFilter:
    """Album filtering system supporting regex patterns on artist/album fields.

    Supports include/exclude patterns with the following semantics:
    - Within a pattern: AND logic (all fields must match)
    - Between patterns: Include-first (start empty, add includes, remove excludes)
    - If no includes: Start with all items, remove excludes
    """

    def __init__(self, patterns: list[str] | None = None, action: FilterAction = FilterAction.INCLUDE):
        """Initialize filter with pattern strings.

        Args:
            patterns: list of pattern strings in format "field:'regex'" or "field:'regex' field:'regex'"
            action: Default action for patterns (INCLUDE or EXCLUDE)
        """
        self.patterns: list[FilterPattern] = []
        self._default_action = action
        if patterns:
            for pattern in patterns:
                self.add_pattern(pattern, action=action)

    def add_pattern(self, pattern_str: str, action: FilterAction = None) -> None:
        """Add a filter pattern.

        Args:
            pattern_str: Pattern string in format "field:'regex'" or "field:'regex' field:'regex'"
            action: Action to take when pattern matches (uses default if not specified)

        Raises:
            ValueError: If pattern format is invalid
        """
        if action is None:
            action = self._default_action
        pattern = self._parse_pattern(pattern_str, action)
        self.patterns.append(pattern)

    def _parse_pattern(self, pattern_str: str, action: FilterAction) -> FilterPattern:
        """Parse a pattern string into a FilterPattern.

        Supports multiple field:'regex' pairs in one pattern (AND logic).

        Args:
            pattern_str: Pattern like "artist:'.*dead.*'" or "artist:'Opeth' album:'Morningrise'"
            action: Action to take when pattern matches

        Returns:
            FilterPattern object

        Raises:
            ValueError: If pattern format is invalid
        """
        pattern_str = pattern_str.strip()
        fields = {}

        # Match all field:'regex' pairs in the string
        matches = re.finditer(r"(artist|album|track):'(.+?)'(?:\s|$)", pattern_str, re.IGNORECASE)

        for match in matches:
            field = match.group(1).lower()
            regex_str = match.group(2)

            # Validate that field is appropriate for albums
            if field not in ("artist", "album"):
                raise ValueError(f"Invalid field '{field}' for album filter. Use 'artist' or 'album'.")

            try:
                compiled_regex = re.compile(regex_str, re.IGNORECASE)
            except re.error as e:
                raise ValueError(f"Invalid regex pattern '{regex_str}': {e}")

            fields[field] = compiled_regex

        if not fields:
            raise ValueError(
                f"Invalid pattern format: {pattern_str}. Expected format: field:'regex' [field:'regex' ...]"
            )

        return FilterPattern(fields=fields, action=action)

    def _matches_pattern(self, item: Album, pattern: FilterPattern) -> bool:
        """Check if an item matches a specific pattern (AND logic for fields).

        Args:
            item: Album to check
            pattern: FilterPattern to match against

        Returns:
            True if all fields in pattern match the item
        """
        for field, regex in pattern.fields.items():
            if field == "artist":
                if not regex.search(item.artist):
                    return False
            elif field == "album":
                if not regex.search(item.title):
                    return False

        return True

    def should_filter_out(self, item: Album) -> bool:
        """Determine if item should be filtered out using include-first logic.

        Logic:
        1. If has includes: item must match at least one include AND not match any exclude
        2. If no includes: item must not match any exclude

        Args:
            item: Album to check

        Returns:
            True if item should be filtered out (not included in results)
        """
        if not self.patterns:
            return False

        include_patterns = [p for p in self.patterns if p.action == FilterAction.INCLUDE]
        exclude_patterns = [p for p in self.patterns if p.action == FilterAction.EXCLUDE]

        # If we have includes, item must match at least one
        if include_patterns:
            matches_include = any(self._matches_pattern(item, p) for p in include_patterns)
            if not matches_include:
                return True  # Filter out - doesn't match any include

        # Check if item matches any exclude
        matches_exclude = any(self._matches_pattern(item, p) for p in exclude_patterns)
        if matches_exclude:
            return True  # Filter out - matches an exclude

        return False  # Include item

    def matches(self, item: Album) -> bool:
        """Check if an item matches any of the filter patterns (legacy method).

        This method maintains backward compatibility with the old OR-logic behavior.
        For old-style filters (all INCLUDE action), returns True if ANY pattern matches.

        Args:
            item: Album to check

        Returns:
            True if item matches any pattern (for backward compatibility)
        """
        if not self.patterns:
            return True

        # Check if this is a legacy filter (all patterns are includes)
        if all(p.action == FilterAction.INCLUDE for p in self.patterns):
            # Old OR logic: match any pattern
            return any(self._matches_pattern(item, p) for p in self.patterns)

        # New logic: invert should_filter_out for consistency
        return not self.should_filter_out(item)

    @classmethod
    def from_patterns_file(cls, file_path: str) -> "AlbumFilter":
        """Create filter from file with +/- prefixed patterns (new format).

        File format:
            + artist:'Taylor Swift'
            - artist:'Volkor X'
            - artist:'Opeth' album:'Still Life'
            + artist:'Opeth' album:'Morningrise'

        Rules are processed sequentially. Later rules can override earlier ones.

        Args:
            file_path: Path to file with prefixed patterns

        Returns:
            AlbumFilter instance

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file contains invalid patterns
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Filter file not found: {file_path}")

        filter_obj = cls()

        with open(file_path, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                original_line = line
                line = line.strip()

                # Skip empty lines and comments
                if not line or line.startswith("#"):
                    continue

                # Parse prefix
                if line.startswith("+"):
                    action = FilterAction.INCLUDE
                    pattern_str = line[1:].strip()
                elif line.startswith("-"):
                    action = FilterAction.EXCLUDE
                    pattern_str = line[1:].strip()
                else:
                    raise ValueError(
                        f"Invalid pattern on line {line_num}: Missing +/- prefix. "
                        f"Expected format: '+ pattern' or '- pattern'"
                    )

                try:
                    filter_obj.add_pattern(pattern_str, action=action)
                except ValueError as e:
                    raise ValueError(f"Invalid pattern on line {line_num}: {e}")

        return filter_obj

    def get_summary(self) -> str:
        """Get a human-readable summary of the filter patterns.

        Returns:
            Summary string
        """
        if not self.patterns:
            return "No filters (all albums included)"

        include_patterns = [p for p in self.patterns if p.action == FilterAction.INCLUDE]
        exclude_patterns = [p for p in self.patterns if p.action == FilterAction.EXCLUDE]

        summary_parts = []

        if include_patterns:
            include_strs = [p.pattern_str for p in include_patterns]
            summary_parts.append(f"Include: {', '.join(include_strs)}")

        if exclude_patterns:
            exclude_strs = [p.pattern_str for p in exclude_patterns]
            summary_parts.append(f"Exclude: {', '.join(exclude_strs)}")

        return "; ".join(summary_parts)

    def __len__(self) -> int:
        """Return number of patterns."""
        return len(self.patterns)

    def __bool__(self) -> bool:
        """Return True if filter has patterns."""
        return bool(self.patterns)


class TrackFilter:
    """Track filtering system supporting regex patterns on artist/track/album fields.

    Supports include/exclude patterns with the following semantics:
    - Within a pattern: AND logic (all fields must match)
    - Between patterns: Include-first (start empty, add includes, remove excludes)
    - If no includes: Start with all items, remove excludes
    """

    def __init__(self, patterns: list[str] | None = None, action: FilterAction = FilterAction.INCLUDE):
        """Initialize filter with pattern strings.

        Args:
            patterns: list of pattern strings in format "field:'regex'" or "field:'regex' field:'regex'"
            action: Default action for patterns (INCLUDE or EXCLUDE)
        """
        self.patterns: list[FilterPattern] = []
        self._default_action = action
        if patterns:
            for pattern in patterns:
                self.add_pattern(pattern, action=action)

    def add_pattern(self, pattern_str: str, action: FilterAction = None) -> None:
        """Add a filter pattern.

        Args:
            pattern_str: Pattern string in format "field:'regex'" or "field:'regex' field:'regex'"
            action: Action to take when pattern matches (uses default if not specified)

        Raises:
            ValueError: If pattern format is invalid
        """
        if action is None:
            action = self._default_action
        pattern = self._parse_pattern(pattern_str, action)
        self.patterns.append(pattern)

    def _parse_pattern(self, pattern_str: str, action: FilterAction) -> FilterPattern:
        """Parse a pattern string into a FilterPattern.

        Supports multiple field:'regex' pairs in one pattern (AND logic).

        Args:
            pattern_str: Pattern like "artist:'.*dead.*'" or "artist:'Opeth' track:'Deliverance'"
            action: Action to take when pattern matches

        Returns:
            FilterPattern object

        Raises:
            ValueError: If pattern format is invalid
        """
        pattern_str = pattern_str.strip()
        fields = {}

        # Match all field:'regex' pairs in the string
        matches = re.finditer(r"(artist|track|album):'(.+?)'(?:\s|$)", pattern_str, re.IGNORECASE)

        for match in matches:
            field = match.group(1).lower()
            regex_str = match.group(2)

            try:
                compiled_regex = re.compile(regex_str, re.IGNORECASE)
            except re.error as e:
                raise ValueError(f"Invalid regex pattern '{regex_str}': {e}")

            fields[field] = compiled_regex

        if not fields:
            raise ValueError(
                f"Invalid pattern format: {pattern_str}. Expected format: field:'regex' [field:'regex' ...]"
            )

        return FilterPattern(fields=fields, action=action)

    def _matches_pattern(self, item: Track, pattern: FilterPattern) -> bool:
        """Check if an item matches a specific pattern (AND logic for fields).

        Args:
            item: Track to check
            pattern: FilterPattern to match against

        Returns:
            True if all fields in pattern match the item
        """
        for field, regex in pattern.fields.items():
            if field == "artist":
                if not regex.search(item.artist):
                    return False
            elif field == "track":
                if not regex.search(item.title):
                    return False
            elif field == "album":
                # Album is optional, skip if not present
                if item.album and not regex.search(item.album):
                    return False
                elif not item.album:
                    # If track has no album but pattern requires it, no match
                    return False

        return True

    def should_filter_out(self, item: Track) -> bool:
        """Determine if item should be filtered out using include-first logic.

        Logic:
        1. If has includes: item must match at least one include AND not match any exclude
        2. If no includes: item must not match any exclude

        Args:
            item: Track to check

        Returns:
            True if item should be filtered out (not included in results)
        """
        if not self.patterns:
            return False

        include_patterns = [p for p in self.patterns if p.action == FilterAction.INCLUDE]
        exclude_patterns = [p for p in self.patterns if p.action == FilterAction.EXCLUDE]

        # If we have includes, item must match at least one
        if include_patterns:
            matches_include = any(self._matches_pattern(item, p) for p in include_patterns)
            if not matches_include:
                return True  # Filter out - doesn't match any include

        # Check if item matches any exclude
        matches_exclude = any(self._matches_pattern(item, p) for p in exclude_patterns)
        if matches_exclude:
            return True  # Filter out - matches an exclude

        return False  # Include item

    def matches(self, item: Track) -> bool:
        """Check if a track matches any of the filter patterns (legacy method).

        This method maintains backward compatibility with the old OR-logic behavior.
        For old-style filters (all INCLUDE action), returns True if ANY pattern matches.

        Args:
            item: Track to check

        Returns:
            True if track matches any pattern (for backward compatibility)
        """
        if not self.patterns:
            return False

        # Check if this is a legacy filter (all patterns are includes)
        if all(p.action == FilterAction.INCLUDE for p in self.patterns):
            # Old OR logic: match any pattern
            return any(self._matches_pattern(item, p) for p in self.patterns)

        # New logic: invert should_filter_out for consistency
        return not self.should_filter_out(item)

    @classmethod
    def from_patterns_file(cls, file_path: str) -> "TrackFilter":
        """Create filter from file with +/- prefixed patterns (new format).

        File format:
            + artist:'Taylor Swift'
            - artist:'Volkor X'
            - artist:'Opeth' track:'Deliverance'
            + artist:'Opeth' track:'Ghost of Perdition'

        Rules are processed sequentially. Later rules can override earlier ones.

        Args:
            file_path: Path to file with prefixed patterns

        Returns:
            TrackFilter instance

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file contains invalid patterns
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Filter file not found: {file_path}")

        filter_obj = cls()

        with open(file_path, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                original_line = line
                line = line.strip()

                # Skip empty lines and comments
                if not line or line.startswith("#"):
                    continue

                # Parse prefix
                if line.startswith("+"):
                    action = FilterAction.INCLUDE
                    pattern_str = line[1:].strip()
                elif line.startswith("-"):
                    action = FilterAction.EXCLUDE
                    pattern_str = line[1:].strip()
                else:
                    raise ValueError(
                        f"Invalid pattern on line {line_num}: Missing +/- prefix. "
                        f"Expected format: '+ pattern' or '- pattern'"
                    )

                try:
                    filter_obj.add_pattern(pattern_str, action=action)
                except ValueError as e:
                    raise ValueError(f"Invalid pattern on line {line_num}: {e}")

        return filter_obj

    def get_summary(self) -> str:
        """Get a human-readable summary of the filter patterns.

        Returns:
            Summary string
        """
        if not self.patterns:
            return "No filters (all tracks included)"

        include_patterns = [p for p in self.patterns if p.action == FilterAction.INCLUDE]
        exclude_patterns = [p for p in self.patterns if p.action == FilterAction.EXCLUDE]

        summary_parts = []

        if include_patterns:
            include_strs = [p.pattern_str for p in include_patterns]
            summary_parts.append(f"Include: {', '.join(include_strs)}")

        if exclude_patterns:
            exclude_strs = [p.pattern_str for p in exclude_patterns]
            summary_parts.append(f"Exclude: {', '.join(exclude_strs)}")

        return "; ".join(summary_parts)

    def __len__(self) -> int:
        """Return number of patterns."""
        return len(self.patterns)

    def __bool__(self) -> bool:
        """Return True if filter has patterns."""
        return bool(self.patterns)
