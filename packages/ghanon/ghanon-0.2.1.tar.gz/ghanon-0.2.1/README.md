# Ghanon

**Ghanon(dorf)** - A strict GitHub Actions workflow linter that validates your workflows against best practices.

[![PyPI version](https://img.shields.io/pypi/v/ghanon.svg)](https://pypi.org/project/ghanon/)
[![Python Version](https://img.shields.io/pypi/pyversions/ghanon.svg)](https://pypi.org/project/ghanon/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Test Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)](https://github.com/nikoheikkila/ghanon)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

## 🎯 What is Ghanon?

Ghanon is a powerful linter for GitHub Actions workflows that goes beyond basic YAML validation. It validates your `.github/workflows/*.yml` files against the official GitHub Actions schema using Pydantic models and enforces best practices with custom validation rules.

### Key Features

- **📋 Complete Schema Validation**: Validates against the full [GitHub Actions Workflow Schema](https://json.schemastore.org/github-workflow.json)
- **🎯 Precise Error Reporting**: Shows exact line numbers where validation errors occur
- **✨ Best Practices Enforcement**: Custom validators that catch common anti-patterns and security issues
- **🔒 Security-First**: Enforces principle of least privilege for secrets and permissions
- **🚀 CI/CD Ready**: Easy to integrate into your continuous integration pipelines
- **💯 Type-Safe**: Built with Pydantic for robust validation

### Best Practices Enforced

- ❌ Discourages `secrets: inherit` (principle of least privilege)
- 🔍 Validates job IDs, step configurations, and runner specifications
- 🛡️ Checks permissions, concurrency settings, and environment configurations

## 📦 Installation

Ghanon requires Python 3.14 or higher.

### Using pip

```bash
pip install ghanon
```

### Using pipx (recommended for CLI tools)

```bash
pipx install ghanon
```

### Using uv

```bash
uv tool install ghanon
```

## 🚀 Usage

### Command Line

Validate a single workflow file:

```bash
ghanon path/to/workflow.yml
```

Validate all workflows in your repository:

```bash
ghanon .github/workflows/*.yml
```

### In CI/CD Pipelines

Add Ghanon to your GitHub Actions workflow:

```yaml
name: Validate Workflows

on:
  pull_request:
    paths:
      - '.github/workflows/**'
  push:
    branches:
      - main

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.14'
      
      - name: Install Ghanon
        run: pip install ghanon
      
      - name: Validate workflows
        run: ghanon .github/workflows/*.yml
```

## 📖 Example Output

When Ghanon finds issues in your workflow:

```
❌ Validation failed for workflow.yml

Error at line 15 (jobs.build.secrets):
  Do not use `secrets: inherit`. Define secrets explicitly for principle of least privilege.
```

## 🛠️ Development

### Prerequisites

- Python 3.14+
- [Task](https://taskfile.dev/) (task runner)
- [uv](https://github.com/astral-sh/uv) (package manager)

### Setup

```bash
# Clone the repository
git clone https://github.com/nikoheikkila/ghanon.git
cd ghanon

# Install dependencies
task install

# Run the linter
uv tool install .
ghanon path/to/workflow.yml
```

### Testing

Ghanon maintains 100% test coverage:

```bash
# Run full test suite (format, lint, test)
task test

# Run only unit tests
task test:unit

# Watch mode for TDD
task test:watch
```

### Code Quality

```bash
# Lint code
task lint

# Format code
task format
```

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) and [Code of Conduct](CODE_OF_CONDUCT.md) before submitting pull requests.

### Quick Start for Contributors

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes following our conventions
4. Ensure all tests pass (`task test`)
5. Commit using [Conventional Commits](https://www.conventionalcommits.org/)
6. Push to your fork and submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Pydantic](https://docs.pydantic.dev/) for robust validation
- Schema based on [SchemaStore's GitHub Workflow Schema](https://json.schemastore.org/github-workflow.json)
- Inspired by the need for better GitHub Actions workflow validation

## 📞 Support

If you encounter any issues or have questions:

- 🐛 [Report a bug](https://github.com/nikoheikkila/ghanon/issues/new?template=bug_report.md)
- 💡 [Request a feature](https://github.com/nikoheikkila/ghanon/issues/new?template=feature_request.md)
- 💬 [Ask a question](https://github.com/nikoheikkila/ghanon/issues)

---

Made with ❤️ by [Niko Heikkilä](https://github.com/nikoheikkila)
