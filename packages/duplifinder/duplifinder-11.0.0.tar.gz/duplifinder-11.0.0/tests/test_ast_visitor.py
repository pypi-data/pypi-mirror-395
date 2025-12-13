# tests/test_ast_visitor.py

"""Tests for AST visitor."""

import ast
from pathlib import Path  # Add import for consistency

from duplifinder.ast_visitor import EnhancedDefinitionVisitor


def test_class_detection():
    code = "class MyClass:\n    pass"
    tree = ast.parse(code)
    visitor = EnhancedDefinitionVisitor({'class'})
    visitor.visit(tree)
    assert len(visitor.definitions['class']) == 1
    assert visitor.definitions['class'][0][0] == 'MyClass'


def test_method_detection():
    code = """
class MyClass:
    def method(self):
        pass
    async def async_method(self):
        pass
"""
    tree = ast.parse(code)
    visitor = EnhancedDefinitionVisitor({'def', 'async_def'})
    visitor.visit(tree)
    assert len(visitor.definitions['def']) == 1
    assert visitor.definitions['def'][0][0] == 'MyClass.method'
    assert len(visitor.definitions['async_def']) == 1
    assert visitor.definitions['async_def'][0][0] == 'MyClass.async_method'


def test_standalone_functions():
    code = "def standalone(): pass\nasync def async_standalone(): pass"
    tree = ast.parse(code)
    visitor = EnhancedDefinitionVisitor({'def', 'async_def'})
    visitor.visit(tree)
    assert len(visitor.definitions['def']) == 1
    assert visitor.definitions['def'][0][0] == 'standalone'
    assert len(visitor.definitions['async_def']) == 1
    assert visitor.definitions['async_def'][0][0] == 'async_standalone'


def test_no_matching_types():
    code = "class MyClass: pass"
    tree = ast.parse(code)
    visitor = EnhancedDefinitionVisitor({'def'})  # No class
    visitor.visit(tree)
    assert 'class' not in visitor.definitions
    assert 'def' not in visitor.definitions  # No defs, so key not populated