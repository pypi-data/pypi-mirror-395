"""
Comprehensive specification compliance tests for Phase I.

This test file validates all functional requirements and user stories
defined in specs-history/phase-1-cli/spec.md
"""

import pytest
from todo_cli.models import Todo
from todo_cli.repository import TodoRepository
from todo_cli.service import TodoService


class TestUserStory1CreateAndView:
    """User Story 1: Create and View Todos"""

    def test_scenario_1_create_todo_with_title_and_description(self):
        """
        Given the application is running with no existing todos,
        When I add a todo with title "Buy groceries" and description "Milk, eggs, bread",
        Then the system confirms creation and assigns a unique ID
        """
        service = TodoService(TodoRepository())

        result = service.create_todo("Buy groceries", "Milk, eggs, bread")

        assert result.is_success()
        todo = result.unwrap()
        assert todo.id is not None
        assert todo.title == "Buy groceries"
        assert todo.description == "Milk, eggs, bread"
        assert todo.completed is False

    def test_scenario_2_view_multiple_todos(self):
        """
        Given I have created 3 todos,
        When I request to view all todos,
        Then I see a formatted list showing ID, title, and completion status
        """
        service = TodoService(TodoRepository())

        service.create_todo("Task 1", "Description 1")
        service.create_todo("Task 2", "Description 2")
        service.create_todo("Task 3", "Description 3")

        todos = service.list_todos()

        assert len(todos) == 3
        assert todos[0].id == 1
        assert todos[0].title == "Task 1"
        assert todos[0].completed is False
        assert todos[1].id == 2
        assert todos[2].id == 3

    def test_scenario_3_create_todo_without_description(self):
        """
        Given I add a todo with only a title "Call dentist" (no description),
        When I view the list,
        Then the todo appears correctly with the title and shows as incomplete
        """
        service = TodoService(TodoRepository())

        result = service.create_todo("Call dentist", "")

        assert result.is_success()
        todo = result.unwrap()
        assert todo.title == "Call dentist"
        assert todo.description == ""
        assert todo.completed is False

        todos = service.list_todos()
        assert len(todos) == 1
        assert todos[0].title == "Call dentist"

    def test_scenario_4_reject_empty_title(self):
        """
        Given the application is running,
        When I attempt to add a todo with an empty title,
        Then the system rejects it with a clear error message
        """
        service = TodoService(TodoRepository())

        result = service.create_todo("", "Some description")

        assert not result.is_success()
        assert "Title cannot be empty" in result.unwrap_error()


class TestUserStory2MarkComplete:
    """User Story 2: Mark Todos Complete"""

    def test_scenario_1_mark_incomplete_todo_complete(self):
        """
        Given I have a todo with ID 1 that is incomplete,
        When I mark it as complete,
        Then the system confirms the change and viewing shows it complete
        """
        service = TodoService(TodoRepository())
        created = service.create_todo("Task 1", "Description")
        todo_id = created.unwrap().id

        result = service.toggle_completion(todo_id)

        assert result.is_success()
        toggled = result.unwrap()
        assert toggled.completed is True
        assert toggled.title == "Task 1"  # Title unchanged

    def test_scenario_2_mark_complete_todo_incomplete(self):
        """
        Given I have a todo with ID that is complete,
        When I mark it as incomplete,
        Then the system confirms the change
        """
        service = TodoService(TodoRepository())
        created = service.create_todo("Task 1", "Description")
        todo_id = created.unwrap().id

        # First mark complete
        service.toggle_completion(todo_id)
        # Then mark incomplete
        result = service.toggle_completion(todo_id)

        assert result.is_success()
        toggled = result.unwrap()
        assert toggled.completed is False

    def test_scenario_3_toggle_nonexistent_todo(self):
        """
        Given I attempt to mark a todo with ID 999 (which doesn't exist),
        When I execute the command,
        Then the system displays error
        """
        service = TodoService(TodoRepository())

        result = service.toggle_completion(999)

        assert not result.is_success()
        assert "Todo with ID 999 not found" in result.unwrap_error()

    def test_scenario_4_toggle_preserves_other_fields(self):
        """
        Given I have marked a todo complete,
        When I view the list,
        Then the title and description remain unchanged
        """
        service = TodoService(TodoRepository())
        created = service.create_todo("Original Title", "Original Description")
        todo_id = created.unwrap().id

        service.toggle_completion(todo_id)

        todos = service.list_todos()
        assert todos[0].title == "Original Title"
        assert todos[0].description == "Original Description"
        assert todos[0].completed is True


