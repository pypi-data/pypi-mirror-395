"""
Environment Configuration Module

This module provides utilities for loading environment variables from .env files
across all tlpytools modules. It ensures consistent environment setup throughout
the package.
"""

import os
from pathlib import Path
from typing import Optional, Union, List
import warnings

try:
    from dotenv import load_dotenv

    HAS_DOTENV = True
except ImportError:
    HAS_DOTENV = False


def get_package_directory() -> Optional[Path]:
    """
    Get the tlpytools package installation directory.

    The package structure is:
    tlpytools/
    ├── .env (fallback env file)
    └── src/
        └── tlpytools/
            └── env_config.py (this file)

    Returns:
        Path to the tlpytools package root directory, or None if not found.
    """
    try:
        # Get the directory containing this file (env_config.py)
        current_file = Path(__file__).resolve()

        # Navigate up from src/tlpytools/env_config.py to tlpytools root
        # Expected path: .../tlpytools/src/tlpytools/env_config.py
        # We want to go up 3 levels: env_config.py -> tlpytools -> src -> tlpytools (root)
        package_root = current_file.parent.parent.parent

        # Verify this looks like the tlpytools package directory
        # Check if it has src/tlpytools structure
        src_dir = package_root / "src"
        tlpytools_dir = src_dir / "tlpytools"

        if src_dir.exists() and tlpytools_dir.exists():
            return package_root

        return None
    except (OSError, AttributeError):
        return None


def find_env_files(start_path: Optional[Union[str, Path]] = None) -> List[Path]:
    """
    Find .env files using simplified logic:
    1. Check current working directory
    2. Walk up parent directories until finding a .git folder (project root) or reaching filesystem root
    3. Fallback to tlpytools installation directory if no .env files found in project directories
    4. Give up on permission errors

    Args:
        start_path: Starting directory to search from. If None, starts from current working directory.

    Returns:
        List of Path objects pointing to .env files, ordered from most specific to most general
    """
    if start_path is None:
        start_path = Path.cwd()
    else:
        start_path = Path(start_path)

    env_files = []
    current_path = start_path.resolve()

    # Walk up the directory tree
    while True:
        try:
            # Check for .env file in current directory
            env_file = current_path / ".env"
            if env_file.exists() and env_file.is_file():
                env_files.append(env_file)

            # Stop if we found a .git folder (project root)
            git_folder = current_path / ".git"
            if git_folder.exists():
                break

            parent = current_path.parent
            if parent == current_path:  # Reached filesystem root
                break
            current_path = parent

        except (PermissionError, OSError):
            # Give up on permission issues or other OS errors
            break

    # If no .env files found in project directories, check tlpytools installation directory
    if not env_files:
        package_dir = get_package_directory()
        if package_dir is not None:
            package_env_file = package_dir / ".env"
            if package_env_file.exists() and package_env_file.is_file():
                env_files.append(package_env_file)

    return env_files


def load_env_file(
    env_path: Optional[Union[str, Path]] = None,
    override: bool = True,
    search_parents: bool = True,
    verbose: bool = False,
) -> bool:
    """
    Load environment variables from .env file(s) using simplified discovery logic.

    Discovery order:
    1. If env_path is specified, loads that file only
    2. If search_parents is True, searches current directory and parent directories
    3. If no .env files found in project directories, falls back to tlpytools installation directory

    Args:
        env_path: Specific path to .env file. If None, searches automatically.
        override: Whether to override existing environment variables.
        search_parents: Whether to search parent directories for .env files.
        verbose: Whether to print verbose loading information.

    Returns:
        True if at least one .env file was loaded successfully, False otherwise.
    """
    if not HAS_DOTENV:
        if verbose:
            warnings.warn(
                "python-dotenv is not installed. Environment file loading is disabled. "
                "Install with: pip install python-dotenv",
                UserWarning,
            )
        return False

    loaded_any = False

    if env_path is not None:
        # Load specific file
        env_path = Path(env_path)
        if env_path.exists():
            success = load_dotenv(env_path, override=override)
            if verbose and success:
                print(f"Loaded environment variables from: {env_path}")
            loaded_any = success
        elif verbose:
            warnings.warn(f"Specified .env file not found: {env_path}", UserWarning)
    else:
        # Auto-discover .env files using simplified logic
        if search_parents:
            env_files = find_env_files()
        else:
            env_files = []
            try:
                env_file = Path.cwd() / ".env"
                if env_file.exists():
                    env_files.append(env_file)
            except (PermissionError, OSError):
                # Give up on permission issues
                pass

        # Load files from most general to most specific (reverse order)
        # This ensures more specific .env files override more general ones
        for env_file in reversed(env_files):
            try:
                success = load_dotenv(env_file, override=override)
                if success:
                    loaded_any = True
                    if verbose:
                        print(f"Loaded environment variables from: {env_file}")
            except (PermissionError, OSError):
                # Skip files with permission issues
                if verbose:
                    warnings.warn(
                        f"Permission denied accessing: {env_file}", UserWarning
                    )
                continue

    return loaded_any


