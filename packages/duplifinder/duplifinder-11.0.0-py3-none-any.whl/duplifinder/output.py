# src/duplifinder/output.py

"""Re-exports for backward compatibility; use submodules for new code."""

from .duplicate_renderer import render_duplicates
from .search_renderer import render_search, render_search_json
from .html_renderer import render_html_report

__all__ = ["render_duplicates", "render_search", "render_search_json", "render_html_report"]