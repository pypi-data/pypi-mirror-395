"""
Entry point for the Todo CLI application.

Run with: python -m todo_cli
"""

from todo_cli.repository import TodoRepository
from todo_cli.service import TodoService
from todo_cli.formatters import OutputFormatter
from todo_cli.cli import TodoCLI


def main() -> None:
    """Main entry point for the application."""
    # Initialize layers
    repository = TodoRepository()
    service = TodoService(repository)
    formatter = OutputFormatter()
    cli = TodoCLI(service, formatter)

    # Run the CLI
    try:
        cli.run()
    except KeyboardInterrupt:
        print("\n\nInterrupted. Goodbye!")
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        print("Please report this issue.")


if __name__ == "__main__":
    main()
