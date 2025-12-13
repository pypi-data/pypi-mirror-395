# tests/test_finder.py

"""Tests for renderers."""

import json
from unittest.mock import patch, Mock  # <-- Import Mock
from pathlib import Path  # <-- FIXED: Added missing import
import logging  # <-- ** FIX 1: ADD THIS IMPORT **

import pytest
from duplifinder.duplicate_renderer import render_duplicates
from duplifinder.search_renderer import render_search, render_search_json
from duplifinder.config import Config

import re
from pathlib import Path
from unittest.mock import patch, Mock
from duplifinder.config import Config
from duplifinder.finder import (
    find_definitions,
    find_text_matches,
    find_search_matches,
    find_token_duplicates,
)


def test_render_duplicates_empty(capsys, mock_config):
    """Test empty dups show 'No duplicates'."""
    mock_config.json_output = False
    # FIXED: Added missing arguments: scanned_files=0, skipped_files=[]
    render_duplicates({}, mock_config, False, 0.0, 0.1, 0, 0, 0, [])
    captured = capsys.readouterr()
    assert "No duplicates found" in captured.out


def test_render_duplicates_alert(capsys, mock_config):
    """Test dup rate alert."""
    mock_config.dup_threshold = 0.1
    mock_config.json_output = False
    # FIXED: Added missing arguments: scanned_files=0, skipped_files=[]
    render_duplicates({}, mock_config, False, 0.15, 0.1, 100, 15, 0, [])
    captured = capsys.readouterr()
    assert "ALERT: Duplication rate" in captured.out


def test_render_search_singleton(capsys, mock_config):
    """Test singleton search output."""
    mock_config.json_output = False
    results = {"class Foo": [("file.py:1", "snippet")]}
    render_search(results, mock_config)
    captured = capsys.readouterr()
    assert "Verified singleton" in captured.out


# FIXED: Switched to use capsys fixture instead of patch
def test_render_search_json(capsys, mock_config):
    """Test JSON search output."""
    mock_config.root = Path(".")
    results = {"class Foo": [("file.py:1", "snippet")]}

    # Call the function, which prints to stdout
    render_search_json(results, mock_config, 1, [])

    # Get captured output from capsys
    output = capsys.readouterr().out

    parsed = json.loads(output)
    assert parsed["search_results"]["class Foo"]["is_singleton"] is True


def test_render_duplicates_token_mode(capsys, mock_config):
    """Test token rendering normalization."""
    mock_config.json_output = False

    # FIXED:
    # 1. Provided two items to pass min_occurrences=2.
    # 2. Used the correct (loc1, loc2, ratio) tuple format.
    token_results = {"token similarity >80%": [
        ("file:1:2", "file:3:4", 0.85),
        ("file:5:6", "file:7:8", 0.88)
    ]}

    # FIXED: Added missing arguments: scanned_files=0, skipped_files=[]
    render_duplicates(token_results, mock_config, False, 0.0, 0.1, 10, 0, 0, [], is_token=True)

    captured = capsys.readouterr()

    # FIXED: Assert the correct format and check that "No duplicates" is not present
    assert "(sim: 85.00%)" in captured.out
    assert "(sim: 88.00%)" in captured.out
    assert "No duplicates found" not in captured.out



def test_find_text_matches(mock_config: Config, caplog):
    """Test the find_text_matches function's core logic."""
    mock_config.verbose = True
    caplog.set_level(logging.INFO)  # <-- ** FIX 2: ADD THIS LINE **
    patterns = [re.compile("TODO")]

    # Mock the dependencies
    mock_discover = patch("duplifinder.text_finder.discover_py_files", return_value=[Path("a.py")])

    # Mock the result from the parallel runner
    mock_run_parallel = patch(
        "duplifinder.text_finder.run_parallel",
        return_value=[
            ({"TODO": ["a.py:1"]}, None, 10),  # A successful result
            (None, "b.py", 0),                 # A skipped file
        ]
    )

    with mock_discover, mock_run_parallel:
        results, skipped, scanned, total_lines, dup_lines = find_text_matches(mock_config, patterns)

    assert scanned == 1
    assert total_lines == 10
    assert skipped == ["b.py"]
    assert "TODO" in results
    assert results["TODO"] == ["a.py:1"]
    assert "Scanned 1 files, skipped 1" in caplog.text

