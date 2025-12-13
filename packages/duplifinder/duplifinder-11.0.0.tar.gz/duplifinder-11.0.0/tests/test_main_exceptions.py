
import sys
from unittest.mock import patch, MagicMock
import pytest
from pydantic import ValidationError
from duplifinder.main import main
from duplifinder.exceptions import DuplifinderError, ConfigError

def test_main_config_error(capsys):
    """Test main handles ConfigError."""
    with patch("duplifinder.main.create_parser") as mock_parser, \
         patch("duplifinder.main.build_config", side_effect=ConfigError("Bad config")), \
         patch("duplifinder.main.PerformanceTracker"):

        with pytest.raises(SystemExit) as exc:
            main()

        assert exc.value.code == 2
        captured = capsys.readouterr()
        assert "Configuration Error:\nBad config" in captured.err

def test_main_validation_error(capsys):
    """Test main handles Pydantic ValidationError."""
    # Create a mock ValidationError
    # ValidationError needs line_errors (list of dicts) and model
    mock_error = MagicMock(spec=ValidationError)
    mock_error.errors.return_value = [
        {'loc': ('field',), 'msg': 'Field is required', 'type': 'value_error'}
    ]
    # We need to make isinstance(e, ValidationError) work, so we need a real one or patch it.
    # But raising a real one is easier if we can.
    # Alternatively, just mock the exception class behavior if possible, but isinstance checks class.

    # Let's try to mock build_config to raise a real ValidationError
    # But constructing a real ValidationError is tricky without a model.
    # However, we can patch isinstance? No, that's messy.

    # Let's use a real model to generate a real ValidationError
    from pydantic import BaseModel
    class TestModel(BaseModel):
        f: int

    try:
        TestModel(f="not int")
    except ValidationError as e:
        real_error = e

    with patch("duplifinder.main.create_parser") as mock_parser, \
         patch("duplifinder.main.build_config", side_effect=real_error), \
         patch("duplifinder.main.PerformanceTracker"):

        with pytest.raises(SystemExit) as exc:
            main()

        assert exc.value.code == 2
        captured = capsys.readouterr()
        assert "Configuration Error:" in captured.err
        assert "Input should be a valid integer" in captured.err

def test_main_duplifinder_error(capsys):
    """Test main handles generic DuplifinderError during execution."""
    mock_config = MagicMock()
    mock_config.search_mode = False
    mock_config.token_mode = False
    mock_config.pattern_regexes = []

    with patch("duplifinder.main.create_parser"), \
         patch("duplifinder.main.build_config", return_value=mock_config), \
         patch("duplifinder.main.PerformanceTracker"), \
         patch("duplifinder.application.find_definitions", side_effect=DuplifinderError("Something went wrong")):

        with pytest.raises(SystemExit) as exc:
            main()

        assert exc.value.code == 1
        captured = capsys.readouterr()
        assert "Error: Something went wrong" in captured.err

def test_main_keyboard_interrupt(capsys):
    """Test main handles KeyboardInterrupt."""
    mock_config = MagicMock()
    mock_config.search_mode = False
    mock_config.token_mode = False
    mock_config.pattern_regexes = []

    with patch("duplifinder.main.create_parser"), \
         patch("duplifinder.main.build_config", return_value=mock_config), \
         patch("duplifinder.main.PerformanceTracker"), \
         patch("duplifinder.application.find_definitions", side_effect=KeyboardInterrupt):

        with pytest.raises(SystemExit) as exc:
            main()

        assert exc.value.code == 130
        captured = capsys.readouterr()
        assert "Operation cancelled by user" in captured.err

def test_main_generic_exception(capsys):
    """Test main handles unexpected Exception."""
    mock_config = MagicMock()
    mock_config.search_mode = False
    mock_config.token_mode = False
    mock_config.pattern_regexes = []

    with patch("duplifinder.main.create_parser"), \
         patch("duplifinder.main.build_config", return_value=mock_config), \
         patch("duplifinder.main.PerformanceTracker"), \
         patch("duplifinder.application.find_definitions", side_effect=RuntimeError("Boom")):

        with pytest.raises(SystemExit) as exc:
            main()

        assert exc.value.code == 1
        captured = capsys.readouterr()
        assert "An unexpected error occurred: Boom" in captured.err

def test_main_system_exit_propagation():
    """Test that SystemExit raised inside try block propagates (e.g. from sys.exit in finders)."""
    mock_config = MagicMock()
    mock_config.search_mode = False
    mock_config.token_mode = False
    mock_config.pattern_regexes = []

    with patch("duplifinder.main.create_parser"), \
         patch("duplifinder.main.build_config", return_value=mock_config), \
         patch("duplifinder.main.PerformanceTracker"), \
         patch("duplifinder.application.find_definitions", side_effect=SystemExit(3)):

        with pytest.raises(SystemExit) as exc:
            main()

        assert exc.value.code == 3
