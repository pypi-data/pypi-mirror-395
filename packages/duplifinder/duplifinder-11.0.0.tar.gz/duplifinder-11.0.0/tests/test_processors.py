# tests/test_processors.py

"""Tests for processors with edges."""

import re
from pathlib import Path

import pytest
from duplifinder.ast_processor import process_file_ast
from duplifinder.text_processor import process_file_text
from duplifinder.token_processor import process_file_tokens, tokenize_block
from duplifinder.config import Config
from duplifinder.processor_utils import estimate_dup_lines

import logging
import tokenize
from unittest.mock import patch

def test_process_file_ast_valid(sample_py_file, mock_config):
    """Test AST processing on valid file."""
    defs, skipped, lines = process_file_ast(sample_py_file, mock_config)
    assert skipped is None
    assert lines == 6
    assert "class" in defs
    assert "SingletonClass" in defs["class"]


def test_process_file_ast_invalid(invalid_py_file, mock_config):
    """Test AST skips syntax errors."""
    defs, skipped, lines = process_file_ast(invalid_py_file, mock_config)
    assert skipped == str(invalid_py_file)
    assert lines == 0


def test_process_file_ast_exclude(mock_config, sample_py_file):
    """Test exclude_patterns skips files."""
    mock_config.exclude_patterns = {"test.py"}
    defs, skipped, lines = process_file_ast(sample_py_file, mock_config)
    assert skipped == str(sample_py_file)


def test_process_file_ast_exclude_names(mock_config, sample_py_file):
    """Test exclude_names filters defs."""
    mock_config.exclude_names = {"Singleton.*"}
    defs, skipped, lines = process_file_ast(sample_py_file, mock_config)
    assert "SingletonClass" not in defs["class"]  # Filtered


def test_tokenize_block():
    """Test tokenization normalizes."""
    text = "def foo(): pass  # comment"
    tokens = tokenize_block(text)
    assert "def" in tokens
    assert "foo" in tokens
    assert "# comment" not in " ".join(tokens)


def test_process_file_text_match(sample_py_file, mock_config):
    """Test text pattern matching."""
    patterns = [re.compile("class")]
    matches, skipped, lines = process_file_text(sample_py_file, patterns, mock_config)
    assert skipped is None
    assert "class" in matches
    assert len(matches["class"]) == 1


def test_process_file_text_no_match(tmp_path: Path, mock_config):
    """Test no matches returns empty."""
    py_file = tmp_path / "no_match.py"
    py_file.write_text("No item here")  # <-- FIXED: Changed text
    patterns = [re.compile("match")]
    matches, skipped, lines = process_file_text(py_file, patterns, mock_config)
    assert matches == {}


def test_process_file_tokens_similarity(tmp_path: Path, mock_config):
    """Test token similarity detection."""
    mock_config.similarity_threshold = 0.5
    py_file = tmp_path / "similar.py"
    py_file.write_text("def sim1(): pass\ndef sim2(): pass")
    similarities, skipped, lines = process_file_tokens(py_file, mock_config)
    assert skipped is None
    assert "token similarity >50%" in similarities


def test_estimate_dup_lines_below_min(mock_config):
    """Test dup estimation < min_occurrences = 0."""
    items = [("loc1", "")]
    assert estimate_dup_lines(items, False, mock_config) == 0


def test_estimate_dup_lines_above_min(mock_config, sample_py_file):
    """Test dup estimation > min."""
    mock_config.min_occurrences = 1
    items = [("loc1", ""), ("loc2", "")]
    assert estimate_dup_lines(items, False, mock_config) > 0


def test_estimate_dup_lines_empty_list(mock_config):
    """Test that an empty list of items results in 0 duplicated lines."""
    assert estimate_dup_lines([], False, mock_config) == 0


def test_estimate_dup_lines_text_like(mock_config):
    """Test dup estimation for text-like duplicates."""
    mock_config.min_occurrences = 1
    items = [("loc1", ""), ("loc2", "")]
    assert estimate_dup_lines(items, True, mock_config) > 0


def test_process_file_ast_preview_indent(tmp_path: Path, mock_config: Config):
    """Test AST snippet generation with indentation."""
    py_file = tmp_path / "test.py"
    # FIXED: File content must be valid Python (no leading indent)
    py_file.write_text("class A:\n    pass\n")
    mock_config.preview = True

    defs, _, _ = process_file_ast(py_file, mock_config)

    assert "class" in defs
    snippet = defs["class"]["A"][0][1]

    # The common indent is 0, so the snippet is unchanged
    assert "1 class A:" in snippet
    assert "2     pass" in snippet # 4 spaces
    assert "    class A:" not in snippet

