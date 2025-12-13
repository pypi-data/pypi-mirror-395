# src/duplifinder/processor_utils.py

"""Shared utilities for processors (e.g., dup estimation)."""

from typing import List

from .config import Config


def estimate_dup_lines(items: List, is_text_like: bool, config: Config) -> int:
    """Estimate duplicated lines from items (occ -1 * avg block size)."""
    if not items:
        return 0
    occ = len(items)
    if occ < config.min_occurrences:
        return 0
    # For AST: use snippet lines if preview, else heuristic (avg 10 lines)
    if not is_text_like:
        avg_size = sum(len(s.split('\n')) if s else 10 for _, s in items) // occ
    else:
        # For text/token: heuristic per match (avg 1-5 lines)
        avg_size = 3
    return (occ - 1) * avg_size * len(items)  # Conservative: per-item dup contrib