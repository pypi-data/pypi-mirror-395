# src/duplifinder/utils.py

"""Shared utilities for file discovery and parallel execution."""

import concurrent.futures
import contextlib
import fnmatch
import json
import logging
import os
import mimetypes
import threading
import time
import tracemalloc
from pathlib import Path
from typing import Callable, Generator, List, Any, Dict, Optional

from tqdm import tqdm

from .config import Config  # <-- Make sure this import is here


def audit_log_event(config: Config, event_type: str, **kwargs) -> None:
    """Emit structured audit event to JSONL if enabled; thread/process-safe append."""
    if not config.audit_enabled:
        return
    event = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "event_type": event_type,
        "root": str(config.root),
        "user": os.environ.get("USER", "unknown"),
        "worker_id": threading.current_thread().name if not config.use_multiprocessing else os.getpid(),
        **kwargs,
    }
    try:
        with open(config.audit_log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(event) + "\n")
            f.flush()  # Ensure visibility in parallel
    except Exception as e:
        logging.warning(f"Audit log write failed: {e}")


# FIXED: Added config: Config argument
def _parse_gitignore(gitignore_path: Path, config: Config) -> List[str]:
    """Simple stdlib parser for .gitignore: lines as fnmatch patterns (basic support for ! negation)."""
    patterns = []
    negate = False
    try:
        with open(gitignore_path, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line or line.startswith("#"):  # Skip comments/empty
                    continue
                if line == "!":  # Negation toggle (basic handling)
                    negate = True
                    continue
                pattern = line
                if negate:
                    pattern = "!" + pattern  # Prefix for negation logic in filter
                    negate = False
                patterns.append(pattern)
        if config.verbose:
            logging.info(f"Parsed {len(patterns)} .gitignore patterns from {gitignore_path}")
        audit_log_event(config, "gitignore_parsed", path=str(gitignore_path), patterns_count=len(patterns))
        return patterns
    except Exception as e:
        logging.warning(f"Failed to parse .gitignore '{gitignore_path}': {e}")
        return []


# FIXED: Added config: Config argument
def _matches_gitignore(path: Path, patterns: List[str], config: Config) -> bool:
    """Check if path matches any .gitignore pattern (with negation support)."""
    rel_path = path.relative_to(config.root).as_posix()
    for pattern in patterns:
        if pattern.startswith("!"):  # Negation: skip if matches
            if fnmatch.fnmatch(rel_path, pattern[1:]):
                return False  # Explicit include overrides
        elif fnmatch.fnmatch(rel_path, pattern):
            return True  # Exclude match
    return False


def discover_py_files(config: Config) -> List[Path]:
    """Discover files to scan, excluding ignored dirs and .gitignore patterns."""
    gitignore_patterns: List[str] = []
    gitignore_path = config.root / ".gitignore"
    if config.respect_gitignore and gitignore_path.exists():
        # FIXED: Pass config
        gitignore_patterns = _parse_gitignore(gitignore_path, config)

    # Build glob patterns from config extensions
    glob_patterns = [f"*.{ext}" for ext in config.extensions]

    candidates = []
    for pattern in glob_patterns:
        candidates.extend(
            p for p in config.root.rglob(pattern)
            if not any(part in config.ignore_dirs for part in p.parts)
            # FIXED: Pass config
            and not _matches_gitignore(p, gitignore_patterns, config)
        )

    py_files = []
    for p in candidates:
        # Audit: Log discovery attempt
        try:
            stat = p.stat()
            audit_log_event(config, "file_discovered", path=str(p), size=stat.st_size)
        except Exception:
            audit_log_event(config, "file_discovered", path=str(p), size=0, error="stat_failed")

        # Only check Python files for Python markers
        if p.suffix == ".py":
            # Check MIME/content for non-Py masqueraders
            mime, _ = mimetypes.guess_type(str(p))
            if mime and mime != "text/x-python":
                audit_log_event(config, "file_skipped", path=str(p), reason=f"MIME {mime}")
                logging.info(f"Skipping non-Py file '{p}': MIME {mime}")
                continue

            # Quick content check (first 1024 bytes)
            try:
                with open(p, "rb") as f:
                    header = f.read(1024)
                    if not (header.startswith(b"#!") or b"def " in header or b"class " in header):
                        audit_log_event(config, "file_skipped", path=str(p), reason="No Python markers")
                        logging.info(f"Skipping non-Py content '{p}': No Python markers")
                        continue
            except Exception:
                audit_log_event(config, "file_skipped", path=str(p), reason="header_read_failed")
                continue

        py_files.append(p)
        audit_log_event(config, "file_accepted", path=str(p))

    return py_files


def run_parallel(
    py_files: List[Path],
    process_fn: Callable,
    *args,
    config: Config,
    **kwargs
) -> Generator[Any, None, None]:
    """Shared parallel execution logic (generator)."""
    if config.max_workers is None:
        config.max_workers = os.cpu_count() or 4
    executor_cls = concurrent.futures.ProcessPoolExecutor if config.use_multiprocessing else concurrent.futures.ThreadPoolExecutor
    with executor_cls(max_workers=config.max_workers) if config.parallel else contextlib.nullcontext() as executor:
        if config.parallel:
            futures = []
            for idx, p in enumerate(py_files):
                future = executor.submit(process_fn, p, *args, config=config, **kwargs)
                # Audit: Log task dispatch
                audit_log_event(config, "task_submitted", file_path=str(p), future_id=id(future), index=idx)
                futures.append(future)
            for future in tqdm(concurrent.futures.as_completed(futures), total=len(py_files), disable=not config.verbose, desc="Processing files"):
                result = future.result()
                # Audit: Log completion (basic; detailed in processors)
                audit_log_event(config, "task_completed", future_id=id(future), success=True, error=None)
                yield result
        else:
            for py_file in tqdm(py_files, disable=not config.verbose, desc="Processing files"):
                # Audit: Log sequential dispatch
                audit_log_event(config, "task_submitted", file_path=str(py_file), future_id=None, index=None)
                result = process_fn(py_file, *args, config=config, **kwargs)
                audit_log_event(config, "task_completed", file_path=str(py_file), success=True, error=None)
                yield result


def log_file_count(py_files: List[Path], config: Config, context: str = "process") -> None:
    """Log the number of files discovered."""
    count = len(py_files)
    if config.verbose:
        logging.info(f"Found {count} Python files to {context}.")
    # Audit: Summary event
    audit_log_event(config, "discovery_summary", file_count=count, context=context)


class PerformanceTracker:
    """Tracks timing and memory usage for performance metrics."""

    def __init__(self, verbose: bool):
        self.verbose = verbose
        self.start_time = 0.0
        self.timings: Dict[str, float] = {}
        self.phases: Dict[str, float] = {}
        self.peak_memory = 0
        self._phase_start = 0.0

    def start(self):
        """Start tracking."""
        if self.verbose:
            self.start_time = time.perf_counter()
            if not tracemalloc.is_tracing():
                tracemalloc.start()
            self._phase_start = self.start_time

    def reset(self):
        """Reset internal state for re-runs."""
        self.start_time = 0.0
        self.timings = {}
        self.phases = {}
        self.peak_memory = 0
        self._phase_start = 0.0
        if tracemalloc.is_tracing():
            tracemalloc.stop()

    def mark_phase(self, name: str):
        """Mark the end of a phase and start a new one."""
        if self.verbose:
            now = time.perf_counter()
            duration = now - self._phase_start
            self.phases[name] = duration
            self._phase_start = now

    def stop(self):
        """Stop tracking and capture final metrics."""
        if self.verbose:
            # Capture total time
            total_duration = time.perf_counter() - self.start_time
            self.timings["total"] = total_duration

            # Capture peak memory
            _, peak = tracemalloc.get_traced_memory()
            self.peak_memory = peak
            tracemalloc.stop()

    def print_metrics(self):
        """Print performance metrics to console."""
        if self.verbose:
            from rich.console import Console
            from rich.table import Table

            console = Console()

            # Create main table
            table = Table(title="Performance Metrics", border_style="blue", show_header=True)
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="green")

            # Add general metrics
            table.add_row("Total Time", f"{self.timings.get('total', 0):.4f}s")
            table.add_row("Peak Memory", f"{self.peak_memory / 1024 / 1024:.2f} MB")

            console.print(table)

            # Create phases table
            if self.phases:
                phase_table = Table(title="Phase Breakdown", border_style="blue", show_header=True)
                phase_table.add_column("Phase", style="cyan")
                phase_table.add_column("Duration", style="green")
                phase_table.add_column("% of Total", style="yellow")

                total = self.timings.get('total', 1) # avoid div by zero
                for phase, duration in self.phases.items():
                    percent = (duration / total) * 100
                    phase_table.add_row(phase, f"{duration:.4f}s", f"{percent:.1f}%")

                console.print(phase_table)