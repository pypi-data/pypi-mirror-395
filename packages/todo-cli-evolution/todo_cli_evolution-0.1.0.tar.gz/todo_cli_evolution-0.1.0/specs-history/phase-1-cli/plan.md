# Technical Implementation Plan: Phase I - In-Memory Python CLI Todo Application

**Project**: The Evolution of Todo
**Phase**: Phase I (Foundation)
**Created**: 2025-12-07
**Status**: Draft
**Plan Version**: 1.0.0

**References**:
- Constitution: `.specify/memory/constitution.md` (v1.0.0)
- Specification: `specs-history/phase-1-cli/spec.md` (v1.0.0)

---

## 1. Phase Overview

### 1.1 Executive Summary

Phase I delivers a **pure Python command-line application** that implements the foundational Todo domain model with five essential CRUD operations. The application maintains all todo data **in-memory only**, with no persistence mechanism, establishing the base architecture and domain model that will remain consistent across all future phases.

**Key Characteristics**:
- **Runtime**: Pure Python 3.10+ (targeting 3.13 for latest features)
- **Interface**: Command-line interface (CLI) with interactive commands
- **Storage**: In-memory data structures (ephemeral, lost on exit)
- **Operations**: Add, View, Update, Delete, Toggle Completion
- **Architecture**: Clean separation between domain logic, storage, and interface layers

**Value Proposition**: Validates the core Todo domain model and CRUD operations in the simplest possible environment before adding complexity in later phases.

### 1.2 Scope Boundaries

**In Scope**:
- Five basic CRUD operations on Todo entities
- In-memory storage with automatic ID assignment
- Input validation and error handling
- Human-readable CLI output formatting
- Comprehensive test coverage

**Out of Scope** (deferred to future phases):
- Any form of persistence (files, databases)
- Search, filter, or sort capabilities
- Advanced features (tags, priorities, due dates)
- Web interfaces or APIs
- Multi-user support or authentication

---

## 2. Technical Stack

### 2.1 Core Technologies

#### Programming Language
**Python 3.10+** (recommend 3.13 for latest features)

**Justification**:
- Constitutional requirement (Section III)
- Mature standard library reduces external dependencies
- Strong type hinting support for code clarity
- Excellent testing ecosystem
- Cross-platform CLI support

