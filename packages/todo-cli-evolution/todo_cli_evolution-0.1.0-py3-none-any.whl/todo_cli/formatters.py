"""
Output formatting utilities for the Todo CLI.

This module provides functions to format todo data for human-readable console output.
"""

from todo_cli.models import Todo


class OutputFormatter:
    """Formatter for console output."""

    def format_single_todo(self, todo: Todo) -> str:
        """Format a single todo for display."""
        status = self._get_status_icon(todo.completed)
        desc = f" - {todo.description}" if todo.description else ""
        return f"[{todo.id}] {status} {todo.title}{desc}"

    def format_todo_list(self, todos: list[Todo]) -> str:
        """Format a list of todos as a table."""
        if not todos:
            return self.format_empty_list_message()

        lines = []
        lines.append("ID | Status | Title                          | Description")
        lines.append("---+--------+--------------------------------+-----------------------------")

        for todo in todos:
            status = self._get_status_icon(todo.completed)
            title = todo.title[:30].ljust(30)
            desc = todo.description[:27][:27] if todo.description else ""
            lines.append(f"{todo.id:2} | {status:6} | {title} | {desc}")

        return "\n".join(lines)

    def format_empty_list_message(self) -> str:
        """Format message for empty todo list."""
        return "No todos found. Use 'add' to create one."

    def format_success_message(self, action: str, todo: Todo) -> str:
        """Format success message."""
        return f"✓ Todo {action} successfully: [{todo.id}] {todo.title}"

    def format_error_message(self, error: str) -> str:
        """Format error message."""
        return f"✗ Error: {error}"

    def _get_status_icon(self, completed: bool) -> str:
        """Get status icon for completed status."""
        return "✓" if completed else "✗"
