# The Evolution of Todo - Project Constitution

## Preamble

This Constitution establishes the governing principles, standards, and invariants for **"The Evolution of Todo"** — a multi-phase educational software project demonstrating the evolution of a simple CLI todo application into a cloud-native, AI-powered, event-driven distributed system.

**Core Purpose**: To teach students modern software engineering through Spec-Driven Development (SDD) and AI-assisted implementation, where humans act as architects and AI (Claude Code) performs all coding work.

**Scope of Authority**: This Constitution applies to ALL phases, ALL features, ALL specifications, ALL plans, ALL tasks, and ALL implementations across the entire project lifecycle.

**Supremacy Clause**: If any specification, plan, task, or implementation conflicts with this Constitution, **THE CONSTITUTION WINS**. The conflicting artifact must be rewritten or regenerated.

---

## I. Core Principles (NON-NEGOTIABLE)

### 1. Spec-Driven Development Only

**Mandate**: All feature development must follow the strict SDD workflow:

```
/sp.constitution → /sp.specify → /sp.plan → /sp.tasks → /sp.implement
```

**Rules**:
- No feature may be implemented without a complete, approved specification
- Humans may NOT manually write feature code
- If generated code is incorrect, refine the SPEC, not the code
- All specifications are versioned and stored in `/specs-history/`
- Every spec must include clear acceptance criteria and test scenarios

**Violations**: Any manually-written feature code is considered non-compliant and must be regenerated through the SDD workflow.

### 2. AI as Primary Developer

**Division of Responsibilities**:

**Humans Must**:
- Write and refine feature specifications
- Review architectural decisions
- Run and validate tests
- Approve changes before merge
- Make final decisions on tradeoffs

**AI (Claude Code) Must**:
- Generate architecture plans from specs
- Write all implementation code
- Create comprehensive test suites
- Perform refactoring and bug fixes
- Document all generated artifacts

**Accountability**: All AI-generated code is traceable to the human-written specification that authorized it.

### 3. Mandatory Traceability

**Requirement**: Every feature must maintain a complete audit trail:

1. **Architecture Decision Record (ADR)** — Why this approach?
2. **Specification** — What are we building?
3. **Architecture Plan** — How will we build it?
4. **Task Breakdown** — What are the specific implementation steps?
5. **Implementation** — The generated code
6. **Test Suite** — Verification of correctness

**Linkage**: All artifacts must cross-reference each other. ADRs link to specs, specs link to plans, plans link to tasks, tasks link to implementations.

**Storage**:
- ADRs → `/history/adr/`
- Specs → `/specs-history/`
- Plans → `/architecture/`
- Code → `/src/`
- Tests → `/tests/`

### 4. Test-First Mandate

**Requirement**: Testing is NOT optional.

**Rules**:
- Tests must be generated before or immediately after implementation
- Every feature must have integration tests covering user journeys
- Unit tests required for complex business logic
- All tests must pass before marking a feature complete
- Test coverage must be maintained across refactoring

**Test Types by Phase**:
- **Phase I (CLI)**: Integration tests for command flows, unit tests for core logic
- **Phase II (Web)**: API integration tests, UI component tests, E2E user journeys
- **Phase III+ (Distributed)**: Contract tests, integration tests, chaos testing

### 5. Evolutionary Consistency

**Principle**: Later phases extend but never break earlier phases.

**Rules**:
- Phase II must support all Phase I functionality
- Phase III must preserve Phase I and II semantics
- Breaking changes require explicit ADR and migration plan
- Domain model extensions are additive only

**Verification**: Regression test suites from earlier phases must continue to pass.

---

## II. Domain Model Governance

### Global Todo Domain Rules

**Base Model (Phase I - Immutable)**:
```
Todo:
  - id: unique identifier
  - title: short description
  - description: detailed text (optional)
  - completed: boolean status
```

**Intermediate Extensions (Phase II - Additive)**:
```
  - priority: enum (low, medium, high)
  - tags: list of strings
  - category: single classification
  - created_at: timestamp
  - updated_at: timestamp
```

**Advanced Extensions (Phase III+ - Additive)**:
```
  - due_date: optional deadline
  - recurrence: optional repeat pattern
  - reminders: list of reminder configs
  - assigned_to: user/agent reference
  - parent_id: for subtasks
```

**Invariants**:
- `id` is immutable once assigned
- `completed` is boolean; no intermediate states
- State transitions are explicit and logged
- All timestamps use ISO 8601 format
- All field additions must maintain backward compatibility