class TestUserStory3UpdateTodoDetails:
    """User Story 3: Update Todo Details"""

    def test_scenario_1_update_title_only(self):
        """
        Given I have a todo with ID 1 titled "Buy groceries",
        When I update its title to "Buy groceries and coffee",
        Then the system confirms the update
        """
        service = TodoService(TodoRepository())
        created = service.create_todo("Buy groceries", "Original desc")
        todo_id = created.unwrap().id

        result = service.update_todo(todo_id, title="Buy groceries and coffee")

        assert result.is_success()
        updated = result.unwrap()
        assert updated.title == "Buy groceries and coffee"
        assert updated.description == "Original desc"  # Unchanged

    def test_scenario_2_update_description_only(self):
        """
        Given I have a todo with description "Original description",
        When I update only the description to "Updated description",
        Then the title remains unchanged
        """
        service = TodoService(TodoRepository())
        created = service.create_todo("Original Title", "Original description")
        todo_id = created.unwrap().id

        result = service.update_todo(todo_id, description="Updated description")

        assert result.is_success()
        updated = result.unwrap()
        assert updated.title == "Original Title"  # Unchanged
        assert updated.description == "Updated description"

    def test_scenario_3_update_both_fields(self):
        """
        Given I have a todo with ID 3,
        When I update both title and description simultaneously,
        Then both fields are updated correctly
        """
        service = TodoService(TodoRepository())
        created = service.create_todo("Old Title", "Old Description")
        todo_id = created.unwrap().id

        result = service.update_todo(
            todo_id,
            title="New Title",
            description="New Description"
        )

        assert result.is_success()
        updated = result.unwrap()
        assert updated.title == "New Title"
        assert updated.description == "New Description"

    def test_scenario_4_update_nonexistent_todo(self):
        """
        Given I attempt to update todo ID 999 (which doesn't exist),
        When I execute the update command,
        Then the system displays error
        """
        service = TodoService(TodoRepository())

        result = service.update_todo(999, title="New Title")

        assert not result.is_success()
        assert "Todo with ID 999 not found" in result.unwrap_error()

    def test_scenario_5_update_title_to_empty(self):
        """
        Given I attempt to update a todo's title to an empty string,
        When I execute the update,
        Then the system rejects it
        """
        service = TodoService(TodoRepository())
        created = service.create_todo("Original Title", "Description")
        todo_id = created.unwrap().id

        result = service.update_todo(todo_id, title="")

        assert not result.is_success()
        assert "Title cannot be empty" in result.unwrap_error()


