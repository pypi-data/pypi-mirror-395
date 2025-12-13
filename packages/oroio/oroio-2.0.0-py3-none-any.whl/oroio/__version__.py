"""Version management for oroio CLI

Syncs major version with backend API, maintains independent patch version.
"""

from pathlib import Path

# Try to read major version from root VERSION file
def _get_version():
    """Read version from VERSION file or use default"""
    # Default version
    major, minor = 2, 0
    cli_patch = 0
    
    # Try to find VERSION file in project root (3 levels up)
    version_file = Path(__file__).parent.parent.parent.parent / "VERSION"
    
    if version_file.exists():
        try:
            for line in version_file.read_text(encoding='utf-8').splitlines():
                line = line.strip()
                if line.startswith("MAJOR="):
                    major = int(line.split("=")[1])
                elif line.startswith("MINOR="):
                    minor = int(line.split("=")[1])
        except Exception:
            pass  # Use default if parsing fails
    
    return f"{major}.{minor}.{cli_patch}"


__version__ = _get_version()
