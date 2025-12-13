"""Dakora Python Client SDK"""

from importlib import metadata as _metadata

from .client import Dakora

try:
    __version__ = _metadata.version("dakora")
except _metadata.PackageNotFoundError:
    __version__ = "0.0.0"

__all__ = ["Dakora", "__version__"]
