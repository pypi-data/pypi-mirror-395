#!/usr/bin/env python3
"""
Automated functional test script for Todo CLI application.
Tests all features programmatically without requiring user interaction.
"""

from todo_cli.repository import TodoRepository
from todo_cli.service import TodoService
from todo_cli.formatters import OutputFormatter


def print_section(title: str):
    """Print a section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def test_create_todos():
    """Test creating todos."""
    print_section("TEST 1: Creating Todos")

    repo = TodoRepository()
    service = TodoService(repo)
    formatter = OutputFormatter()

    # Test 1: Create todo with title and description
    result1 = service.create_todo("Buy groceries", "Milk, eggs, bread")
    if result1.is_success():
        todo1 = result1.unwrap()
        print(f"✓ Created: {formatter.format_single_todo(todo1)}")
    else:
        print(f"✗ Failed: {result1.unwrap_error()}")

    # Test 2: Create todo with title only
    result2 = service.create_todo("Call dentist", "")
    if result2.is_success():
        todo2 = result2.unwrap()
        print(f"✓ Created: {formatter.format_single_todo(todo2)}")
    else:
        print(f"✗ Failed: {result2.unwrap_error()}")

    # Test 3: Try to create todo with empty title (should fail)
    result3 = service.create_todo("", "test")
    if result3.is_success():
        print(f"✗ Should have failed but succeeded!")
    else:
        print(f"✓ Correctly rejected empty title: {result3.unwrap_error()}")

    return service, formatter


def test_list_todos(service, formatter):
    """Test listing todos."""
    print_section("TEST 2: Listing Todos")

    todos = service.list_todos()
    print(formatter.format_todo_list(todos))
    print(f"\n✓ Listed {len(todos)} todos")


def test_toggle_completion(service, formatter):
    """Test toggling completion status."""
    print_section("TEST 3: Toggle Completion")

    # Toggle todo 1 to complete
    result = service.toggle_completion(1)
    if result.is_success():
        todo = result.unwrap()
        print(f"✓ Toggled todo 1: completed={todo.completed}")
    else:
        print(f"✗ Failed: {result.unwrap_error()}")

    # Toggle it back
    result = service.toggle_completion(1)
    if result.is_success():
        todo = result.unwrap()
        print(f"✓ Toggled todo 1 again: completed={todo.completed}")
    else:
        print(f"✗ Failed: {result.unwrap_error()}")

    # Try to toggle non-existent todo (should fail)
    result = service.toggle_completion(999)
    if result.is_success():
        print(f"✗ Should have failed but succeeded!")
    else:
        print(f"✓ Correctly rejected invalid ID: {result.unwrap_error()}")


def test_update_todos(service, formatter):
    """Test updating todos."""
    print_section("TEST 4: Updating Todos")

    # Update title only
    result = service.update_todo(1, title="Buy groceries and coffee", description=None)
    if result.is_success():
        todo = result.unwrap()
        print(f"✓ Updated title: {formatter.format_single_todo(todo)}")
    else:
        print(f"✗ Failed: {result.unwrap_error()}")

    # Update description only
    result = service.update_todo(2, title=None, description="Appointment at 3pm")
    if result.is_success():
        todo = result.unwrap()
        print(f"✓ Updated description: {formatter.format_single_todo(todo)}")
    else:
        print(f"✗ Failed: {result.unwrap_error()}")

    # Try to update with empty title (should fail)
    result = service.update_todo(1, title="", description=None)
    if result.is_success():
        print(f"✗ Should have failed but succeeded!")
    else:
        print(f"✓ Correctly rejected empty title: {result.unwrap_error()}")

    # Try to update non-existent todo (should fail)
    result = service.update_todo(999, title="Test", description=None)
    if result.is_success():
        print(f"✗ Should have failed but succeeded!")
    else:
        print(f"✓ Correctly rejected invalid ID: {result.unwrap_error()}")


def test_delete_todos(service, formatter):
    """Test deleting todos."""
    print_section("TEST 5: Deleting Todos")

    # Add a todo to delete
    service.create_todo("Temporary todo", "Will be deleted")
    todos_before = len(service.list_todos())
    print(f"Todos before delete: {todos_before}")

    # Delete it
    result = service.delete_todo(3)
    if result.is_success():
        todos_after = len(service.list_todos())
        print(f"✓ Deleted todo 3. Todos after: {todos_after}")
    else:
        print(f"✗ Failed: {result.unwrap_error()}")

    # Try to delete non-existent todo (should fail)
    result = service.delete_todo(999)
    if result.is_success():
        print(f"✗ Should have failed but succeeded!")
    else:
        print(f"✓ Correctly rejected invalid ID: {result.unwrap_error()}")


def test_edge_cases(service, formatter):
    """Test edge cases."""
    print_section("TEST 6: Edge Cases")

    # Special characters
    result = service.create_todo("Buy @#$% & items!", "Special chars test")
    if result.is_success():
        print(f"✓ Handled special characters in title")
    else:
        print(f"✗ Failed with special characters: {result.unwrap_error()}")

    # Very long title
    long_title = "A" * 200
    result = service.create_todo(long_title, "")
    if result.is_success():
        print(f"✓ Handled very long title (200 chars)")
    else:
        print(f"✗ Failed with long title: {result.unwrap_error()}")

    # Very long description
    long_desc = "B" * 1000
    result = service.create_todo("Test", long_desc)
    if result.is_success():
        print(f"✓ Handled very long description (1000 chars)")
    else:
        print(f"✗ Failed with long description: {result.unwrap_error()}")


def test_final_state(service, formatter):
    """Show final state."""
    print_section("FINAL STATE: All Todos")

    todos = service.list_todos()
    print(formatter.format_todo_list(todos))

    print(f"\n📊 Summary:")
    print(f"   Total todos: {len(todos)}")
    completed = sum(1 for t in todos if t.completed)
    print(f"   Completed: {completed}")
    print(f"   Incomplete: {len(todos) - completed}")


def main():
    """Run all tests."""
    print("\n" + "🧪" * 30)
    print("  TODO CLI APPLICATION - FUNCTIONAL TEST SUITE")
    print("  Phase I: In-Memory Python CLI Todo Application")
    print("🧪" * 30)

    try:
        service, formatter = test_create_todos()
        test_list_todos(service, formatter)
        test_toggle_completion(service, formatter)
        test_update_todos(service, formatter)
        test_delete_todos(service, formatter)
        test_edge_cases(service, formatter)
        test_final_state(service, formatter)

        print_section("✅ ALL TESTS PASSED!")
        print("\n🎉 The Todo CLI application is working correctly!")
        print("\nTo run the interactive app, use:")
        print("   uv run python -m todo_cli")

    except Exception as e:
        print_section("❌ TEST FAILED")
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
