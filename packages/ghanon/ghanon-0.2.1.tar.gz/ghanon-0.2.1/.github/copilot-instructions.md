# Ghanon Development Guide

## Project Overview

Ghanon is a strict GitHub Actions workflow linter that validates `.github/workflows/*.yml` or user-provided files against best practices using Pydantic models and custom validation rules. The tool parses YAML workflows, validates them against the GitHub Actions schema, and reports validation errors with precise line numbers.

## Architecture

### Domain Models

- **`ghanon/domain/`**: Pydantic models implementing the [GitHub Actions Workflow Schema](https://json.schemastore.org/github-workflow.json)
  - Models mirror the official schema structure, translating JSON Schema to Pydantic with Python naming conventions
  - **`base.py`**: Base models for all domain classes
    - `StrictModel`: Base with `extra="forbid"` - rejects unknown fields (use by default)
    - `FlexibleModel`: Base with `extra="allow"` - accepts additional properties (for user-defined mappings)
    - `FilterableEventModel`: Base for events supporting branches/tags/paths filters with exclusivity validation
  - **`workflow.py`**: Root workflow model
    - `Workflow`: Top-level workflow definition with `on`, `jobs`, `permissions`, `env`, `defaults`, `concurrency` fields
  - **`jobs.py`**: Job definitions
    - `NormalJob`: Standard job with `runs-on`, `steps`, `strategy`, `environment`, `services`, etc.
    - `ReusableWorkflowCallJob`: Job calling reusable workflows with `uses`, `with`, `secrets`
    - `Job`: Union type `NormalJob | ReusableWorkflowCallJob`
  - **`step.py`**: Step definitions
    - `Step`: Job step with `run` or `uses`, plus `name`, `id`, `if`, `env`, `with`, `continue-on-error`, etc.
  - **`triggers.py`**: Workflow trigger configuration
    - `OnConfiguration`: Complete event trigger map with all 50+ GitHub event types
    - `On`: Union of `OnConfiguration | EventType | list[EventType]` for flexible trigger syntax
  - **`events.py`**: Event-specific configuration models (28 classes)
    - Activity-based events: `BranchProtectionRuleEvent`, `CheckRunEvent`, `CheckSuiteEvent`, `DiscussionEvent`, `DiscussionCommentEvent`, `IssueCommentEvent`, `IssuesEvent`, `LabelEvent`, `MergeGroupEvent`, `MilestoneEvent`, `ProjectEvent`, `ProjectCardEvent`, `ProjectColumnEvent`, `PullRequestReviewEvent`, `PullRequestReviewCommentEvent`, `RegistryPackageEvent`, `ReleaseEvent`, `WorkflowRunEvent`
    - Filterable events: `PullRequestEvent`, `PullRequestTargetEvent`, `PushEvent` (inherit from `FilterableEventModel`)
    - Special events: `ScheduleItem` (cron syntax), `WorkflowDispatchEvent` (manual triggers with inputs), `WorkflowCallEvent` (reusable workflow interface with inputs/outputs/secrets)
  - **`permissions.py`**: GITHUB_TOKEN permissions
    - `PermissionsEvent`: Fine-grained permissions (actions, contents, deployments, issues, pull-requests, etc.)
    - `Permissions`: Union of `PermissionsEvent | PermissionAccess` for workflow/job-level permissions
  - **`matrix.py`**: Build matrix strategy
    - `Matrix`: Build matrix with `include`/`exclude` plus custom dimensions (uses `FlexibleModel`)
    - `Strategy`: Matrix strategy with `matrix`, `fail-fast`, `max-parallel`
  - **`environment.py`**: Deployment environments
    - `Environment`: Environment reference with `name` and optional `url`
  - **`defaults.py`**: Default settings
    - `DefaultsRun`: Default shell and working directory for run steps
    - `Defaults`: Workflow/job-level defaults containing `DefaultsRun`
  - **`concurrency.py`**: Concurrency control
    - `Concurrency`: Concurrency group with `group` and `cancel-in-progress`
  - **`container.py`**: Container configurations
    - `Container`: Docker container config with `image`, `credentials`, `env`, `ports`, `volumes`, `options`
    - `ContainerCredentials`: Registry credentials with `username` and `password`
  - **`runner.py`**: Runner specifications
    - `RunnerGroup`: Runner group selection with `group` and `labels`
    - `RunsOn`: Type alias for runner specifications (string, list, RunnerGroup, or expression)
  - **`enums.py`**: Enumerations (30 enums)
    - `ErrorMessage`: Custom validation error messages for best practice enforcement
    - `EventType`: All 50+ GitHub event type names
    - `PermissionLevel`: `read`, `write`, `none` for GITHUB_TOKEN scopes
    - `PermissionAccess`: `read-all`, `write-all` for bulk permission setting
    - `ShellType`: Shell types (bash, pwsh, python, sh, cmd, powershell)
    - Activity type enums (26 total): `*ActivityType` for each event supporting activity filtering
    - Input type enums: `WorkflowDispatchInputType`, `WorkflowCallInputType` (boolean, choice, environment, number, string)
  - **`types.py`**: Type aliases and common types
    - `ExpressionSyntax`: Pattern for `${{ ... }}` expressions
    - `StringContainingExpression`: Strings containing expressions
    - `JobName`: Valid job identifier pattern
    - `JobNeeds`: Single job or list of job dependencies
    - `Globs`: Glob patterns for branches/tags/paths
    - `EnvMapping`: Environment variable mappings
    - `MatrixIncludeExclude`: Matrix include/exclude configurations

### Application Layer

- **`ghanon/cli.py`**: Click-based CLI that formats errors with line numbers using the line map from `YamlLoader`
- **`ghanon/parser.py`**: `WorkflowParser` orchestrates YAML parsing and Pydantic validation, returns `ParsingResult` with success/errors/line_map
- **`ghanon/yaml.py`**: `YamlLoader` handles YAML parsing with special handling for `on: true` (YAML 1.1 quirk) and builds a line map by traversing YAML nodes
- **`ghanon/formatter.py`**: Colorama-based terminal output formatting
- **`ghanon/logger.py`**: Logging utilities for consistent log messages

### Data Flow

1. CLI reads workflow file and passes it to `WorkflowParser.parse()`
2. `YamlLoader` parses YAML and builds a line map (dotted path → line number)
3. Pydantic validates data against `Workflow` model
4. Custom validators enforce best practices (see `@field_validator` and `@model_validator` in domain models)
5. Errors include location paths (e.g., `jobs.build.steps.0.run`) matched against line map for precise error reporting

## Development Workflow

### Package Management

Uses `uv` for dependency management. Python 3.14+ required.

```bash
# Install dependencies
task install

# Run application
task run -- path/to/workflow.yml
```

### Testing

Tests use `pytest` with `assertpy` for fluent assertions. 100% coverage requirement enforced.

```bash
# Run full test suite (format, lint, test)
task test

# Run only unit tests
task test:unit  # or: uv run pytest tests

# Watch mode for TDD
task test:watch

# Update snapshots (for CLI output tests)
task test:update
```

**Testing Patterns:**
- Use `minimal_workflow` and `minimal_job` fixtures from `conftest.py`
- Parametrize test cases with `@pytest.mark.parametrize`
- Use `assertpy` for assertions: `assert_that(result).has_exit_code(0)`
- Snapshot testing with `.snapshot()` for CLI output (stored in `__snapshots__/`)
- Test fixtures in `tests/fixtures/*.yml` for integration tests

### Acceptance Test-Driven Development with Gherkin

Feature specifications live in `features/ghanon.feature` using Gherkin syntax:

```gherkin
Scenario Outline: Error Cases
  Given a workflow "<workflow>"
  When I parse it
  Then the validation should fail
  And I should see message "<error>"

  Examples:
    | workflow            | error                                   |
    | branch_trigger.yml  | Use the `pull_request` trigger instead  |
    | secrets_inherit.yml | Do not use `secrets: inherit`          |
```

The TDD-Red agent (`.github/agents/tdd_red.agent.md`) uses these feature files to guide test-first development.
The ATDD workflow is following:

1. Write a new Gherkin scenario describing the desired behavior into `features/ghanon.feature`
2. Translate the Gherkin scenarios into a failing Pytest tests in `tests/` directory
3. Implement the minimum code changes to make the tests pass with `task test`
4. Refactor code as needed while keeping tests passing
5. Write the next Gherkin scenario and repeat the process

### Linting & Formatting

Uses Ruff with comprehensive rule set (`select = ["ALL"]`). Specific ignores in `pyproject.toml`:
- Tests: No docstrings, type hints, or `assert` warnings
- `cli.py`: Boolean options allowed (`FBT001`)

```bash
task lint    # Check only
task format  # Fix and format
```

## Project-Specific Conventions

### Pydantic Model Patterns

1. **Use `StrictModel` by default** (extra="forbid") to catch unknown fields
2. **Use `FlexibleModel`** only for user-defined mappings (e.g., environment variables)
3. **Alias fields** with hyphens: `runs_on = Field(alias="runs-on")`
4. **Custom validators** in domain models enforce GitHub Actions best practices:
   ```python
   @field_validator("secrets")
   @classmethod
   def check_secrets_inherit(cls, value):
       if value == "inherit":
           raise ValueError(ErrorMessage.SECRETS_INHERIT)
   ```
5. **Use `ErrorMessage` enum** for reusable validation messages
6. **Model validators** check cross-field constraints (e.g., `FilterableEventModel.check_filter_exclusivity`)

### Line Mapping Strategy

The `YamlLoader.build_line_map()` creates dotted paths matching Pydantic error locations. When formatting errors:
- Try longest matching path first (e.g., `jobs.build.steps.0.run`)
- Fall back to shorter paths if no match (handles Pydantic model class names in error paths)
- See `cli.get_line_info()` for path matching logic

### Testing Domain Models

- Test both valid and invalid configurations
- Use parametrized tests for multiple invalid patterns
- Verify error messages match `ErrorMessage` enum values
- Example: `test_workflow_model.py` validates job ID patterns

### Adding New Validators

Example from `jobs.py` showing how to enforce best practices:

```python
@field_validator("secrets")
@classmethod
def validate_secrets(cls, value):
    """Validate that secrets are explicitly defined rather than inherited.

    Using secrets: inherit violates principle of least privilege.
    """
    if value == "inherit":
        raise ValueError(ErrorMessage.SECRETS_INHERIT)
    return value
```

### Updating the GitHub Actions Schema

The domain models implement the [official GitHub Actions schema](https://json.schemastore.org/github-workflow.json).

To update:

1. **Monitor GitHub Actions changes**: Check [GitHub Actions documentation](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions) and [schema updates](https://github.com/SchemaStore/schemastore/blob/master/src/schemas/json/github-workflow.json)

2. **Identify schema differences**: Compare current models against the JSON Schema
   - New event types → add to `events.py` and `EventType` enum
   - New job properties → update `NormalJob` or `ReusableWorkflowCallJob`
   - New step properties → update `Step` model in `step.py`

3. **Translate JSON Schema to Pydantic**:
   - JSON Schema `type: string` → `str`
   - JSON Schema `type: array` → `list[T]`
   - JSON Schema `oneOf` → `Union` types
   - JSON Schema `pattern` → `Field(pattern="...")`
   - Properties with hyphens → use `alias="property-name"`

4. **Add validation rules**: If new features have best practices, add `@field_validator` or `@model_validator`

5. **Update tests**: Add test cases for new features in `tests/` directory

6. **Update test fixtures**: Add example workflows using new features to `tests/fixtures/`

## Key Files

- `main.py`: Entry point (imports `cli.main()`)
- `Taskfile.yml`: Task runner configuration (preferred over direct commands)
- `pyproject.toml`: Package config, Ruff rules, pytest options
- `tests/fixtures/`: Sample workflow files for validation testing
