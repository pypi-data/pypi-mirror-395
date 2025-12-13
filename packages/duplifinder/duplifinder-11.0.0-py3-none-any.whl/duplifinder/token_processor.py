# src/duplifinder/token_processor.py

"""Token file processor for similarity detection."""

import difflib
import fnmatch
import io
import logging
import tokenize
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

import ast

from .config import Config
from .utils import audit_log_event


def tokenize_block(text: str) -> List[str]:
    """Tokenize a code block into normalized tokens."""
    tokens = []
    try:
        for token in tokenize.tokenize(io.BytesIO(text.encode('utf-8', errors='replace')).readline):
            if token.type not in (tokenize.COMMENT, tokenize.NL, tokenize.INDENT, tokenize.DEDENT, tokenize.ENDMARKER):
                tokens.append(token.string.strip())
    except tokenize.TokenError:
        pass
    return tokens


def process_file_tokens(py_file: Path, config: Config) -> Tuple[Dict[str, List[Tuple[str, str, float]]], str | None, int]:
    """Process a single Python file for token-based duplicates; return total_lines."""
    str_py_file = str(py_file)
    if any(fnmatch.fnmatch(py_file.name, pat) for pat in config.exclude_patterns):
        if config.verbose:
            logging.info(f"Skipping {str_py_file}: matches exclude pattern")
        audit_log_event(config, "file_skipped", path=str_py_file, reason="exclude_pattern_match")
        return {}, str_py_file, 0

    total_lines = 0
    try:
        # Audit: Log open attempt
        audit_log_event(config, "file_opened", path=str_py_file, action="token_open")
        # Encoding-aware open
        with open(py_file, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()
        bytes_read = len(text)
        total_lines = len(text.splitlines())
        audit_log_event(config, "file_parsed", path=str_py_file, action="token_success", bytes_read=bytes_read, lines=total_lines)
        
        # Extract code blocks (simple: split on def/class, or use AST for bodies)
        tree = ast.parse(text, filename=str_py_file)
        blocks = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                # Extract body lines via lineno/end_lineno
                lines = text.splitlines()
                start = node.lineno - 1
                end = (node.end_lineno or node.lineno) 
                block_text = '\n'.join(lines[start:end])
                blocks.append((f"{node.lineno}:{end}", tokenize_block(block_text)))
        
        # Self-compare blocks for similarity (intra-file for now; extend later)
        similarities: Dict[str, List[Tuple[str, str, float]]] = defaultdict(list)
        for i, (loc1, tokens1) in enumerate(blocks):
            for j, (loc2, tokens2) in enumerate(blocks[i+1:], i+1):
                matcher = difflib.SequenceMatcher(None, tokens1, tokens2)
                ratio = matcher.ratio()
                if ratio >= config.similarity_threshold:
                    key = f"token similarity >{int(config.similarity_threshold*100)}%"
                    similarities[key].append((f"{str_py_file}:{loc1}", f"{str_py_file}:{loc2}", ratio))
        
        return similarities, None, total_lines
    except UnicodeDecodeError as e:
        reason = f"encoding_error: {e}"
        audit_log_event(config, "file_skipped", path=str_py_file, reason=reason)
        logging.warning(f"Skipping {str_py_file} due to encoding error: {e}")
        return {}, str_py_file, 0
    except Exception as e:
        reason = f"{type(e).__name__}: {e}"
        audit_log_event(config, "file_skipped", path=str_py_file, reason=reason)
        logging.error(f"Skipping {str_py_file} for tokens: {reason}", exc_info=config.verbose)
        return {}, str_py_file, 0