"""Common type aliases for GitHub Actions Workflow models."""

from typing import Annotated, Any

from pydantic import Field

__all__ = [
    "Configuration",
    "EnvMapping",
    "EnvVarValue",
    "ExpressionSyntax",
    "Globs",
    "JobName",
    "JobNeeds",
    "MatrixIncludeExclude",
    "StringContainingExpression",
]


ExpressionSyntax = Annotated[str, Field(pattern=r"^\$\{\{(.|\r|\n)*\}\}$")]
"""GitHub Actions expression syntax: ${{ ... }}"""

StringContainingExpression = Annotated[str, Field(pattern=r"^.*\$\{\{(.|\r|\n)*\}\}.*$")]
"""String containing GitHub Actions expression syntax."""

JobName = Annotated[str, Field(pattern=r"^[_a-zA-Z][a-zA-Z0-9_-]*$")]
"""Valid job/input identifier: starts with letter or underscore, contains alphanumeric, dash, or underscore."""

JobNeeds = JobName | Annotated[list[JobName], Field(min_length=1)]
"""
Jobs that must complete successfully before this job will run.

It can be a string or array of strings. If a job fails, all jobs that need it
are skipped unless the jobs use a conditional statement that causes the job to continue.

Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/workflow-syntax-for-github-actions#jobsjob_idneeds
"""

EnvVarValue = str | int | float | bool
"""Valid types for environment variable values."""

EnvMapping = dict[str, EnvVarValue] | StringContainingExpression
"""
Environment variables mapping.

To set custom environment variables, you need to specify the variables in the workflow file.
You can define environment variables for a step, job, or entire workflow using the
jobs.<job_id>.steps[*].env, jobs.<job_id>.env, and env keywords.

Reference: https://docs.github.com/en/actions/learn-github-actions/environment-variables
"""

Globs = Annotated[list[str], Field(min_length=1)]
"""Array of glob patterns with at least one item."""

Configuration = str | int | float | bool | dict[str, Any] | list[Any]
"""Recursive configuration type for matrix values."""

MatrixIncludeExclude = ExpressionSyntax | list[dict[str, Configuration]]
"""Include/exclude entries in a matrix."""
