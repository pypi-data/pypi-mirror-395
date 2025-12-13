import importlib.metadata

try:
    __version__ = importlib.metadata.version("plexus-msgs-python")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"