def test_process_file_ast_unicode_error(tmp_path: Path, mock_config: Config, caplog):
    """Test AST processor handles UnicodeDecodeError."""
    py_file = tmp_path / "test.py"
    py_file.write_text("pass") # Content doesn't matter, mock will raise

    with patch("tokenize.open", side_effect=UnicodeDecodeError("utf-8", b"", 0, 1, "test error")):
        defs, skipped, lines = process_file_ast(py_file, mock_config)

    assert skipped == str(py_file)
    # FIXED: Check the warning log, not the error log
    assert "encoding error" in caplog.text

def test_process_file_ast_generic_error(tmp_path: Path, mock_config: Config, caplog):
    """Test AST processor handles a generic Exception."""
    py_file = tmp_path / "test.py"
    py_file.write_text("pass")

    with patch("tokenize.open", side_effect=IOError("Disk full")):
        defs, skipped, lines = process_file_ast(py_file, mock_config)

    assert skipped == str(py_file)
    # FIXED: IOError is OSError
    assert "OSError: Disk full" in caplog.text

def test_process_file_text_exclude(tmp_path: Path, mock_config: Config, caplog):
    """Test text processor respects exclude_patterns."""
    caplog.set_level(logging.INFO)  # <-- ** FIX 1: ADD THIS LINE **
    mock_config.exclude_patterns = {"test.py"}
    mock_config.verbose = True
    py_file = tmp_path / "test.py"
    py_file.write_text("TODO")

    matches, skipped, lines = process_file_text(py_file, [], mock_config)

    assert skipped == str(py_file)
    assert "matches exclude pattern" in caplog.text

def test_process_file_text_unicode_error(tmp_path: Path, mock_config: Config, caplog):
    """Test text processor handles UnicodeDecodeError."""
    py_file = tmp_path / "test.py"
    py_file.write_text("pass")

    with patch("builtins.open", side_effect=UnicodeDecodeError("utf-8", b"", 0, 1, "test error")):
        matches, skipped, lines = process_file_text(py_file, [], mock_config)

    assert skipped == str(py_file)
    assert "encoding error" in caplog.text

def test_process_file_text_generic_error(tmp_path: Path, mock_config: Config, caplog):
    """Test text processor handles a generic Exception."""
    py_file = tmp_path / "test.py"
    py_file.write_text("pass")

    with patch("builtins.open", side_effect=IOError("Disk full")):
        matches, skipped, lines = process_file_text(py_file, [], mock_config)

    assert skipped == str(py_file)
    # FIXED: IOError is OSError
    assert "OSError: Disk full" in caplog.text

def test_tokenize_block_token_error():
    """Test that tokenize_block gracefully handles TokenError."""
    with patch("tokenize.tokenize", side_effect=tokenize.TokenError("bad token")):
        tokens = tokenize_block("def a(): pass")
    assert tokens == [] # Should fail gracefully and return empty list

def test_process_file_tokens_exclude(tmp_path: Path, mock_config: Config, caplog):
    """Test token processor respects exclude_patterns."""
    caplog.set_level(logging.INFO)  # <-- ** FIX 2: ADD THIS LINE **
    mock_config.exclude_patterns = {"test.py"}
    mock_config.verbose = True
    py_file = tmp_path / "test.py"
    py_file.write_text("def a(): pass")

    sim, skipped, lines = process_file_tokens(py_file, mock_config)

    assert skipped == str(py_file)
    assert "matches exclude pattern" in caplog.text

def test_process_file_tokens_unicode_error(tmp_path: Path, mock_config: Config, caplog):
    """Test token processor handles UnicodeDecodeError."""
    py_file = tmp_path / "test.py"
    py_file.write_text("def a(): pass")

    with patch("builtins.open", side_effect=UnicodeDecodeError("utf-8", b"", 0, 1, "test error")):
        sim, skipped, lines = process_file_tokens(py_file, mock_config)

    assert skipped == str(py_file)
    assert "encoding error" in caplog.text

def test_process_file_tokens_generic_error(tmp_path: Path, mock_config: Config, caplog):
    """Test token processor handles a generic Exception."""
    py_file = tmp_path / "test.py"
    py_file.write_text("def a(): pass")

    with patch("builtins.open", side_effect=IOError("Disk full")):
        sim, skipped, lines = process_file_tokens(py_file, mock_config)

    assert skipped == str(py_file)
    # FIXED: IOError is OSError
    assert "OSError: Disk full" in caplog.text
