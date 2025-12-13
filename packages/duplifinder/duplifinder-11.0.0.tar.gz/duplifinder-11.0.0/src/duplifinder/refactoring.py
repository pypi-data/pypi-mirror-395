"""Module for generating refactoring suggestions based on duplicate types and occurrences."""

def get_refactoring_suggestion(duplicate_type: str, occurrences: int) -> str:
    """
    Generate a refactoring suggestion based on the duplicate type and number of occurrences.

    Args:
        duplicate_type (str): The type of duplicate (e.g., 'function my_func', 'class MyClass', 'text', 'token').
        occurrences (int): The number of times the duplicate appears.

    Returns:
        str: A string containing the refactoring suggestion.
    """
    if duplicate_type.startswith("function") or duplicate_type.startswith("async function"):
        # Handle "function name" and "async function name"
        parts = duplicate_type.split(" ")
        name = parts[-1] if len(parts) > 1 else "function"
        return f"Extract '{name}' to a shared utility module or a common base class."

    if duplicate_type.startswith("class"):
        name = duplicate_type.split(" ", 1)[1] if " " in duplicate_type else "class"
        return f"Consider using inheritance or composition to share '{name}' logic."

    if duplicate_type == "text":
        return "Move duplicated text to a constant, configuration file, or localization resource."

    if duplicate_type == "token":
        return "Refactor the similar logic into a shared function or parameterized method."

    return "Consider refactoring to reduce duplication."
