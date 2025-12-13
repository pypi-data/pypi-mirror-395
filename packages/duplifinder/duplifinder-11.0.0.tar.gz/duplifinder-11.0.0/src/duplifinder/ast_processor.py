# src/duplifinder/ast_processor.py

"""AST file processor for definition extraction."""

import fnmatch
import logging
import tokenize
import re  # For exclude_names
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

import ast

from .ast_visitor import EnhancedDefinitionVisitor
from .config import Config
from .utils import audit_log_event
from .exceptions import FileProcessingError
from .cache import CacheManager


def process_file_ast(py_file: Path, config: Config, cache_manager: CacheManager = None) -> Tuple[Dict[str, Dict[str, List[Tuple[str, str]]]], str | None, int]:
    """Process a single Python file for definitions using AST; return total_lines."""
    str_py_file = str(py_file)
    if any(fnmatch.fnmatch(py_file.name, pat) for pat in config.exclude_patterns):
        if config.verbose:
            logging.info(f"Skipping {str_py_file}: matches exclude pattern")
        audit_log_event(config, "file_skipped", path=str_py_file, reason="exclude_pattern_match")
        return {}, str_py_file, 0

    # Cache check
    file_hash = None
    if cache_manager:
        file_hash = CacheManager.compute_hash(py_file)
        if file_hash:
            cached = cache_manager.get(str_py_file, file_hash)
            if cached:
                if config.verbose:
                    logging.info(f"Cache hit for {str_py_file}")
                return cached["definitions"], None, cached["total_lines"]

    total_lines = 0
    try:
        # Audit: Log open attempt
        audit_log_event(config, "file_opened", path=str_py_file, action="ast_open")
        # Encoding-aware open with fallback
        with tokenize.open(py_file) as fh:  # Handles BOM/encoding
            text = fh.read()
        bytes_read = len(text)
        total_lines = len(text.splitlines())
        audit_log_event(config, "file_parsed", path=str_py_file, action="ast_success", bytes_read=bytes_read, lines=total_lines)
        
        try:
            tree = ast.parse(text, filename=str_py_file)
        except (SyntaxError, ValueError) as e:
            # Re-raise as known processing error, which will be caught below or handled
            raise FileProcessingError(f"Parsing failed: {e}", str_py_file, reason=f"{type(e).__name__}: {e}")

        lines = text.splitlines() if config.preview else []
        visitor = EnhancedDefinitionVisitor(config.types_to_search)
        visitor.visit(tree)
        definitions: Dict[str, Dict[str, List[Tuple[str, str]]]] = {t: defaultdict(list) for t in config.types_to_search}
        for t, items in visitor.definitions.items():
            for name, lineno, end_lineno, _ in items:
                if any(re.match(pat, name) for pat in config.exclude_names):
                    continue
                loc = f"{str_py_file}:{lineno}"
                snippet = ""
                if config.preview and lines:
                    snippet_lines = lines[lineno - 1 : end_lineno]
                    if snippet_lines:
                        # Find minimum indent, ignoring empty lines
                        indent = min((len(line) - len(line.lstrip())) for line in snippet_lines if line.strip())
                        snippet_lines = [line[indent:] for line in snippet_lines]
                        snippet = "\n".join(f"{i + 1} {line}" for i, line in enumerate(snippet_lines))
                definitions[t][name].append((loc, snippet))

        # Update cache
        if cache_manager and file_hash:
            cache_manager.set(str_py_file, file_hash, {
                "definitions": definitions,
                "total_lines": total_lines
            })

        return definitions, None, total_lines
    
    except UnicodeDecodeError as e:
        reason = f"encoding_error: {e}"
        audit_log_event(config, "file_skipped", path=str_py_file, reason=reason)
        logging.warning(f"Skipping {str_py_file} due to encoding error: {e}; try --encoding flag in future")
        return {}, str_py_file, 0
    except FileProcessingError as e:
        reason = e.reason
        audit_log_event(config, "file_skipped", path=str_py_file, reason=reason)
        # We can now provide richer error info if we want, or just log it.
        # The requirement says "More granular error reporting".
        # Currently we just log and skip.
        # If we wanted to fail hard on syntax errors, we would re-raise here if config.fail_on_error was true (but it's not a config option yet).
        # For now, we continue to skip but we have the infrastructure to propagate it if needed.
        logging.error(f"Skipping {str_py_file} due to processing error: {e.args[0]}", exc_info=config.verbose)
        return {}, str_py_file, 0
    except Exception as e:
        reason = f"{type(e).__name__}: {e}"
        audit_log_event(config, "file_skipped", path=str_py_file, reason=reason)
        logging.error(f"Skipping {str_py_file}: {reason}", exc_info=config.verbose)
        return {}, str_py_file, 0
