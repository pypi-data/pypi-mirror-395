# tests/test_cli.py

"""Tests for CLI parsing and config building."""

import argparse
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from duplifinder.cli import create_parser, build_config
from duplifinder.config import Config, DEFAULT_IGNORES


def test_create_parser_basic():
    """Test parser creation and --help."""
    parser = create_parser()
    assert isinstance(parser, argparse.ArgumentParser)
    assert parser.description == "Find duplicate Python definitions across a project."


def test_create_parser_args_parsing():
    """Test arg parsing with sample CLI."""
    parser = create_parser()
    args = parser.parse_args([".", "--verbose", "--find", "class", "--pattern-regex", "TODO"])
    assert args.root == ["."]
    assert args.verbose is True
    assert args.find == ["class"]
    assert args.pattern_regex == ["TODO"]


def test_build_config_default():
    """Test build_config with no args (defaults)."""
    mock_args = Mock(spec=argparse.Namespace)
    mock_args.root = []
    mock_args.config = None
    mock_args.verbose = False
    mock_args.ignore = ""
    mock_args.exclude_patterns = ""
    mock_args.exclude_names = ""
    mock_args.find_regex = []
    mock_args.pattern_regex = []
    mock_args.search = None
    mock_args.find = []
    mock_args.min = 2
    mock_args.token_mode = False
    mock_args.similarity_threshold = 0.8
    mock_args.dup_threshold = 0.1
    mock_args.json = False
    mock_args.fail = False
    mock_args.parallel = False
    mock_args.use_multiprocessing = False
    mock_args.max_workers = None
    mock_args.preview = False
    # FIXED: Add missing mock attributes
    mock_args.audit = False
    mock_args.audit_log = None
    mock_args.no_gitignore = False
    mock_args.watch = False
    mock_args.extensions = []
    with patch("duplifinder.cli.load_config_file", return_value={}):
        config = build_config(mock_args)
    assert config.root == Path(".")
    assert config.types_to_search == {"class", "def", "async_def"}
    assert config.ignore_dirs == DEFAULT_IGNORES
    assert config.min_occurrences == 2


def test_build_config_with_yaml(tmp_path):
    """Test merge CLI + YAML."""
    mock_args = Mock(spec=argparse.Namespace)
    mock_args.root = []
    mock_args.config = "dummy.yaml"  # Dummy; patch load
    mock_args.min = 2
    mock_args.verbose = True
    mock_args.ignore = ""
    mock_args.exclude_patterns = ""
    mock_args.exclude_names = ""
    mock_args.find_regex = []
    mock_args.pattern_regex = []
    mock_args.search = None
    mock_args.find = []
    mock_args.token_mode = False
    mock_args.similarity_threshold = 0.8
    mock_args.dup_threshold = 0.1
    mock_args.json = False
    mock_args.fail = False
    mock_args.parallel = False
    mock_args.use_multiprocessing = False
    mock_args.max_workers = None
    mock_args.preview = False
    # FIXED: Add missing mock attributes
    mock_args.audit = False
    mock_args.audit_log = None
    mock_args.no_gitignore = False
    mock_args.watch = False
    mock_args.extensions = []
    with patch("duplifinder.cli.load_config_file", return_value={'find': ['class'], 'min': 3}):
        config = build_config(mock_args)
    assert config.types_to_search == {"class"}
    assert config.min_occurrences == 2  # CLI precedence


def test_build_config_invalid_regex():
    """Test Pydantic validation raises SystemExit(2)."""
    mock_args = Mock(spec=argparse.Namespace)
    mock_args.root = []
    mock_args.config = None
    mock_args.verbose = False
    mock_args.pattern_regex = ["[unclosed"]  # Invalid: unclosed character class
    mock_args.ignore = ""
    mock_args.exclude_patterns = ""
    mock_args.exclude_names = ""
    mock_args.find_regex = []
    mock_args.search = None
    mock_args.find = []
    mock_args.min = 2
    mock_args.token_mode = False
    mock_args.similarity_threshold = 0.8
    mock_args.dup_threshold = 0.1
    mock_args.json = False
    mock_args.fail = False
    mock_args.parallel = False
    mock_args.use_multiprocessing = False
    mock_args.max_workers = None
    mock_args.preview = False
    # FIXED: Add missing mock attributes
    mock_args.audit = False
    mock_args.audit_log = None
    mock_args.no_gitignore = False
    mock_args.watch = False
    mock_args.extensions = []
    mock_args.watch = False
    mock_args.extensions = []
    mock_args.watch = False
    mock_args.extensions = []
    with patch("duplifinder.cli.load_config_file", return_value={}):
        with pytest.raises(SystemExit) as exc:
            build_config(mock_args)
        assert exc.value.code == 2


def test_build_config_invalid_search_spec():
    """Test invalid search spec → SystemExit(2)."""
    mock_args = Mock(spec=argparse.Namespace)
    mock_args.root = []
    mock_args.config = None
    mock_args.verbose = False
    mock_args.search = ["class"]  # Bare type
    mock_args.ignore = ""
    mock_args.exclude_patterns = ""
    mock_args.exclude_names = ""
    mock_args.find_regex = []
    mock_args.pattern_regex = []
    mock_args.find = []
    mock_args.min = 2
    mock_args.token_mode = False
    mock_args.similarity_threshold = 0.8
    mock_args.dup_threshold = 0.1
    mock_args.json = False
    mock_args.fail = False
    mock_args.parallel = False
    mock_args.use_multiprocessing = False
    mock_args.max_workers = None
    mock_args.preview = False
    # FIXED: Add missing mock attributes
    mock_args.audit = False
    mock_args.audit_log = None
    mock_args.no_gitignore = False
    mock_args.watch = False
    mock_args.extensions = []
    mock_args.watch = False
    mock_args.extensions = []
    with patch("duplifinder.cli.load_config_file", return_value={}):
        with pytest.raises(SystemExit) as exc:
            build_config(mock_args)
        assert exc.value.code == 2


def test_build_config_find_processing():
    """Test --find arg processing."""
    mock_args = Mock(spec=argparse.Namespace)
    mock_args.root = []
    mock_args.config = None
    mock_args.verbose = False
    mock_args.find = ["class", "MyDef"]
    mock_args.ignore = ""
    mock_args.exclude_patterns = ""
    mock_args.exclude_names = ""
    mock_args.find_regex = []
    mock_args.pattern_regex = []
    mock_args.search = None
    mock_args.min = 2
    mock_args.token_mode = False
    mock_args.similarity_threshold = 0.8
    mock_args.dup_threshold = 0.1
    mock_args.json = False
    mock_args.fail = False
    mock_args.parallel = False
    mock_args.use_multiprocessing = False
    mock_args.max_workers = None
    mock_args.preview = False
    # FIXED: Add missing mock attributes
    mock_args.audit = False
    mock_args.audit_log = None
    mock_args.no_gitignore = False
    mock_args.watch = False
    mock_args.extensions = []
    with patch("duplifinder.cli.load_config_file", return_value={}):
        config = build_config(mock_args)
    assert "class" in config.types_to_search
    assert "MyDef" in config.filter_names
