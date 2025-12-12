"""Workflow trigger configuration models."""

from __future__ import annotations

from typing import Annotated

from pydantic import Field

from .base import FlexibleModel, StrictModel
from .enums import EventType
from .events import (
    BranchProtectionRuleEvent,
    CheckRunEvent,
    CheckSuiteEvent,
    DiscussionCommentEvent,
    DiscussionEvent,
    IssueCommentEvent,
    IssuesEvent,
    LabelEvent,
    MergeGroupEvent,
    MilestoneEvent,
    ProjectCardEvent,
    ProjectColumnEvent,
    ProjectEvent,
    PullRequestEvent,
    PullRequestReviewCommentEvent,
    PullRequestReviewEvent,
    PullRequestTargetEvent,
    PushEvent,
    RegistryPackageEvent,
    ReleaseEvent,
    ScheduleItem,
    WorkflowCallEvent,
    WorkflowDispatchEvent,
    WorkflowRunEvent,
)

__all__ = ["On", "OnConfiguration"]


class OnConfiguration(StrictModel):
    """Complete event trigger configuration.

    The name of the GitHub event that triggers the workflow. You can provide
    a single event string, array of events, array of event types, or an event
    configuration map that schedules a workflow or restricts the execution of
    a workflow to specific files, tags, or branch changes.

    Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/events-that-trigger-workflows
    """

    branch_protection_rule: BranchProtectionRuleEvent | None = None
    check_run: CheckRunEvent | None = None
    check_suite: CheckSuiteEvent | None = None
    create: FlexibleModel | None = Field(
        default=None,
        description="Runs your workflow anytime someone creates a branch or tag.",
    )
    delete: FlexibleModel | None = Field(
        default=None,
        description="Runs your workflow anytime someone deletes a branch or tag.",
    )
    deployment: FlexibleModel | None = Field(
        default=None,
        description="Runs your workflow anytime someone creates a deployment.",
    )
    deployment_status: FlexibleModel | None = Field(
        default=None,
        description="Runs your workflow anytime a third party provides a deployment status.",
    )
    discussion: DiscussionEvent | None = None
    discussion_comment: DiscussionCommentEvent | None = None
    fork: FlexibleModel | None = Field(
        default=None,
        description="Runs your workflow anytime when someone forks a repository.",
    )
    gollum: FlexibleModel | None = Field(
        default=None,
        description="Runs your workflow when someone creates or updates a Wiki page.",
    )
    issue_comment: IssueCommentEvent | None = None
    issues: IssuesEvent | None = None
    label: LabelEvent | None = None
    merge_group: MergeGroupEvent | None = None
    milestone: MilestoneEvent | None = None
    page_build: FlexibleModel | None = Field(
        default=None,
        description="Runs your workflow anytime someone pushes to a GitHub Pages-enabled branch.",
    )
    project: ProjectEvent | None = None
    project_card: ProjectCardEvent | None = None
    project_column: ProjectColumnEvent | None = None
    public: FlexibleModel | None = Field(
        default=None,
        description="Runs your workflow anytime someone makes a private repository public.",
    )
    pull_request: PullRequestEvent | None = None
    pull_request_review: PullRequestReviewEvent | None = None
    pull_request_review_comment: PullRequestReviewCommentEvent | None = None
    pull_request_target: PullRequestTargetEvent | None = None
    push: PushEvent | None = None
    registry_package: RegistryPackageEvent | None = None
    release: ReleaseEvent | None = None
    status: FlexibleModel | None = Field(
        default=None,
        description="Runs your workflow anytime the status of a Git commit changes.",
    )
    watch: FlexibleModel | None = Field(
        default=None,
        description="Runs your workflow anytime the watch event occurs.",
    )
    workflow_call: WorkflowCallEvent | None = None
    workflow_dispatch: WorkflowDispatchEvent | None = None
    workflow_run: WorkflowRunEvent | None = None
    repository_dispatch: FlexibleModel | None = Field(
        default=None,
        description=(
            "You can use the GitHub API to trigger a webhook event called repository_dispatch "
            "when you want to trigger a workflow for activity that happens outside of GitHub."
        ),
    )
    schedule: Annotated[list[ScheduleItem], Field(min_length=1)] | None = Field(
        default=None,
        description=(
            "You can schedule a workflow to run at specific UTC times using POSIX cron syntax. "
            "The shortest interval you can run scheduled workflows is once every 5 minutes."
        ),
    )


On = EventType | list[EventType] | OnConfiguration
"""
Workflow trigger configuration.

Can be a single event, list of events, or detailed event configuration.
"""
