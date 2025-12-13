
import pytest
from pathlib import Path
from duplifinder.html_renderer import render_html_report
from duplifinder.config import Config

def test_html_report_generation(tmp_path):
    report_path = tmp_path / "report.html"
    config = Config(html_report=report_path)

    duplicates = {
        "Function foo": [
            ("file1.py:10", "def foo():\n    pass"),
            ("file2.py:10", "def foo():\n    pass")
        ]
    }

    render_html_report(duplicates, config, 10, 100, 20, 0.2)

    assert report_path.exists()
    content = report_path.read_text(encoding="utf-8")
    assert "Duplifinder Report" in content
    assert "Function foo" in content
    assert "file1.py:10" in content
    assert "20.0%" in content

def test_html_report_no_path(tmp_path):
    config = Config(html_report=None)
    render_html_report({}, config, 0, 0, 0, 0)
    # Should not crash
