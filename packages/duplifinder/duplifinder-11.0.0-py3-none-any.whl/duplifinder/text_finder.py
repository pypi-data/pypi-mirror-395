# src/duplifinder/text_finder.py

"""Text pattern finder using regex matches."""

import logging
import re
from collections import defaultdict
from typing import Dict, List ,Tuple

from .config import Config
from .processors import process_file_text, estimate_dup_lines
from .utils import discover_py_files, run_parallel, log_file_count


def find_text_matches(config: Config, patterns: List[re.Pattern]) -> Tuple[Dict[str, List[str]], List[str], int, int, int]:
    """Find text matches across the project, optionally in parallel; return total_lines, dup_lines."""
    all_matches: Dict[str, List[str]] = defaultdict(list)
    skipped: List[str] = []
    scanned = 0
    total_lines = 0
    dup_lines = 0

    py_files = discover_py_files(config)
    log_file_count(py_files, config)

    for result in run_parallel(py_files, process_file_text, patterns, config=config):
        matches, skipped_file, file_lines = result
        if isinstance(skipped_file, str):
            skipped.append(skipped_file)
            logging.debug(f"Skipped file: {skipped_file}")
        else:
            scanned += 1
            total_lines += file_lines
            for matched, locs in matches.items():
                all_matches[matched].extend(locs)
                dup_lines += estimate_dup_lines(locs, True, config)

    if config.verbose:
        logging.info(f"Scanned {scanned} files, skipped {len(skipped)}, total lines: {total_lines}, estimated dup lines: {dup_lines}")

    return all_matches, skipped, scanned, total_lines, dup_lines