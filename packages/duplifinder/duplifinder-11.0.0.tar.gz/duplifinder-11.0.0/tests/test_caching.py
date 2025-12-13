import json
import tempfile
import time
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from duplifinder.cache import CacheManager
from duplifinder.config import Config

@pytest.fixture
def temp_cache_dir():
    with tempfile.TemporaryDirectory() as tmp:
        yield Path(tmp)

def test_cache_manager_init(temp_cache_dir):
    config = Config(root=temp_cache_dir)
    # Mock cache path to be inside temp_cache_dir
    cache_path = temp_cache_dir / ".duplifinder_cache.json"
    manager = CacheManager(cache_path)
    assert manager.cache_path == cache_path
    assert manager.data == {}

def test_cache_save_load(temp_cache_dir):
    cache_path = temp_cache_dir / ".duplifinder_cache.json"
    manager = CacheManager(cache_path)
    manager.set("file1.py", "hash1", {"result": "data"})
    manager.save()

    assert cache_path.exists()

    # Reload
    manager2 = CacheManager(cache_path)
    manager2.load()
    assert manager2.get("file1.py", "hash1") == {"result": "data"}
    assert manager2.get("file1.py", "hash2") is None # Wrong hash

def test_cache_invalidation(temp_cache_dir):
    cache_path = temp_cache_dir / ".duplifinder_cache.json"
    manager = CacheManager(cache_path)
    manager.set("file1.py", "hash1", {"result": "data"})

    # Check invalidation
    assert manager.get("file1.py", "hash2") is None

def test_file_hashing(temp_cache_dir):
    f = temp_cache_dir / "test.py"
    f.write_text("content", encoding="utf-8")

    h = CacheManager.compute_hash(f)
    assert h is not None

    f.write_text("content2", encoding="utf-8")
    h2 = CacheManager.compute_hash(f)
    assert h != h2
