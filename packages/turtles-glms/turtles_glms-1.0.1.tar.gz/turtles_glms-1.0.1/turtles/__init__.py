"""
Configure global settings for package.
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("turtles-glms")
except PackageNotFoundError:
    __version__ = "0.0.0"

# modules
__all__ = ["preprocess", "stats", "plotting"]
