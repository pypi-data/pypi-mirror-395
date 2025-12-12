"""Concurrency configuration for GitHub Actions Workflows."""

from __future__ import annotations

from typing import Annotated

from pydantic import Field

from .base import StrictModel

__all__ = ["Concurrency"]


ExpressionSyntax = Annotated[str, Field(pattern=r"^\$\{\{(.|\r|\n)*\}\}$")]
"""GitHub Actions expression syntax: ${{ ... }}"""


class Concurrency(StrictModel):
    """Concurrency configuration.

    Concurrency ensures that only a single job or workflow using the same
    concurrency group will run at a time.

    Reference: https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#example-using-concurrency-to-cancel-any-in-progress-job-or-run-1
    """

    group: str = Field(
        ...,
        description=(
            "When a concurrent job or workflow is queued, if another job or workflow "
            "using the same concurrency group in the repository is in progress, the "
            "queued job or workflow will be pending. Any previously pending job or "
            "workflow in the concurrency group will be canceled."
        ),
    )
    cancel_in_progress: bool | ExpressionSyntax | None = Field(
        default=None,
        alias="cancel-in-progress",
        description=(
            "To cancel any currently running job or workflow in the same concurrency group, "
            "specify cancel-in-progress: true."
        ),
    )
