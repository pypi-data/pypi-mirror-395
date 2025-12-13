# tests/test_utils.py

import pytest
from pathlib import Path
import json
import logging
from unittest.mock import Mock, patch
from duplifinder.utils import (
    audit_log_event,
    run_parallel,
    discover_py_files,
    _parse_gitignore,
    _matches_gitignore,
    log_file_count
)
from duplifinder.config import Config


@pytest.fixture
def audit_config(tmp_path: Path) -> Config:
    """Fixture for an audit-enabled config."""
    log_file = tmp_path / "audit.jsonl"
    return Config(
        root=tmp_path,
        audit_enabled=True,
        audit_log_path=log_file,
        verbose=True
    )

def test_audit_log_event_enabled(audit_config: Config):
    """Test that audit log events are written when enabled."""
    audit_log_event(audit_config, "test_event", key="value")

    log_file = audit_config.audit_log_path
    assert log_file.exists()
    with open(log_file, "r") as f:
        data = json.loads(f.read())

    assert data["event_type"] == "test_event"
    assert data["key"] == "value"
    assert "timestamp" in data

def test_audit_log_event_disabled(tmp_path: Path):
    """Test that no log file is created when audit is disabled."""
    log_file = tmp_path / "audit.jsonl"
    config = Config(audit_enabled=False, audit_log_path=log_file)

    audit_log_event(config, "test_event")

    assert not log_file.exists()

def test_run_parallel_sequential(mock_config: Config):
    """Test run_parallel in sequential (non-parallel) mode."""
    mock_config.parallel = False
    items = [Path("a.py"), Path("b.py")]
    process_fn = Mock(return_value="processed")

    # FIXED: Removed "src." from the patch path
    with patch("duplifinder.utils.tqdm", side_effect=lambda x, **kwargs: x):
         results = list(run_parallel(items, process_fn, config=mock_config))

    assert results == ["processed", "processed"]
    assert process_fn.call_count == 2

def test_run_parallel_parallel(mock_config: Config):
    """Test run_parallel in parallel mode (with ThreadPoolExecutor)."""
    mock_config.parallel = True
    mock_config.use_multiprocessing = False
    mock_config.max_workers = 2
    items = [Path("a.py"), Path("b.py")]
    process_fn = Mock(return_value="processed")

    # FIXED: Removed "src." from the patch path
    with patch("duplifinder.utils.tqdm") as mock_tqdm:
        # Mock the as_completed iterator
        mock_future = Mock()
        mock_future.result.return_value = "processed"

        # This mocks the result of as_completed(futures)
        mock_tqdm.return_value = [mock_future, mock_future]

        results = list(run_parallel(items, process_fn, config=mock_config))

    # In a real parallel run, results might be out of order, but here we mock the return.
    assert results == ["processed", "processed"]
    assert process_fn.call_count == 2

def test_parse_gitignore(tmp_path: Path, audit_config: Config):
    """Test parsing of .gitignore files."""
    gitignore = tmp_path / ".gitignore"
    gitignore.write_text("*.log\n!important.log\n# a comment\n/build/\n!\nnegated.txt\n")
    audit_config.root = tmp_path

    patterns = _parse_gitignore(gitignore, audit_config)
    assert "*.log" in patterns
    assert "!important.log" in patterns
    assert "# a comment" not in patterns
    assert "/build/" in patterns
    assert "!negated.txt" in patterns  # Test the '!\npattern' format

def test_discover_py_files_with_gitignore(tmp_path: Path, mock_config: Config):
    """Test that discover_py_files respects .gitignore."""
    mock_config.root = tmp_path
    mock_config.respect_gitignore = True
    (tmp_path / ".gitignore").write_text("bad.py\n__pycache__/\n")

    (tmp_path / "good.py").write_text("class Good: pass")
    (tmp_path / "bad.py").write_text("class Bad: pass")

    # Test directory exclusion
    (tmp_path / "__pycache__").mkdir()
    (tmp_path / "__pycache__" / "cache.py").write_text("pass")

    # FIXED: Removed "src." from the patch path
    with patch("duplifinder.utils.mimetypes.guess_type", return_value=("text/x-python", None)):
        files = discover_py_files(mock_config)

    paths = [f.name for f in files]

    assert "good.py" in paths
    assert "bad.py" not in paths
    assert "cache.py" not in paths

def test_log_file_count(caplog, mock_config: Config):
    """Test verbose logging of file count."""
    mock_config.verbose = True
    with caplog.at_level(logging.INFO):
        log_file_count([Path("a.py")], mock_config, "testing")

    assert "Found 1 Python files to testing" in caplog.text


def test_audit_log_event_write_error(audit_config: Config, caplog):
    """Test that audit log write failures are warned."""
    # Patch open to fail
    with patch("builtins.open", side_effect=IOError("Permission denied")):
        audit_log_event(audit_config, "test_event")

    assert "Audit log write failed: Permission denied" in caplog.text

