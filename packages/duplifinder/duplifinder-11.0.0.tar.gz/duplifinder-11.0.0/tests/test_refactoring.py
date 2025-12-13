import pytest
from duplifinder.refactoring import get_refactoring_suggestion

def test_function_duplication_suggestion():
    suggestion = get_refactoring_suggestion("function process_data", 3)
    assert "Extract 'process_data' to a shared utility module" in suggestion

def test_class_duplication_suggestion():
    suggestion = get_refactoring_suggestion("class UserHandler", 2)
    assert "Consider using inheritance or composition" in suggestion
    assert "UserHandler" in suggestion

def test_text_duplication_suggestion():
    suggestion = get_refactoring_suggestion("text", 5)
    assert "Move duplicated text to a constant" in suggestion

def test_async_function_duplication_suggestion():
    suggestion = get_refactoring_suggestion("async function fetch_data", 2)
    assert "Extract 'fetch_data' to a shared utility module" in suggestion

def test_token_duplication_suggestion():
    suggestion = get_refactoring_suggestion("token", 2)
    assert "Refactor the similar logic into a shared function" in suggestion
