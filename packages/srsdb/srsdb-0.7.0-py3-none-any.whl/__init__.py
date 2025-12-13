"""
SRSDB - Spaced Repetition System Database

A Python library for managing SRS (Spaced Repetition System) learning data
using SQLite with support for different SRS algorithms.
"""

from .srs_database import SrsDatabase
from .fsrs_database import FsrsDatabase

try:
    from .ebisu_database import EbisuDatabase
    __all__ = ["SrsDatabase", "FsrsDatabase", "EbisuDatabase"]
except ImportError:
    # ebisu package not installed
    __all__ = ["SrsDatabase", "FsrsDatabase"]

__version__ = "0.7.0"
