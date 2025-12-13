import os
from pathlib import Path
from duplifinder.config import Config
from duplifinder.utils import discover_py_files

def test_multilanguage_discovery(fs):
    fs.create_file("test.py", contents="def foo(): pass")
    fs.create_file("test.js", contents="function foo() { }")
    fs.create_file("test.ts", contents="function foo(): void { }")
    fs.create_file("test.java", contents="public class Test { }")
    fs.create_file("test.cpp", contents="int main() { }")

    config = Config(root=Path("."))
    # Ensure default extensions include py, js, ts, java
    assert "js" in config.extensions
    assert "ts" in config.extensions
    assert "java" in config.extensions

    files = discover_py_files(config)
    filenames = [f.name for f in files]

    assert "test.py" in filenames
    assert "test.js" in filenames
    assert "test.ts" in filenames
    assert "test.java" in filenames
    assert "test.cpp" not in filenames

def test_custom_extensions(fs):
    fs.create_file("test.go", contents="package main")
    config = Config(root=Path("."), extensions={"go"})

    files = discover_py_files(config)
    filenames = [f.name for f in files]

    assert "test.go" in filenames
    assert "test.py" not in filenames  # If overridden
