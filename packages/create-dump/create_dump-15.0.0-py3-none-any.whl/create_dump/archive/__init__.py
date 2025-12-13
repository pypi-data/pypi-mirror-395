# src/create_dump/archive/__init__.py
"""
This package splits the archiver logic into SRP-focused components:
- Finder: Finds dump pairs.
- Packager: Groups, validates, and zips archives.
- Pruner: Enforces retention policies.
"""
from .core import ArchiveError
from .finder import ArchiveFinder
from .packager import ArchivePackager
from .pruner import ArchivePruner

__all__ = ["ArchiveFinder", "ArchivePackager", "ArchivePruner", "ArchiveError"]