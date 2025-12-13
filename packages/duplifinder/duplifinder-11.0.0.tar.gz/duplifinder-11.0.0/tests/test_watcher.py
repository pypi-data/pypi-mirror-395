import time
import pytest
from unittest.mock import MagicMock
from watchdog.events import FileSystemEvent
from duplifinder.watcher import CodeWatcher

class TestCodeWatcher:
    def test_init(self):
        watcher = CodeWatcher(patterns=["*.py"])
        assert watcher.patterns == ["*.py"]
        assert not watcher.dirty_event.is_set()

    def test_on_modified(self):
        watcher = CodeWatcher(patterns=["*.py"])
        event = FileSystemEvent("test.py")

        watcher.on_modified(event)

        assert watcher.dirty_event.is_set()
        assert watcher.last_path == "test.py"

    def test_on_created(self):
        watcher = CodeWatcher(patterns=["*.py"])
        event = FileSystemEvent("test.py")

        watcher.on_created(event)

        assert watcher.dirty_event.is_set()

    def test_on_deleted(self):
        watcher = CodeWatcher(patterns=["*.py"])
        event = FileSystemEvent("test.py")

        watcher.on_deleted(event)

        assert watcher.dirty_event.is_set()

    def test_ignores(self):
        # Note: watchdog's dispatch logic handles pattern matching before calling on_modified.
        # But PatternMatchingEventHandler logic is:
        # dispatch(event) -> checks patterns/ignores -> if match calls on_method

        watcher = CodeWatcher(patterns=["*.py"], ignore_patterns=["*.log"])

        # We can simulate the dispatch call to verify ignore logic if we want,
        # or we can trust watchdog library and just test that our _mark_dirty works.
        # Let's verify _mark_dirty is what we are testing here basically.

        event = FileSystemEvent("test.log")
        # Direct call to on_modified bypasses the filter logic in PatternMatchingEventHandler.dispatch
        # So we should test that on_modified sets the flag.
        watcher.on_modified(event)
        assert watcher.dirty_event.is_set()

    def test_pattern_matching_integration(self):
        """Verify that standard watchdog dispatch logic respects our configuration."""
        watcher = CodeWatcher(patterns=["*.py"], ignore_patterns=["*.log"])

        # 1. Match
        event_py = FileSystemEvent("src/main.py")
        event_py.event_type = "modified"
        event_py.is_directory = False

        # We need to simulate the dispatch call which does the filtering
        watcher.dispatch(event_py)
        assert watcher.dirty_event.is_set()
        watcher.dirty_event.clear()

        # 2. Ignore
        event_log = FileSystemEvent("app.log")
        event_log.event_type = "modified"
        event_log.is_directory = False

        watcher.dispatch(event_log)
        assert not watcher.dirty_event.is_set()
