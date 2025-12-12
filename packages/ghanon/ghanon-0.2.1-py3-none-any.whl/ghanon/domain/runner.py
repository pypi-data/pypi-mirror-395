"""Runner-related models for GitHub Actions Workflows."""

from pydantic import BaseModel

from .types import ExpressionSyntax, StringContainingExpression

__all__ = [
    "RunnerGroup",
    "RunsOn",
]


class RunnerGroup(BaseModel):
    """Runner group configuration for choosing runners in a group."""

    group: str | None = None
    labels: str | list[str] | None = None


RunsOn = str | list[str] | RunnerGroup | StringContainingExpression | ExpressionSyntax
"""
The type of machine to run the job on.

The machine can be either a GitHub-hosted runner or a self-hosted runner.

Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/workflow-syntax-for-github-actions#jobsjob_idruns-on
"""
