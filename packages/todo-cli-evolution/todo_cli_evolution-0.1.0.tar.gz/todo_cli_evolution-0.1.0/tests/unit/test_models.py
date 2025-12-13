"""
Unit tests for the Todo domain model.

Tests cover creation, validation, and edge cases for the Todo entity.
"""

import pytest
from todo_cli.models import Todo


def test_create_todo_with_all_fields():
    """Test creating a Todo with all fields provided."""
    todo = Todo(
        id=None,
        title="Buy milk",
        description="From the store",
        completed=False
    )

    assert todo.title == "Buy milk"
    assert todo.description == "From the store"
    assert todo.completed is False
    assert todo.id is None  # ID assigned by repository


def test_create_todo_with_title_only():
    """Test creating a Todo with only title (description is optional)."""
    todo = Todo(
        id=None,
        title="Call dentist",
        description="",
        completed=False
    )

    assert todo.title == "Call dentist"
    assert todo.description == ""
    assert todo.completed is False


def test_create_todo_empty_title_raises_error():
    """Test that creating a Todo with empty title raises ValueError."""
    with pytest.raises(ValueError, match="Title cannot be empty"):
        Todo(id=None, title="", description="test", completed=False)


def test_create_todo_whitespace_title_raises_error():
    """Test that creating a Todo with whitespace-only title raises ValueError."""
    with pytest.raises(ValueError, match="Title cannot be empty"):
        Todo(id=None, title="   ", description="test", completed=False)


def test_create_todo_special_characters():
    """Test that special characters in title and description are preserved."""
    title_with_special = "Buy @#$% & items!"
    desc_with_newlines = "Line 1\nLine 2\nLine 3"

    todo = Todo(
        id=None,
        title=title_with_special,
        description=desc_with_newlines,
        completed=False
    )

    assert todo.title == title_with_special
    assert todo.description == desc_with_newlines


def test_create_todo_long_strings():
    """Test that very long titles and descriptions are stored without truncation."""
    long_title = "A" * 500
    long_description = "B" * 2000

    todo = Todo(
        id=None,
        title=long_title,
        description=long_description,
        completed=False
    )

    assert len(todo.title) == 500
    assert len(todo.description) == 2000
    assert todo.title == long_title
    assert todo.description == long_description
