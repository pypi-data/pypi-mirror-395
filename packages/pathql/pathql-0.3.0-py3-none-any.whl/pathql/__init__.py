"""
PQuery - Path querying functionality for TPath objects.

Provides a pathql-inspired API for querying files with lambda expressions.
"""

from ._pquery import (
    PathInput,
    PathLike,
    PathSequence,
    PQuery,
    pquery,
)

__all__ = [
    "pquery",
    "PQuery",
    "PathLike",
    "PathSequence",
    "PathInput",
]

__version__ = "0.3.0"
