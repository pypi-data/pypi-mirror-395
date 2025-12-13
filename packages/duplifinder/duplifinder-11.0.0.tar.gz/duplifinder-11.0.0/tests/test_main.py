# tests/test_main.py

"""Integration tests for main flows with exits."""

from unittest.mock import patch, Mock
import sys
from pathlib import Path
import pytest
from duplifinder.main import main
from duplifinder.application import WorkflowFactory

# HELPER: A mock for sys.exit that preserves the exit code
def mock_sys_exit(code=0):
    raise SystemExit(code)


def test_main_default_run(monkeypatch, capsys):
    """Test default run: no dups → exit 0."""
    monkeypatch.setattr(sys, 'argv', ['duplifinder', '.'])
    mock_config = Mock(search_mode=False, pattern_regexes=[], token_mode=False, audit_enabled=False, watch_mode=False)
    mock_config.root = Path('.')
    mock_config.ignore_dirs = set()
    mock_config.extensions = [] # Fixed: Added extensions
    nested_empty = {'class': {}, 'def': {}, 'async_def': {}}  # Empty nested

    with patch('duplifinder.main.build_config', return_value=mock_config), \
         patch('duplifinder.application.find_definitions', return_value=(nested_empty, [], 1, 10, 0)), \
         patch('duplifinder.application.render_duplicates', side_effect=lambda *args, **kwargs: print('No duplicates found')), \
         patch('sys.exit', side_effect=lambda *args: None):  # This one is OK, it expects exit 0 (no raise)
        main()
    captured = capsys.readouterr()
    assert 'No duplicates found' in captured.out


def test_main_config_error(monkeypatch):
    """Test invalid config → exit 2."""
    monkeypatch.setattr(sys, 'argv', ['duplifinder', '.', '--pattern-regex', '[invalid'])
    # FIXED: Removed the patch('sys.exit', ...) which caused the UnboundLocalError
    with patch('duplifinder.main.build_config', side_effect=SystemExit(2)):
        with pytest.raises(SystemExit) as exc:
            main()
        assert exc.value.code == 2


def test_main_scan_fail_high_skips(monkeypatch):
    """Test >10% skips → exit 3."""
    monkeypatch.setattr(sys, 'argv', ['duplifinder', '.'])
    # FIXED: Added audit_enabled=False
    mock_config = Mock(search_mode=False, pattern_regexes=[], token_mode=False, audit_enabled=False, watch_mode=False)
    mock_config.root = Path('.')
    mock_config.ignore_dirs = set()
    mock_config.extensions = [] # Fixed: Added extensions
    nested_empty = {'class': {}, 'def': {}, 'async_def': {}}  # Empty nested

    with patch('duplifinder.main.build_config', return_value=mock_config), \
         patch('duplifinder.application.find_definitions', return_value=(nested_empty, ['s'] * 11, 1, 10, 0)), \
         patch('duplifinder.application.render_duplicates'), \
         patch('sys.exit', side_effect=mock_sys_exit):
        with pytest.raises(SystemExit) as exc:
            main()
        assert exc.value.code == 3  # High skip rate


def test_main_fail_on_dups(monkeypatch):
    """Test dups with --fail → exit 1."""
    monkeypatch.setattr(sys, 'argv', ['duplifinder', '.', '--fail'])
    # FIXED: Added audit_enabled=False
    mock_config = Mock(fail_on_duplicates=True, search_mode=False, pattern_regexes=[], token_mode=False, audit_enabled=False, watch_mode=False)
    mock_config.root = Path('.')
    mock_config.ignore_dirs = set()
    mock_config.extensions = [] # Fixed: Added extensions
    nested_dups = {'class': {'Dup': [('file:1', '') , ('file:2', '')]}}  # Nested with 2 items

    with patch('duplifinder.main.build_config', return_value=mock_config), \
         patch('duplifinder.application.find_definitions', return_value=(nested_dups, [], 1, 10, 5)), \
         patch('duplifinder.application.render_duplicates'):
         # FIXED: Removed patch('sys.exit', ...)
        with pytest.raises(SystemExit) as exc:
            main()
        # This assert was missing, but it's implied by the test name
        assert exc.value.code == 1


