from importlib import metadata


def get_version(default: str = "0.0.0") -> str:
    """Return the installed package version, falling back to a default in dev."""
    try:
        return metadata.version("agentgear-ai")
    except metadata.PackageNotFoundError:
        return default


__all__ = ["get_version"]
