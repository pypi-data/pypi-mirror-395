# tests/test_renderers.py

"""Tests for renderers."""

import json
from unittest.mock import patch, Mock
from pathlib import Path

import pytest
from duplifinder.duplicate_renderer import render_duplicates
from duplifinder.search_renderer import render_search, render_search_json
from duplifinder.config import Config


def test_render_duplicates_empty(capsys, mock_config):
    """Test empty dups show 'No duplicates'."""
    mock_config.json_output = False
    render_duplicates({}, mock_config, False, 0.0, 0.1, 0, 0, 0, [])
    captured = capsys.readouterr()
    assert "No duplicates found" in captured.out


def test_render_duplicates_alert(capsys, mock_config):
    """Test dup rate alert."""
    mock_config.dup_threshold = 0.1
    mock_config.json_output = False
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
    
    # FIXED: Provide *two* items to satisfy min_occurrences=2
    token_results = {"token similarity >80%": [
        ("file:1:2", "file:3:4", 0.85),
        ("file:5:6", "file:7:8", 0.88)  # <-- Added a second item
    ]}

    render_duplicates(token_results, mock_config, False, 0.0, 0.1, 10, 0, 0, [], is_token=True)
    captured = capsys.readouterr()

    # Check that both items are rendered and the "No duplicates" message is gone
    assert "(sim: 85.00%)" in captured.out
    assert "(sim: 88.00%)" in captured.out
    assert "No duplicates found" not in captured.out
    

def test_render_duplicates_json(capsys, mock_config):
    """Test JSON output."""
    mock_config.json_output = True
    mock_config.root = Path("/app")
    dups = {"class MyClass": [("a.py:10", "snippet1"), ("b.py:20", "snippet2")]}
    
    render_duplicates(dups, mock_config, False, 0.5, 0.1, 100, 50, 2, ["skipped.py"])
    
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    
    assert data["root"] == "/app"
    assert data["scanned_files"] == 2
    assert data["skipped_files"] == ["skipped.py"]
    assert data["duplicate_count"] == 1
    assert "class MyClass" in data["duplicates"]
    assert data["duplicates"]["class MyClass"][0]["loc"] == "a.py:10"

def test_render_search_no_occurrences(capsys, mock_config):
    """Test search output for no results."""
    mock_config.json_output = False
    render_search({"class NotFound": []}, mock_config)
    captured = capsys.readouterr()
    assert "No occurrences found" in captured.out

def test_render_search_multiple_occurrences(capsys, mock_config):
    """Test search output for multiple results."""
    mock_config.json_output = False
    results = {"def my_func": [("a.py:1", "snip"), ("b.py:2", "snip")]}
    render_search(results, mock_config)
    captured = capsys.readouterr()
    assert "found 2 time(s)" in captured.out
    assert "a.py:1" in captured.out
    assert "b.py:2" in captured.out


def test_render_duplicates_preview_token_mode(capsys, mock_config):
    """Test that preview mode works with is_token=True (Lines 29-30)."""
    mock_config.preview = True
    
    token_results = {"token similarity >80%": [
        ("file:1:2", "file:3:4", 0.85),
        ("file:5:6", "file:7:8", 0.88)
    ]}
    
    with patch("duplifinder.duplicate_renderer.Panel") as mock_panel, \
         patch("duplifinder.duplicate_renderer.Syntax") as mock_syntax:
        
        render_duplicates(token_results, mock_config, False, 0.0, 0.1, 10, 0, 1, [], is_token=True)
    
    captured = capsys.readouterr()
    
    mock_syntax.assert_not_called()
    mock_panel.assert_not_called() # Tokens don't have snippets, so panel isn't called
    
    assert "token similarity >80%" in captured.out
    assert "file:1:2" in captured.out
    assert "┏" not in captured.out # No table chars

def test_render_duplicates_audit_nudge(capsys, mock_config):
    """Test that the audit nudge is printed (Line 114)."""
    mock_config.audit_enabled = True
    mock_config.audit_log_path = "fake/audit.jsonl"
    mock_config.preview = False # Use table mode
    
    render_duplicates({}, mock_config, False, 0.0, 0.1, 10, 0, 1, [], is_token=False)
    
    captured = capsys.readouterr()
    assert "Audit trail logged to fake/audit.jsonl" in captured.out

