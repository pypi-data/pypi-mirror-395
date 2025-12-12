"""Shared fixtures for GitHub Actions Workflow tests."""

import pytest


@pytest.fixture
def minimal_job() -> dict[str, list[dict[str, str]] | str]:
    """Minimal valid job configuration."""
    return {"runs-on": "ubuntu-latest", "steps": [{"run": "echo hello"}]}


@pytest.fixture
def minimal_workflow(minimal_job):
    """Minimal valid workflow."""
    return {"on": "push", "jobs": {"build": minimal_job}}
