# Tasks: Phase I - In-Memory Python CLI Todo Application

**Project**: The Evolution of Todo
**Phase**: Phase I (Foundation)
**Created**: 2025-12-07
**Status**: Ready for Implementation

**Input Documents**:
- Specification: `specs-history/phase-1-cli/spec.md` (v1.0.0)
- Architecture Plan: `specs-history/phase-1-cli/plan.md` (v1.0.0)
- Constitution: `.specify/memory/constitution.md` (v1.0.0)

**Test-First Mandate**: Per Constitution Section I.4, tests MUST be written FIRST (or immediately with implementation), verified to FAIL, then implementation makes them PASS (Red-Green-Refactor cycle).

---

## Task Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: User story mapping (US1=Create/View, US2=Toggle, US3=Update, US4=Delete, SETUP=Infrastructure)
- **File paths**: Exact paths specified for traceability

---

## Phase 1: Project Setup & Infrastructure (SETUP)

**Purpose**: Initialize project structure, tooling, and foundational components required by ALL user stories

**⚠️ CRITICAL**: This phase BLOCKS all user story implementation. Must complete before ANY feature work.

### Project Initialization

- [ ] **T001** [P] [SETUP] Initialize Python project with UV in `/mnt/d/code/hackathon/HackathonII/In-Memory-Python-Console-App/`
  - Run: `uv init --name todo-cli --lib`
  - Verify: `pyproject.toml` created with project metadata
  - **Acceptance**: Project can be synced with `uv sync`

- [ ] **T002** [P] [SETUP] Create project folder structure per constitutional requirements
  - Create: `src/todo_cli/` (package root)
  - Create: `tests/unit/` (unit tests)
  - Create: `tests/integration/` (integration tests)
  - Create: `docs/phase-1-cli/` (phase documentation)
  - **Acceptance**: All directories exist and match Constitution Section IV

- [ ] **T003** [P] [SETUP] Configure `pyproject.toml` with dependencies and metadata
  - Add: `pytest >= 8.0.0` (dev dependency)
  - Add: `pytest-cov >= 4.0.0` (dev dependency)
  - Add: `mypy >= 1.7.0` (optional dev dependency)
  - Set: `requires-python = ">=3.10"`
  - Set: Project name, version, description
  - **Acceptance**: `uv sync` installs all dependencies successfully

- [ ] **T004** [P] [SETUP] Create Python package structure in `src/todo_cli/`
  - Create: `src/todo_cli/__init__.py` (package init with version)
  - Create: `src/todo_cli/__main__.py` (entry point stub)
  - Create: `src/todo_cli/models.py` (placeholder with module docstring)
  - Create: `src/todo_cli/repository.py` (placeholder with module docstring)
  - Create: `src/todo_cli/service.py` (placeholder with module docstring)
  - Create: `src/todo_cli/cli.py` (placeholder with module docstring)
  - Create: `src/todo_cli/formatters.py` (placeholder with module docstring)
  - **Acceptance**: All modules can be imported without errors

- [ ] **T005** [SETUP] Configure pytest in `pyproject.toml`
  - Add `[tool.pytest.ini_options]` section
  - Set `testpaths = ["tests"]`
  - Set `python_files = ["test_*.py"]`
  - Set `python_functions = ["test_*"]`
  - **Acceptance**: `uv run pytest` runs (even with no tests yet)

- [ ] **T006** [P] [SETUP] Create `.gitignore` for Python project
  - Ignore: `__pycache__/`, `*.pyc`, `.pytest_cache/`, `.coverage`, `htmlcov/`
  - Ignore: `.venv/`, `.uv/`, `*.egg-info/`
  - Ignore: `.mypy_cache/`, `.ruff_cache/`
  - **Acceptance**: Generated files not tracked by git

- [ ] **T007** [P] [SETUP] Create initial `README.md` with setup instructions
  - Document: Python 3.10+ requirement
  - Document: UV installation instructions
  - Document: Project setup: `uv sync`
  - Document: Run application: `uv run python -m todo_cli`
  - Document: Run tests: `uv run pytest`
  - **Acceptance**: Another developer can follow README to set up project

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 2: Domain Model (Foundational - BLOCKS ALL)

**Purpose**: Implement core Todo entity that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until Todo model is complete and tested

### Tests for Domain Model (RED PHASE - Write FIRST)

- [ ] **T008** [P] [SETUP] Create unit test file `tests/unit/test_models.py`
  - Import: `pytest`, `todo_cli.models`
  - Add: Module docstring describing test coverage
  - **Acceptance**: File exists and can be imported