def test_parse_gitignore_read_error(tmp_path: Path, audit_config: Config, caplog):
    """Test _parse_gitignore handles read errors."""
    gitignore = tmp_path / ".gitignore"
    gitignore.write_text("*.log")
    audit_config.root = tmp_path

    with patch("builtins.open", side_effect=IOError("Cannot read")):
        patterns = _parse_gitignore(gitignore, audit_config)

    assert patterns == []
    assert "Failed to parse .gitignore" in caplog.text


def test_discover_py_files_non_python_mime(tmp_path: Path, mock_config: Config, caplog):
    """Test discover_py_files skips non-python mime types."""
    mock_config.root = tmp_path
    (tmp_path / "test.py").write_text("pass")

    # ** THE FIX IS HERE: Set caplog level to INFO **
    with patch("mimetypes.guess_type", return_value=("text/plain", None)), \
         caplog.at_level(logging.INFO):
        files = discover_py_files(mock_config)

    assert "MIME text/plain" in caplog.text
    assert len(files) == 0

def test_discover_py_files_no_markers(tmp_path: Path, mock_config: Config, caplog):
    """Test discover_py_files skips .py files with no Python markers."""
    mock_config.root = tmp_path
    (tmp_path / "test.py").write_text("just some text") # No 'def' or 'class'

    # ** THE FIX IS HERE: Set caplog level to INFO **
    with patch("mimetypes.guess_type", return_value=("text/x-python", None)), \
         caplog.at_level(logging.INFO):
        files = discover_py_files(mock_config)

    assert "No Python markers" in caplog.text
    assert len(files) == 0


def test_run_parallel_multiprocessing(mock_config: Config):
    """Test run_parallel with ProcessPoolExecutor."""
    mock_config.parallel = True
    mock_config.use_multiprocessing = True # <-- Key change
    mock_config.max_workers = 2
    items = [Path("a.py"), Path("b.py")]
    process_fn = Mock(return_value="processed")

    # FIXED: Removed "src." from patch paths
    with patch("duplifinder.utils.tqdm") as mock_tqdm, \
         patch("concurrent.futures.ProcessPoolExecutor") as mock_executor:

        mock_future = Mock()
        mock_future.result.return_value = "processed"
        mock_tqdm.return_value = [mock_future, mock_future]

        mock_executor.return_value.__enter__.return_value.submit.return_value = mock_future

        results = list(run_parallel(items, process_fn, config=mock_config))

    assert results == ["processed", "processed"]



def test_matches_gitignore_negation(mock_config: Config):
    """Test .gitignore negation logic."""
    mock_config.root = Path("/app")
    # Patterns must match relative paths
    patterns = ["!logs/important.log", "logs/*.log"]

    assert _matches_gitignore(Path("/app/logs/test.log"), patterns, mock_config) is True
    assert _matches_gitignore(Path("/app/logs/important.log"), patterns, mock_config) is False



def test_discover_py_files_stat_error(tmp_path: Path, audit_config, caplog):
    """Test discover_py_files handles stat errors."""
    audit_config.root = tmp_path

    mock_file = Mock(spec=Path)
    mock_file.name = "test.py"
    mock_file.suffix = ".py" # Needs suffix to be checked as a python file
    mock_file.parts = ("test.py",)
    mock_file.relative_to.return_value = Path("test.py") # Required for gitignore check
    mock_file.stat.side_effect = PermissionError("stat failed")

    # FIXED: Added mimetypes patch here as well.
    with patch("pathlib.Path.rglob", return_value=[mock_file]), \
         patch("mimetypes.guess_type", return_value=("text/x-python", None)):
        files = discover_py_files(audit_config)

    log_content = audit_config.audit_log_path.read_text()
    assert "stat_failed" in log_content
    assert len(files) == 0  # File is skipped because open() is not mocked for the Mock path object


def test_discover_py_files_read_header_error(tmp_path: Path, audit_config, caplog):
    """Test discover_py_files handles read errors on header check."""
    audit_config.root = tmp_path
    (tmp_path / "test.py").touch()

    audit_config.respect_gitignore = False

    original_open = open

    def smart_open(path, *args, **kwargs):
        # Make sure we only fail the 'rb' read, not the audit log 'a' write
        if "test.py" in str(path) and args and args[0] == "rb":
            raise IOError("read failed")
        return original_open(path, *args, **kwargs)

    with patch("mimetypes.guess_type", return_value=("text/x-python", None)), \
         patch("builtins.open", side_effect=smart_open):
        files = discover_py_files(audit_config)

    log_content = audit_config.audit_log_path.read_text()
    assert "header_read_failed" in log_content
    assert len(files) == 0  # File is skipped