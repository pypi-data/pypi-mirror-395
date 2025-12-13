# src/duplifinder/ast_visitor.py

"""AST visitor for collecting Python definitions."""

import ast
from collections import defaultdict
from typing import Dict, List, Set, Tuple

from .config import KNOWN_TYPES


class EnhancedDefinitionVisitor(ast.NodeVisitor):
    """AST visitor to collect definitions and method names within classes."""

    def __init__(self, types_to_search: Set[str]) -> None:
        self.definitions: Dict[str, List[Tuple[str, int, int, str]]] = defaultdict(list)
        self.types_to_search = types_to_search
        self.current_class = None  # Track class context for methods

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        if "class" in self.types_to_search:
            end_lineno = node.end_lineno if node.end_lineno is not None else node.lineno
            self.definitions["class"].append((node.name, node.lineno, end_lineno, ""))
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = None

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._collect_function(node, "def")

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._collect_function(node, "async_def")

    def _collect_function(self, node, typ: str) -> None:
        if typ not in self.types_to_search:
            return
        end_lineno = node.end_lineno if node.end_lineno is not None else node.lineno
        name = node.name
        if self.current_class:
            name = f"{self.current_class}.{name}"
        self.definitions[typ].append((name, node.lineno, end_lineno, ""))
        self.generic_visit(node)

    def generic_visit(self, node: ast.AST) -> None:
        # No additional collection here; handled in specific visit methods
        super().generic_visit(node)