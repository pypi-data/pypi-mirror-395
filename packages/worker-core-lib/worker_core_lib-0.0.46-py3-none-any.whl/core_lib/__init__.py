"""
Core library for worker services.

This package contains the core functionality for worker services in the Mesh-Sync platform.
"""

import importlib.metadata

try:
    # Try the normalized package name (PyPI uses hyphens, Python normalizes to underscores)
    __version__ = importlib.metadata.version("worker-core-lib")
except importlib.metadata.PackageNotFoundError:
    try:
        # Try the underscore version
        __version__ = importlib.metadata.version("worker_core_lib")
    except importlib.metadata.PackageNotFoundError:
        __version__ = "0.0.1"  # Fallback for development