def get_env_var(
    key: str, default: Optional[str] = None, required: bool = False
) -> Optional[str]:
    """
    Get environment variable with optional default and validation.

    Args:
        key: Environment variable name.
        default: Default value if variable is not set.
        required: Whether the variable is required (raises ValueError if missing).

    Returns:
        Environment variable value or default.

    Raises:
        ValueError: If required variable is missing and no default provided.
    """
    value = os.environ.get(key, default)

    if required and (value is None or value.strip() == ""):
        raise ValueError(
            f"Required environment variable '{key}' is not set or is empty. "
            f"Please set this variable in your .env file or system environment. "
            f"See ENVIRONMENT_VARIABLES.md for details."
        )

    return value


def get_env_bool(key: str, default: bool = False, required: bool = False) -> bool:
    """
    Get environment variable as boolean with support for various boolean representations.

    Args:
        key: Environment variable name.
        default: Default value if variable is not set.
        required: Whether the variable is required (raises ValueError if missing).

    Returns:
        Boolean value parsed from environment variable.

    Raises:
        ValueError: If required variable is missing or cannot be parsed as boolean.
    """
    value = os.environ.get(key)

    if value is None:
        if required:
            raise ValueError(
                f"Required environment variable '{key}' is not set. "
                f"Please set this variable in your .env file or system environment. "
                f"See ENVIRONMENT_VARIABLES.md for details."
            )
        return default

    # Handle empty strings
    value = value.strip()
    if value == "":
        if required:
            raise ValueError(
                f"Required environment variable '{key}' is empty. "
                f"Please set this variable in your .env file or system environment. "
                f"See ENVIRONMENT_VARIABLES.md for details."
            )
        return default

    # Convert string to boolean
    # Support: true/false, 1/0, yes/no, on/off (case insensitive)
    value_lower = value.lower()

    if value_lower in ("true", "1", "yes", "on"):
        return True
    elif value_lower in ("false", "0", "no", "off"):
        return False
    else:
        raise ValueError(
            f"Environment variable '{key}' has invalid boolean value: '{value}'. "
            f"Valid values are: true/false, 1/0, yes/no, on/off (case insensitive)."
        )


# Module-level flag to track if environment has been loaded
_env_loaded = False


def ensure_env_loaded(force_reload: bool = False, verbose: bool = False) -> bool:
    """
    Ensure environment variables are loaded. Can be called multiple times safely.

    Args:
        force_reload: Force reloading even if already loaded.
        verbose: Whether to print verbose information.

    Returns:
        True if environment was loaded (or reloaded), False otherwise.
    """
    global _env_loaded

    if not _env_loaded or force_reload:
        _env_loaded = load_env_file(verbose=verbose)
        return _env_loaded

    return _env_loaded


# Auto-load environment on module import
# This ensures .env files are loaded whenever any tlpytools module is imported
_env_loaded = load_env_file(verbose=False)

# Export commonly used functions
__all__ = [
    "load_env_file",
    "find_env_files",
    "get_package_directory",
    "get_env_var",
    "get_env_bool",
    "ensure_env_loaded",
]
