# src/duplifinder/finder.py

"""Dispatcher for finder modes; import submodules for focused logic."""

from .definition_finder import find_definitions
from .text_finder import find_text_matches
from .token_finder import find_token_duplicates
from .search_finder import find_search_matches

__all__ = ["find_definitions", "find_text_matches", "find_token_duplicates", "find_search_matches"]