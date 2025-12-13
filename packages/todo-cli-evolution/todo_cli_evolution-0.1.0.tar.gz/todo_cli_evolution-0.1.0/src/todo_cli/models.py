"""
Domain models for the Todo CLI application.

This module defines the core Todo entity and its business rules.
"""

from dataclasses import dataclass


@dataclass
class Todo:
    """
    Todo entity representing a task.

    Attributes:
        id: Unique identifier (assigned by repository, None before persistence)
        title: Short description of the task (required, non-empty)
        description: Detailed text providing context (optional)
        completed: Boolean flag indicating completion status

    Raises:
        ValueError: If title is empty or whitespace-only
    """

    id: int | None
    title: str
    description: str
    completed: bool

    def __post_init__(self) -> None:
        """Validate that title is non-empty after initialization."""
        if not self.title or not self.title.strip():
            raise ValueError("Title cannot be empty")
