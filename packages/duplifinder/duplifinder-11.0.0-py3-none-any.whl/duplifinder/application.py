# src/duplifinder/application.py

"""Application workflow orchestration."""

import sys
import time
import re
from abc import ABC, abstractmethod
from typing import Dict, List, Tuple

from .config import Config
from watchdog.observers import Observer

from .watcher import CodeWatcher
from .utils import PerformanceTracker, audit_log_event
from .finder import find_definitions, find_text_matches, find_token_duplicates, find_search_matches
from .output import render_duplicates, render_search, render_search_json


class Workflow(ABC):
    """Abstract base class for Duplifinder workflows."""

    def __init__(self, config: Config, tracker: PerformanceTracker, workflow_start: float):
        self.config = config
        self.tracker = tracker
        self.workflow_start = workflow_start

    @abstractmethod
    def run(self) -> int:
        """Run the workflow and return exit code."""
        pass

    def run_with_watch(self) -> int:
        """Run the workflow in watch mode."""

        # Initial run
        print("\n🚀 Starting Watch Mode... (Press Ctrl+C to stop)\n")
        self.run()

        # Setup watcher with filters
        # Build patterns from extensions (e.g., ["*.py", "*.js"])
        patterns = [f"*.{ext}" for ext in self.config.extensions]

        # Build ignore patterns
        ignore_patterns = [f"{d}/*" for d in self.config.ignore_dirs]
        # Always ignore our own output files to prevent infinite loops
        ignore_patterns.append(str(self.config.audit_log_path.name))
        if self.config.html_report:
            ignore_patterns.append(str(self.config.html_report.name))
        ignore_patterns.append(".git/*")

        event_handler = CodeWatcher(
            patterns=patterns,
            ignore_patterns=ignore_patterns,
            ignore_directories=True,
            case_sensitive=False
        )
        observer = Observer()

        # Watch the root directory
        # If root is a file, watch its parent
        watch_path = str(self.config.root) if self.config.root.is_dir() else str(self.config.root.parent)
        observer.schedule(event_handler, watch_path, recursive=True)
        observer.start()

        print("\n👀 Watching for changes...\n")

        try:
            while True:
                # Check for dirty flag
                if event_handler.dirty_event.wait(timeout=1.0):
                    # Debounce: Wait a bit to coalesce rapid changes
                    time.sleep(0.5)
                    # Clear event immediately so we can detect changes during scan
                    event_handler.dirty_event.clear()

                    print(f"\n🔄 File changed ({event_handler.last_path})! Re-scanning...\n")

                    # Reset tracker and re-run
                    self.tracker.reset()
                    self.tracker.start()
                    self.workflow_start = time.perf_counter()
                    self.run()
                    print("\n👀 Watching for changes...\n")

        except KeyboardInterrupt:
            observer.stop()
            print("\n🛑 Stopping Watch Mode.")

        observer.join()
        return 0


class SearchWorkflow(Workflow):
    """Workflow for Search Mode."""

    def run(self) -> int:
        results, skipped, scanned = find_search_matches(self.config)
        self.tracker.mark_phase("Scanning")
        duration_ms = (time.perf_counter() - self.workflow_start) * 1000

        if self.config.json_output:
            render_search_json(results, self.config, scanned, skipped)
        else:
            render_search(results, self.config)
        self.tracker.mark_phase("Rendering")

        audit_log_event(self.config, "scan_completed", mode="search", scanned=scanned, skipped=len(skipped), duration_ms=duration_ms)

        self.tracker.stop()
        self.tracker.print_metrics()

        has_multi = any(len(occ) > 1 for occ in results.values())
        return 1 if (self.config.fail_on_duplicates and has_multi) else 0