#### Project & Environment Manager
**UV** (Astral's fast Python package manager)

**Justification**:
- Constitutional requirement (Section V)
- Significantly faster than pip/poetry
- Modern dependency resolution
- Built-in virtual environment management
- Compatible with standard Python packaging

### 2.2 Development Tools

#### CLI Implementation
**Python Standard Library** (no framework required)

**Options Evaluated**:
1. **Custom REPL loop** (RECOMMENDED)
   - Full control over interaction flow
   - Simple to implement and test
   - Best UX for interactive todo management

2. **argparse** (single-command style)
   - Better for scriptable automation
   - Less intuitive for interactive task management
   - Would require multiple command invocations

**Decision**: Custom REPL loop (see ADR-001 below)

#### Testing Framework
**pytest** (de facto Python testing standard)

**Justification**:
- Pythonic, minimal boilerplate
- Rich assertion introspection
- Powerful fixture system for test data
- Excellent plugin ecosystem
- Constitutional test-first mandate compatibility

#### Type Checking (Optional but Recommended)
**mypy** (static type checker)

**Justification**:
- Enforces type hints at development time
- Catches errors before runtime
- Improves code documentation
- Aligns with constitutional code quality standards

### 2.3 Dependencies

**Production Dependencies**: None (standard library only)

**Development Dependencies**:
- `pytest` >= 8.0.0 (testing framework)
- `pytest-cov` >= 4.0.0 (test coverage reporting)
- `mypy` >= 1.7.0 (optional type checking)

**Rationale**: Minimal dependencies reduce complexity, improve maintainability, and align with constitutional simplicity principles.

---

## 3. Architecture Design

### 3.1 High-Level Architecture

**Layered Architecture** (Clean Architecture principles):

```
┌─────────────────────────────────────┐
│      CLI Interface Layer            │  User interaction
│  (cli.py, formatters.py)            │  Command parsing, output
├─────────────────────────────────────┤
│      Application Layer              │  Business logic orchestration
│  (service.py)                       │  Validation, error handling
├─────────────────────────────────────┤
│      Domain Layer                   │  Core business entities
│  (models.py)                        │  Todo entity, domain rules
├─────────────────────────────────────┤
│      Infrastructure Layer           │  Data storage
│  (repository.py)                    │  In-memory storage management
└─────────────────────────────────────┘
```

**Design Principles**:
- **Separation of Concerns**: Each layer has single, clear responsibility
- **Dependency Inversion**: Domain layer has no dependencies; other layers depend on domain
- **Testability**: Each layer independently testable
- **Evolvability**: Storage and interface layers replaceable in future phases

### 3.2 Module Structure

```
src/
└── todo_cli/
    ├── __init__.py              # Package initialization, version
    ├── __main__.py              # Entry point for `python -m todo_cli`
    ├── models.py                # Domain models (Todo entity)
    ├── repository.py            # Storage abstraction (in-memory)
    ├── service.py               # Business logic & validation
    ├── cli.py                   # CLI controller & REPL loop
    └── formatters.py            # Output formatting utilities

tests/
├── unit/
│   ├── test_models.py           # Todo entity tests
│   ├── test_repository.py       # Storage layer tests
│   ├── test_service.py          # Business logic tests
│   └── test_formatters.py       # Output formatting tests
└── integration/
    └── test_cli_flows.py        # End-to-end user journey tests

pyproject.toml                   # UV project configuration
README.md                        # Setup and usage instructions
CLAUDE.md                        # AI agent instructions
```

### 3.3 Core Components

#### 3.3.1 Domain Layer (`models.py`)

**Responsibility**: Define the Todo entity and its invariants

**Todo Entity**:
```python
@dataclass
class Todo:
    id: int | str           # Unique identifier (see ADR-002)
    title: str              # Required, non-empty
    description: str        # Optional, can be empty
    completed: bool         # Default: False
```

**Invariants** (enforced at creation/update):
- `id` is immutable once assigned
- `title` is always non-empty after validation
- `completed` is strictly boolean (no None or intermediate states)
- All fields are immutable (dataclass with frozen=True or explicit control)

**Methods**:
- `__post_init__()`: Validate title is non-empty
- Factory methods for creation with validation

#### 3.3.2 Infrastructure Layer (`repository.py`)

**Responsibility**: Manage in-memory storage and retrieval of Todo entities

**TodoRepository Class**:
```python
class TodoRepository:
    def __init__(self):
        self._todos: dict[int, Todo] = {}  # ID -> Todo mapping
        self._next_id: int = 1              # Auto-increment counter

    # Core operations
    def add(todo: Todo) -> Todo            # Assigns ID, stores
    def get_by_id(id: int) -> Todo | None  # Retrieve single
    def get_all() -> list[Todo]            # Retrieve all
    def update(todo: Todo) -> None         # Replace existing
    def delete(id: int) -> bool            # Remove, return success
    def exists(id: int) -> bool            # Check existence
```

**Design Decisions**:
- Dictionary storage for O(1) lookup by ID
- Separate ID counter for automatic assignment
- Returns Todo copies to prevent external mutation (defensive programming)
- No query/filter methods (not needed in Phase I)

#### 3.3.3 Application Layer (`service.py`)

**Responsibility**: Orchestrate business logic, validation, and error handling

**TodoService Class**:
```python
class TodoService:
    def __init__(self, repository: TodoRepository):
        self._repo = repository

    # High-level operations with validation
    def create_todo(title: str, description: str = "") -> Result[Todo, str]
    def list_todos() -> list[Todo]
    def update_todo(id: int, title: str | None, description: str | None) -> Result[Todo, str]
    def delete_todo(id: int) -> Result[bool, str]
    def toggle_completion(id: int) -> Result[Todo, str]
```

**Validation Rules**:
- Title cannot be empty or whitespace-only
- IDs must exist for update/delete/toggle operations
- At least one field (title or description) required for updates

**Error Handling**:
- Returns `Result` type (success/error union) for explicit error handling
- Error messages are user-friendly, not technical
- No exceptions for business rule violations (expected errors)

#### 3.3.4 CLI Interface Layer (`cli.py`)

**Responsibility**: Handle user interaction, command parsing, and output delegation

**CLI Controller**:
```python
class TodoCLI:
    def __init__(self, service: TodoService, formatter: OutputFormatter):
        self._service = service
        self._formatter = formatter

    def run():                  # Main REPL loop
    def show_menu():            # Display available commands
    def parse_command(input: str) -> Command | None
    def execute_command(cmd: Command) -> None

    # Command handlers
    def _handle_add():
    def _handle_list():
    def _handle_update():
    def _handle_delete():
    def _handle_toggle():
    def _handle_help():
    def _handle_exit():
```

**REPL Flow**:
1. Display menu/prompt
2. Read user input
3. Parse into command + arguments
4. Execute via service layer
5. Format and display result
6. Loop until exit command

**Command Interface**:
- Simple text commands: `add`, `list`, `update`, `delete`, `toggle`, `help`, `exit`
- Guided prompts for command arguments (title, description, ID)
- Clear error messages for invalid input

#### 3.3.5 Output Formatting (`formatters.py`)

**Responsibility**: Format data for human-readable console output

**OutputFormatter Class**:
```python
class OutputFormatter:
    def format_todo_list(todos: list[Todo]) -> str
    def format_single_todo(todo: Todo) -> str
    def format_success_message(action: str, todo: Todo) -> str
    def format_error_message(error: str) -> str
    def format_empty_list_message() -> str
```

**Output Standards**:
- Tabular format for todo lists (aligned columns)
- Completion indicator: ✓ (complete) / ✗ (incomplete)
- Consistent spacing and borders
- Color support optional (basic version: plain text)

**Example Output**:
```
ID | Status | Title                  | Description
---+--------+------------------------+---------------------------
1  | ✗      | Buy groceries          | Milk, eggs, bread
2  | ✓      | Call dentist           |
3  | ✗      | Finish project report  | Due Friday
```

### 3.4 Data Flow

**Example: Add Todo**
```
User input: "add"
  ↓
CLI prompts for title & description
  ↓
User enters: title="Buy milk", description=""
  ↓
CLI → Service.create_todo("Buy milk", "")
  ↓
Service validates title (non-empty ✓)
  ↓
Service → Repository.add(Todo)
  ↓
Repository assigns ID=1, stores in dict
  ↓
Repository returns Todo(id=1, ...)
  ↓
Service returns Result.success(Todo)
  ↓
CLI → Formatter.format_success_message(...)
  ↓
Display: "✓ Todo created successfully: [1] Buy milk"
```

**Example: Error Handling**
```
User input: "update"
  ↓
CLI prompts for ID
  ↓
User enters: ID=999
  ↓
CLI → Service.update_todo(999, ...)
  ↓
Service → Repository.get_by_id(999)
  ↓
Repository returns None (not found)
  ↓
Service returns Result.error("Todo with ID 999 not found")
  ↓
CLI → Formatter.format_error_message(...)
  ↓
Display: "✗ Error: Todo with ID 999 not found"
```

### 3.5 Entry Point

**`__main__.py`** (enables `python -m todo_cli`):
```python
from todo_cli.repository import TodoRepository
from todo_cli.service import TodoService
from todo_cli.formatters import OutputFormatter
from todo_cli.cli import TodoCLI

def main():
    repo = TodoRepository()
    service = TodoService(repo)
    formatter = OutputFormatter()
    cli = TodoCLI(service, formatter)

    cli.run()  # Enter REPL loop

if __name__ == "__main__":
    main()
```

---

## 4. Implementation Phases

### Phase 1: Project Initialization
**Duration**: 1 implementation cycle
**Goal**: Set up project structure and tooling

**Tasks**:
1. Initialize project with UV: `uv init todo-cli`
2. Configure `pyproject.toml` with project metadata
3. Create folder structure (`src/todo_cli/`, `tests/unit/`, `tests/integration/`)
4. Create placeholder Python files with module docstrings
5. Set up pytest configuration
6. Create initial README.md with setup instructions
7. Verify structure matches constitutional requirements

**Acceptance Criteria**:
- Project can be installed with `uv sync`
- `pytest` can be run (even with no tests yet)
- All placeholder modules import successfully

---

### Phase 2: Domain Model
**Duration**: 1 implementation cycle
**Goal**: Implement core Todo entity with validation

**Tasks**:
1. Define `Todo` dataclass in `models.py`
2. Implement field validation (title non-empty)
3. Add factory method for safe creation
4. Write unit tests for Todo creation and validation
5. Test edge cases (empty title, long strings, special characters)

**Acceptance Criteria**:
- Todo instances can be created with valid data
- Invalid todos (empty title) raise appropriate errors
- All unit tests pass
- Type hints are complete and mypy-clean

---

### Phase 3: Infrastructure Layer
**Duration**: 1-2 implementation cycles
**Goal**: Implement in-memory storage repository

**Tasks**:
1. Implement `TodoRepository` class in `repository.py`
2. Implement ID auto-increment strategy (see ADR-002)
3. Implement all CRUD operations (add, get_by_id, get_all, update, delete)
4. Add defensive copying to prevent external mutation
5. Write unit tests for all repository operations
6. Test edge cases (duplicate IDs, non-existent IDs, empty repository)

**Acceptance Criteria**:
- Repository correctly stores and retrieves todos
- IDs are unique and automatically assigned
- All CRUD operations work correctly
- All unit tests pass

---

### Phase 4: Application Layer
**Duration**: 1-2 implementation cycles
**Goal**: Implement business logic and validation service

**Tasks**:
1. Implement `TodoService` class in `service.py`
2. Implement all five operations with validation
3. Implement `Result` type for error handling
4. Add comprehensive input validation (title, ID existence)
5. Write unit tests for all service operations
6. Test validation rules and error conditions

**Acceptance Criteria**:
- Service validates all inputs correctly
- Service returns user-friendly error messages
- All business rules enforced (title non-empty, ID must exist)
- All unit tests pass

---

### Phase 5: Output Formatting
**Duration**: 1 implementation cycle
**Goal**: Implement console output formatting

**Tasks**:
1. Implement `OutputFormatter` class in `formatters.py`
2. Design table layout for todo lists
3. Implement completion status indicators (✓/✗)
4. Implement success and error message formatting
5. Write unit tests for all formatting methods
6. Test edge cases (empty list, very long titles)

**Acceptance Criteria**:
- Todo lists display in clean, readable format
- All output is human-friendly (no raw data dumps)
- Edge cases handled gracefully
- All unit tests pass

---

### Phase 6: CLI Interface
**Duration**: 2-3 implementation cycles
**Goal**: Implement interactive command-line interface

**Tasks**:
1. Implement `TodoCLI` class in `cli.py`
2. Implement REPL loop (read-eval-print loop)
3. Implement command parser (add, list, update, delete, toggle, help, exit)
4. Implement guided prompts for each command
5. Integrate with service and formatter layers
6. Add input validation and error handling
7. Write integration tests for complete user journeys
8. Test all acceptance scenarios from specification

**Acceptance Criteria**:
- All five core operations accessible via CLI
- Guided prompts make commands intuitive
- Error messages clear and actionable
- All integration tests pass
- All specification acceptance scenarios satisfied

---

### Phase 7: Testing & Quality Assurance
**Duration**: 1-2 implementation cycles
**Goal**: Ensure comprehensive test coverage and code quality

**Tasks**:
1. Review test coverage (aim for >90%)
2. Add missing edge case tests
3. Run mypy for type checking
4. Review code for constitutional compliance (modularity, simplicity)
5. Write manual testing checklist
6. Perform manual testing of all user journeys
7. Document any known limitations

**Acceptance Criteria**:
- Test coverage >90%
- All tests pass
- No mypy errors
- Code follows constitutional quality standards
- Manual testing checklist complete

---

### Phase 8: Documentation & Finalization
**Duration**: 1 implementation cycle
**Goal**: Complete documentation and prepare for delivery

**Tasks**:
1. Write comprehensive README.md (setup, usage, examples)
2. Update CLAUDE.md with any implementation-specific notes
3. Create user guide with command examples
4. Document project structure
5. Add inline code comments where needed (complex logic only)
6. Create final acceptance checklist from specification
7. Verify all constitutional compliance requirements

**Acceptance Criteria**:
- README contains complete setup and usage instructions
- All examples are tested and accurate
- Code is well-documented
- Specification acceptance checklist complete
- Ready for human architect review

---

## 5. Architectural Decision Records (ADRs)

The following decisions require ADR documentation per constitutional requirements (three-part significance test: Impact + Alternatives + Scope).

### ADR-001: CLI Interaction Model

**Decision**: Use interactive REPL loop instead of argparse command-line arguments

**Context**:
Phase I requires a user-friendly CLI for managing todos. Two primary approaches exist:

**Options Considered**:

1. **Interactive REPL Loop**
   - User launches app once, enters commands interactively
   - Commands: `add`, `list`, `update`, etc.
   - Guided prompts for arguments (title, description, ID)

2. **Argument-based CLI (argparse)**
   - User runs `python -m todo_cli add "Buy milk"`
   - Each operation is a separate program invocation
   - Standard UNIX command-line pattern

**Analysis**:

| Criterion | REPL Loop | argparse CLI |
|-----------|-----------|--------------|
| User Experience | Intuitive for task management | Better for scripting |
| Learning Curve | Lower (guided prompts) | Higher (must learn syntax) |
| Implementation | Moderate complexity | Simple (stdlib argparse) |
| Testing | Integration tests | Unit tests |
| Future Evolution | Smooth transition to web UI | Less similar to web patterns |
| Session Context | Maintains state (future: undo) | Stateless each run |

**Recommendation**: **Interactive REPL Loop**

**Rationale**:
- Better UX for interactive task management (primary use case)
- Guided prompts reduce errors and improve discoverability
- Maintains session context (foundation for future features like undo)
- More similar to web UI interactions (smoother Phase II transition)
- Constitutional principle: optimize for user value over technical convenience

**Consequences**:
- Requires custom command parser (not complex)
- Integration testing more important than pure unit testing
- Exit command needed (argparse has implicit exit after each command)

**Status**: Proposed (requires human approval)

---

### ADR-002: Todo ID Strategy

**Decision**: Use auto-incrementing integers for Todo IDs

**Context**:
Each todo requires a unique identifier. Two common approaches:

**Options Considered**:

1. **Auto-incrementing Integer**
   - Start at 1, increment for each new todo
   - Simple, predictable, human-readable
   - Easy to reference in CLI (type "1" vs "550e8400-e29b-41d4-a716-446655440000")

2. **UUID (Universally Unique Identifier)**
   - Generated via `uuid.uuid4()`
   - Globally unique, no collision risk
   - Standard for distributed systems

**Analysis**:

| Criterion | Auto-increment | UUID |
|-----------|----------------|------|
| Uniqueness | Local only | Global |
| Readability | High ("ID 1") | Low (long hex string) |
| CLI Usability | Excellent | Poor (typing long IDs) |
| Future Phases | Must migrate to UUID for distributed | Already compatible |
| Implementation | Simple counter | Single function call |
| Collision Risk | None (single process) | Negligible |
| Migration Cost | Phase IV: moderate effort | None |

**Recommendation**: **Auto-incrementing Integer**

**Rationale**:
- Phase I is single-process, in-memory (no distribution concerns)
- CLI usability is paramount: "delete 3" vs "delete 550e8400-..."
- Constitutional principle: simplicity and user focus
- Phase IV migration is acceptable cost (one-time effort, well-defined)
- IDs are ephemeral in Phase I anyway (lost on exit)

**Migration Path** (for Phase IV):
- Introduce UUID alongside integer ID
- Map integer IDs to UUIDs for distributed system
- OR: Switch to short collision-resistant IDs (nanoid, shortid)

**Consequences**:
- ID counter must be managed in repository
- IDs reset on application restart (acceptable for Phase I)
- Future phase will require ID strategy migration (documented tradeoff)

**Status**: Proposed (requires human approval)

---

### ADR-003: Error Handling Strategy

**Decision**: Use Result type pattern instead of exceptions for business logic errors

**Context**:
Business rule violations (e.g., "todo not found", "title empty") need consistent handling.

**Options Considered**:

1. **Result Type Pattern**
   - Functions return `Result[T, Error]` (success or error)
   - Caller must explicitly handle both cases
   - Errors are expected, not exceptional

2. **Exceptions**
   - Raise custom exceptions (e.g., `TodoNotFoundError`)
   - Caller catches exceptions or lets them propagate
   - Standard Python pattern

**Analysis**:

| Criterion | Result Type | Exceptions |
|-----------|-------------|------------|
| Explicitness | Forces error handling | Easy to forget to catch |
| Type Safety | Mypy can verify | Runtime only |
| Performance | No stack unwinding | Slower (stack traces) |
| Pythonic | Less common in Python | Standard practice |
| Control Flow | Explicit checks | Try/except blocks |
| Error Context | Structured error data | Exception message + traceback |

**Recommendation**: **Result Type Pattern**

**Rationale**:
- Business rule violations are *expected* conditions, not exceptions
- Type system can verify all error paths are handled
- More explicit contract: "this operation can fail, handle it"
- Better performance (no exception overhead)
- Constitutional principle: explicit over implicit, testability

**Implementation**:
```python
from typing import Generic, TypeVar

T = TypeVar('T')
E = TypeVar('E')

class Result(Generic[T, E]):
    @staticmethod
    def success(value: T) -> Result[T, E]: ...

    @staticmethod
    def error(error: E) -> Result[T, E]: ...

    def is_success(self) -> bool: ...
    def unwrap(self) -> T: ...
    def unwrap_error(self) -> E: ...
```

**Consequences**:
- Requires implementing Result type (50-100 lines)
- Less familiar to Python developers (learning curve)
- CLI layer must unwrap results and format appropriately
- More verbose than try/except in some cases

**Alternative**: Use exceptions for truly exceptional conditions (e.g., system errors)

**Status**: Proposed (requires human approval)

---

### ADR-004: In-Memory Storage Data Structure

**Decision**: Use dictionary (dict[int, Todo]) for primary storage

**Context**:
Repository needs to store todos in memory with efficient access patterns.

**Options Considered**:

1. **Dictionary (dict[int, Todo])**
   - Key: todo ID, Value: Todo instance
   - O(1) lookup, update, delete by ID

2. **List (list[Todo])**
   - Sequential storage, indexed by position
   - O(n) lookup by ID (must search)

3. **Both (dict for lookup + list for ordering)**
   - Maintain both structures
   - Fast lookup + guaranteed order

**Analysis**:

| Criterion | Dictionary | List | Both |
|-----------|------------|------|------|
| Lookup by ID | O(1) | O(n) | O(1) |
| Insertion Order | Guaranteed (Python 3.7+) | Natural | Guaranteed |
| Memory | Moderate | Low | High (duplicate) |
| Complexity | Low | Low | Moderate |
| Phase I Needs | Sufficient | Slower | Over-engineered |

**Recommendation**: **Dictionary**

**Rationale**:
- All operations (update, delete, toggle) require ID lookup → O(1) critical
- Python 3.7+ dicts maintain insertion order (no need for separate list)
- Phase I has no special ordering requirements (no sort/filter)
- Constitutional principle: simplicity, no premature optimization
- List iteration available via `dict.values()` when needed

**Consequences**:
- Natural iteration order is insertion order (acceptable)
- If future phase requires custom sorting, can migrate to dual structure
- Efficient for all CRUD operations

**Status**: Proposed (requires human approval)

---

## 6. Testing Strategy

### 6.1 Testing Principles

**Test-First Mandate** (Constitutional Section I.4):
- Tests written before or immediately after implementation
- All acceptance scenarios from specification must have corresponding tests
- Test coverage >90% (unit + integration)
- No feature marked complete until tests pass

### 6.2 Unit Testing

**Scope**: Individual components in isolation

**Test Coverage by Module**:

#### `models.py` (Todo Entity)
- ✓ Create todo with valid title and description
- ✓ Create todo with title only (empty description)
- ✗ Create todo with empty title (must fail)
- ✗ Create todo with whitespace-only title (must fail)
- ✓ Todo immutability (fields cannot be changed directly)
- ✓ Special characters in title/description
- ✓ Very long title/description (1000+ chars)

#### `repository.py` (Storage Layer)
- ✓ Add todo assigns unique ID
- ✓ Add multiple todos increments IDs correctly
- ✓ Get todo by ID returns correct todo
- ✗ Get todo by non-existent ID returns None
- ✓ Get all todos returns all stored todos
- ✓ Get all from empty repository returns empty list
- ✓ Update todo replaces existing todo
- ✗ Update non-existent todo (verify behavior)
- ✓ Delete todo removes it from storage
- ✗ Delete non-existent todo returns False
- ✓ Exists check for present and absent IDs

#### `service.py` (Business Logic)
- ✓ Create todo with valid title succeeds
- ✗ Create todo with empty title returns error
- ✗ Create todo with whitespace-only title returns error
- ✓ List todos returns all todos
- ✓ Update todo title succeeds
- ✓ Update todo description succeeds
- ✓ Update both title and description succeeds
- ✗ Update with empty title returns error
- ✗ Update non-existent ID returns error
- ✓ Delete todo succeeds
- ✗ Delete non-existent ID returns error
- ✓ Toggle completion incomplete → complete
- ✓ Toggle completion complete → incomplete
- ✗ Toggle non-existent ID returns error

#### `formatters.py` (Output Formatting)
- ✓ Format single todo displays all fields
- ✓ Format todo list with multiple todos
- ✓ Format empty list shows appropriate message
- ✓ Completion status indicator (✓ vs ✗)
- ✓ Success message formatting
- ✓ Error message formatting
- ✓ Very long title/description wrapping (if implemented)

### 6.3 Integration Testing

**Scope**: End-to-end user journeys through full stack

**Test Scenarios** (from Specification):

#### User Story 1: Create and View Todos (P1)
- **Test**: Add todo with title and description, verify in list
- **Test**: Add todo with title only, verify in list
- **Test**: Add multiple todos, verify all appear
- **Test**: Attempt to add todo with empty title, verify error message

#### User Story 2: Mark Complete (P2)
- **Test**: Create todo, mark complete, verify status changes
- **Test**: Mark todo incomplete, verify status changes
- **Test**: Toggle completion preserves title and description
- **Test**: Attempt to toggle non-existent ID, verify error

#### User Story 3: Update Details (P3)
- **Test**: Update todo title, verify change
- **Test**: Update todo description, verify change
- **Test**: Update both fields, verify both change
- **Test**: Attempt to update with empty title, verify error
- **Test**: Attempt to update non-existent ID, verify error

#### User Story 4: Delete Todos (P4)
- **Test**: Delete todo, verify it no longer appears
- **Test**: Delete middle todo from list of 3, verify others remain
- **Test**: Attempt to delete non-existent ID, verify error
- **Test**: Delete last remaining todo, verify empty list message

#### Edge Case Tests
- **Test**: Add 100 todos, verify all accessible
- **Test**: Title with special characters (!@#$%^&*)
- **Test**: Very long title (500 chars)
- **Test**: Very long description (2000 chars)
- **Test**: Rapid create/delete cycles (stress test)

### 6.4 Test Data Management

**Fixtures** (pytest fixtures for common test data):
```python
@pytest.fixture
def empty_repository():
    return TodoRepository()

@pytest.fixture
def repository_with_todos():
    repo = TodoRepository()
    repo.add(Todo(title="Task 1", description="Desc 1", completed=False))
    repo.add(Todo(title="Task 2", description="Desc 2", completed=True))
    return repo

@pytest.fixture
def todo_service(repository):
    return TodoService(repository)
```

### 6.5 Manual Testing Checklist

**Pre-Release Manual Tests**:
- [ ] Launch application successfully
- [ ] Add 5 different todos with various titles/descriptions
- [ ] List todos and verify all 5 appear correctly
- [ ] Mark 2 todos as complete
- [ ] Verify completion status shows correctly in list
- [ ] Update title of one todo
- [ ] Update description of one todo
- [ ] Verify updates reflected in list
- [ ] Delete 2 todos
- [ ] Verify deleted todos no longer appear
- [ ] Delete all remaining todos
- [ ] Verify empty list message displays
- [ ] Attempt to update non-existent ID (e.g., 999)
- [ ] Verify clear error message
- [ ] Attempt to delete non-existent ID
- [ ] Verify clear error message
- [ ] Attempt to create todo with empty title
- [ ] Verify validation error message
- [ ] Test help command (if implemented)
- [ ] Test exit command
- [ ] Re-launch app and verify data is gone (expected: in-memory)

### 6.6 Test Automation

**CI/CD Integration** (future):
- `pytest` runs on every commit
- Code coverage report generated
- Minimum coverage threshold: 90%
- Type checking with `mypy`

**Test Execution**:
```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=todo_cli --cov-report=html

# Run only unit tests
uv run pytest tests/unit/

# Run only integration tests
uv run pytest tests/integration/

# Run with verbose output
uv run pytest -v
```

---

## 7. Validation & Compliance

### 7.1 Constitutional Compliance Checklist

**Section I: Core Principles**
- [ ] Spec-Driven Development workflow followed
- [ ] No manual code written (all AI-generated from approved spec)
- [ ] Complete traceability: Constitution → Spec → Plan → Tasks → Code
- [ ] Test-first approach: tests written before/with implementation
- [ ] No features beyond Phase I scope (evolutionary consistency)

**Section II: Domain Model**
- [ ] Todo model matches constitutional base model exactly
- [ ] Fields: id, title, description, completed (no additions)
- [ ] `id` is immutable once assigned
- [ ] `completed` is strictly boolean
- [ ] No Phase II+ extensions (tags, priorities, timestamps)

**Section III: Technology Governance**
- [ ] Python 3.10+ required (recommend 3.13)
- [ ] Type hints for all public interfaces
- [ ] Modular, single-responsibility design
- [ ] Domain logic separated from infrastructure
- [ ] No global mutable state
- [ ] No hardcoded configuration
- [ ] No circular dependencies

**Section IV: Repository Structure**
- [ ] Code in `/src/todo_cli/`
- [ ] Tests in `/tests/unit/` and `/tests/integration/`
- [ ] Spec in `/specs-history/phase-1-cli/`
- [ ] Plan in `/specs-history/phase-1-cli/plan.md` (this file)
- [ ] ADRs in `/history/adr/` (when created)
- [ ] README.md and CLAUDE.md present

**Section V: Quality Standards**
- [ ] Clear, testable acceptance criteria met
- [ ] Clean, readable, self-documenting code
- [ ] Cyclomatic complexity <10 per function
- [ ] No code duplication (DRY)
- [ ] Error handling for all failure modes
- [ ] No over-engineering or premature optimization

**Section VIII: Workflow Enforcement**
- [ ] Specification approved before planning
- [ ] Plan identifies all ADR-worthy decisions
- [ ] Tasks will be created via `/sp.tasks`
- [ ] Implementation will be via `/sp.implement`
- [ ] PHR will be created documenting session

### 7.2 Specification Compliance

**Functional Requirements** (FR-001 to FR-021):
- [ ] All five CRUD operations implemented
- [ ] Automatic unique ID assignment
- [ ] Human-readable formatted output
- [ ] Update title and/or description
- [ ] Toggle completion status
- [ ] Delete by ID
- [ ] Title validation (non-empty)
- [ ] Error messages for non-existent IDs
- [ ] Input validation and error handling
- [ ] Data integrity maintained
- [ ] In-memory only (no persistence)
- [ ] Command-line interface
- [ ] No raw Python objects in output
- [ ] Confirmation messages
- [ ] Graceful error handling (no crashes)
- [ ] Python 3.10+
- [ ] No persistence mechanisms
- [ ] Clean architecture separation
- [ ] UV-compatible project structure

**Success Criteria** (SC-001 to SC-020):
- [ ] All acceptance scenarios pass
- [ ] Error messages are clear and actionable
- [ ] All AI-generated code (no manual coding)
- [ ] Clear separation of concerns
- [ ] Functions have single responsibility
- [ ] All tests pass
- [ ] Intuitive CLI commands
- [ ] Properly formatted output
- [ ] Responsive performance (<1s per operation)
- [ ] Traceability complete
- [ ] ADRs created for significant decisions
- [ ] PHR created

**Exclusions Enforced**:
- [ ] No file persistence
- [ ] No database
- [ ] No search/filter/sort
- [ ] No tags, priorities, or categories
- [ ] No web UI or API
- [ ] No timestamps
- [ ] No multi-user features

### 7.3 Quality Gates

**Before marking Phase I complete**:

**Code Quality**:
- [ ] All mypy type checks pass (zero errors)
- [ ] All pytest tests pass (100% pass rate)
- [ ] Test coverage >90%
- [ ] No pylint critical errors
- [ ] No dead code or commented-out blocks

**Functional Quality**:
- [ ] All specification acceptance scenarios verified
- [ ] Manual testing checklist complete
- [ ] Edge cases handled gracefully
- [ ] Error messages user-friendly
- [ ] No crashes on invalid input

**Documentation Quality**:
- [ ] README.md complete with setup and usage
- [ ] CLAUDE.md updated with implementation notes
- [ ] All modules have docstrings
- [ ] Complex logic has inline comments
- [ ] ADRs created and linked

**Process Quality**:
- [ ] Specification approved by human architect
- [ ] Plan approved by human architect
- [ ] Tasks created via `/sp.tasks`
- [ ] Code generated via `/sp.implement`
- [ ] PHR created for session
- [ ] All constitutional requirements met

---

## 8. Risk Analysis & Mitigation

### 8.1 Technical Risks

**Risk**: ID collision if counter is not properly managed
- **Likelihood**: Low
- **Impact**: Medium (data integrity issues)
- **Mitigation**: Repository exclusively manages counter; comprehensive unit tests
- **Monitoring**: Test suite verifies ID uniqueness

**Risk**: Memory exhaustion with large todo lists
- **Likelihood**: Low (Phase I scope limited)
- **Impact**: Low (acceptable for Phase I)
- **Mitigation**: Document memory limits; Phase II adds persistence
- **Acceptance**: Reasonable tradeoff for Phase I simplicity

**Risk**: User confusion with REPL interface
- **Likelihood**: Medium
- **Impact**: Medium (usability)
- **Mitigation**: Clear help command; guided prompts; good error messages
- **Testing**: Manual usability testing with checklist

### 8.2 Process Risks

**Risk**: Scope creep (adding Phase II+ features)
- **Likelihood**: Medium
- **Impact**: High (violates constitution)
- **Mitigation**: Strict adherence to specification exclusions; code review
- **Prevention**: Clear acceptance criteria; ADR for any additions

**Risk**: Manual code writing bypassing SDD workflow
- **Likelihood**: Low (constitutional mandate)
- **Impact**: High (process violation)
- **Mitigation**: Code review verification; traceability audit
- **Prevention**: Clear communication of constitutional requirements

**Risk**: Insufficient test coverage
- **Likelihood**: Low (test-first mandate)
- **Impact**: High (quality risk)
- **Mitigation**: Coverage reporting (>90% required); test-first TDD
- **Prevention**: Integration with pytest-cov; automated checks

### 8.3 Quality Risks

**Risk**: Poor error messages (technical jargon)
- **Likelihood**: Medium
- **Impact**: Medium (usability)
- **Mitigation**: Manual testing checklist; error message review
- **Prevention**: Specification explicitly requires user-friendly messages

**Risk**: Output formatting unclear or ugly
- **Likelihood**: Low
- **Impact**: Low (aesthetic only)
- **Mitigation**: Manual visual inspection; iterate on formatting
- **Acceptance**: Example outputs in specification

---

## 9. Dependencies & Assumptions

### 9.1 External Dependencies

**Python Runtime**:
- Python 3.10+ available on target system
- Standard library complete and functional

**UV Package Manager**:
- UV installed and accessible
- Compatible with Python 3.10+

**Development Environment**:
- Terminal with UTF-8 support for proper character display (✓, ✗)
- Modern OS (Linux, macOS, Windows with WSL/PowerShell)

### 9.2 Assumptions

**User Context**:
- User has basic command-line proficiency
- User understands data is ephemeral (lost on exit)
- Single-user, local execution environment

**Technical Context**:
- No concurrency required (single-threaded)
- No network access needed
- No file system access needed (beyond Python module loading)

**Future Evolution**:
- Phase II will add persistence (migration path documented)
- Domain model is stable (base fields immutable)
- CRUD operations remain consistent across phases

---

## 10. Success Metrics

### 10.1 Completion Criteria

Phase I is considered **COMPLETE** and ready for delivery when:

**Functional**:
- [ ] All 5 CRUD operations work correctly
- [ ] All specification acceptance scenarios pass
- [ ] All edge cases handled gracefully
- [ ] Error messages clear and actionable

**Technical**:
- [ ] All tests pass (unit + integration)
- [ ] Test coverage >90%
- [ ] Zero mypy errors
- [ ] Code quality meets constitutional standards

**Process**:
- [ ] Specification approved
- [ ] Plan approved (this document)
- [ ] Tasks created via `/sp.tasks`
- [ ] Code generated via `/sp.implement`
- [ ] ADRs created for all significant decisions
- [ ] PHR created for session
- [ ] Manual testing checklist complete

**Documentation**:
- [ ] README.md complete
- [ ] CLAUDE.md updated
- [ ] Code well-commented
- [ ] ADRs linked and accessible

### 10.2 Quality Metrics

**Code Quality**:
- Cyclomatic complexity: <10 per function (target: <7 average)
- Test coverage: >90% (target: 95%+)
- Type hint coverage: 100% of public interfaces
- Documentation: All public APIs documented

**User Experience**:
- Error message clarity: 100% user-friendly (no stack traces)
- Output formatting: Human-readable (no raw objects)
- Command response time: <1 second for all operations

**Constitutional Compliance**:
- SDD workflow adherence: 100%
- Domain model accuracy: 100% (matches constitution)
- Excluded features: 0 violations
- Traceability: 100% complete

---

## 11. Next Steps

Upon approval of this plan:

### 11.1 ADR Creation

**Required ADRs** (from Section 5):
1. **ADR-001**: CLI Interaction Model (REPL vs argparse)
2. **ADR-002**: Todo ID Strategy (auto-increment vs UUID)
3. **ADR-003**: Error Handling Strategy (Result type vs exceptions)
4. **ADR-004**: In-Memory Storage Structure (dict vs list)

**Process**:
- Human architect reviews proposed decisions
- Approves or requests modifications
- AI creates ADRs via `/sp.adr <decision-title>`
- ADRs stored in `/history/adr/NNNN-<decision-title>.md`

### 11.2 Task Breakdown

**Command**: `/sp.tasks`

**Inputs**:
- This plan document
- Approved specification
- Approved ADRs

**Outputs**:
- Granular task breakdown in `specs-history/phase-1-cli/tasks.md`
- Each task with clear acceptance criteria
- Tasks ordered by implementation phases (1-8)
- Testable tasks with explicit validation

### 11.3 Implementation

**Command**: `/sp.implement`

**Inputs**:
- Tasks from `/sp.tasks`
- Approved plan and specification
- Approved ADRs

**Outputs**:
- Generated Python code in `/src/todo_cli/`
- Generated tests in `/tests/`
- All code AI-generated (no manual coding)

### 11.4 Review & Approval

**Human Architect Responsibilities**:
- Review generated code for constitutional compliance
- Run test suite and verify all pass
- Perform manual testing using checklist
- Approve or request refinements
- Sign off on Phase I completion

### 11.5 PHR Creation

**Automatic** (per constitutional Section VIII.6):
- Prompt History Record created documenting this planning session
- Stored in `/history/prompts/phase-1-cli/`
- Links to specification, plan, and ADRs
- Captures full context for future reference

---

## 12. Document Control

**Version**: 1.0.0
**Status**: Draft (Awaiting Approval)
**Created By**: Claude Code (AI)
**Reviewed By**: [Pending Human Architect]
**Approved By**: [Pending]
**Approval Date**: [Pending]

**Related Documents**:
- Constitution: `.specify/memory/constitution.md` (v1.0.0)
- Specification: `specs-history/phase-1-cli/spec.md` (v1.0.0)
- ADRs: `/history/adr/0001-*.md` to `/history/adr/0004-*.md` (pending creation)
- Tasks: `specs-history/phase-1-cli/tasks.md` (to be created)

**Change History**:
- v1.0.0 (2025-12-07): Initial plan created from approved specification

---

## Appendix A: Technology Comparison Matrix

### CLI Framework Options

| Framework | Pros | Cons | Verdict |
|-----------|------|------|---------|
| **Custom REPL** | Full control, guided prompts, session state | Manual parsing | ✓ RECOMMENDED |
| **argparse** | Stdlib, simple, well-tested | Per-command invocation, less intuitive | ❌ Not Phase I optimal |
| **Click** | Feature-rich, popular | External dependency | ❌ Violates minimal deps |
| **Typer** | Modern, type-hinted | External dependency | ❌ Violates minimal deps |

### ID Generation Options

| Strategy | Pros | Cons | Verdict |
|----------|------|------|---------|
| **Auto-increment int** | Simple, readable, CLI-friendly | Local only, collision in distributed | ✓ RECOMMENDED (Phase I) |
| **UUID4** | Globally unique, distribution-ready | Poor UX (long strings) | ❌ Premature for Phase I |
| **Short ID (nanoid)** | Balance of uniqueness + readability | External dependency | ❌ Over-engineering |

### Error Handling Options

| Strategy | Pros | Cons | Verdict |
|----------|------|------|---------|
| **Result type** | Explicit, type-safe, performant | Unfamiliar to Python devs | ✓ RECOMMENDED |
| **Exceptions** | Pythonic, standard practice | Easy to miss error cases | ❌ Less explicit |
| **Error codes** | Simple | Outdated pattern, poor DX | ❌ Not recommended |

---

## Appendix B: File Structure Reference

```
todo-cli/
├── .specify/
│   ├── memory/
│   │   └── constitution.md
│   └── templates/
├── history/
│   ├── adr/
│   │   ├── 0001-cli-interaction-model.md
│   │   ├── 0002-todo-id-strategy.md
│   │   ├── 0003-error-handling-strategy.md
│   │   └── 0004-storage-data-structure.md
│   └── prompts/
│       └── phase-1-cli/
│           └── 001-planning-session.prompt.md
├── specs-history/
│   └── phase-1-cli/
│       ├── spec.md
│       ├── plan.md              # THIS FILE
│       └── tasks.md             # To be created
├── src/
│   └── todo_cli/
│       ├── __init__.py
│       ├── __main__.py
│       ├── models.py
│       ├── repository.py
│       ├── service.py
│       ├── cli.py
│       └── formatters.py
├── tests/
│   ├── unit/
│   │   ├── test_models.py
│   │   ├── test_repository.py
│   │   ├── test_service.py
│   │   └── test_formatters.py
│   └── integration/
│       └── test_cli_flows.py
├── pyproject.toml
├── README.md
├── CLAUDE.md
└── .gitignore
```

---

**Constitutional Compliance Statement**: This plan fully complies with "The Evolution of Todo" Constitution v1.0.0. It implements the architecture necessary to satisfy the Phase I Specification while adhering to all constitutional principles: Spec-Driven Development, AI as primary developer, mandatory traceability, test-first mandate, and evolutionary consistency.

**ADR Requirement**: This plan identifies 4 architecturally significant decisions requiring ADRs per constitutional Section VIII (three-part significance test). Human approval requested before ADR creation.

---

*End of Technical Implementation Plan*