def test_find_definitions(mock_config: Config, caplog):
    """Test the find_definitions function's core logic."""
    mock_config.verbose = True
    caplog.set_level(logging.INFO)  # <-- ** FIX 3: ADD THIS LINE **

    # Mock the dependencies
    mock_discover = patch("duplifinder.definition_finder.discover_py_files", return_value=[Path("a.py")])

    # Mock the result from the parallel runner
    mock_run_parallel = patch(
        "duplifinder.definition_finder.run_parallel",
        return_value=[
            ({"class": {"MyClass": [("a.py:1", "snippet")]}}, None, 5), # Successful
            (None, "b.py", 0),                                         # Skipped
        ]
    )

    with mock_discover, mock_run_parallel:
        results, skipped, scanned, total_lines, dup_lines = find_definitions(mock_config)

    assert scanned == 1
    assert total_lines == 5
    assert skipped == ["b.py"]
    assert "class" in results
    assert "MyClass" in results["class"]
    assert results["class"]["MyClass"] == [("a.py:1", "snippet")]
    assert "Scanned 1 files, skipped 1" in caplog.text

def test_find_search_matches(mock_config: Config, caplog):
    """Test the find_search_matches function's core logic."""
    mock_config.verbose = True
    caplog.set_level(logging.INFO)  # <-- ** FIX 4: ADD THIS LINE **
    mock_config.search_specs = ["class MyClass"]

    # Mock the dependencies
    mock_discover = patch("duplifinder.search_finder.discover_py_files", return_value=[Path("a.py")])

    # Mock the result from the parallel runner
    mock_run_parallel = patch(
        "duplifinder.search_finder.run_parallel",
        return_value=[
            ({"class": {"MyClass": [("a.py:1", "snippet")]}}, None, 5), # Successful
            (None, "b.py", 0),                                         # Skipped
        ]
    )

    with mock_discover, mock_run_parallel:
        results, skipped, scanned = find_search_matches(mock_config)

    assert scanned == 1
    assert skipped == ["b.py"]
    assert "class MyClass" in results
    assert results["class MyClass"] == [("a.py:1", "snippet")]
    assert "Searched 1 files, skipped 1" in caplog.text

def test_find_token_duplicates(mock_config: Config, caplog):
    """Test the find_token_duplicates function's core logic."""
    mock_config.verbose = True
    caplog.set_level(logging.INFO)  # <-- ** FIX 5: ADD THIS LINE **

    # Mock the dependencies
    mock_discover = patch("duplifinder.token_finder.discover_py_files", return_value=[Path("a.py")])

    # Mock the result from the parallel runner
    mock_run_parallel = patch(
        "duplifinder.token_finder.run_parallel",
        return_value=[
            ({"similar": [("a.py:1", "a.py:5", 0.9)]}, None, 10), # Successful
            (None, "b.py", 0),                                     # Skipped
        ]
    )

    with mock_discover, mock_run_parallel:
        results, skipped, scanned, total_lines, dup_lines = find_token_duplicates(mock_config)

    assert scanned == 1
    assert total_lines == 10
    assert skipped == ["b.py"]
    assert "similar" in results
    assert "Scanned 1 files, skipped 1" in caplog.text


def test_find_search_matches_invalid_spec(mock_config: Config):
    """Test that find_search_matches raises ValueError for invalid specs."""
    mock_config.search_specs = ["invalid_spec"]
    with pytest.raises(ValueError, match="Invalid spec"):
        find_search_matches(mock_config)


def test_find_search_matches_invalid_type(mock_config: Config):
    """Test that find_search_matches raises ValueError for invalid types."""
    mock_config.search_specs = ["invalid_type MyClass"]
    with pytest.raises(ValueError, match="Invalid type"):
        find_search_matches(mock_config)

def test_find_search_matches_verbose_logging(mock_config: Config, caplog):
    """Test verbose logging in find_search_matches."""
    mock_config.verbose = True
    mock_config.search_specs = ["class MyClass"]
    caplog.set_level(logging.INFO)

    with patch('duplifinder.search_finder.discover_py_files', return_value=[]):
        find_search_matches(mock_config)

    assert "Searched 0 files" in caplog.text
