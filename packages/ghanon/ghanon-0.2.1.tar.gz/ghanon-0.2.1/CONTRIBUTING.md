# Contributing to Ghanon

Thank you for your interest in contributing to Ghanon! This document provides guidelines and instructions for contributing.

## 🌟 How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the [existing issues](https://github.com/nikoheikkila/ghanon/issues) to avoid duplicates. When creating a bug report, include as many details as possible:

- Use a clear and descriptive title
- Describe the exact steps to reproduce the problem
- Provide specific examples (workflow files, commands, error messages)
- Describe the behavior you observed and what you expected
- Include your environment details (Python version, OS, etc.)

### Suggesting Features

Feature suggestions are welcome! Please:

- Use a clear and descriptive title
- Provide a detailed description of the proposed feature
- Explain why this feature would be useful
- Include examples of how it would work

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** following our coding conventions
3. **Add tests** for any new functionality
4. **Ensure all tests pass** with 100% coverage
5. **Update documentation** as needed
6. **Follow commit message conventions** (see below)
7. **Submit your pull request**

## 🛠️ Development Setup

### Prerequisites

- Python 3.14 or higher
- [Task](https://taskfile.dev/) - Task runner
- [uv](https://github.com/astral-sh/uv) - Python package manager

### Initial Setup

```bash
# Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/ghanon.git
cd ghanon

# Install dependencies
task install

# Verify setup by running tests
task test
```

## 📝 Coding Conventions

### Python Style

Ghanon uses [Ruff](https://docs.astral.sh/ruff/) with a comprehensive rule set (`select = ["ALL"]`). The configuration is in `pyproject.toml`.

```bash
# Check code style
task lint

# Auto-format code
task format
```

### Type Hints

- All functions must have type hints
- Use Python 3.14+ type syntax
- Leverage Pydantic models for validation

### Docstrings

- Use Google-style docstrings
- Document all public modules, classes, and functions
- Include examples for complex functionality

Example:
```python
def validate_workflow(path: str) -> ParsingResult:
    """Validate a GitHub Actions workflow file.
    
    Args:
        path: Path to the workflow YAML file
        
    Returns:
        ParsingResult containing validation status and any errors
        
    Raises:
        FileNotFoundError: If the workflow file doesn't exist
    """
```

## 🧪 Testing

Ghanon maintains **100% test coverage**. All contributions must include tests.

### Running Tests

```bash
# Run full test suite (format, lint, test)
task test

# Run only unit tests
task test:unit

# Watch mode for TDD
task test:watch

# Update snapshot tests
task test:update
```

### Writing Tests

- Use `pytest` with `assertpy` for fluent assertions
- Use fixtures from `conftest.py` (e.g., `minimal_workflow`, `minimal_job`)
- Parametrize test cases with `@pytest.mark.parametrize`
- Use snapshot testing for CLI output validation
- Place test fixtures in `tests/fixtures/`

Example test:
```python
import pytest
from assertpy import assert_that

@pytest.mark.parametrize("invalid_value", ["inherit", "INHERIT"])
def test_secrets_inherit_validation(invalid_value):
    """Test that secrets: inherit is rejected."""
    workflow = {
        "on": "push",
        "jobs": {
            "test": {
                "runs-on": "ubuntu-latest",
                "secrets": invalid_value,
                "steps": [{"run": "echo test"}]
            }
        }
    }
    
    result = WorkflowParser.parse(workflow)
    assert_that(result.is_valid).is_false()
    assert_that(result.errors).contains("Do not use `secrets: inherit`")
```

### Acceptance Test-Driven Development (ATDD)

For new features, follow the ATDD workflow:

1. Write Gherkin scenarios in `features/ghanon.feature`
2. Translate scenarios to failing pytest tests
3. Implement minimum code to pass tests
4. Refactor while keeping tests green
5. Repeat

Example Gherkin scenario:
```gherkin
Scenario: Reject secrets inheritance
  Given a workflow with "secrets: inherit"
  When I parse it
  Then the validation should fail
  And I should see message "Do not use `secrets: inherit`"
```

## 📋 Commit Message Guidelines

Ghanon follows [Conventional Commits](https://www.conventionalcommits.org/) specification.

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, no logic change)
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Maintenance tasks

### Examples

```
feat(validators): add check for deprecated GitHub Actions syntax

Implements validation for deprecated workflow syntax patterns
according to GitHub's latest recommendations.

Closes #123
```

```
fix(parser): handle YAML anchors correctly

Previously, YAML anchors caused parsing failures. This fix
properly resolves anchors during the loading phase.

Fixes #456
```

```
docs(readme): add installation instructions for pipx

Added pipx as a recommended installation method for CLI tools.
```

## 🎯 Adding New Validators

When adding best practice validators:

1. **Define error message** in `ghanon/domain/enums.py`:
   ```python
   class ErrorMessage(str, Enum):
       YOUR_ERROR = "Clear, actionable error message"
   ```

2. **Add validator** to the relevant model:
   ```python
   @field_validator("field_name")
   @classmethod
   def validate_field(cls, value):
       if is_invalid(value):
           raise ValueError(ErrorMessage.YOUR_ERROR)
       return value
   ```

3. **Write tests** in `tests/`:
   - Test valid cases
   - Test invalid cases with expected error messages
   - Use parametrized tests for multiple scenarios

4. **Update documentation** if the validator enforces a new best practice

## 🔄 Pull Request Process

1. **Ensure your PR**:
   - Has a clear title and description
   - References any related issues
   - Includes tests with 100% coverage
   - Passes all CI checks
   - Follows conventional commit format

2. **PR Review**:
   - Maintainers will review your PR
   - Address any feedback
   - Keep your branch up to date with `main`

3. **After Approval**:
   - Maintainers will merge your PR
   - Your contribution will be included in the next release

## 📚 Resources

- [GitHub Actions Workflow Schema](https://json.schemastore.org/github-workflow.json)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Conventional Commits](https://www.conventionalcommits.org/)

## ❓ Questions?

If you have questions about contributing:

- Check existing [issues](https://github.com/nikoheikkila/ghanon/issues)
- Open a new issue with the `question` label
- Be respectful and follow our [Code of Conduct](CODE_OF_CONDUCT.md)

## 🙏 Thank You!

Your contributions help make Ghanon better for everyone. We appreciate your time and effort!
