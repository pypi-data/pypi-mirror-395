import importlib.metadata
import sys
import tomllib
from pathlib import Path

from secrets_safe_library import config, exceptions


def _get_version_from_pyproject() -> str | None:
    """Get version from pyproject.toml (development fallback)."""
    try:
        # Find pyproject.toml starting from this file's location
        current_path = Path(__file__)
        for parent in [current_path] + list(current_path.parents):
            pyproject_path = parent / "pyproject.toml"
            if pyproject_path.exists():
                with open(pyproject_path, "rb") as f:
                    pyproject_data = tomllib.load(f)
                    # Try tool.poetry.version first (Poetry style)
                    if "tool" in pyproject_data and "poetry" in pyproject_data["tool"]:
                        return pyproject_data["tool"]["poetry"].get("version")
                    # Try project.version (PEP 621 style)
                    if "project" in pyproject_data:
                        return pyproject_data["project"].get("version")
                break
    except (FileNotFoundError, PermissionError, tomllib.TOMLDecodeError, KeyError):
        # Expected errors when pyproject.toml is missing, unreadable, or malformed
        pass
    return None


def _get_version_from_pyinstaller_metadata() -> str | None:
    """Get version from PyInstaller bundle metadata."""
    if not (getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS")):
        return None

    # Try to get version from the bundled package metadata
    try:
        return importlib.metadata.version("beyondtrust-bips-cli")
    except importlib.metadata.PackageNotFoundError:
        # Expected when package metadata is not available in bundle
        pass

    return None


def get_cli_version(app) -> str | None:
    """
    Get CLI version with simplified approach prioritizing standard Python packaging.

    Priority order:
    1. Package metadata (installed package)
    2. PyInstaller bundle metadata
    3. Version module (PyInstaller fallback)
    4. pyproject.toml (development fallback)
    """

    # Try package metadata first (works for installed packages)
    try:
        version = importlib.metadata.version("beyondtrust-bips-cli")
        return version
    except importlib.metadata.PackageNotFoundError:
        pass

    # Try PyInstaller bundle metadata
    version = _get_version_from_pyinstaller_metadata()
    if version:
        return version

    # Try version module (reliable for PyInstaller)
    try:
        from ps_cli.__version__ import __version__

        return __version__
    except (ImportError, AttributeError):
        # Expected when __version__.py doesn't exist or __version__ is not defined
        pass

    # Final fallback: read from pyproject.toml (development)
    version = _get_version_from_pyproject()
    if version:
        return version

    # Log error if all methods failed
    if app and app.log:
        app.log.error("It was not possible to read CLI version from any source")
    return None


def get_api_version(app) -> str | None:
    """
    Retrieve the API version using the Configuration class.
    """
    try:
        config_obj = config.Configuration(
            authentication=app.authentication, logger=app.log.logger
        )
        version_info = config_obj.get_version()
        version = version_info.get("Version", "Unknown") if version_info else "Unknown"
        return version
    except exceptions.LookupError as e:
        app.log.error(f"Error retrieving API version: {e}")
        return None