- [ ] **T009** [P] [SETUP] Write test: Create Todo with all fields in `tests/unit/test_models.py`
  - Test: `test_create_todo_with_all_fields()`
  - Given: Valid title "Buy milk", description "From store", completed=False
  - When: Todo created
  - Then: All fields match input, ID is None (assigned by repository)
  - **Acceptance**: Test FAILS (Todo class doesn't exist yet) ❌

- [ ] **T010** [P] [SETUP] Write test: Create Todo with title only in `tests/unit/test_models.py`
  - Test: `test_create_todo_with_title_only()`
  - Given: Title "Call dentist", no description
  - When: Todo created
  - Then: title set, description empty string, completed=False
  - **Acceptance**: Test FAILS ❌

- [ ] **T011** [P] [SETUP] Write test: Reject empty title in `tests/unit/test_models.py`
  - Test: `test_create_todo_empty_title_raises_error()`
  - Given: Empty title ""
  - When: Attempt to create Todo
  - Then: Raises `ValueError` with message "Title cannot be empty"
  - **Acceptance**: Test FAILS ❌

- [ ] **T012** [P] [SETUP] Write test: Reject whitespace-only title in `tests/unit/test_models.py`
  - Test: `test_create_todo_whitespace_title_raises_error()`
  - Given: Whitespace title "   "
  - When: Attempt to create Todo
  - Then: Raises `ValueError` with message "Title cannot be empty"
  - **Acceptance**: Test FAILS ❌

- [ ] **T013** [P] [SETUP] Write test: Todo with special characters in `tests/unit/test_models.py`
  - Test: `test_create_todo_special_characters()`
  - Given: Title with special chars "Buy @#$% & items!", description with newlines
  - When: Todo created
  - Then: Characters preserved exactly
  - **Acceptance**: Test FAILS ❌

- [ ] **T014** [P] [SETUP] Write test: Todo with very long strings in `tests/unit/test_models.py`
  - Test: `test_create_todo_long_strings()`
  - Given: Title 500 chars, description 2000 chars
  - When: Todo created
  - Then: Full strings stored (no truncation)
  - **Acceptance**: Test FAILS ❌

### Implementation for Domain Model (GREEN PHASE - Make tests PASS)

- [ ] **T015** [SETUP] Implement `Todo` dataclass in `src/todo_cli/models.py`
  - Define: `@dataclass class Todo`
  - Fields: `id: int | None`, `title: str`, `description: str`, `completed: bool`
  - Add: `__post_init__()` validation for non-empty title
  - Add: Type hints for all fields
  - Add: Module docstring explaining domain model
  - **Acceptance**: All domain model tests (T009-T014) now PASS ✅

**Checkpoint**: Domain model complete and tested - can now implement storage and services

---

## Phase 3: Infrastructure Layer - Repository (Foundational - BLOCKS ALL)

**Purpose**: Implement in-memory storage that ALL user stories need for persistence

### Tests for Repository (RED PHASE - Write FIRST)

- [ ] **T016** [P] [SETUP] Create unit test file `tests/unit/test_repository.py`
  - Import: `pytest`, `todo_cli.models`, `todo_cli.repository`
  - Add fixtures: `empty_repository()`, `repository_with_todos()`
  - **Acceptance**: File exists with fixtures

- [ ] **T017** [P] [SETUP] Write test: Add todo assigns unique ID in `tests/unit/test_repository.py`
  - Test: `test_add_todo_assigns_id()`
  - Given: Empty repository, Todo without ID
  - When: `repository.add(todo)`
  - Then: Returned todo has `id=1`
  - **Acceptance**: Test FAILS ❌

- [ ] **T018** [P] [SETUP] Write test: Add multiple todos increments IDs in `tests/unit/test_repository.py`
  - Test: `test_add_multiple_todos_increments_ids()`
  - Given: Empty repository
  - When: Add 3 todos
  - Then: IDs are 1, 2, 3 (sequential)
  - **Acceptance**: Test FAILS ❌

- [ ] **T019** [P] [SETUP] Write test: Get todo by ID in `tests/unit/test_repository.py`
  - Test: `test_get_by_id_returns_todo()`
  - Given: Repository with todos (IDs 1, 2, 3)
  - When: `repository.get_by_id(2)`
  - Then: Returns todo with ID 2
  - **Acceptance**: Test FAILS ❌

- [ ] **T020** [P] [SETUP] Write test: Get non-existent ID returns None in `tests/unit/test_repository.py`
  - Test: `test_get_by_id_nonexistent_returns_none()`
  - Given: Repository with todos
  - When: `repository.get_by_id(999)`
  - Then: Returns `None`
  - **Acceptance**: Test FAILS ❌

- [ ] **T021** [P] [SETUP] Write test: Get all todos in `tests/unit/test_repository.py`
  - Test: `test_get_all_returns_all_todos()`
  - Given: Repository with 3 todos
  - When: `repository.get_all()`
  - Then: Returns list of 3 todos in insertion order
  - **Acceptance**: Test FAILS ❌

- [ ] **T022** [P] [SETUP] Write test: Get all from empty repository in `tests/unit/test_repository.py`
  - Test: `test_get_all_empty_repository()`
  - Given: Empty repository
  - When: `repository.get_all()`
  - Then: Returns empty list `[]`
  - **Acceptance**: Test FAILS ❌

- [ ] **T023** [P] [SETUP] Write test: Update todo in `tests/unit/test_repository.py`
  - Test: `test_update_todo_replaces_existing()`
  - Given: Repository with todo ID 1
  - When: `repository.update(todo_with_id_1_modified)`
  - Then: Retrieved todo has new values
  - **Acceptance**: Test FAILS ❌

- [ ] **T024** [P] [SETUP] Write test: Delete todo in `tests/unit/test_repository.py`
  - Test: `test_delete_todo_removes_from_storage()`
  - Given: Repository with todo ID 2
  - When: `repository.delete(2)`
  - Then: Returns `True`, `get_by_id(2)` returns `None`
  - **Acceptance**: Test FAILS ❌

- [ ] **T025** [P] [SETUP] Write test: Delete non-existent ID in `tests/unit/test_repository.py`
  - Test: `test_delete_nonexistent_returns_false()`
  - Given: Repository
  - When: `repository.delete(999)`
  - Then: Returns `False`
  - **Acceptance**: Test FAILS ❌

- [ ] **T026** [P] [SETUP] Write test: Exists check in `tests/unit/test_repository.py`
  - Test: `test_exists_check()`
  - Given: Repository with ID 5
  - When: `repository.exists(5)` and `repository.exists(999)`
  - Then: Returns `True` and `False` respectively
  - **Acceptance**: Test FAILS ❌

### Implementation for Repository (GREEN PHASE - Make tests PASS)

- [ ] **T027** [SETUP] Implement `TodoRepository` class in `src/todo_cli/repository.py`
  - Define: `class TodoRepository`
  - Initialize: `self._todos: dict[int, Todo] = {}`
  - Initialize: `self._next_id: int = 1`
  - Implement: `add(todo: Todo) -> Todo` (assigns ID, stores, returns copy)
  - Implement: `get_by_id(id: int) -> Todo | None`
  - Implement: `get_all() -> list[Todo]` (returns list in insertion order)
  - Implement: `update(todo: Todo) -> None` (replaces existing)
  - Implement: `delete(id: int) -> bool` (removes, returns success)
  - Implement: `exists(id: int) -> bool`
  - Add: Type hints for all methods
  - Add: Docstrings for all public methods
  - **Acceptance**: All repository tests (T017-T026) now PASS ✅

**Checkpoint**: Storage layer complete - can now implement business logic

---

## Phase 4: Application Layer - Service (Foundational - BLOCKS ALL)

**Purpose**: Implement business logic and validation that ALL user stories use

### Tests for Service Layer (RED PHASE - Write FIRST)

- [ ] **T028** [P] [SETUP] Create unit test file `tests/unit/test_service.py`
  - Import: `pytest`, `todo_cli.service`, `todo_cli.repository`, `todo_cli.models`
  - Add fixture: `todo_service()` with mocked/test repository
  - **Acceptance**: File exists with fixtures

- [ ] **T029** [P] [SETUP] Write test: Create todo with valid title in `tests/unit/test_service.py`
  - Test: `test_create_todo_success()`
  - Given: Service with empty repository
  - When: `service.create_todo("Buy milk", "From store")`
  - Then: Returns success Result with Todo (ID assigned, fields match)
  - **Acceptance**: Test FAILS ❌

- [ ] **T030** [P] [SETUP] Write test: Create todo rejects empty title in `tests/unit/test_service.py`
  - Test: `test_create_todo_empty_title_error()`
  - Given: Service
  - When: `service.create_todo("", "description")`
  - Then: Returns error Result with message "Title cannot be empty"
  - **Acceptance**: Test FAILS ❌

- [ ] **T031** [P] [SETUP] Write test: Create todo rejects whitespace title in `tests/unit/test_service.py`
  - Test: `test_create_todo_whitespace_title_error()`
  - Given: Service
  - When: `service.create_todo("   ", "")`
  - Then: Returns error Result with message "Title cannot be empty"
  - **Acceptance**: Test FAILS ❌

- [ ] **T032** [P] [SETUP] Write test: List todos in `tests/unit/test_service.py`
  - Test: `test_list_todos()`
  - Given: Service with 3 todos in repository
  - When: `service.list_todos()`
  - Then: Returns list of 3 todos
  - **Acceptance**: Test FAILS ❌

- [ ] **T033** [P] [SETUP] Write test: Update todo title in `tests/unit/test_service.py`
  - Test: `test_update_todo_title_success()`
  - Given: Service with todo ID 1
  - When: `service.update_todo(1, title="New title", description=None)`
  - Then: Returns success Result, title updated, description unchanged
  - **Acceptance**: Test FAILS ❌

- [ ] **T034** [P] [SETUP] Write test: Update todo description in `tests/unit/test_service.py`
  - Test: `test_update_todo_description_success()`
  - Given: Service with todo ID 1
  - When: `service.update_todo(1, title=None, description="New desc")`
  - Then: Returns success Result, description updated, title unchanged
  - **Acceptance**: Test FAILS ❌

- [ ] **T035** [P] [SETUP] Write test: Update both fields in `tests/unit/test_service.py`
  - Test: `test_update_todo_both_fields_success()`
  - Given: Service with todo ID 1
  - When: `service.update_todo(1, title="New", description="New desc")`
  - Then: Returns success Result, both fields updated
  - **Acceptance**: Test FAILS ❌

- [ ] **T036** [P] [SETUP] Write test: Update rejects empty title in `tests/unit/test_service.py`
  - Test: `test_update_todo_empty_title_error()`
  - Given: Service with todo ID 1
  - When: `service.update_todo(1, title="", description=None)`
  - Then: Returns error Result with message "Title cannot be empty"
  - **Acceptance**: Test FAILS ❌

- [ ] **T037** [P] [SETUP] Write test: Update non-existent ID in `tests/unit/test_service.py`
  - Test: `test_update_todo_nonexistent_error()`
  - Given: Service
  - When: `service.update_todo(999, title="New", description=None)`
  - Then: Returns error Result with message "Todo with ID 999 not found"
  - **Acceptance**: Test FAILS ❌

- [ ] **T038** [P] [SETUP] Write test: Delete todo in `tests/unit/test_service.py`
  - Test: `test_delete_todo_success()`
  - Given: Service with todo ID 3
  - When: `service.delete_todo(3)`
  - Then: Returns success Result
  - **Acceptance**: Test FAILS ❌

- [ ] **T039** [P] [SETUP] Write test: Delete non-existent ID in `tests/unit/test_service.py`
  - Test: `test_delete_todo_nonexistent_error()`
  - Given: Service
  - When: `service.delete_todo(999)`
  - Then: Returns error Result with message "Todo with ID 999 not found"
  - **Acceptance**: Test FAILS ❌

- [ ] **T040** [P] [SETUP] Write test: Toggle incomplete to complete in `tests/unit/test_service.py`
  - Test: `test_toggle_completion_incomplete_to_complete()`
  - Given: Service with incomplete todo ID 1
  - When: `service.toggle_completion(1)`
  - Then: Returns success Result, todo now completed=True
  - **Acceptance**: Test FAILS ❌

- [ ] **T041** [P] [SETUP] Write test: Toggle complete to incomplete in `tests/unit/test_service.py`
  - Test: `test_toggle_completion_complete_to_incomplete()`
  - Given: Service with complete todo ID 2
  - When: `service.toggle_completion(2)`
  - Then: Returns success Result, todo now completed=False
  - **Acceptance**: Test FAILS ❌

- [ ] **T042** [P] [SETUP] Write test: Toggle preserves other fields in `tests/unit/test_service.py`
  - Test: `test_toggle_completion_preserves_fields()`
  - Given: Service with todo (title, description, completed)
  - When: `service.toggle_completion(id)`
  - Then: Only completed field changes, title and description unchanged
  - **Acceptance**: Test FAILS ❌

- [ ] **T043** [P] [SETUP] Write test: Toggle non-existent ID in `tests/unit/test_service.py`
  - Test: `test_toggle_completion_nonexistent_error()`
  - Given: Service
  - When: `service.toggle_completion(999)`
  - Then: Returns error Result with message "Todo with ID 999 not found"
  - **Acceptance**: Test FAILS ❌

### Implementation for Service Layer (GREEN PHASE - Make tests PASS)

- [ ] **T044** [SETUP] Implement `Result` type in `src/todo_cli/service.py`
  - Define: `class Result[T, E]` (generic success/error type)
  - Implement: `@staticmethod success(value: T) -> Result[T, E]`
  - Implement: `@staticmethod error(error: E) -> Result[T, E]`
  - Implement: `is_success() -> bool`
  - Implement: `unwrap() -> T` (returns value or raises)
  - Implement: `unwrap_error() -> E` (returns error or raises)
  - Add: Type hints and docstrings
  - **Acceptance**: Result type works correctly in tests

- [ ] **T045** [SETUP] Implement `TodoService` class in `src/todo_cli/service.py`
  - Define: `class TodoService`
  - Initialize: `__init__(self, repository: TodoRepository)`
  - Implement: `create_todo(title: str, description: str = "") -> Result[Todo, str]`
    - Validate: title.strip() is not empty
    - Call: `repository.add(Todo(...))`
    - Return: success or error Result
  - Implement: `list_todos() -> list[Todo]`
    - Call: `repository.get_all()`
  - Implement: `update_todo(id: int, title: str | None, description: str | None) -> Result[Todo, str]`
    - Validate: ID exists, at least one field provided, title not empty if provided
    - Update: fields that are not None
    - Return: success or error Result
  - Implement: `delete_todo(id: int) -> Result[bool, str]`
    - Validate: ID exists
    - Call: `repository.delete(id)`
    - Return: success or error Result
  - Implement: `toggle_completion(id: int) -> Result[Todo, str]`
    - Validate: ID exists
    - Toggle: `completed` field
    - Update: via repository
    - Return: success or error Result
  - Add: Type hints for all methods
  - Add: Docstrings for all public methods
  - **Acceptance**: All service tests (T029-T043) now PASS ✅

**Checkpoint**: Business logic complete - ALL foundational layers ready for user stories

---

## Phase 5: Output Formatting (Foundational - BLOCKS CLI)

**Purpose**: Implement output formatting for human-readable console display

### Tests for Formatters (RED PHASE - Write FIRST)

- [ ] **T046** [P] [SETUP] Create unit test file `tests/unit/test_formatters.py`
  - Import: `pytest`, `todo_cli.formatters`, `todo_cli.models`
  - Add fixture: `sample_todos()` (list of test todos)
  - **Acceptance**: File exists with fixtures

- [ ] **T047** [P] [SETUP] Write test: Format single todo in `tests/unit/test_formatters.py`
  - Test: `test_format_single_todo()`
  - Given: Todo (ID 1, "Buy milk", "From store", completed=False)
  - When: `formatter.format_single_todo(todo)`
  - Then: Output contains ID, title, description, status indicator
  - **Acceptance**: Test FAILS ❌

- [ ] **T048** [P] [SETUP] Write test: Format todo list in `tests/unit/test_formatters.py`
  - Test: `test_format_todo_list()`
  - Given: List of 3 todos (mix of complete/incomplete)
  - When: `formatter.format_todo_list(todos)`
  - Then: Output is tabular with columns: ID, Status, Title, Description
  - **Acceptance**: Test FAILS ❌

- [ ] **T049** [P] [SETUP] Write test: Format empty list in `tests/unit/test_formatters.py`
  - Test: `test_format_empty_list()`
  - Given: Empty list
  - When: `formatter.format_todo_list([])`
  - Then: Output is "No todos found" or similar message
  - **Acceptance**: Test FAILS ❌

- [ ] **T050** [P] [SETUP] Write test: Completion status indicators in `tests/unit/test_formatters.py`
  - Test: `test_completion_status_indicators()`
  - Given: Complete todo and incomplete todo
  - When: Format both
  - Then: Complete shows "✓", incomplete shows "✗"
  - **Acceptance**: Test FAILS ❌

- [ ] **T051** [P] [SETUP] Write test: Success message in `tests/unit/test_formatters.py`
  - Test: `test_format_success_message()`
  - Given: Action "created", Todo
  - When: `formatter.format_success_message("created", todo)`
  - Then: Output is "✓ Todo created successfully: [ID] Title"
  - **Acceptance**: Test FAILS ❌

- [ ] **T052** [P] [SETUP] Write test: Error message in `tests/unit/test_formatters.py`
  - Test: `test_format_error_message()`
  - Given: Error "Todo with ID 999 not found"
  - When: `formatter.format_error_message(error)`
  - Then: Output is "✗ Error: Todo with ID 999 not found"
  - **Acceptance**: Test FAILS ❌

- [ ] **T053** [P] [SETUP] Write test: Very long title truncation/wrapping in `tests/unit/test_formatters.py`
  - Test: `test_format_long_title()`
  - Given: Todo with 200-character title
  - When: Format todo
  - Then: Output handles long title gracefully (wrap or truncate with ...)
  - **Acceptance**: Test FAILS ❌

### Implementation for Formatters (GREEN PHASE - Make tests PASS)

- [ ] **T054** [SETUP] Implement `OutputFormatter` class in `src/todo_cli/formatters.py`
  - Define: `class OutputFormatter`
  - Implement: `format_single_todo(todo: Todo) -> str`
    - Format: "[ID] Title - Description (✓/✗)"
  - Implement: `format_todo_list(todos: list[Todo]) -> str`
    - Format: Tabular layout with headers and aligned columns
    - Columns: ID | Status | Title | Description
  - Implement: `format_empty_list_message() -> str`
    - Return: "No todos found. Use 'add' to create one."
  - Implement: `format_success_message(action: str, todo: Todo) -> str`
    - Format: "✓ Todo {action} successfully: [ID] {title}"
  - Implement: `format_error_message(error: str) -> str`
    - Format: "✗ Error: {error}"
  - Add: Helper method for status indicator: `_get_status_icon(completed: bool) -> str`
  - Add: Type hints and docstrings
  - **Acceptance**: All formatter tests (T047-T053) now PASS ✅

**Checkpoint**: All foundational layers complete - ready to implement user stories

---

## Phase 6: User Story 1 - Create and View Todos (Priority: P1) 🎯 MVP

**Goal**: Enable users to add todos and view them in a list (minimum viable product)

**Independent Test**: Launch CLI, add 3 todos with different titles/descriptions, view list showing all 3

### Integration Tests for User Story 1 (RED PHASE - Write FIRST)

- [ ] **T055** [P] [US1] Create integration test file `tests/integration/test_cli_flows.py`
  - Import: `pytest`, `io.StringIO`, CLI components
  - Add helper: `simulate_cli_input(commands: list[str])` to mock user input
  - Add helper: `capture_cli_output() -> str` to capture printed output
  - **Acceptance**: File exists with test helpers

- [ ] **T056** [US1] Write integration test: Add todo with title and description in `tests/integration/test_cli_flows.py`
  - Test: `test_add_todo_with_description()`
  - Given: CLI running with empty repository
  - When: User enters: "add" → "Buy groceries" → "Milk, eggs, bread"
  - Then: Success message shown, todo list shows new todo with ID 1
  - **Acceptance**: Test FAILS ❌

- [ ] **T057** [US1] Write integration test: Add todo with title only in `tests/integration/test_cli_flows.py`
  - Test: `test_add_todo_title_only()`
  - Given: CLI running
  - When: User enters: "add" → "Call dentist" → "" (empty description)
  - Then: Success message shown, todo appears in list
  - **Acceptance**: Test FAILS ❌

- [ ] **T058** [US1] Write integration test: Add multiple todos in `tests/integration/test_cli_flows.py`
  - Test: `test_add_multiple_todos()`
  - Given: CLI running
  - When: User adds 3 todos
  - Then: List shows all 3 with IDs 1, 2, 3
  - **Acceptance**: Test FAILS ❌

- [ ] **T059** [US1] Write integration test: Reject empty title in `tests/integration/test_cli_flows.py`
  - Test: `test_add_todo_empty_title_error()`
  - Given: CLI running
  - When: User enters: "add" → "" (empty title)
  - Then: Error message "Title cannot be empty" shown
  - **Acceptance**: Test FAILS ❌

- [ ] **T060** [US1] Write integration test: View empty list in `tests/integration/test_cli_flows.py`
  - Test: `test_list_empty_todos()`
  - Given: CLI running with empty repository
  - When: User enters: "list"
  - Then: "No todos found" message shown
  - **Acceptance**: Test FAILS ❌

### Implementation for User Story 1 (GREEN PHASE - Make tests PASS)

- [ ] **T061** [US1] Implement CLI command parser in `src/todo_cli/cli.py`
  - Define: `class TodoCLI`
  - Initialize: `__init__(self, service: TodoService, formatter: OutputFormatter)`
  - Implement: `parse_command(input: str) -> str | None` (returns command name)
  - Implement: `show_menu() -> None` (prints available commands)
  - Implement: `show_welcome_message() -> None`
  - **Acceptance**: Command parsing logic works

- [ ] **T062** [US1] Implement 'add' command handler in `src/todo_cli/cli.py`
  - Implement: `_handle_add() -> None`
  - Prompt: "Enter title: "
  - Prompt: "Enter description (optional): "
  - Call: `service.create_todo(title, description)`
  - Handle: Result success/error
  - Print: Formatted success or error message
  - **Acceptance**: Add command works in isolation

- [ ] **T063** [US1] Implement 'list' command handler in `src/todo_cli/cli.py`
  - Implement: `_handle_list() -> None`
  - Call: `service.list_todos()`
  - Format: Using `formatter.format_todo_list(todos)`
  - Print: Formatted list or empty message
  - **Acceptance**: List command works in isolation

- [ ] **T064** [US1] Implement main REPL loop in `src/todo_cli/cli.py`
  - Implement: `run() -> None`
  - Loop: Show menu → read input → parse → execute → repeat
  - Handle: Invalid commands gracefully
  - Exit: On 'exit' or 'quit' command
  - **Acceptance**: REPL loop runs without crashing

- [ ] **T065** [US1] Implement entry point in `src/todo_cli/__main__.py`
  - Import: Repository, Service, Formatter, CLI classes
  - Implement: `main()` function
    - Create: repository instance
    - Create: service instance with repository
    - Create: formatter instance
    - Create: CLI instance with service and formatter
    - Call: `cli.run()`
  - Add: `if __name__ == "__main__": main()`
  - **Acceptance**: Application can be launched with `python -m todo_cli`

- [ ] **T066** [US1] Add 'help' command handler in `src/todo_cli/cli.py`
  - Implement: `_handle_help() -> None`
  - Print: Command list with descriptions
  - Commands: add, list, update, delete, toggle, help, exit
  - **Acceptance**: Help command shows all available commands

- [ ] **T067** [US1] Add 'exit' command handler in `src/todo_cli/cli.py`
  - Implement: `_handle_exit() -> None`
  - Print: Goodbye message
  - Set: flag to exit REPL loop
  - **Acceptance**: Exit command terminates application gracefully

- [ ] **T068** [US1] Verify all User Story 1 integration tests pass
  - Run: `uv run pytest tests/integration/test_cli_flows.py -k US1`
  - **Acceptance**: All US1 tests (T056-T060) now PASS ✅

**Checkpoint**: User Story 1 COMPLETE - MVP is functional! Can add and view todos.

---

## Phase 7: User Story 2 - Mark Todos Complete (Priority: P2)

**Goal**: Enable users to toggle todo completion status

**Independent Test**: Add 2 todos, mark one complete, verify status changes, toggle back to incomplete

### Integration Tests for User Story 2 (RED PHASE - Write FIRST)

- [ ] **T069** [US2] Write integration test: Toggle incomplete to complete in `tests/integration/test_cli_flows.py`
  - Test: `test_toggle_incomplete_to_complete()`
  - Given: CLI with incomplete todo ID 1
  - When: User enters: "toggle" → "1"
  - Then: Success message, list shows todo with ✓ status
  - **Acceptance**: Test FAILS ❌

- [ ] **T070** [US2] Write integration test: Toggle complete to incomplete in `tests/integration/test_cli_flows.py`
  - Test: `test_toggle_complete_to_incomplete()`
  - Given: CLI with complete todo ID 2
  - When: User enters: "toggle" → "2"
  - Then: Success message, list shows todo with ✗ status
  - **Acceptance**: Test FAILS ❌

- [ ] **T071** [US2] Write integration test: Toggle preserves title and description in `tests/integration/test_cli_flows.py`
  - Test: `test_toggle_preserves_fields()`
  - Given: CLI with todo (title, description, incomplete)
  - When: User toggles completion
  - Then: Only status changes, title and description unchanged
  - **Acceptance**: Test FAILS ❌

- [ ] **T072** [US2] Write integration test: Toggle non-existent ID in `tests/integration/test_cli_flows.py`
  - Test: `test_toggle_nonexistent_id_error()`
  - Given: CLI
  - When: User enters: "toggle" → "999"
  - Then: Error message "Todo with ID 999 not found"
  - **Acceptance**: Test FAILS ❌

### Implementation for User Story 2 (GREEN PHASE - Make tests PASS)

- [ ] **T073** [US2] Implement 'toggle' command handler in `src/todo_cli/cli.py`
  - Implement: `_handle_toggle() -> None`
  - Prompt: "Enter todo ID to toggle: "
  - Validate: Input is integer
  - Call: `service.toggle_completion(id)`
  - Handle: Result success/error
  - Print: Formatted success or error message
  - **Acceptance**: Toggle command works correctly

- [ ] **T074** [US2] Verify all User Story 2 integration tests pass
  - Run: `uv run pytest tests/integration/test_cli_flows.py -k US2`
  - **Acceptance**: All US2 tests (T069-T072) now PASS ✅

**Checkpoint**: User Story 2 COMPLETE - Can now mark todos complete/incomplete

---

## Phase 8: User Story 3 - Update Todo Details (Priority: P3)

**Goal**: Enable users to update todo title and/or description

**Independent Test**: Add todo, update title, verify change, update description, verify change

### Integration Tests for User Story 3 (RED PHASE - Write FIRST)

- [ ] **T075** [US3] Write integration test: Update title only in `tests/integration/test_cli_flows.py`
  - Test: `test_update_title_only()`
  - Given: CLI with todo ID 1 (title "Buy groceries")
  - When: User enters: "update" → "1" → "Buy groceries and coffee" → "" (no description change)
  - Then: Success message, list shows updated title, description unchanged
  - **Acceptance**: Test FAILS ❌

- [ ] **T076** [US3] Write integration test: Update description only in `tests/integration/test_cli_flows.py`
  - Test: `test_update_description_only()`
  - Given: CLI with todo ID 2
  - When: User enters: "update" → "2" → "" (no title change) → "New description"
  - Then: Success message, list shows updated description, title unchanged
  - **Acceptance**: Test FAILS ❌

- [ ] **T077** [US3] Write integration test: Update both fields in `tests/integration/test_cli_flows.py`
  - Test: `test_update_both_fields()`
  - Given: CLI with todo ID 3
  - When: User updates both title and description
  - Then: Success message, both fields updated in list
  - **Acceptance**: Test FAILS ❌

- [ ] **T078** [US3] Write integration test: Update rejects empty title in `tests/integration/test_cli_flows.py`
  - Test: `test_update_empty_title_error()`
  - Given: CLI with todo ID 1
  - When: User enters: "update" → "1" → "" (empty title)
  - Then: Error message "Title cannot be empty"
  - **Acceptance**: Test FAILS ❌

- [ ] **T079** [US3] Write integration test: Update non-existent ID in `tests/integration/test_cli_flows.py`
  - Test: `test_update_nonexistent_id_error()`
  - Given: CLI
  - When: User enters: "update" → "999" → "New title"
  - Then: Error message "Todo with ID 999 not found"
  - **Acceptance**: Test FAILS ❌

### Implementation for User Story 3 (GREEN PHASE - Make tests PASS)

- [ ] **T080** [US3] Implement 'update' command handler in `src/todo_cli/cli.py`
  - Implement: `_handle_update() -> None`
  - Prompt: "Enter todo ID to update: "
  - Validate: Input is integer
  - Prompt: "Enter new title (leave empty to keep current): "
  - Prompt: "Enter new description (leave empty to keep current): "
  - Determine: Which fields to update (non-empty inputs)
  - Call: `service.update_todo(id, title, description)`
  - Handle: Result success/error
  - Print: Formatted success or error message
  - **Acceptance**: Update command works correctly

- [ ] **T081** [US3] Verify all User Story 3 integration tests pass
  - Run: `uv run pytest tests/integration/test_cli_flows.py -k US3`
  - **Acceptance**: All US3 tests (T075-T079) now PASS ✅

**Checkpoint**: User Story 3 COMPLETE - Can now update todo details

---

## Phase 9: User Story 4 - Delete Todos (Priority: P4)

**Goal**: Enable users to delete todos they no longer need

**Independent Test**: Add 3 todos, delete middle one, verify it's gone and others remain

### Integration Tests for User Story 4 (RED PHASE - Write FIRST)

- [ ] **T082** [US4] Write integration test: Delete todo in `tests/integration/test_cli_flows.py`
  - Test: `test_delete_todo()`
  - Given: CLI with 3 todos (IDs 1, 2, 3)
  - When: User enters: "delete" → "2"
  - Then: Success message, list shows only IDs 1 and 3
  - **Acceptance**: Test FAILS ❌

- [ ] **T083** [US4] Write integration test: Delete last remaining todo in `tests/integration/test_cli_flows.py`
  - Test: `test_delete_last_todo()`
  - Given: CLI with 1 todo
  - When: User deletes it
  - Then: Success message, list shows "No todos found"
  - **Acceptance**: Test FAILS ❌

- [ ] **T084** [US4] Write integration test: Delete non-existent ID in `tests/integration/test_cli_flows.py`
  - Test: `test_delete_nonexistent_id_error()`
  - Given: CLI
  - When: User enters: "delete" → "999"
  - Then: Error message "Todo with ID 999 not found"
  - **Acceptance**: Test FAILS ❌

- [ ] **T085** [US4] Write integration test: Operations on deleted todo fail in `tests/integration/test_cli_flows.py`
  - Test: `test_operations_on_deleted_todo_fail()`
  - Given: CLI, delete todo ID 5
  - When: User attempts to update/toggle/delete ID 5 again
  - Then: All operations return "Todo with ID 5 not found"
  - **Acceptance**: Test FAILS ❌

### Implementation for User Story 4 (GREEN PHASE - Make tests PASS)

- [ ] **T086** [US4] Implement 'delete' command handler in `src/todo_cli/cli.py`
  - Implement: `_handle_delete() -> None`
  - Prompt: "Enter todo ID to delete: "
  - Validate: Input is integer
  - Prompt: "Are you sure? (y/n): " (confirmation)
  - If confirmed, call: `service.delete_todo(id)`
  - Handle: Result success/error
  - Print: Formatted success or error message
  - **Acceptance**: Delete command works correctly

- [ ] **T087** [US4] Verify all User Story 4 integration tests pass
  - Run: `uv run pytest tests/integration/test_cli_flows.py -k US4`
  - **Acceptance**: All US4 tests (T082-T085) now PASS ✅

**Checkpoint**: User Story 4 COMPLETE - All core features implemented!

---

## Phase 10: Edge Cases & Error Handling

**Purpose**: Ensure robustness with special inputs and error conditions

### Edge Case Tests (RED PHASE - Write FIRST)

- [ ] **T088** [P] Write edge case test: Title with special characters in `tests/integration/test_cli_flows.py`
  - Test: `test_special_characters_in_title()`
  - Given: CLI
  - When: User creates todo with title "Buy @#$% & items!"
  - Then: Todo created successfully, characters preserved
  - **Acceptance**: Test FAILS ❌

- [ ] **T089** [P] Write edge case test: Very long title in `tests/integration/test_cli_flows.py`
  - Test: `test_very_long_title()`
  - Given: CLI
  - When: User creates todo with 500-character title
  - Then: Todo created, full title stored and displayed
  - **Acceptance**: Test FAILS ❌

- [ ] **T090** [P] Write edge case test: Very long description in `tests/integration/test_cli_flows.py`
  - Test: `test_very_long_description()`
  - Given: CLI
  - When: User creates todo with 2000-character description
  - Then: Todo created, full description stored
  - **Acceptance**: Test FAILS ❌

- [ ] **T091** [P] Write edge case test: Invalid ID format in `tests/integration/test_cli_flows.py`
  - Test: `test_invalid_id_format()`
  - Given: CLI with todos
  - When: User enters non-integer ID (e.g., "abc")
  - Then: Error message "Invalid ID. Please enter a number."
  - **Acceptance**: Test FAILS ❌

- [ ] **T092** [P] Write edge case test: Invalid command in `tests/integration/test_cli_flows.py`
  - Test: `test_invalid_command()`
  - Given: CLI running
  - When: User enters unknown command "foo"
  - Then: Error message with available commands
  - **Acceptance**: Test FAILS ❌

### Edge Case Implementation (GREEN PHASE - Make tests PASS)

- [ ] **T093** Add input validation for ID parsing in `src/todo_cli/cli.py`
  - Add: `_parse_id(input: str) -> int | None` helper method
  - Validate: Input is numeric, convert to int
  - Return: None if invalid
  - **Acceptance**: Invalid IDs handled gracefully

- [ ] **T094** Add invalid command handling in `src/todo_cli/cli.py`
  - Update: `run()` method to handle unknown commands
  - Print: Error message with available commands
  - Suggest: "Type 'help' for available commands"
  - **Acceptance**: Unknown commands don't crash application

- [ ] **T095** Verify all edge case tests pass
  - Run: `uv run pytest tests/integration/test_cli_flows.py -k edge`
  - **Acceptance**: All edge case tests (T088-T092) now PASS ✅

**Checkpoint**: Edge cases handled - application is robust

---

## Phase 11: Testing & Quality Assurance

**Purpose**: Ensure comprehensive test coverage and code quality

- [ ] **T096** Run full test suite and verify coverage
  - Run: `uv run pytest --cov=todo_cli --cov-report=html`
  - Verify: Test coverage >90%
  - Review: Coverage report in `htmlcov/index.html`
  - **Acceptance**: Coverage meets constitutional requirement (>90%)

- [ ] **T097** [P] Run type checking with mypy
  - Run: `uv run mypy src/todo_cli/`
  - Fix: Any type errors
  - **Acceptance**: Zero mypy errors

- [ ] **T098** [P] Review code for constitutional compliance
  - Check: Separation of concerns (domain/service/interface/infrastructure)
  - Check: No global mutable state
  - Check: Cyclomatic complexity <10 per function
  - Check: No code duplication
  - **Acceptance**: Code meets all constitutional standards

- [ ] **T099** Add missing unit tests for uncovered code
  - Identify: Uncovered lines from coverage report
  - Write: Tests for uncovered paths
  - **Acceptance**: Coverage reaches >95%

- [ ] **T100** Manual testing: Full user journey
  - Execute: Manual testing checklist from plan.md Section 6.5
  - Test: All 20 manual test scenarios
  - Document: Any issues found
  - **Acceptance**: All manual tests pass

**Checkpoint**: Quality assurance complete - ready for documentation

---

## Phase 12: Documentation & Finalization

**Purpose**: Complete documentation and verify all deliverables

- [ ] **T101** [P] Update `README.md` with complete instructions
  - Add: Prerequisites (Python 3.10+, UV installation)
  - Add: Setup steps (`uv sync`)
  - Add: Usage examples for each command (add, list, update, delete, toggle)
  - Add: Running tests (`uv run pytest`)
  - Add: Project structure overview
  - **Acceptance**: Another developer can follow README to use application

- [ ] **T102** [P] Create `CLAUDE.md` with AI implementation notes
  - Document: Implementation decisions made during `/sp.implement`
  - Document: Any deviations from plan (if any)
  - Document: Known limitations
  - Document: Future phase migration notes
  - **Acceptance**: CLAUDE.md provides complete implementation context

- [ ] **T103** [P] Create user guide in `docs/phase-1-cli/user-guide.md`
  - Document: Each command with examples
  - Document: Common workflows (e.g., "Managing daily tasks")
  - Document: Troubleshooting common issues
  - Add: Screenshots or ASCII output examples
  - **Acceptance**: User guide is clear and helpful

- [ ] **T104** [P] Add inline code comments for complex logic
  - Review: All modules for clarity
  - Add: Comments only where logic is non-obvious
  - Avoid: Over-commenting self-evident code
  - **Acceptance**: Code is self-documenting with strategic comments

- [ ] **T105** Create Phase I completion checklist
  - Copy: Acceptance checklist from spec.md
  - Verify: All items checked
  - Document: Any exceptions or notes
  - **Acceptance**: Checklist demonstrates Phase I completeness

- [ ] **T106** Verify all constitutional compliance requirements
  - Check: All 13 constitutional sections compliance (from plan.md Section 7.1)
  - Check: All specification requirements met (FR-001 to FR-021)
  - Check: All success criteria met (SC-001 to SC-020)
  - **Acceptance**: 100% constitutional compliance verified

**Checkpoint**: Documentation complete - Phase I ready for delivery

---

## Dependencies & Execution Order

### Phase Dependencies

1. **Phase 1 (Setup)**: No dependencies - start immediately
2. **Phase 2 (Domain)**: Depends on Phase 1 complete
3. **Phase 3 (Repository)**: Depends on Phase 2 complete
4. **Phase 4 (Service)**: Depends on Phase 2-3 complete
5. **Phase 5 (Formatters)**: Depends on Phase 2 complete (independent of 3-4)
6. **Phase 6 (US1)**: Depends on Phases 1-5 ALL complete ⚠️
7. **Phase 7 (US2)**: Depends on Phase 6 complete
8. **Phase 8 (US3)**: Depends on Phase 6 complete (can run parallel with Phase 7)
9. **Phase 9 (US4)**: Depends on Phase 6 complete (can run parallel with 7-8)
10. **Phase 10 (Edge Cases)**: Depends on Phases 6-9 complete
11. **Phase 11 (QA)**: Depends on all previous phases
12. **Phase 12 (Docs)**: Depends on Phase 11 complete

### Parallel Execution Opportunities

**Within Phase 1 (Setup)**:
- T001, T002, T003, T006, T007 can run in parallel

**Within Phase 2 (Domain Tests)**:
- T009, T010, T011, T012, T013, T014 can run in parallel (all writing tests)

**Within Phase 3 (Repository Tests)**:
- T017-T026 can run in parallel (all writing tests)

**Within Phase 4 (Service Tests)**:
- T029-T043 can run in parallel (all writing tests)

**Within Phase 5 (Formatter Tests)**:
- T047-T053 can run in parallel (all writing tests)

**User Stories (after Phase 6 complete)**:
- Phase 7 (US2), Phase 8 (US3), Phase 9 (US4) can run in parallel if team capacity allows

**Within Phase 10 (Edge Cases)**:
- T088-T092 can run in parallel (all writing tests)

**Within Phase 12 (Documentation)**:
- T101, T102, T103, T104 can run in parallel (different files)

### Critical Path (Sequential)

T001 → T004 → T005 → T015 → T027 → T044-T045 → T054 → T061-T065 → T073 → T080 → T086 → T096-T100 → T105-T106

**Estimated Total Tasks**: 106
**Parallel Tasks**: ~40 (marked with [P])
**Sequential Tasks**: ~66

---

## Implementation Strategy

### Test-Driven Development (TDD) Flow

**RED Phase**:
1. Write test that describes desired behavior
2. Run test → verify it FAILS ❌
3. Commit failing test

**GREEN Phase**:
4. Write minimal code to make test PASS ✅
5. Run test → verify it PASSES
6. Commit passing implementation

**REFACTOR Phase** (optional):
7. Improve code quality without changing behavior
8. Run tests → verify still PASS
9. Commit refactored code

### MVP-First Approach

**Week 1 Goal**: User Story 1 Complete
- Complete Phases 1-5 (foundational)
- Complete Phase 6 (US1)
- Deliverable: Can add and view todos

**Week 2 Goal**: All User Stories Complete
- Complete Phases 7-9 (US2-US4)
- Complete Phase 10 (edge cases)
- Deliverable: Full CRUD functionality

**Week 3 Goal**: Production Ready
- Complete Phase 11 (QA)
- Complete Phase 12 (documentation)
- Deliverable: Fully documented, tested, Phase I complete

---

## Success Criteria

Phase I is **COMPLETE** when:

**Functional**:
- ✅ All 4 user stories (US1-US4) pass integration tests
- ✅ All edge cases handled gracefully
- ✅ All 5 CRUD operations work correctly

**Technical**:
- ✅ All 106 tasks completed
- ✅ Test coverage >90% (target: 95%+)
- ✅ Zero mypy type errors
- ✅ All unit tests pass (60+ tests)
- ✅ All integration tests pass (20+ tests)

**Process**:
- ✅ Specification approved (DONE)
- ✅ Plan approved (DONE)
- ✅ Tasks created (THIS DOCUMENT)
- ✅ ADRs created for 4 architectural decisions
- ✅ Code generated via `/sp.implement` (no manual code)
- ✅ PHR created documenting session
- ✅ Manual testing checklist 100% complete

**Documentation**:
- ✅ README.md complete with setup and usage
- ✅ CLAUDE.md updated with implementation notes
- ✅ User guide created
- ✅ Code appropriately commented
- ✅ All acceptance criteria verified

**Constitutional Compliance**:
- ✅ SDD workflow followed (constitution → spec → plan → tasks → implement)
- ✅ Domain model matches Constitution Section II exactly
- ✅ Repository structure matches Constitution Section IV
- ✅ Code quality meets Constitution Section V
- ✅ No Phase II+ features implemented (exclusions enforced)

---

## Notes

- **[P] Tasks**: Can be executed in parallel (different files, no dependencies)
- **Test-First**: All tests written FIRST, verified to FAIL, then implementation makes them PASS
- **Checkpoints**: Stop and validate after each phase completion
- **Commit Often**: Commit after each task or logical group
- **Constitutional Compliance**: Every task aligns with Constitution and Specification
- **Traceability**: Each task references exact file paths and acceptance criteria

---

## Document Control

**Version**: 1.0.0
**Status**: Ready for Implementation
**Created By**: Claude Code (AI)
**Approved By**: [Pending Human Architect]

**Related Documents**:
- Constitution: `.specify/memory/constitution.md` (v1.0.0)
- Specification: `specs-history/phase-1-cli/spec.md` (v1.0.0)
- Plan: `specs-history/phase-1-cli/plan.md` (v1.0.0)
- ADRs: `/history/adr/` (pending creation)

**Next Step**: `/sp.implement` to generate code following this task breakdown

---

*End of Task Breakdown*
