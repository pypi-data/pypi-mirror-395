# src/duplifinder/cli.py

"""CLI argument parsing and config building."""

import argparse
import logging
import pathlib
from typing import Dict
from importlib import metadata

from .config import Config, load_config_file, DEFAULT_IGNORES
from .exceptions import ConfigError


def create_parser() -> argparse.ArgumentParser:
    """Create the main argument parser."""
    parser = argparse.ArgumentParser(
        description="Find duplicate Python definitions across a project.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    
    # Positional: Scan roots
    parser.add_argument("root", nargs="*", help="Root directory to scan or find arguments.")
    
    # Config & Filtering Groups
    config_group = parser.add_argument_group("Configuration & Filtering")
    config_group.add_argument("--config", help="Path to configuration file (.duplifinder.yaml).")
    config_group.add_argument("--ignore", default="", help="Comma-separated directory names to ignore.")
    config_group.add_argument("--exclude-patterns", default="", help="Comma-separated glob patterns for files to exclude.")
    config_group.add_argument("--exclude-names", default="", help="Comma-separated regex patterns for definition names to exclude.")
    config_group.add_argument("--no-gitignore", action="store_true", help="Disable auto-respect of .gitignore patterns (default: respect).")
    
    # Scan Mode Groups
    scan_group = parser.add_argument_group("Scan Modes")
    scan_group.add_argument("-f", "--find", nargs="*", help="Types and names to find (e.g., 'class Base').")
    scan_group.add_argument("--find-regex", nargs="*", help="Regex patterns for types and names (e.g., 'class UI.*Manager').")
    scan_group.add_argument("--pattern-regex", nargs="*", help="Regex patterns for duplicate code snippets.")
    scan_group.add_argument("-s", "--search", nargs='+', help="Search all occurrences of specific definitions (e.g., 'class UIManager', 'def dashboard_menu'). Requires type and name.")
    scan_group.add_argument("--token-mode", action="store_true", help="Enable token-based duplication detection for non-definition code.")
    
    # Thresholds & Behavior
    behavior_group = parser.add_argument_group("Thresholds & Behavior")
    behavior_group.add_argument("--similarity-threshold", type=float, default=0.8, help="Similarity ratio threshold for token duplicates (0.0-1.0, default: 0.8).")
    behavior_group.add_argument("--dup-threshold", type=float, default=0.1, help="Duplication rate threshold for alerts (0.0-1.0, default: 0.1; warns if exceeded).")
    behavior_group.add_argument("--min", type=int, default=2, help="Min occurrences to report as duplicate.")
    behavior_group.add_argument("--parallel", action="store_true", help="Scan files in parallel.")
    behavior_group.add_argument("--use-multiprocessing", action="store_true", help="Use multiprocessing instead of threading.")
    behavior_group.add_argument("--max-workers", type=int, help="Max workers for parallel processing.")
    behavior_group.add_argument("--watch", action="store_true", help="Watch mode: live scanning on file changes.")

    # Output & Misc
    output_group = parser.add_argument_group("Output & Misc")
    output_group.add_argument("-p", "--preview", action="store_true", help="Show formatted preview of duplicates.")
    output_group.add_argument("--json", action="store_true", help="Output as JSON.")
    output_group.add_argument("--fail", action="store_true", help="Exit 1 if duplicates found.")
    output_group.add_argument("--verbose", action="store_true", help="Print detailed logs.")
    output_group.add_argument("--audit", action="store_true", help="Enable audit logging for file access trails (JSONL).")
    output_group.add_argument("--audit-log", type=str, help="Path for audit log output (defaults to .duplifinder_audit.jsonl).")
    
    try:
        __version__ = metadata.version("duplifinder")
    except metadata.PackageNotFoundError:
        __version__ = "0.0.0"
    output_group.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    
    return parser


def build_config(args: argparse.Namespace) -> Config:
    """Merge CLI args with config file (if provided); validate via Pydantic."""
    # Load config file if specified
    config_dict = {}
    if args.config:
        config_dict = load_config_file(args.config)

    root_candidates = args.root or config_dict.get("root", ["."])
    root_str = root_candidates[0] if len(root_candidates) > 0 and pathlib.Path(root_candidates[0]).exists() and pathlib.Path(root_candidates[0]).is_dir() else "."
    extra = root_candidates[1:] if len(root_candidates) > 1 else []

    # Setup logging early
    logging.basicConfig(
        level=logging.INFO if args.verbose else logging.WARNING,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

    # Merge into dict for Pydantic
    merged = {
        "root": root_str,
        "ignore_dirs": {x.strip() for x in (args.ignore or config_dict.get("ignore", "")).split(",") if x.strip()},
        "exclude_patterns": {x.strip() for x in (args.exclude_patterns or config_dict.get("exclude_patterns", "")).split(",") if x.strip()},
        "exclude_names": {x.strip() for x in (args.exclude_names or config_dict.get("exclude_names", "")).split(",") if x.strip()},
        "filter_regexes": args.find_regex or config_dict.get("find_regex", []),
        "pattern_regexes": args.pattern_regex or config_dict.get("pattern_regex", []),  # Fixed: singular
        "search_specs": args.search or config_dict.get("search", []),
        "search_mode": bool(args.search or config_dict.get("search", [])),
        "token_mode": args.token_mode or config_dict.get("token_mode", False),
        "similarity_threshold": args.similarity_threshold or config_dict.get("similarity_threshold", 0.8),
        "dup_threshold": args.dup_threshold or config_dict.get("dup_threshold", 0.1),
        "json_output": args.json or config_dict.get("json", False),
        "fail_on_duplicates": args.fail or config_dict.get("fail", False),
        "min_occurrences": args.min or config_dict.get("min", 2),
        "verbose": args.verbose or config_dict.get("verbose", False),
        "parallel": args.parallel or config_dict.get("parallel", False),
        "use_multiprocessing": args.use_multiprocessing or config_dict.get("use_multiprocessing", False),
        "max_workers": args.max_workers or config_dict.get("max_workers", None),
        "preview": args.preview or config_dict.get("preview", False),
        "audit_enabled": args.audit or config_dict.get("audit", False),
        "audit_log_path": args.audit_log or config_dict.get("audit_log", ".duplifinder_audit.jsonl"),
        "respect_gitignore": not getattr(args, 'no_gitignore', False) and config_dict.get("respect_gitignore", True),
        "watch_mode": args.watch or config_dict.get("watch", False),
    }

    # Process find arguments
    find_args = (args.find or config_dict.get("find", [])) + extra
    types_to_search = set()
    filter_names = set()
    for item in find_args:
        if item in {"class", "def", "async_def"}:
            types_to_search.add(item)
        else:
            filter_names.add(item)
    if not types_to_search:
        types_to_search = {"class", "def", "async_def"}
    merged["types_to_search"] = types_to_search
    merged["filter_names"] = filter_names

    # Validate via Pydantic
    try:
        config = Config(**merged)
    except (ValueError, ConfigError) as e:
        logging.error(f"Config validation failed: {e}")
        raise SystemExit(2)  # Config error code

    # Merge ignore_dirs with defaults
    config.ignore_dirs = DEFAULT_IGNORES.union(config.ignore_dirs)

    return config