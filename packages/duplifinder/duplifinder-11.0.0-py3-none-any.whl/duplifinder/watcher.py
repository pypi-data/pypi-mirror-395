import time
import threading
from typing import Callable, Any, List
from watchdog.events import PatternMatchingEventHandler, FileSystemEvent

class CodeWatcher(PatternMatchingEventHandler):
    """
    Watches for file changes matching specific patterns and sets a dirty flag.
    """
    def __init__(
        self,
        patterns: List[str] = None,
        ignore_patterns: List[str] = None,
        ignore_directories: bool = True,
        case_sensitive: bool = False
    ):
        super().__init__(
            patterns=patterns,
            ignore_patterns=ignore_patterns,
            ignore_directories=ignore_directories,
            case_sensitive=case_sensitive
        )
        self.dirty_event = threading.Event()
        self.last_path = ""

    def on_modified(self, event: FileSystemEvent) -> None:
        self._mark_dirty(event)

    def on_created(self, event: FileSystemEvent) -> None:
        self._mark_dirty(event)

    def on_deleted(self, event: FileSystemEvent) -> None:
        self._mark_dirty(event)

    def on_moved(self, event: FileSystemEvent) -> None:
        self._mark_dirty(event)

    def _mark_dirty(self, event: FileSystemEvent) -> None:
        self.last_path = event.src_path
        self.dirty_event.set()
