# tests/test_config.py

"""Tests for Config validation."""

import pytest
from pathlib import Path
from pydantic import ValidationError
from duplifinder.config import Config, load_config_file
from duplifinder.exceptions import ConfigError


def test_valid_config_creation():
    """Test valid Config instantiation."""
    config = Config(root=Path("."), types_to_search={"class"})
    assert config.root == Path(".")
    assert config.types_to_search == {"class"}
    assert 0.0 <= config.similarity_threshold <= 1.0


def test_invalid_types_validation():
    """Test unsupported types raise ConfigError (direct) or ValidationError (wrapped)."""
    # Note: If ConfigError inherits from Exception (not ValueError), Pydantic might propagate it directly.
    # If it is wrapped, it will be ValidationError.
    # Based on local test, if ConfigError inherits from Exception, it is propagated directly!
    # But my previous test failed showing ConfigError WAS raised but pytest caught it. Wait.
    # The previous failure said:
    # E   duplifinder.exceptions.ConfigError: Unsupported types: invalid. Supported: async_def, def, class
    # AND the test used `with pytest.raises(ValidationError)`.
    # So it DID raise ConfigError directly.

    with pytest.raises(ConfigError) as exc:
        Config(types_to_search={"invalid"})
    assert "Unsupported types" in str(exc.value)


def test_regex_validation():
    """Test invalid regex raises ConfigError."""
    with pytest.raises(ConfigError) as exc:
        Config(pattern_regexes="[unclosed]") # Invalid regex
    assert "Invalid regex" in str(exc.value)


def test_search_specs_validation():
    """Test invalid search specs raise ConfigError."""
    with pytest.raises(ConfigError) as exc:
        Config(search_specs=["class"])  # Bare type
    assert "Must be 'type name'" in str(exc.value)

    with pytest.raises(ConfigError) as exc:
        Config(search_specs=["invalid Foo"])
    assert "Invalid type" in str(exc.value)


def test_load_config_file_valid(tmp_path: Path):
    """Test loading valid YAML."""
    yaml_file = tmp_path / ".duplifinder.yaml"
    yaml_file.write_text("root: .\ntypes_to_search: [class]")
    config_dict = load_config_file(yaml_file)
    assert config_dict["root"] == "."
    assert config_dict["types_to_search"] == ["class"]


def test_load_config_file_invalid(tmp_path: Path):
    """Test loading invalid YAML raises ConfigError."""
    # load_config_file raises ConfigError directly, not wrapped in ValidationError
    yaml_file = tmp_path / "invalid.yaml"
    yaml_file.write_text("invalid: yaml: syntax")
    with pytest.raises(ConfigError, match="Failed to load config"):
        load_config_file(yaml_file)
