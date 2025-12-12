"""
BitAds V3 Core - Miner Scoring Module

A minimal, testable core for computing BitAds Miner Scores.
"""
from pathlib import Path

# Read version from pyproject.toml (single source of truth)
def _get_version():
    """Get version from pyproject.toml or package metadata."""
    # Try to get version from installed package metadata first
    try:
        from importlib.metadata import version, PackageNotFoundError
        return version("bitads-v3-core")
    except (PackageNotFoundError, ImportError):
        pass
    
    # Fallback: read from pyproject.toml when in development
    # pyproject.toml is in the parent directory (project root)
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    if pyproject_path.exists():
        try:
            # Python 3.11+ has tomllib in stdlib
            import tomllib
            with open(pyproject_path, "rb") as f:
                pyproject = tomllib.load(f)
                return pyproject.get("project", {}).get("version", "0.0.0")
        except ImportError:
            # Python < 3.11, try tomli or fallback to regex
            try:
                import tomli as tomllib
                with open(pyproject_path, "rb") as f:
                    pyproject = tomllib.load(f)
                    return pyproject.get("project", {}).get("version", "0.0.0")
            except ImportError:
                # Last resort: simple regex parsing
                import re
                content = pyproject_path.read_text()
                match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
                return match.group(1) if match else "0.0.0"
    
    return "0.0.0"

__version__ = _get_version()

# Note: Import domain and app modules directly when needed:
# from bitads_v3_core.domain import models, math_ops, percentiles
# from bitads_v3_core.app import scoring, ports

__all__ = [
    "__version__",
]

