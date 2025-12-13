import os
import yaml
from pathlib import Path

def test_pre_commit_hook_config_exists():
    """Test that the .pre-commit-hooks.yaml file exists in the project root."""
    # Assuming tests are in tests/ and .pre-commit-hooks.yaml is in root
    root_dir = Path(__file__).parent.parent
    hook_file = root_dir / ".pre-commit-hooks.yaml"

    assert hook_file.exists(), ".pre-commit-hooks.yaml not found in project root"

def test_pre_commit_hook_config_content():
    """Test the content of the pre-commit hook configuration."""
    root_dir = Path(__file__).parent.parent
    hook_file = root_dir / ".pre-commit-hooks.yaml"

    if not hook_file.exists():
        return # Test will fail in the previous test case

    with open(hook_file, "r") as f:
        hooks = yaml.safe_load(f)

    assert isinstance(hooks, list), "Hooks should be a list"
    assert len(hooks) > 0, "No hooks defined"

    hook = hooks[0]
    assert hook["id"] == "duplifinder"
    assert hook["name"] == "Duplifinder"
    assert hook["entry"] == "duplifinder"
    assert hook["language"] == "python"
    assert "python" in hook["types"]