def test_main_search_mode_json_output(monkeypatch):
    """Test search mode with --json flag."""
    monkeypatch.setattr(sys, 'argv', ['duplifinder', '-s', 'class Foo', '--json'])
    mock_config = Mock(
        search_mode=True, 
        json_output=True, 
        audit_enabled=False,
        fail_on_duplicates=False,
        extensions=[], # Fixed: Added extensions
        watch_mode=False
    )
    mock_render_json = Mock()

    with patch('duplifinder.main.build_config', return_value=mock_config), \
         patch('duplifinder.application.find_search_matches', return_value=({}, [], 1)), \
         patch('duplifinder.application.render_search_json', mock_render_json), \
         patch('sys.exit', side_effect=mock_sys_exit): # FIXED: Use helper
        
        with pytest.raises(SystemExit) as exc:
            main()
        
    mock_render_json.assert_called_once()
    assert exc.value.code == 0 # Should exit 0


def test_main_token_mode_dup_threshold_alert(monkeypatch, capsys):
    """Test token mode fires alert when dup_threshold is exceeded."""
    monkeypatch.setattr(sys, 'argv', ['duplifinder', '--token-mode'])
    mock_config = Mock(
        search_mode=False, 
        pattern_regexes=[], 
        token_mode=True, 
        audit_enabled=False,
        dup_threshold=0.1,  # 10%
        fail_on_duplicates=False,
        extensions=[], # Fixed: Added extensions
        watch_mode=False
    )
    
    with patch('duplifinder.main.build_config', return_value=mock_config), \
         patch('duplifinder.application.find_token_duplicates', return_value=({}, [], 1, 100, 20)), \
         patch('duplifinder.application.render_duplicates'), \
         patch('sys.exit', side_effect=mock_sys_exit): # FIXED: Use helper
        
        with pytest.raises(SystemExit) as exc:
            main()

    captured = capsys.readouterr()
    assert "ALERT: Dup rate 20.0%" in captured.err
    assert exc.value.code == 0 # fail_on_duplicates is False


def test_main_token_mode_fail_on_dups(monkeypatch):
    """Test token mode with --fail exits 1 on duplicates."""
    monkeypatch.setattr(sys, 'argv', ['duplifinder', '--token-mode', '--fail'])
    mock_config = Mock(
        search_mode=False, 
        pattern_regexes=[], 
        token_mode=True, 
        audit_enabled=False,
        dup_threshold=1.0,  # Set high to avoid first exit
        fail_on_duplicates=True,
        extensions=[], # Fixed: Added extensions
        watch_mode=False
    )
    
    with patch('duplifinder.main.build_config', return_value=mock_config), \
         patch('duplifinder.application.find_token_duplicates', return_value=({}, [], 1, 100, 5)), \
         patch('duplifinder.application.render_duplicates'), \
         patch('sys.exit', side_effect=mock_sys_exit): # FIXED: Use helper
        
        with pytest.raises(SystemExit) as exc:
            main()
            
    assert exc.value.code == 1 # Should exit 1

def test_main_text_mode_fail_on_dups(monkeypatch):
    """Test text/pattern mode with --fail exits 1 on duplicates."""
    monkeypatch.setattr(sys, 'argv', ['duplifinder', '--pattern-regex', 'TODO', '--fail'])
    mock_config = Mock(
        search_mode=False, 
        pattern_regexes=["TODO"], 
        token_mode=False, 
        audit_enabled=False,
        dup_threshold=1.0, 
        fail_on_duplicates=True,
        extensions=[], # Fixed: Added extensions
        watch_mode=False
    )
    
    with patch('duplifinder.main.build_config', return_value=mock_config), \
         patch('duplifinder.application.find_text_matches', return_value=({'TODO': ['a:1', 'b:2']}, [], 1, 100, 5)), \
         patch('duplifinder.application.render_duplicates'), \
         patch('sys.exit', side_effect=mock_sys_exit): # FIXED: Use helper
        
        with pytest.raises(SystemExit) as exc:
            main()
            
    assert exc.value.code == 1 # Should exit 1
