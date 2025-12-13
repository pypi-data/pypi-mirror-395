"""
Repository layer for in-memory storage of Todo entities.

This module manages the storage and retrieval of todos using in-memory data structures.
"""

from copy import deepcopy
from todo_cli.models import Todo


class TodoRepository:
    """
    In-memory repository for Todo entities.

    Uses a dictionary for O(1) lookup by ID and maintains insertion order.
    IDs are auto-incremented starting from 1.
    """

    def __init__(self) -> None:
        """Initialize an empty repository."""
        self._todos: dict[int, Todo] = {}
        self._next_id: int = 1

    def add(self, todo: Todo) -> Todo:
        """
        Add a new todo to the repository with auto-assigned ID.

        Args:
            todo: Todo instance (id should be None)

        Returns:
            Todo with assigned ID
        """
        todo_with_id = Todo(
            id=self._next_id,
            title=todo.title,
            description=todo.description,
            completed=todo.completed
        )
        self._todos[self._next_id] = deepcopy(todo_with_id)
        self._next_id += 1
        return todo_with_id

    def get_by_id(self, id: int) -> Todo | None:
        """
        Retrieve a todo by ID.

        Args:
            id: Todo ID

        Returns:
            Todo if found, None otherwise
        """
        todo = self._todos.get(id)
        return deepcopy(todo) if todo else None

    def get_all(self) -> list[Todo]:
        """
        Retrieve all todos in insertion order.

        Returns:
            List of all todos
        """
        return [deepcopy(todo) for todo in self._todos.values()]

    def update(self, todo: Todo) -> None:
        """
        Update an existing todo.

        Args:
            todo: Todo with existing ID and updated fields
        """
        if todo.id is not None and todo.id in self._todos:
            self._todos[todo.id] = deepcopy(todo)

    def delete(self, id: int) -> bool:
        """
        Delete a todo by ID.

        Args:
            id: Todo ID to delete

        Returns:
            True if deleted, False if not found
        """
        if id in self._todos:
            del self._todos[id]
            return True
        return False

    def exists(self, id: int) -> bool:
        """
        Check if a todo with given ID exists.

        Args:
            id: Todo ID to check

        Returns:
            True if exists, False otherwise
        """
        return id in self._todos