**Semantic Consistency**:
- "Creating a todo" has the same meaning in CLI, Web UI, API, and AI agent
- "Marking complete" follows identical rules across all interfaces
- Search/filter/sort behavior is consistent across all phases

---

## III. Technology Governance

### Python Backend Standards

**Requirements**:
- Python 3.10+ required
- Type hints for all public interfaces
- Modular, single-responsibility design
- Separation of concerns: domain logic ≠ infrastructure
- No global mutable state
- Dependency injection for testability

**Forbidden**:
- Mixing business logic with I/O operations
- Hardcoded configuration values
- Circular dependencies between modules
- Undocumented magic numbers or strings

### Next.js Frontend Standards (Phase II+)

**Requirements**:
- Clear separation: server components vs. client components
- Type-safe API contracts (TypeScript interfaces)
- Responsive design (mobile-first)
- Accessibility (WCAG 2.1 AA minimum)
- Error boundaries for graceful degradation

**Forbidden**:
- Direct database access from frontend
- Hardcoded API URLs
- Inline styles (use CSS modules or Tailwind)
- Unvalidated user input

### AI Agent Standards (Phase III+)

**Requirements**:
- Natural language inputs must map to existing Todo operations
- Graceful handling of ambiguous commands
- Confirmation prompts for destructive actions
- All agent logic must be spec-driven
- Comprehensive intent recognition testing

**Forbidden**:
- Agents creating undocumented side effects
- Bypassing validation rules
- Silent failures on misunderstood commands

### Cloud & Kubernetes Standards (Phase IV+)

**Requirements**:
- 12-Factor App principles strictly enforced
- All configuration via environment variables
- Secrets stored in external secret managers (never in code/repos)
- Docker images must be reproducible and minimal
- Kubernetes manifests must be declarative (Helm/Kustomize)
- Health checks (liveness, readiness) required
- Resource limits defined for all containers
- Horizontal Pod Autoscaling configured where appropriate

**Forbidden**:
- Hard-coded credentials or API keys
- Imperative kubectl commands in production
- Mutable infrastructure
- Unversioned Docker images (no `latest` tag)

---

## IV. Repository Structure (MANDATORY)

**Standard Layout** (all phases must conform):

```
/
├── .specify/
│   ├── memory/
│   │   └── constitution.md          # THIS FILE
│   ├── templates/                    # SDD templates
│   └── scripts/                      # Automation scripts
├── history/
│   ├── adr/                          # Architecture Decision Records
│   │   └── NNNN-decision-title.md
│   └── prompts/                      # Prompt History Records
│       ├── constitution/
│       ├── <feature-name>/
│       └── general/
├── specs-history/
│   └── <feature-name>/
│       ├── spec.md                   # Feature specification
│       ├── plan.md                   # Architecture plan
│       └── tasks.md                  # Task breakdown
├── src/
│   └── <phase-name>/                 # e.g., phase-1-cli, phase-2-web
│       ├── core/                     # Domain logic
│       ├── interfaces/               # CLI/API/UI
│       └── infrastructure/           # DB, file I/O, external services
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── infra/
│   ├── docker/
│   ├── kubernetes/
│   └── terraform/                    # Infrastructure as Code
├── docs/
│   └── <phase-name>/
│       └── README.md                 # Setup and usage per phase
├── README.md                         # Project overview
└── CLAUDE.md                         # AI agent instructions
```

**Enforcement**: No alternative structures permitted. All new phases must follow this layout.

---

## V. Quality Standards (Global)

### Specification Quality

**Required Elements**:
- Clear problem statement
- User stories with acceptance criteria
- Edge cases and error scenarios explicitly listed
- Performance requirements (if applicable)
- Security considerations
- Success metrics

**Forbidden**:
- Ambiguous requirements ("should be fast", "user-friendly")
- Implementation details in specs (specs define WHAT, not HOW)
- Untestable acceptance criteria

### Code Quality

**Requirements**:
- Clean, readable, self-documenting code
- Consistent naming conventions
- Minimal complexity (cyclomatic complexity < 10 per function)
- No code duplication (DRY principle)
- Error handling for all failure modes
- Logging for debugging and audit trails

**Forbidden**:
- Over-engineering or premature optimization
- God objects or god functions
- Magic numbers or strings
- Dead code or commented-out code blocks

