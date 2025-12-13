# src/duplifinder/token_finder.py

"""Token-based duplicate finder using similarity ratios."""

import logging
from collections import defaultdict
from typing import Dict, List, Tuple

from .config import Config
from .processors import process_file_tokens
from .utils import discover_py_files, run_parallel, log_file_count


def find_token_duplicates(config: Config) -> Tuple[Dict[str, List[Tuple[str, str, float]]], List[str], int, int, int]:
    """Find token-based duplicates across the project, optionally in parallel; return total_lines, dup_lines."""
    all_similarities: Dict[str, List[Tuple[str, str, float]]] = defaultdict(list)
    skipped: List[str] = []
    scanned = 0
    total_lines = 0
    dup_lines = 0  # Heuristic: refine with actual spans in future

    py_files = discover_py_files(config)
    log_file_count(py_files, config)

    for result in run_parallel(py_files, process_file_tokens, config=config):
        similarities, skipped_file, file_lines = result
        if isinstance(skipped_file, str):
            skipped.append(skipped_file)
            logging.debug(f"Skipped file: {skipped_file}")
        else:
            scanned += 1
            total_lines += file_lines
            for key, pairs in similarities.items():
                all_similarities[key].extend(pairs)
                dup_lines += len(pairs) * 20  # Avg block heuristic

    if config.verbose:
        logging.info(f"Scanned {scanned} files, skipped {len(skipped)}, total lines: {total_lines}, estimated dup lines: {dup_lines}")

    return all_similarities, skipped, scanned, total_lines, dup_lines