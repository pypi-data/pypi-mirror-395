from importlib.metadata import version, PackageNotFoundError


def get_version():
    """Get the package version from metadata."""
    try:
        return version("aristotlelib")
    except PackageNotFoundError:
        return "unknown"
