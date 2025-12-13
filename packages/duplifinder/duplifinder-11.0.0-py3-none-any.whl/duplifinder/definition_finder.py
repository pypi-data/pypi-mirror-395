# src/duplifinder/definition_finder.py

"""AST-based definition finder for classes, functions, and async functions."""

import logging
from collections import defaultdict
from typing import Dict, List, Tuple

from .config import Config
from .processors import process_file_ast, estimate_dup_lines
from .utils import discover_py_files, run_parallel, log_file_count
from .cache import CacheManager


def find_definitions(config: Config) -> Tuple[Dict[str, Dict[str, List[Tuple[str, str]]]], List[str], int, int, int]:
    """Find definitions across the project using AST, optionally in parallel; return total_lines, dup_lines."""
    all_definitions: Dict[str, Dict[str, List[Tuple[str, str]]]] = {t: defaultdict(list) for t in config.types_to_search}
    skipped: List[str] = []
    scanned = 0
    total_lines = 0
    dup_lines = 0

    py_files = discover_py_files(config)
    # Filter for AST: Only .py files supported for now
    py_files = [p for p in py_files if p.suffix == '.py']

    log_file_count(py_files, config)

    # Load cache if enabled
    cache_manager = None
    if config.enable_cache:
        cache_manager = CacheManager(config.cache_path, config=config)

    for result in run_parallel(py_files, process_file_ast, config=config, cache_manager=cache_manager):
        defs, skipped_file, file_lines = result
        if isinstance(skipped_file, str):
            skipped.append(skipped_file)
            logging.debug(f"Skipped file: {skipped_file}")
        else:
            scanned += 1
            total_lines += file_lines
            for t, name_locs in defs.items():
                for name, items in name_locs.items():
                    all_definitions[t][name].extend(items)
                    dup_lines += estimate_dup_lines(items, False, config)

    # Save cache if enabled
    if cache_manager:
        cache_manager.save()

    if config.verbose:
        logging.info(f"Scanned {scanned} files, skipped {len(skipped)}, total lines: {total_lines}, estimated dup lines: {dup_lines}")

    return all_definitions, skipped, scanned, total_lines, dup_lines