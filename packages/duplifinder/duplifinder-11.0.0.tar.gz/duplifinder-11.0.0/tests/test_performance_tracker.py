
import time
from unittest.mock import MagicMock, patch
import pytest
from duplifinder.utils import PerformanceTracker


@pytest.fixture
def mock_tracemalloc():
    with patch("duplifinder.utils.tracemalloc") as mock:
        yield mock


@pytest.fixture
def mock_time():
    with patch("duplifinder.utils.time") as mock:
        mock.perf_counter.side_effect = [100.0, 101.0, 103.0, 105.0]  # Start, Mark 1, Stop (Total), ...
        yield mock


@pytest.fixture
def mock_console():
    with patch("rich.console.Console") as mock:
        yield mock


def test_tracker_init():
    tracker = PerformanceTracker(verbose=True)
    assert tracker.verbose is True
    assert tracker.timings == {}
    assert tracker.phases == {}


def test_tracker_lifecycle_verbose(mock_tracemalloc, mock_time, mock_console):
    # Setup tracemalloc return
    mock_tracemalloc.get_traced_memory.return_value = (1000, 5000)  # current, peak
    mock_tracemalloc.is_tracing.return_value = False # Ensure is_tracing returns False initially

    tracker = PerformanceTracker(verbose=True)

    # Start
    tracker.start()
    assert tracker.start_time == 100.0
    mock_tracemalloc.start.assert_called_once()

    # Mark Phase
    tracker.mark_phase("Phase 1")
    # Duration = 101.0 - 100.0 = 1.0
    assert tracker.phases["Phase 1"] == 1.0

    # Stop
    tracker.stop()
    # Total = 103.0 - 100.0 = 3.0
    assert tracker.timings["total"] == 3.0
    assert tracker.peak_memory == 5000
    mock_tracemalloc.stop.assert_called_once()

    # Print Metrics
    tracker.print_metrics()
    mock_console.return_value.print.assert_called()


def test_tracker_lifecycle_non_verbose(mock_tracemalloc, mock_time, mock_console):
    tracker = PerformanceTracker(verbose=False)

    tracker.start()
    mock_tracemalloc.start.assert_not_called()

    tracker.mark_phase("Phase 1")
    assert "Phase 1" not in tracker.phases

    tracker.stop()
    mock_tracemalloc.stop.assert_not_called()

    tracker.print_metrics()
    mock_console.return_value.print.assert_not_called()
