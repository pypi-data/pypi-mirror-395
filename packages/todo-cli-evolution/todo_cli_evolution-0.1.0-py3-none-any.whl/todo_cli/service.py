"""
Business logic layer for Todo operations.

This module provides the service layer that orchestrates business logic,
validation, and error handling for todo operations.
"""

from dataclasses import dataclass
from typing import Generic, TypeVar

from todo_cli.models import Todo
from todo_cli.repository import TodoRepository


T = TypeVar('T')
E = TypeVar('E')


@dataclass
class Result(Generic[T, E]):
    """
    Result type for operations that can succeed or fail.

    Represents either a success with a value or an error with an error message.
    """

    _value: T | None = None
    _error: E | None = None
    _is_success: bool = False

    @staticmethod
    def success(value: T) -> 'Result[T, E]':
        """Create a successful result."""
        return Result(_value=value, _is_success=True)

    @staticmethod
    def error(error: E) -> 'Result[T, E]':
        """Create an error result."""
        return Result(_error=error, _is_success=False)

    def is_success(self) -> bool:
        """Check if the result is successful."""
        return self._is_success

    def unwrap(self) -> T:
        """Get the success value or raise if error."""
        if not self._is_success:
            raise ValueError("Cannot unwrap error result")
        return self._value  # type: ignore

    def unwrap_error(self) -> E:
        """Get the error value or raise if success."""
        if self._is_success:
            raise ValueError("Cannot unwrap_error on success result")
        return self._error  # type: ignore


class TodoService:
    """
    Service layer for todo business logic.

    Coordinates validation, repository operations, and error handling.
    """

    def __init__(self, repository: TodoRepository) -> None:
        """Initialize service with a repository."""
        self._repo = repository

    def create_todo(self, title: str, description: str = "") -> Result[Todo, str]:
        """
        Create a new todo.

        Args:
            title: Todo title (required, non-empty)
            description: Todo description (optional)

        Returns:
            Result with created Todo or error message
        """
        # Validate title
        if not title or not title.strip():
            return Result.error("Title cannot be empty")

        try:
            todo = Todo(id=None, title=title, description=description, completed=False)
            created_todo = self._repo.add(todo)
            return Result.success(created_todo)
        except ValueError as e:
            return Result.error(str(e))

    def list_todos(self) -> list[Todo]:
        """
        Get all todos.

        Returns:
            List of all todos
        """
        return self._repo.get_all()

    def update_todo(
        self,
        id: int,
        title: str | None = None,
        description: str | None = None
    ) -> Result[Todo, str]:
        """
        Update an existing todo.

        Args:
            id: Todo ID
            title: New title (None to keep current)
            description: New description (None to keep current)

        Returns:
            Result with updated Todo or error message
        """
        # Check if todo exists
        existing = self._repo.get_by_id(id)
        if existing is None:
            return Result.error(f"Todo with ID {id} not found")

        # Validate at least one field is being updated
        if title is None and description is None:
            return Result.error("At least one field (title or description) must be provided")

        # Validate title if provided
        if title is not None and (not title or not title.strip()):
            return Result.error("Title cannot be empty")

        # Update fields
        new_title = title if title is not None else existing.title
        new_description = description if description is not None else existing.description

        try:
            updated_todo = Todo(
                id=id,
                title=new_title,
                description=new_description,
                completed=existing.completed
            )
            self._repo.update(updated_todo)
            return Result.success(updated_todo)
        except ValueError as e:
            return Result.error(str(e))

    def delete_todo(self, id: int) -> Result[bool, str]:
        """
        Delete a todo.

        Args:
            id: Todo ID

        Returns:
            Result with True or error message
        """
        if not self._repo.exists(id):
            return Result.error(f"Todo with ID {id} not found")

        self._repo.delete(id)
        return Result.success(True)

    def toggle_completion(self, id: int) -> Result[Todo, str]:
        """
        Toggle completion status of a todo.

        Args:
            id: Todo ID

        Returns:
            Result with toggled Todo or error message
        """
        existing = self._repo.get_by_id(id)
        if existing is None:
            return Result.error(f"Todo with ID {id} not found")

        toggled_todo = Todo(
            id=existing.id,
            title=existing.title,
            description=existing.description,
            completed=not existing.completed
        )
        self._repo.update(toggled_todo)
        return Result.success(toggled_todo)