def test_render_duplicates_fail_on_duplicates(mock_config):
    """Test SystemExit is raised (Line 117)."""
    mock_config.fail_on_duplicates = True
    mock_config.preview = False # Use table mode
    dups = {"def MyFunc": [("a.py:1", ""), ("b.py:2", "")]} # Has duplicates
    
    with pytest.raises(SystemExit) as e:
        render_duplicates(dups, mock_config, False, 0.0, 0.1, 10, 2, 2, [], is_token=False)
    
    assert e.value.code == 1


def test_render_duplicates_preview_mode(capsys, mock_config):
    """Test that preview mode uses panels (Lines 71-92)."""
    mock_config.preview = True
    
    # ** THE FIX: Provide two items to pass the min_occurrences=2 filter **
    dups = {"def MyFunc": [("a.py:1", "snippet1"), ("b.py:2", "snippet2")]}
    
    with patch("duplifinder.duplicate_renderer.Panel") as mock_panel, \
         patch("duplifinder.duplicate_renderer.Syntax") as mock_syntax:
        
        render_duplicates(dups, mock_config, False, 0.0, 0.1, 10, 1, 1, [], is_token=False)
    
    captured = capsys.readouterr()
    
    # Assert the panel/syntax was called (it will be called twice)
    assert mock_syntax.call_count == 2
    assert mock_panel.call_count == 2
    
    # Assert the output text is correct (no table)
    assert "def MyFunc" in captured.out
    assert "a.py:1" in captured.out
    assert "b.py:2" in captured.out
    assert "┏" not in captured.out # No table chars



def test_render_duplicates_preview_mode_no_snippet(capsys, mock_config):
    """Test preview mode when an item has no snippet (Line 80 branch)."""
    mock_config.preview = True

    # ** THE FIX: Provide two items to pass the min_occurrences=2 filter **
    dups = {"text TODO": [("a.py:1", ""), ("b.py:2", "")]} # Two items, empty snippets
    
    with patch("duplifinder.duplicate_renderer.Panel") as mock_panel, \
         patch("duplifinder.duplicate_renderer.Syntax") as mock_syntax:
        
        render_duplicates(dups, mock_config, False, 0.0, 0.1, 10, 1, 1, [], is_token=False)
    
    captured = capsys.readouterr()
    
    # It should print the location but not call Syntax or Panel
    mock_syntax.assert_not_called()
    mock_panel.assert_not_called()
    assert "text TODO" in captured.out
    assert "a.py:1" in captured.out
    assert "b.py:2" in captured.out
    assert "No duplicates found" not in captured.out


def test_render_search_preview_mode(capsys, mock_config: Config):
    """Test that preview mode is triggered for search results."""
    mock_config.preview = True
    results = {"class Foo": [("file.py:1", "snippet")]}
    with patch("duplifinder.search_renderer.Syntax") as mock_syntax, \
         patch("duplifinder.search_renderer.Panel") as mock_panel:
        render_search(results, mock_config)
    mock_syntax.assert_called_once_with("snippet", "python", theme="monokai", line_numbers=False)
    mock_panel.assert_called_once()


def test_render_search_fail_on_duplicates(mock_config: Config):
    """Test that SystemExit is raised for multiple occurrences when fail_on_duplicates is True."""
    mock_config.fail_on_duplicates = True
    results = {"def my_func": [("a.py:1", "snip"), ("b.py:2", "snip")]}
    with pytest.raises(SystemExit) as e:
        render_search(results, mock_config)
    assert e.value.code == 1


def test_render_search_no_snippet(capsys, mock_config: Config):
    """Test that the preview is skipped if the snippet is empty."""
    mock_config.preview = True
    results = {"class Foo": [("file.py:1", "")]}
    with patch("duplifinder.search_renderer.Syntax") as mock_syntax:
        render_search(results, mock_config)
    mock_syntax.assert_not_called()
