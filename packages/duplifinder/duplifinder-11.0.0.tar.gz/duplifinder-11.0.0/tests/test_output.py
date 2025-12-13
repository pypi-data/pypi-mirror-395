# tests/test_output.py

"""Tests for output rendering."""

from unittest.mock import patch, Mock
import json

import pytest
from duplifinder.output import render_duplicates, render_search, render_search_json
from duplifinder.config import Config
from pathlib import Path


def test_render_duplicates_empty(capsys):
    """Test empty dups show 'No duplicates'."""
    # FIXED: Added audit_enabled=False
    config = Mock(spec=Config, preview=False, json_output=False, fail_on_duplicates=False, audit_enabled=False, html_report=None)
    # FIXED: Added missing arguments: scanned_files=0, skipped_files=[]
    render_duplicates({}, config, False, 0.0, 0.1, 0, 0, 0, [])
    captured = capsys.readouterr()
    assert 'No duplicates found' in captured.out


def test_render_search_singleton(capsys):
    """Test singleton search output."""
    config = Mock(spec=Config, preview=False, fail_on_duplicates=False)
    results = {'class UIManager': [('file.py:1', 'snippet')]}
    render_search(results, config)
    captured = capsys.readouterr()
    assert 'Verified singleton' in captured.out
    assert 'file.py:1' in captured.out


# FIXED: Refactored test to use capsys fixture instead of patching sys.stdout
def test_render_search_json(capsys):
    """Test JSON search output."""
    config = Mock(spec=Config, verbose=True, search_specs=[])
    config.root = Path('.')
    results = {'class UIManager': [('file.py:1', 'snippet')]}

    # Call the function directly, capsys will capture the print
    render_search_json(results, config, 1, [])

    # Get the captured output
    output = capsys.readouterr().out

    parsed = json.loads(output)
    assert parsed['search_results']['class UIManager']['is_singleton'] is True
    assert len(parsed['search_results']['class UIManager']['occurrences']) == 1


def test_render_duplicates_with_metrics(capsys):
    """Test dup rate alert."""
    
    # ** THE FIX IS HERE: Added preview=False **
    config = Mock(spec=Config, dup_threshold=0.1, json_output=False, fail_on_duplicates=False, audit_enabled=False, preview=False, html_report=None)
    
    # FIXED: Added missing arguments: scanned_files=0, skipped_files=[]
    render_duplicates({}, config, False, 0.15, 0.1, 100, 15, 0, [])
    captured = capsys.readouterr()
    
    # ** ADDED THIS ASSERT (it was missing from your file copy) **
    assert 'ALERT: Duplication rate' in captured.out
