"""Event configuration models for GitHub Actions Workflows.

Reference: https://docs.github.com/en/actions/learn-github-actions/events-that-trigger-workflows
"""

from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel, Field, model_validator

from .base import FilterableEventModel, FlexibleModel, StrictModel
from .enums import (
    BranchProtectionRuleActivityType,
    CheckRunActivityType,
    CheckSuiteActivityType,
    DiscussionActivityType,
    DiscussionCommentActivityType,
    IssueCommentActivityType,
    IssuesActivityType,
    LabelActivityType,
    MergeGroupActivityType,
    MilestoneActivityType,
    ProjectActivityType,
    ProjectCardActivityType,
    ProjectColumnActivityType,
    PullRequestActivityType,
    PullRequestReviewActivityType,
    PullRequestReviewCommentActivityType,
    PullRequestTargetActivityType,
    RegistryPackageActivityType,
    ReleaseActivityType,
    WorkflowCallInputType,
    WorkflowDispatchInputType,
    WorkflowRunActivityType,
)
from .types import Globs

__all__ = [
    "BranchProtectionRuleEvent",
    "CheckRunEvent",
    "CheckSuiteEvent",
    "DiscussionCommentEvent",
    "DiscussionEvent",
    "IssueCommentEvent",
    "IssuesEvent",
    "LabelEvent",
    "MergeGroupEvent",
    "MilestoneEvent",
    "ProjectCardEvent",
    "ProjectColumnEvent",
    "ProjectEvent",
    "PullRequestEvent",
    "PullRequestReviewCommentEvent",
    "PullRequestReviewEvent",
    "PullRequestTargetEvent",
    "PushEvent",
    "RegistryPackageEvent",
    "ReleaseEvent",
    "ScheduleItem",
    "WorkflowCallEvent",
    "WorkflowCallInput",
    "WorkflowCallOutput",
    "WorkflowCallSecret",
    "WorkflowDispatchEvent",
    "WorkflowDispatchInput",
    "WorkflowRunEvent",
]


class BranchProtectionRuleEvent(FlexibleModel):
    """Branch protection rule event configuration.

    Runs your workflow anytime the branch_protection_rule event occurs.

    Reference: https://docs.github.com/en/actions/learn-github-actions/events-that-trigger-workflows#branch_protection_rule
    """

    types: list[BranchProtectionRuleActivityType] | BranchProtectionRuleActivityType | None = None


class CheckRunEvent(FlexibleModel):
    """Check run event configuration.

    Runs your workflow anytime the check_run event occurs.

    Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/events-that-trigger-workflows#check-run-event-check_run
    """

    types: list[CheckRunActivityType] | CheckRunActivityType | None = None


class CheckSuiteEvent(FlexibleModel):
    """Check suite event configuration.

    Runs your workflow anytime the check_suite event occurs.

    Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/events-that-trigger-workflows#check-suite-event-check_suite
    """

    types: list[CheckSuiteActivityType] | CheckSuiteActivityType | None = None


class DiscussionEvent(FlexibleModel):
    """Discussion event configuration.

    Runs your workflow anytime the discussion event occurs.

    Reference: https://docs.github.com/en/actions/reference/events-that-trigger-workflows#discussion
    """

    types: list[DiscussionActivityType] | DiscussionActivityType | None = None


class DiscussionCommentEvent(FlexibleModel):
    """Discussion comment event configuration.

    Reference: https://docs.github.com/en/actions/reference/events-that-trigger-workflows#discussion_comment
    """

    types: list[DiscussionCommentActivityType] | DiscussionCommentActivityType | None = None


class IssueCommentEvent(FlexibleModel):
    """Issue comment event configuration.

    Runs your workflow anytime the issue_comment event occurs.

    Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/events-that-trigger-workflows#issue-comment-event-issue_comment
    """

    types: list[IssueCommentActivityType] | IssueCommentActivityType | None = None


class IssuesEvent(FlexibleModel):
    """Issues event configuration.

    Runs your workflow anytime the issues event occurs.

    Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/events-that-trigger-workflows#issues-event-issues
    """

    types: list[IssuesActivityType] | IssuesActivityType | None = None


class LabelEvent(FlexibleModel):
    """Label event configuration.

    Runs your workflow anytime the label event occurs.

    Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/events-that-trigger-workflows#label-event-label
    """

    types: list[LabelActivityType] | LabelActivityType | None = None