### Documentation Quality

**Required per Phase**:
- `README.md`: Setup instructions, dependencies, how to run
- `CLAUDE.md`: AI agent operational instructions
- Inline code comments for complex logic only
- API documentation (OpenAPI/Swagger for REST APIs)
- Database schema documentation

**Standards**:
- Documentation is versioned with code
- Outdated documentation is worse than no documentation (keep it current)
- Examples and usage patterns included

---

## VI. Security & Compliance

### Universal Security Rules

**Requirements**:
- Input validation on all external data
- SQL injection prevention (use parameterized queries)
- XSS prevention (escape output, CSP headers)
- CSRF protection for state-changing operations
- Authentication and authorization for Phase II+
- Secrets management (environment variables, secret managers)
- HTTPS/TLS for all production traffic
- Regular dependency vulnerability scanning

**Forbidden**:
- Storing passwords in plaintext
- Trusting client-side validation alone
- Exposing sensitive data in logs or error messages
- Using deprecated cryptographic algorithms

### Data Privacy

**Requirements**:
- Minimal data collection (only what's needed)
- Clear data retention policies
- Secure data deletion mechanisms
- Privacy-by-design principles

---

## VII. Phase Evolution Rules

### Phase Transition Requirements

**Before Starting a New Phase**:
1. Previous phase must be complete and tested
2. ADR documenting the phase transition must exist
3. Migration plan documented (if data/schema changes)
4. Backward compatibility strategy defined
5. Regression test suite from prior phases passing

**Phase Independence**:
- Each phase is independently deployable
- Phase II does not require Phase I to be running (unless explicitly designed as extension)
- Clear interface boundaries between phases

### Supported Phases (Evolution Path)

**Phase I**: In-Memory Python CLI
- Core domain model
- CRUD operations
- File-based persistence (optional)
- CLI interface

**Phase II**: Web Application
- REST API (FastAPI)
- Next.js frontend
- Database persistence (PostgreSQL/SQLite)
- Authentication and authorization

**Phase III**: AI-Powered
- Natural language interface
- AI agent integration
- Smart suggestions and automation
- Voice/chat interfaces

**Phase IV**: Cloud-Native Distributed
- Microservices architecture
- Event-driven design (Kafka/RabbitMQ)
- Kubernetes deployment
- Scalability and fault tolerance

**Phase V**: Enterprise Features
- Multi-tenancy
- Advanced analytics
- Integrations (Slack, email, calendars)
- Audit logging and compliance

---

## VIII. Workflow Enforcement

### SDD Workflow (Strictly Required)

**Step 1: Constitution** (`/sp.constitution`)
- Establish or verify governing principles
- Run ONCE per project or on major pivots

**Step 2: Specify** (`/sp.specify`)
- Write clear, testable feature specification
- Human-authored, AI-assisted refinement
- Stored in `/specs-history/<feature-name>/spec.md`

**Step 3: Plan** (`/sp.plan`)
- AI generates architecture plan from spec
- Identifies significant decisions requiring ADRs
- Stored in `/specs-history/<feature-name>/plan.md`

**Step 4: Tasks** (`/sp.tasks`)
- AI breaks plan into granular, testable tasks
- Each task has clear acceptance criteria
- Stored in `/specs-history/<feature-name>/tasks.md`

**Step 5: Implement** (`/sp.implement`)
- AI generates code from tasks
- AI writes tests
- Human reviews and approves

**Step 6: Record** (Automatic)
- Prompt History Record (PHR) created for session
- ADRs created for significant decisions (on human approval)

**Violations**: Skipping steps or working out-of-order invalidates the work.

### ADR Creation Rules

**When to Create ADRs** (Three-Part Test):
1. **Impact**: Does this have long-term consequences? (framework choice, data model, API design, security approach, platform selection)
2. **Alternatives**: Were multiple viable options considered with tradeoffs?
3. **Scope**: Is this cross-cutting or architecturally significant?

**If ALL THREE = YES**: Suggest ADR creation

**Format**: "📋 Architectural decision detected: [brief]. Document reasoning and tradeoffs? Run `/sp.adr [decision-title]`"

**Process**:
- Wait for human consent
- Never auto-create ADRs
- Group related decisions (e.g., "authentication stack") into one ADR when appropriate
- Store in `/history/adr/NNNN-decision-title.md`

---

## IX. Human-AI Collaboration Contract

### Human as Architect

**Humans are responsible for**:
- Strategic direction
- Requirement gathering
- Specification authoring
- Architecture review and approval
- Final decision-making on tradeoffs
- Quality assurance and acceptance testing

**Humans must NOT**:
- Write feature implementation code
- Skip the SDD workflow
- Override the Constitution without amendment
- Deploy untested or unreviewed code

### AI as Developer

**AI is responsible for**:
- Code generation from approved specs
- Test suite creation
- Refactoring and optimization
- Documentation generation
- Bug fixing (when spec is clarified)

**AI must NOT**:
- Make architectural decisions without human approval
- Proceed with ambiguous requirements (must ask for clarification)
- Skip testing or quality checks
- Auto-approve its own work

### Escalation Protocol

**When AI encounters**:
- Ambiguous requirements → Ask 2-3 targeted clarifying questions
- Conflicting constraints → Present options with tradeoffs, request decision
- Unforeseen dependencies → Surface them, ask for prioritization
- Technical blockers → Document the issue, suggest alternatives

**Human Response Time**: AI should wait for human input rather than making assumptions.

---

## X. Academic & Professional Integrity

### Honesty Requirements

**Commitments**:
- All code originates from AI, guided by human-authored specs
- No copy-paste from external sources without attribution
- No plagiarism of specifications or designs
- All work is reproducible by another developer or AI agent

**Attribution**:
- AI-generated code clearly marked (e.g., commit messages, code comments)
- Third-party libraries and frameworks documented
- Inspiration or reference materials cited

**Educational Value**:
- Students learn architecture and specification skills
- Students understand AI capabilities and limitations
- Students gain experience in human-AI collaboration
- Students develop systems thinking and design judgment

---

## XI. Versioning & Change Management

### Constitution Amendments

**Process**:
1. Propose amendment with justification
2. Document impact on existing phases
3. Create ADR for the constitutional change
4. Require explicit approval
5. Update version number
6. Communicate to all project stakeholders

**Versioning**: MAJOR.MINOR.PATCH
- MAJOR: Fundamental principle changes, breaking compatibility
- MINOR: New principles or clarifications
- PATCH: Typo fixes, formatting improvements

### Specification Versioning

**Rules**:
- All specs are immutable once approved
- Changes require new version in `/specs-history/`
- Version format: `spec-v2.md`, `spec-v3.md`
- Link to superseded versions for audit trail

---

## XII. Governance & Enforcement

### Constitution Supremacy

**Conflict Resolution Order**:
1. **Constitution** (this document) — HIGHEST AUTHORITY
2. Architecture Decision Records (ADRs)
3. Feature Specifications
4. Architecture Plans
5. Task Breakdowns
6. Implementation Code — LOWEST AUTHORITY

**Rule**: If any lower-level artifact conflicts with a higher-level one, the **higher-level artifact wins**. The conflicting item must be rewritten.

### Compliance Verification

**Required Checks** (before merging):
- Spec exists and is approved ✓
- Plan exists and links to spec ✓
- Tasks exist and link to plan ✓
- ADRs exist for significant decisions ✓
- Tests pass ✓
- Code review completed ✓
- PHR created ✓
- No Constitution violations ✓

**Enforcement Mechanisms**:
- Pre-commit hooks validate structure
- CI/CD pipelines verify tests pass
- Code review checklist includes Constitution compliance
- AI agents refuse to proceed with non-compliant requests

### Review & Audit

**Regular Reviews**:
- Monthly audit of PHRs and ADRs for completeness
- Quarterly review of Constitution effectiveness
- Annual assessment of phase evolution progress

**Metrics**:
- Spec compliance rate
- Test coverage percentage
- ADR creation for significant decisions
- Time from spec approval to implementation

---

## XIII. Final Authority

This Constitution represents the governing law of **The Evolution of Todo** project.

**Ratification**: This Constitution is in effect immediately upon creation.

**Amendment Authority**: Amendments require documented justification, ADR, and explicit approval.

**Interpretation**: In case of ambiguity, the spirit of Spec-Driven Development and human-AI collaboration governs.

**Non-Compliance**: Work that violates this Constitution must be rejected and regenerated according to SDD principles.

---

**Version**: 1.0.0
**Ratified**: 2025-12-07
**Last Amended**: 2025-12-07
**Status**: Active and Binding

---

*"Spec first, code second. Human architects, AI builds. Evolution through discipline."*
