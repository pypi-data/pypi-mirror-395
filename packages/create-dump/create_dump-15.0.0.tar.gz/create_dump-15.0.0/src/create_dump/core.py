# src/create_dump/core.py

"""Core models and configuration.

Pydantic models for validation, config loading.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, field_validator

from .logging import logger  # ⚡ REFACTOR: Corrected import from .utils
import toml

# Canonical pattern for dump artifacts (imported/used by modules)
DEFAULT_DUMP_PATTERN = r".*_all_create_dump_\d{8}_\d{6}\.(md(\.gz)?|sha256)$"


class Config(BaseModel):
    """Validated config with env support."""

    default_includes: List[str] = Field(default_factory=list)
    default_excludes: List[str] = Field(default_factory=list)
    use_gitignore: bool = True
    git_meta: bool = True
    max_file_size_kb: Optional[int] = Field(None, ge=0)
    dest: Optional[Path] = Field(None, description="Default output destination (CLI --dest overrides)")
    dump_pattern: str = Field(DEFAULT_DUMP_PATTERN, description="Canonical regex for dump artifacts")
    excluded_dirs: List[str] = Field(
        default_factory=lambda: [
            "__pycache__", ".git", ".venv", "venv", "myenv", ".mypy_cache",
            ".pytest_cache", ".idea", "node_modules", "build", "dist",
            "vendor", ".gradle", ".tox", "eggs", ".egg-info",
        ]
    )
    metrics_port: int = Field(8000, ge=1, le=65535)

    # ⚡ NEW: v8 feature flags
    git_ls_files: bool = Field(False, description="Use 'git ls-files' for file collection.")
    scan_secrets: bool = Field(False, description="Enable secret scanning.")
    hide_secrets: bool = Field(False, description="Redact found secrets (requires scan_secrets=True).")
    custom_secret_patterns: List[str] = Field(default_factory=list, description="List of custom regex patterns to scan for secrets.")


    @field_validator("max_file_size_kb", mode="before")
    @classmethod
    def non_negative(cls, v):
        if v is not None and v < 0:
            raise ValueError("must be non-negative")
        return v

    @field_validator("dest", mode="before")
    @classmethod
    def validate_dest(cls, v):
        if v is not None:
            try:
                path = Path(v)
                if not path.name:
                    logger.warning("Empty dest path; defaulting to None.")
                    return None
                return path
            except Exception as e:
                logger.warning("Invalid dest path '%s': %s; defaulting to None.", v, e)
                return None
        return v

    @field_validator("dump_pattern", mode="after")
    @classmethod
    def validate_dump_pattern(cls, v):
        if not v or not re.match(r'.*_all_create_dump_', v):
            logger.warning("Loose or invalid dump_pattern '%s'; enforcing default: %s", v, DEFAULT_DUMP_PATTERN)
            return DEFAULT_DUMP_PATTERN
        return v


class GitMeta(BaseModel):
    branch: Optional[str] = None
    commit: Optional[str] = None


class DumpFile(BaseModel):
    path: str
    language: Optional[str] = None
    temp_path: Optional[Path] = None
    # ⚡ NEW: Support in-memory content for generated files (like DB dumps)
    content: Optional[str] = None
    error: Optional[str] = None
    todos: List[str] = Field(default_factory=list)


def has_local_config(path: Path) -> bool:
    """Checks if a directory has a local create-dump configuration file."""
    if (path / ".create_dump.toml").exists() or (path / "create_dump.toml").exists():
        return True

    pyproj = path / "pyproject.toml"
    if pyproj.exists():
        try:
            full_data = toml.load(pyproj)
            if full_data.get("tool", {}).get("create-dump"):
                return True
        except Exception:
            pass
    return False


# 🐞 FIX: Add `_cwd` parameter for testability
def load_config(path: Optional[Path] = None, _cwd: Optional[Path] = None, profile: Optional[str] = None) -> Config:
    """Loads config from [tool.create-dump] in TOML files."""
    config_data: Dict[str, Any] = {}
    
    # 🐞 FIX: Use provided _cwd for testing, or default to Path.cwd()
    cwd = _cwd or Path.cwd()

    possible_paths = (
        [path]
        if path
        else [
            Path.home() / ".create_dump.toml", # 1. Home dir
            cwd / ".create_dump.toml",         # 2. CWD .create_dump.toml
            cwd / "create_dump.toml",          # 3. CWD create_dump.toml
            cwd / "pyproject.toml",          # 4. CWD pyproject.toml
        ]
    )
    
    for conf_path in possible_paths:
        if conf_path.exists():
            try:
                full_data = toml.load(conf_path)
                config_data = full_data.get("tool", {}).get("create-dump", {})
                if config_data and profile:
                    logger.debug("Merging config profile", profile=profile)
                    profile_data = full_data.get("tool", {}).get("create-dump", {}).get("profile", {}).get(profile, {})
                    if profile_data:
                        config_data.update(profile_data)
                        logger.debug("Profile merged", keys=list(profile_data.keys()))
                    else:
                        logger.warning("Config profile not found, using base", profile=profile)

                if config_data:  # Stop if we find it
                    logger.debug("Config loaded", path=conf_path, keys=list(config_data.keys()))
                    break
            except (toml.TomlDecodeError, OSError) as e:
                logger.warning("Config load failed", path=conf_path, error=str(e))
    return Config(**config_data)


# ⚡ REFACTOR: Removed generate_default_config() function.
# This logic is now handled by the interactive wizard in cli/main.py.