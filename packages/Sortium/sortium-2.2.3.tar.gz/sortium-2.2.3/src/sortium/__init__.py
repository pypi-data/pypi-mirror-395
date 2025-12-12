"""Public API for the Sortium package."""

from .sorter import Sorter
from .file_utils import FileUtils

__version__ = "2.1.0"

__all__ = [
    "Sorter",
    "FileUtils",
    "__version__",
]