class MergeGroupEvent(FlexibleModel):
    """Merge group event configuration.

    Runs your workflow when a pull request is added to a merge queue.

    Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/events-that-trigger-workflows#merge_group
    """

    types: list[MergeGroupActivityType] | MergeGroupActivityType | None = None


class MilestoneEvent(FlexibleModel):
    """Milestone event configuration.

    Runs your workflow anytime the milestone event occurs.

    Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/events-that-trigger-workflows#milestone-event-milestone
    """

    types: list[MilestoneActivityType] | MilestoneActivityType | None = None


class ProjectEvent(FlexibleModel):
    """Project event configuration.

    Runs your workflow anytime the project event occurs.

    Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/events-that-trigger-workflows#project-event-project
    """

    types: list[ProjectActivityType] | ProjectActivityType | None = None


class ProjectCardEvent(FlexibleModel):
    """Project card event configuration.

    Runs your workflow anytime the project_card event occurs.

    Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/events-that-trigger-workflows#project-card-event-project_card
    """

    types: list[ProjectCardActivityType] | ProjectCardActivityType | None = None


class ProjectColumnEvent(FlexibleModel):
    """Project column event configuration.

    Runs your workflow anytime the project_column event occurs.

    Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/events-that-trigger-workflows#project-column-event-project_column
    """

    types: list[ProjectColumnActivityType] | ProjectColumnActivityType | None = None


class PullRequestEvent(FilterableEventModel):
    """Pull request event configuration.

    Runs your workflow anytime the pull_request event occurs.

    Note: Workflows do not run on private base repositories when you open a
    pull request from a forked repository.

    Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/events-that-trigger-workflows#pull-request-event-pull_request
    """

    types: list[PullRequestActivityType] | PullRequestActivityType | None = None


class PullRequestTargetEvent(FilterableEventModel):
    """Pull request target event configuration.

    This event is similar to pull_request, except that it runs in the context
    of the base repository of the pull request, rather than in the merge commit.

    Reference: https://docs.github.com/en/actions/reference/events-that-trigger-workflows#pull_request_target
    """

    types: list[PullRequestTargetActivityType] | PullRequestTargetActivityType | None = None


class PullRequestReviewEvent(FlexibleModel):
    """Pull request review event configuration.

    Runs your workflow anytime the pull_request_review event occurs.

    Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/events-that-trigger-workflows#pull-request-review-event-pull_request_review
    """

    types: list[PullRequestReviewActivityType] | PullRequestReviewActivityType | None = None


class PullRequestReviewCommentEvent(FlexibleModel):
    """Pull request review comment event configuration.

    Runs your workflow anytime a comment on a pull request's unified diff is modified.

    Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/events-that-trigger-workflows#pull-request-review-comment-event-pull_request_review_comment
    """

    types: list[PullRequestReviewCommentActivityType] | PullRequestReviewCommentActivityType | None = None


class PushEvent(FilterableEventModel):
    """Push event configuration.

    Runs your workflow when someone pushes to a repository branch.

    Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/events-that-trigger-workflows#push-event-push
    """


class RegistryPackageEvent(FlexibleModel):
    """Registry package event configuration.

    Runs your workflow anytime a package is published or updated.

    Reference: https://help.github.com/en/actions/reference/events-that-trigger-workflows#registry-package-event-registry_package
    """

    types: list[RegistryPackageActivityType] | RegistryPackageActivityType | None = None


class ReleaseEvent(FlexibleModel):
    """Release event configuration.

    Runs your workflow anytime the release event occurs.

    Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/events-that-trigger-workflows#release-event-release
    """

    types: list[ReleaseActivityType] | ReleaseActivityType | None = None


class ScheduleItem(StrictModel):
    """A single schedule entry with cron syntax."""

    cron: str = Field(
        ...,
        description="POSIX cron syntax for scheduling. The shortest interval is once every 5 minutes.",
    )