class TestUserStory4DeleteTodos:
    """User Story 4: Delete Todos"""

    def test_scenario_1_delete_todo_from_list(self):
        """
        Given I have 3 todos with IDs 1, 2, 3,
        When I delete todo ID 2,
        Then viewing the list shows only IDs 1 and 3
        """
        service = TodoService(TodoRepository())
        service.create_todo("Task 1", "")
        service.create_todo("Task 2", "")
        service.create_todo("Task 3", "")

        result = service.delete_todo(2)

        assert result.is_success()
        todos = service.list_todos()
        assert len(todos) == 2
        assert todos[0].id == 1
        assert todos[1].id == 3

    def test_scenario_2_deleted_todo_not_found_on_operations(self):
        """
        Given I delete a todo with ID 5,
        When I attempt to view, update, or mark complete the same ID,
        Then all operations return error
        """
        service = TodoService(TodoRepository())
        created = service.create_todo("Task to delete", "")
        todo_id = created.unwrap().id

        service.delete_todo(todo_id)

        # Try update
        update_result = service.update_todo(todo_id, title="New")
        assert not update_result.is_success()

        # Try toggle
        toggle_result = service.toggle_completion(todo_id)
        assert not toggle_result.is_success()

    def test_scenario_3_delete_nonexistent_todo(self):
        """
        Given I attempt to delete todo ID 999 (which doesn't exist),
        When I execute the delete command,
        Then the system displays error
        """
        service = TodoService(TodoRepository())

        result = service.delete_todo(999)

        assert not result.is_success()
        assert "Todo with ID 999 not found" in result.unwrap_error()

    def test_scenario_4_delete_last_remaining_todo(self):
        """
        Given I have only one todo remaining,
        When I delete it,
        Then viewing the list shows empty list
        """
        service = TodoService(TodoRepository())
        created = service.create_todo("Last Task", "")
        todo_id = created.unwrap().id

        result = service.delete_todo(todo_id)

        assert result.is_success()
        todos = service.list_todos()
        assert len(todos) == 0


class TestEdgeCases:
    """Edge Cases from specification"""

    def test_id_uniqueness(self):
        """IDs must be unique and auto-increment"""
        service = TodoService(TodoRepository())

        todo1 = service.create_todo("Task 1", "").unwrap()
        todo2 = service.create_todo("Task 2", "").unwrap()
        todo3 = service.create_todo("Task 3", "").unwrap()

        assert todo1.id != todo2.id
        assert todo2.id != todo3.id
        assert todo1.id < todo2.id < todo3.id

    def test_special_characters_in_title(self):
        """Special characters should be preserved"""
        service = TodoService(TodoRepository())

        special_title = "Buy @#$% & items!"
        result = service.create_todo(special_title, "")

        assert result.is_success()
        todo = result.unwrap()
        assert todo.title == special_title

    def test_special_characters_in_description(self):
        """Special characters in description with newlines"""
        service = TodoService(TodoRepository())

        desc_with_newlines = "Line 1\nLine 2\nLine 3"
        result = service.create_todo("Title", desc_with_newlines)

        assert result.is_success()
        todo = result.unwrap()
        assert todo.description == desc_with_newlines

    def test_long_title(self):
        """Very long titles should be accepted"""
        service = TodoService(TodoRepository())

        long_title = "A" * 500
        result = service.create_todo(long_title, "")

        assert result.is_success()
        todo = result.unwrap()
        assert len(todo.title) == 500

    def test_long_description(self):
        """Very long descriptions should be accepted"""
        service = TodoService(TodoRepository())

        long_desc = "B" * 2000
        result = service.create_todo("Title", long_desc)

        assert result.is_success()
        todo = result.unwrap()
        assert len(todo.description) == 2000

    def test_empty_list_handling(self):
        """Empty list should return empty list, not error"""
        service = TodoService(TodoRepository())

        todos = service.list_todos()

        assert todos == []

    def test_update_completed_todo(self):
        """Can update a completed todo"""
        service = TodoService(TodoRepository())
        created = service.create_todo("Original", "Desc")
        todo_id = created.unwrap().id

        # Mark complete
        service.toggle_completion(todo_id)
        # Update it
        result = service.update_todo(todo_id, title="Updated")

        assert result.is_success()
        updated = result.unwrap()
        assert updated.title == "Updated"
        assert updated.completed is True  # Status preserved

    def test_whitespace_only_title_rejected(self):
        """Whitespace-only title should be rejected"""
        service = TodoService(TodoRepository())

        result = service.create_todo("   ", "Description")

        assert not result.is_success()
        assert "Title cannot be empty" in result.unwrap_error()

    def test_operation_sequencing(self):
        """Complex operation sequence: create, complete, update, toggle"""
        service = TodoService(TodoRepository())

        # Create
        created = service.create_todo("Task", "Description")
        todo_id = created.unwrap().id

        # Mark complete
        service.toggle_completion(todo_id)

        # Update
        service.update_todo(todo_id, title="Updated Task")

        # Mark incomplete
        result = service.toggle_completion(todo_id)

        assert result.is_success()
        final = result.unwrap()
        assert final.title == "Updated Task"
        assert final.completed is False


