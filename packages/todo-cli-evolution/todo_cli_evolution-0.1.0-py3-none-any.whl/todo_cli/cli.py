"""
Command-line interface for the Todo application.

This module provides the interactive REPL interface for managing todos.
"""

from todo_cli.service import TodoService
from todo_cli.formatters import OutputFormatter


class TodoCLI:
    """Interactive CLI for todo management."""

    def __init__(self, service: TodoService, formatter: OutputFormatter) -> None:
        """Initialize CLI with service and formatter."""
        self._service = service
        self._formatter = formatter
        self._running = True

    def run(self) -> None:
        """Start the REPL loop."""
        self.show_welcome_message()

        while self._running:
            self.show_menu()
            command = input("\nEnter command: ").strip().lower()

            if command == "add":
                self._handle_add()
            elif command == "list":
                self._handle_list()
            elif command == "update":
                self._handle_update()
            elif command == "delete":
                self._handle_delete()
            elif command == "toggle":
                self._handle_toggle()
            elif command == "help":
                self._handle_help()
            elif command in ("exit", "quit"):
                self._handle_exit()
            else:
                print(self._formatter.format_error_message("Unknown command. Type 'help' for available commands."))

    def show_welcome_message(self) -> None:
        """Display welcome message."""
        print("=" * 60)
        print("  Todo CLI - Phase I: In-Memory Python CLI Todo Application")
        print("  Part of 'The Evolution of Todo' project")
        print("=" * 60)

    def show_menu(self) -> None:
        """Display main menu."""
        print("\nAvailable commands: add, list, update, delete, toggle, help, exit")

    def _handle_add(self) -> None:
        """Handle add todo command."""
        title = input("Enter title: ").strip()
        description = input("Enter description (optional): ").strip()

        result = self._service.create_todo(title, description)

        if result.is_success():
            todo = result.unwrap()
            print(self._formatter.format_success_message("created", todo))
        else:
            error = result.unwrap_error()
            print(self._formatter.format_error_message(error))

    def _handle_list(self) -> None:
        """Handle list todos command."""
        todos = self._service.list_todos()
        print("\n" + self._formatter.format_todo_list(todos))

    def _handle_update(self) -> None:
        """Handle update todo command."""
        id_str = input("Enter todo ID to update: ").strip()

        id_value = self._parse_id(id_str)
        if id_value is None:
            print(self._formatter.format_error_message("Invalid ID. Please enter a number."))
            return

        print("Leave empty to keep current value:")
        title = input("Enter new title: ").strip()
        description = input("Enter new description: ").strip()

        # Convert empty strings to None to keep current values
        title_value = title if title else None
        description_value = description if description else None

        result = self._service.update_todo(id_value, title_value, description_value)

        if result.is_success():
            todo = result.unwrap()
            print(self._formatter.format_success_message("updated", todo))
        else:
            error = result.unwrap_error()
            print(self._formatter.format_error_message(error))

    def _handle_delete(self) -> None:
        """Handle delete todo command."""
        id_str = input("Enter todo ID to delete: ").strip()

        id_value = self._parse_id(id_str)
        if id_value is None:
            print(self._formatter.format_error_message("Invalid ID. Please enter a number."))
            return

        confirm = input(f"Are you sure you want to delete todo {id_value}? (y/n): ").strip().lower()

        if confirm != "y":
            print("Delete cancelled.")
            return

        result = self._service.delete_todo(id_value)

        if result.is_success():
            print(f"✓ Todo {id_value} deleted successfully")
        else:
            error = result.unwrap_error()
            print(self._formatter.format_error_message(error))

    def _handle_toggle(self) -> None:
        """Handle toggle completion command."""
        id_str = input("Enter todo ID to toggle: ").strip()

        id_value = self._parse_id(id_str)
        if id_value is None:
            print(self._formatter.format_error_message("Invalid ID. Please enter a number."))
            return

        result = self._service.toggle_completion(id_value)

        if result.is_success():
            todo = result.unwrap()
            status = "completed" if todo.completed else "incomplete"
            print(f"✓ Todo [{todo.id}] marked as {status}")
        else:
            error = result.unwrap_error()
            print(self._formatter.format_error_message(error))

    def _handle_help(self) -> None:
        """Handle help command."""
        print("\nAvailable Commands:")
        print("  add     - Add a new todo")
        print("  list    - List all todos")
        print("  update  - Update an existing todo")
        print("  delete  - Delete a todo")
        print("  toggle  - Toggle completion status")
        print("  help    - Show this help message")
        print("  exit    - Exit the application")

    def _handle_exit(self) -> None:
        """Handle exit command."""
        print("\nGoodbye! Your todos will be lost (in-memory only).")
        self._running = False

    def _parse_id(self, id_str: str) -> int | None:
        """Parse ID string to integer."""
        try:
            return int(id_str)
        except ValueError:
            return None
