# src/duplifinder/config.py

"""Configuration management with Pydantic validation."""

from __future__ import annotations
from pathlib import Path
from typing import Dict, List, Set, Optional

# MODIFIED: Import field_validator and ValidationInfo, remove validator
from pydantic import BaseModel, Field, field_validator, ValidationInfo
import yaml
from .exceptions import ConfigError

DEFAULT_IGNORES = {".git", "__pycache__", ".venv", "venv", "build", "dist", "node_modules"}
KNOWN_TYPES = {"class", "def", "async_def"}


class Config(BaseModel):
    """Validated configuration model."""

    root: Path = Field(default_factory=lambda: Path("."), description="Scan root directory")
    ignore_dirs: Set[str] = Field(default_factory=lambda: DEFAULT_IGNORES.copy())
    exclude_patterns: Set[str] = Field(default_factory=set)
    exclude_names: Set[str] = Field(default_factory=set)  # Raw patterns; compiled in processors
    types_to_search: Set[str] = Field(default_factory=lambda: {"class", "def", "async_def"})
    filter_names: Set[str] = Field(default_factory=set)
    filter_regexes: List[str] = Field(default_factory=list)
    pattern_regexes: List[str] = Field(default_factory=list)
    search_specs: List[str] = Field(default_factory=list)
    search_mode: bool = False
    token_mode: bool = False
    similarity_threshold: float = Field(0.8, ge=0.0, le=1.0)
    dup_threshold: float = Field(0.1, ge=0.0, le=1.0)
    json_output: bool = False
    fail_on_duplicates: bool = False
    min_occurrences: int = Field(2, ge=1)
    verbose: bool = False
    parallel: bool = False
    use_multiprocessing: bool = False
    max_workers: int | None = Field(None, ge=1)
    preview: bool = False
    audit_enabled: bool = Field(False, description="Enable audit logging for file access trails")
    audit_log_path: Path = Field(
        default_factory=lambda: Path(".duplifinder_audit.jsonl"),
        description="Path for audit log output (JSONL format)"
    )
    respect_gitignore: bool = Field(True, description="Auto-respect .gitignore patterns for exclusions")
    watch_mode: bool = Field(False, description="Enable watch mode for live scanning")

    # Language Support
    extensions: Set[str] = Field(default_factory=lambda: {"py", "js", "ts", "java"}, description="File extensions to scan")

    # Caching
    enable_cache: bool = Field(False, description="Enable file result caching")
    cache_path: Path = Field(
        default_factory=lambda: Path(".duplifinder_cache.json"),
        description="Path to the cache file"
    )

    # HTML Report
    html_report: Optional[Path] = Field(None, description="Path to generate HTML report")

    # MODIFIED: Use @field_validator
    @field_validator("types_to_search")
    def validate_types(cls, v: Set[str]) -> Set[str]:
        invalid = v - KNOWN_TYPES
        if invalid:
            raise ConfigError(f"Unsupported types: {', '.join(invalid)}. Supported: {', '.join(KNOWN_TYPES)}")
        return v

    # MODIFIED: Use @field_validator with mode='before' (for pre=True)
    @field_validator("filter_regexes", "pattern_regexes", "exclude_names", mode='before')
    def compile_regexes(cls, v: List[str]) -> List[str]:
        import re
        compiled = []
        for pat in v:
            try:
                re.compile(pat)
                compiled.append(pat)
            except re.error as e:
                raise ConfigError(f"Invalid regex '{pat}': {e}")
        return compiled

    # MODIFIED: Use @field_validator with mode='before' (for pre=True)
    @field_validator("search_specs", mode='before')
    def validate_search_specs(cls, v: List[str]) -> List[str]:
        if not v:
            return v
        import re
        valid_types = KNOWN_TYPES
        for spec in v:
            parts = spec.strip().split(maxsplit=1)
            if len(parts) != 2:
                raise ConfigError(f"Invalid search spec '{spec}': Must be 'type name'.")
            typ, name = parts
            if typ not in valid_types:
                raise ConfigError(f"Invalid type '{typ}' in '{spec}': {', '.join(valid_types)}")
            if not name:
                raise ConfigError(f"Empty name in '{spec}'.")
        return v

    # MODIFIED: Use @field_validator and ValidationInfo to access other field data
    @field_validator("audit_log_path")
    def validate_audit_path(cls, v: Path, info: ValidationInfo) -> Path:
        # Access 'values' dict via info.data
        if info.data.get("audit_enabled") and not isinstance(v, Path):
            v = Path(v)
        if info.data.get("audit_enabled") and v.exists() and not v.parent.is_dir():
            raise ConfigError(f"Audit log path '{v}' parent directory does not exist")
        return v


def load_config_file(path: str | Path) -> Dict:
    """Load YAML config with error handling."""
    try:
        with open(path, "r") as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        raise ConfigError(f"Failed to load config '{path}': {e}")