class TestFunctionalRequirements:
    """Test explicit functional requirements from spec"""

    def test_fr001_create_with_title_and_description(self):
        """FR-001: Allow users to add todo with title and description"""
        service = TodoService(TodoRepository())
        result = service.create_todo("Title", "Description")
        assert result.is_success()

    def test_fr002_auto_assign_id(self):
        """FR-002: Automatically assign unique ID"""
        service = TodoService(TodoRepository())
        result = service.create_todo("Title", "")
        todo = result.unwrap()
        assert todo.id is not None
        assert isinstance(todo.id, int)

    def test_fr003_display_all_todos(self):
        """FR-003: Display all todos with ID, title, completion"""
        service = TodoService(TodoRepository())
        service.create_todo("Task 1", "Desc 1")
        service.create_todo("Task 2", "Desc 2")

        todos = service.list_todos()
        assert len(todos) == 2
        for todo in todos:
            assert todo.id is not None
            assert todo.title is not None
            assert todo.completed is not None

    def test_fr004_update_title_and_description(self):
        """FR-004: Update title and/or description by ID"""
        service = TodoService(TodoRepository())
        created = service.create_todo("Old", "Old")
        todo_id = created.unwrap().id

        result = service.update_todo(todo_id, "New Title", "New Desc")
        assert result.is_success()

    def test_fr005_toggle_completion(self):
        """FR-005: Toggle completion status by ID"""
        service = TodoService(TodoRepository())
        created = service.create_todo("Task", "")
        todo_id = created.unwrap().id

        result = service.toggle_completion(todo_id)
        assert result.is_success()
        assert result.unwrap().completed is True

    def test_fr006_delete_by_id(self):
        """FR-006: Delete todo by ID"""
        service = TodoService(TodoRepository())
        created = service.create_todo("Task", "")
        todo_id = created.unwrap().id

        result = service.delete_todo(todo_id)
        assert result.is_success()

    def test_fr007_reject_empty_title_creation(self):
        """FR-007: Reject empty title on creation"""
        service = TodoService(TodoRepository())
        result = service.create_todo("", "Description")
        assert not result.is_success()

    def test_fr008_reject_empty_title_update(self):
        """FR-008: Reject empty title on update"""
        service = TodoService(TodoRepository())
        created = service.create_todo("Task", "")
        todo_id = created.unwrap().id

        result = service.update_todo(todo_id, title="")
        assert not result.is_success()

    def test_fr009_error_on_nonexistent_id(self):
        """FR-009: Return clear error for non-existent IDs"""
        service = TodoService(TodoRepository())

        update_result = service.update_todo(999, title="New")
        assert not update_result.is_success()
        assert "not found" in update_result.unwrap_error().lower()

    def test_fr011_preserve_data_during_update(self):
        """FR-011: Preserve data during update unless explicitly changed"""
        service = TodoService(TodoRepository())
        created = service.create_todo("Title", "Description")
        todo_id = created.unwrap().id

        # Update only title
        service.update_todo(todo_id, title="New Title")

        todos = service.list_todos()
        assert todos[0].description == "Description"  # Preserved

    def test_fr012_no_duplicate_ids(self):
        """FR-012: No duplicate IDs"""
        service = TodoService(TodoRepository())

        todos_created = []
        for i in range(10):
            result = service.create_todo(f"Task {i}", "")
            todos_created.append(result.unwrap().id)

        # All IDs should be unique
        assert len(todos_created) == len(set(todos_created))


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
