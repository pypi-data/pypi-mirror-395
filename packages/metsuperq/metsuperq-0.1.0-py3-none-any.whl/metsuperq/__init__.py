"""MetSuperQ package initializer."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("metsuperq")
except PackageNotFoundError:
    # Fallback for editable installs with setuptools-scm
    try:
        from metsuperq._version import __version__  # type: ignore[import-not-found]
    except ImportError:
        __version__ = "0.0.0+unknown"

# Import all submodules to make them accessible
from metsuperq import analysis, data_handling, database, integrations, monitoring, utils
from metsuperq.utils.utils import setup_logging

__all__ = [
    "analysis",
    "data_handling",
    "database",
    "integrations",
    "monitoring",
    "utils",
    "__version__",
]

setup_logging(__name__)
