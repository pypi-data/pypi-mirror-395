"""Profile configuration manager for pushtunes."""

import json
import os
import sys
from pathlib import Path
from typing import Any

from platformdirs import PlatformDirs

# Import YAML if available
try:
    import yaml

    HAS_YAML = True
except ImportError:
    HAS_YAML = False

# Import TOML - use tomllib for Python 3.11+, otherwise tomli
if sys.version_info >= (3, 11):
    import tomllib

    HAS_TOML = True
else:
    try:
        import tomli as tomllib

        HAS_TOML = True
    except ImportError:
        HAS_TOML = False


def _find_profile_file(profile_path: str) -> Path | None:
    """
    Find a profile file by searching in order:
    1. Absolute path (if provided)
    2. Current working directory
    3. ~/.config/pushtunes/ (using platformdirs)

    Args:
        profile_path: The profile filename or path

    Returns:
        Path object if file found, None otherwise
    """
    # Try as absolute or relative path first
    candidate = Path(profile_path)
    if candidate.is_absolute() and candidate.exists():
        return candidate

    # Try in current working directory
    cwd_path = Path.cwd() / profile_path
    if cwd_path.exists():
        return cwd_path

    # Try in config directory
    dirs = PlatformDirs(appname="pushtunes", appauthor="psy-q")
    config_path = Path(dirs.user_config_dir) / profile_path
    if config_path.exists():
        return config_path

    return None


def _load_profile_file(profile_path: Path) -> dict[str, Any]:
    """
    Load a profile file and return its contents as a dict.
    Auto-detects format by extension (.yaml, .json, .toml).

    Args:
        profile_path: Path to the profile file

    Returns:
        Dictionary with profile contents

    Raises:
        ValueError: If file format is unsupported or required library is missing
        Exception: If file parsing fails
    """
    suffix = profile_path.suffix.lower()

    if suffix in [".yaml", ".yml"]:
        if not HAS_YAML:
            raise ValueError(
                "YAML support requires PyYAML. Install with: pip install pyyaml"
            )
        with open(profile_path, "r") as f:
            return yaml.safe_load(f) or {}

    elif suffix == ".json":
        with open(profile_path, "r") as f:
            return json.load(f)

    elif suffix == ".toml":
        if not HAS_TOML:
            raise ValueError(
                "TOML support requires tomli for Python <3.11. Install with: pip install tomli"
            )
        with open(profile_path, "rb") as f:
            return tomllib.load(f)

    else:
        raise ValueError(
            f"Unsupported profile format: {suffix}. Supported formats: .yaml, .yml, .json, .toml"
        )


def load_profile(profile_path: str, command: str) -> dict[str, Any]:
    """
    Load a profile configuration for a specific command.

    Profiles can have command-specific sections like:
    ```toml
    [albums]
    from = "spotify"
    to = "ytm"

    [tracks]
    from = "subsonic"
    to = "csv"
    ```

    Or flat structure (all options at root level):
    ```toml
    from = "spotify"
    to = "ytm"
    ```

    Args:
        profile_path: Path or filename of the profile
        command: Command name ('albums', 'tracks', 'playlist')

    Returns:
        Dictionary with profile configuration for the command

    Raises:
        FileNotFoundError: If profile file cannot be found
        ValueError: If file format is unsupported or parsing fails
    """
    # Find the profile file
    found_path = _find_profile_file(profile_path)
    if found_path is None:
        raise FileNotFoundError(
            f"Profile not found: {profile_path}\n"
            f"Searched in:\n"
            f"  - Current directory: {Path.cwd()}\n"
            f"  - Config directory: {PlatformDirs(appname='pushtunes', appauthor='psy-q').user_config_dir}"
        )

    # Load the profile
    try:
        profile_data = _load_profile_file(found_path)
    except Exception as e:
        raise ValueError(f"Failed to parse profile {found_path}: {e}")

    # Check if profile has command-specific sections
    if command in profile_data and isinstance(profile_data[command], dict):
        return profile_data[command]

    # Otherwise return the whole profile (flat structure)
    return profile_data


def merge_with_cli_args(
    profile: dict[str, Any], cli_args: dict[str, Any]
) -> dict[str, Any]:
    """
    Merge profile configuration with CLI arguments.
    CLI arguments take precedence over profile values.

    For list values (include, exclude), CLI args are appended to profile values.

    Args:
        profile: Profile configuration dictionary
        cli_args: CLI arguments dictionary

    Returns:
        Merged configuration dictionary
    """
    merged = profile.copy()

    for key, cli_value in cli_args.items():
        # Skip None values from CLI (not explicitly provided)
        if cli_value is None:
            continue

        # For list values, append CLI args to profile values
        if key in ["include", "exclude"] and isinstance(cli_value, list):
            profile_list = merged.get(key, [])
            if isinstance(profile_list, list):
                merged[key] = profile_list + cli_value
            else:
                merged[key] = cli_value
        else:
            # CLI value overrides profile value
            merged[key] = cli_value

    return merged