class TokenWorkflow(Workflow):
    """Workflow for Token Mode."""

    def run(self) -> int:
        results, skipped, scanned, total_lines, dup_lines = find_token_duplicates(self.config)
        self.tracker.mark_phase("Scanning")
        dup_rate = dup_lines / total_lines if total_lines else 0
        duration_ms = (time.perf_counter() - self.workflow_start) * 1000

        if dup_rate > self.config.dup_threshold:
            print(f"ALERT: Dup rate {dup_rate:.1%} > threshold {self.config.dup_threshold:.1%}", file=sys.stderr)
            if self.config.fail_on_duplicates:
                return 1

        render_duplicates(results, self.config, False, dup_rate, self.config.dup_threshold, total_lines, dup_lines, scanned, skipped, is_token=True)
        self.tracker.mark_phase("Rendering")

        audit_log_event(self.config, "scan_completed", mode="token", scanned=scanned, skipped=len(skipped), total_lines=total_lines, dup_lines=dup_lines, dup_rate=dup_rate, duration_ms=duration_ms)

        self.tracker.stop()
        self.tracker.print_metrics()

        return 0 if not self.config.fail_on_duplicates or dup_lines == 0 else 1


class PatternWorkflow(Workflow):
    """Workflow for Pattern Regex Mode."""

    def run(self) -> int:
        patterns = [re.compile(p) for p in self.config.pattern_regexes]
        results, skipped, scanned, total_lines, dup_lines = find_text_matches(self.config, patterns)
        self.tracker.mark_phase("Scanning")
        dup_rate = dup_lines / total_lines if total_lines else 0
        duration_ms = (time.perf_counter() - self.workflow_start) * 1000

        render_duplicates(results, self.config, False, dup_rate, self.config.dup_threshold, total_lines, dup_lines, scanned, skipped)
        self.tracker.mark_phase("Rendering")

        audit_log_event(self.config, "scan_completed", mode="text_pattern", scanned=scanned, skipped=len(skipped), total_lines=total_lines, dup_lines=dup_lines, dup_rate=dup_rate, duration_ms=duration_ms)

        self.tracker.stop()
        self.tracker.print_metrics()

        return 0 if not self.config.fail_on_duplicates or dup_lines == 0 else 1


class DefaultWorkflow(Workflow):
    """Workflow for Default (Definition) Mode."""

    def run(self) -> int:
        results, skipped, scanned, total_lines, dup_lines = find_definitions(self.config)
        self.tracker.mark_phase("Scanning")
        dup_rate = dup_lines / total_lines if total_lines else 0
        duration_ms = (time.perf_counter() - self.workflow_start) * 1000

        # Scan fail if >10% skipped
        skip_rate = len(skipped) / (scanned + len(skipped)) if scanned + len(skipped) > 0 else 0
        if skip_rate > 0.1:
            print(f"SCAN FAIL: {skip_rate:.1%} files skipped (>10% threshold)", file=sys.stderr)
            audit_log_event(self.config, "scan_completed", mode="definitions", scanned=scanned, skipped=len(skipped), total_lines=total_lines, dup_lines=dup_lines, dup_rate=dup_rate, skip_rate=skip_rate, duration_ms=duration_ms, status="failed_skip_threshold")
            return 3  # Scan fail

        flat_results = self._flatten_definitions(results)
        render_duplicates(flat_results, self.config, False, dup_rate, self.config.dup_threshold, total_lines, dup_lines, scanned, skipped)
        self.tracker.mark_phase("Rendering")

        audit_log_event(self.config, "scan_completed", mode="definitions", scanned=scanned, skipped=len(skipped), total_lines=total_lines, dup_lines=dup_lines, dup_rate=dup_rate, duration_ms=duration_ms)

        self.tracker.stop()
        self.tracker.print_metrics()

        return 0 if not self.config.fail_on_duplicates or dup_lines == 0 else 1

    def _flatten_definitions(self, results: Dict[str, Dict[str, List[Tuple[str, str]]]]) -> Dict[str, List[Tuple[str, str]]]:
        """Flatten nested definitions to flat Dict[str, List[Tuple]]."""
        flat = {}
        for typ, name_locs in results.items():
            for name, items in name_locs.items():
                key = f"{typ} {name}"
                flat[key] = items
        return flat


class WorkflowFactory:
    """Factory to create the appropriate workflow."""

    @staticmethod
    def create(config: Config, tracker: PerformanceTracker, workflow_start: float) -> Workflow:
        if config.search_mode:
            return SearchWorkflow(config, tracker, workflow_start)
        elif config.token_mode:
            return TokenWorkflow(config, tracker, workflow_start)
        elif config.pattern_regexes:
            return PatternWorkflow(config, tracker, workflow_start)
        else:
            return DefaultWorkflow(config, tracker, workflow_start)
