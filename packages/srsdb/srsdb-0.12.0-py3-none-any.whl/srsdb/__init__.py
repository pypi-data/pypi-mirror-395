"""
SRSDB - Spaced Repetition System Database

A Python library for managing SRS (Spaced Repetition System) learning data
using SQLite with support for different SRS algorithms.
"""

from .srs_database import SrsDatabase
from .fsrs_database import FsrsDatabase, FsrsKnobs

try:
    from .ebisu_database import EbisuDatabase, EbisuKnobs
    __all__ = ["SrsDatabase", "FsrsDatabase", "FsrsKnobs", "EbisuDatabase", "EbisuKnobs"]
except ImportError:
    # ebisu package not installed
    __all__ = ["SrsDatabase", "FsrsDatabase", "FsrsKnobs"]

__version__ = "0.12.0"