class WorkflowDispatchInput(StrictModel):
    """Input parameter for workflow_dispatch event.

    Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/metadata-syntax-for-github-actions#inputsinput_id
    """

    description: str = Field(
        ...,
        description="A string description of the input parameter.",
    )
    deprecation_message: str | None = Field(
        default=None,
        alias="deprecationMessage",
        description="A string shown to users using the deprecated input.",
    )
    required: bool | None = Field(
        default=None,
        description="A boolean to indicate whether the action requires the input parameter.",
    )
    default: str | bool | int | float | None = Field(
        default=None,
        description="The default value is used when an input parameter isn't specified in a workflow file.",
    )
    type: WorkflowDispatchInputType | None = Field(
        default=None,
        description="A string representing the type of the input.",
    )
    options: Annotated[list[str], Field(min_length=1)] | None = Field(
        default=None,
        description="The options of the dropdown list, if the type is a choice.",
    )

    @model_validator(mode="after")
    def validate_type_constraints(self) -> WorkflowDispatchInput:
        """Validate that options are provided when type is choice."""
        if self.type == WorkflowDispatchInputType.CHOICE and self.options is None:
            msg = "'options' is required when type is 'choice'"
            raise ValueError(msg)
        return self


class WorkflowDispatchEvent(StrictModel):
    """Workflow dispatch event configuration.

    You can now create workflows that are manually triggered with the new
    workflow_dispatch event. You will then see a 'Run workflow' button on
    the Actions tab, enabling you to easily trigger a run.

    Reference: https://github.blog/changelog/2020-07-06-github-actions-manual-triggers-with-workflow_dispatch/
    """

    inputs: dict[str, WorkflowDispatchInput] | None = Field(
        default=None,
        description=(
            "Input parameters allow you to specify data that the action expects to use during runtime. "
            "GitHub stores input parameters as environment variables. Input ids with uppercase letters "
            "are converted to lowercase during runtime. We recommend using lowercase input ids."
        ),
    )


class WorkflowCallInput(StrictModel):
    """Input parameter for workflow_call event."""

    description: str | None = Field(
        default=None,
        description="A string description of the input parameter.",
    )
    required: bool | None = Field(
        default=None,
        description="A boolean to indicate whether the action requires the input parameter.",
    )
    type: WorkflowCallInputType = Field(
        ...,
        description="The data type of the input. This must be one of: boolean, number, or string.",
    )
    default: bool | int | float | str | None = Field(
        default=None,
        description="The default value is used when an input parameter isn't specified in a workflow file.",
    )


class WorkflowCallOutput(StrictModel):
    """Output for workflow_call event."""

    description: str | None = Field(
        default=None,
        description="A string description of the output parameter.",
    )
    value: str = Field(
        ...,
        description=(
            "The value that the output parameter will be mapped to. You can set this to a string "
            "or an expression with context. For example, you can use the steps context to set "
            "the value of an output to the output value of a step."
        ),
    )


class WorkflowCallSecret(StrictModel):
    """Secret definition for workflow_call event."""

    description: str | None = Field(
        default=None,
        description="A string description of the secret parameter.",
    )
    required: bool | None = Field(
        default=None,
        description="A boolean specifying whether the secret must be supplied.",
    )


class WorkflowCallEvent(BaseModel):
    """Workflow call event configuration.

    Allows workflows to be reused by other workflows.

    Reference: https://docs.github.com/en/actions/learn-github-actions/events-that-trigger-workflows#workflow_call
    """

    inputs: dict[str, WorkflowCallInput] | None = Field(
        default=None,
        description="Inputs that are passed to the called workflow from the caller workflow.",
    )
    outputs: dict[str, WorkflowCallOutput] | None = Field(
        default=None,
        description="Outputs that are passed from the called workflow to the caller workflow.",
    )
    secrets: dict[str, WorkflowCallSecret] | None = Field(
        default=None,
        description="A map of the secrets that can be used in the called workflow.",
    )


class WorkflowRunEvent(FlexibleModel):
    """Workflow run event configuration.

    This event occurs when a workflow run is requested or completed, and allows
    you to execute a workflow based on the finished result of another workflow.

    Reference: https://docs.github.com/en/actions/reference/events-that-trigger-workflows#workflow_run
    """

    types: list[WorkflowRunActivityType] | WorkflowRunActivityType | None = None
    workflows: Annotated[list[str], Field(min_length=1)] | None = Field(
        default=None,
        description="The workflows to trigger on.",
    )
    branches: Globs | None = None
    branches_ignore: Globs | None = Field(default=None, alias="branches-ignore")
