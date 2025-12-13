# src/duplifinder/search_finder.py

"""Search finder for specific definition occurrences (no dup filtering)."""

import logging
from collections import defaultdict
from typing import Dict, List, Tuple

from .config import Config
from .processors import process_file_ast
from .utils import discover_py_files, run_parallel, log_file_count


def _parse_search_specs(config: Config) -> Dict[str, set]:
    """Parse search specs into {type: set(names)}."""
    spec_map = {}
    for spec in config.search_specs:
        parts = spec.strip().split(maxsplit=1)
        if len(parts) != 2:
            raise ValueError(f"Invalid spec '{spec}': Expected 'type name'")
        typ, name = parts
        if typ not in {"class", "def", "async_def"}:
            raise ValueError(f"Invalid type '{typ}' in '{spec}': Must be class, def, or async_def")
        spec_map.setdefault(typ, set()).add(name)
    return spec_map


def find_search_matches(config: Config) -> Tuple[Dict[str, List[Tuple[str, str]]], List[str], int]:
    """Find all occurrences matching search specs; no dup filtering."""
    all_matches: Dict[str, List[Tuple[str, str]]] = defaultdict(list)  # spec -> list of (loc, snippet)
    skipped: List[str] = []
    scanned = 0

    spec_map = _parse_search_specs(config)

    py_files = discover_py_files(config)
    log_file_count(py_files, config, "search")

    for result in run_parallel(py_files, process_file_ast, config=config):
        defs, skipped_file, _ = result  # Ignore lines for search
        if isinstance(skipped_file, str):
            skipped.append(skipped_file)
            logging.debug(f"Skipped file: {skipped_file}")
        else:
            scanned += 1
            for t, name_locs in defs.items():
                if t in spec_map:
                    for name, items in name_locs.items():
                        if name in spec_map[t]:
                            spec_key = f"{t} {name}"
                            all_matches[spec_key].extend(items)  # All locs/snippets

    if config.verbose:
        logging.info(f"Searched {scanned} files, skipped {len(skipped)}, found {sum(len(occ) for occ in all_matches.values())} occurrences")

    return all_matches, skipped, scanned