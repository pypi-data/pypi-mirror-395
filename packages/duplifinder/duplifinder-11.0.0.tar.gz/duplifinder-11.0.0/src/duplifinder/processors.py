# src/duplifinder/processors.py

"""Re-exports for backward compatibility; use submodules for new code."""

from .ast_processor import process_file_ast
from .text_processor import process_file_text
from .token_processor import process_file_tokens, tokenize_block
from .processor_utils import estimate_dup_lines

__all__ = ["process_file_ast", "process_file_text", "process_file_tokens", "tokenize_block", "estimate_dup_lines"]