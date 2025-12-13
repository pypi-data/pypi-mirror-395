"""
Unit tests for the TodoRepository.

Tests cover CRUD operations for in-memory todo storage.
"""

import pytest
from todo_cli.models import Todo
from todo_cli.repository import TodoRepository


@pytest.fixture
def empty_repository():
    """Fixture providing an empty repository."""
    return TodoRepository()


@pytest.fixture
def repository_with_todos():
    """Fixture providing a repository with sample todos."""
    repo = TodoRepository()
    repo.add(Todo(id=None, title="Task 1", description="Desc 1", completed=False))
    repo.add(Todo(id=None, title="Task 2", description="Desc 2", completed=True))
    repo.add(Todo(id=None, title="Task 3", description="Desc 3", completed=False))
    return repo


def test_add_todo_assigns_id(empty_repository):
    """Test that adding a todo assigns ID 1."""
    todo = Todo(id=None, title="Buy milk", description="", completed=False)
    result = empty_repository.add(todo)

    assert result.id == 1
    assert result.title == "Buy milk"


def test_add_multiple_todos_increments_ids(empty_repository):
    """Test that adding multiple todos increments IDs sequentially."""
    todo1 = empty_repository.add(Todo(id=None, title="Task 1", description="", completed=False))
    todo2 = empty_repository.add(Todo(id=None, title="Task 2", description="", completed=False))
    todo3 = empty_repository.add(Todo(id=None, title="Task 3", description="", completed=False))

    assert todo1.id == 1
    assert todo2.id == 2
    assert todo3.id == 3


def test_get_by_id_returns_todo(repository_with_todos):
    """Test retrieving a todo by ID."""
    todo = repository_with_todos.get_by_id(2)

    assert todo is not None
    assert todo.id == 2
    assert todo.title == "Task 2"


def test_get_by_id_nonexistent_returns_none(repository_with_todos):
    """Test that retrieving non-existent ID returns None."""
    result = repository_with_todos.get_by_id(999)

    assert result is None


def test_get_all_returns_all_todos(repository_with_todos):
    """Test retrieving all todos."""
    todos = repository_with_todos.get_all()

    assert len(todos) == 3
    assert todos[0].id == 1
    assert todos[1].id == 2
    assert todos[2].id == 3


def test_get_all_empty_repository(empty_repository):
    """Test that get_all on empty repository returns empty list."""
    todos = empty_repository.get_all()

    assert todos == []


def test_update_todo_replaces_existing(repository_with_todos):
    """Test updating a todo."""
    updated_todo = Todo(id=2, title="Updated Task 2", description="New desc", completed=False)
    repository_with_todos.update(updated_todo)

    retrieved = repository_with_todos.get_by_id(2)
    assert retrieved.title == "Updated Task 2"
    assert retrieved.description == "New desc"
    assert retrieved.completed is False


def test_delete_todo_removes_from_storage(repository_with_todos):
    """Test deleting a todo."""
    result = repository_with_todos.delete(2)

    assert result is True
    assert repository_with_todos.get_by_id(2) is None
    assert len(repository_with_todos.get_all()) == 2


def test_delete_nonexistent_returns_false(repository_with_todos):
    """Test deleting non-existent ID returns False."""
    result = repository_with_todos.delete(999)

    assert result is False


def test_exists_check(repository_with_todos):
    """Test exists method."""
    assert repository_with_todos.exists(1) is True
    assert repository_with_todos.exists(999) is False
