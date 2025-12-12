"""Enumerations for GitHub Actions workflow models."""

from __future__ import annotations

from enum import StrEnum

__all__ = [
    "Architecture",
    "BranchProtectionRuleActivityType",
    "CheckRunActivityType",
    "CheckSuiteActivityType",
    "Description",
    "DiscussionActivityType",
    "DiscussionCommentActivityType",
    "ErrorMessage",
    "EventType",
    "IssueCommentActivityType",
    "IssuesActivityType",
    "LabelActivityType",
    "Machine",
    "MergeGroupActivityType",
    "MilestoneActivityType",
    "ModelPermissionLevel",
    "PermissionAccess",
    "PermissionLevel",
    "ProjectActivityType",
    "ProjectCardActivityType",
    "ProjectColumnActivityType",
    "PullRequestActivityType",
    "PullRequestReviewActivityType",
    "PullRequestReviewCommentActivityType",
    "PullRequestTargetActivityType",
    "RegistryPackageActivityType",
    "ReleaseActivityType",
    "ShellType",
    "WorkflowCallInputType",
    "WorkflowDispatchInputType",
    "WorkflowRunActivityType",
]


class Description(StrEnum):
    """Common field descriptions used across workflow models."""

    JOB_NAME = "The name of the job displayed on GitHub."
    CONCURRENCY = (
        "Concurrency ensures that only a single job or workflow using the same concurrency group will run at a time."
    )


class ErrorMessage(StrEnum):
    """Validation error messages for workflow models."""

    SECRETS_INHERIT = "Do not use `secrets: inherit` with reusable workflows as it can be insecure"
    NO_PERMISSIONS = (
        "Jobs should specify `contents: read` permission at minimum to satisfy the principle of least privilege"
    )
    NO_PERMISSIONS_REUSABLE = (
        "Reusable workflow jobs should specify `contents: read` permission at minimum "
        "to satisfy the principle of least privilege"
    )
    NO_CONTENTS_PERMISSION = "When modifying the default permissions, `contents: read/write` is explicitly required"


class PermissionLevel(StrEnum):
    """Permission access levels for GITHUB_TOKEN."""

    READ = "read"
    WRITE = "write"
    NONE = "none"


class PermissionAccess(StrEnum):
    """Global permission access shortcuts."""

    READ_ALL = "read-all"
    WRITE_ALL = "write-all"


class Architecture(StrEnum):
    """Supported architectures for runners."""

    ARM32 = "ARM32"
    X64 = "x64"
    X86 = "x86"


class Machine(StrEnum):
    """Supported machine types."""

    LINUX = "linux"
    MACOS = "macos"
    WINDOWS = "windows"


class EventType(StrEnum):
    """GitHub events that can trigger workflows.

    Reference: https://help.github.com/en/github/automating-your-workflow-with-github-actions/events-that-trigger-workflows
    """

    BRANCH_PROTECTION_RULE = "branch_protection_rule"
    CHECK_RUN = "check_run"
    CHECK_SUITE = "check_suite"
    CREATE = "create"
    DELETE = "delete"
    DEPLOYMENT = "deployment"
    DEPLOYMENT_STATUS = "deployment_status"
    DISCUSSION = "discussion"
    DISCUSSION_COMMENT = "discussion_comment"
    FORK = "fork"
    GOLLUM = "gollum"
    ISSUE_COMMENT = "issue_comment"
    ISSUES = "issues"
    LABEL = "label"
    MERGE_GROUP = "merge_group"
    MILESTONE = "milestone"
    PAGE_BUILD = "page_build"
    PROJECT = "project"
    PROJECT_CARD = "project_card"
    PROJECT_COLUMN = "project_column"
    PUBLIC = "public"
    PULL_REQUEST = "pull_request"
    PULL_REQUEST_REVIEW = "pull_request_review"
    PULL_REQUEST_REVIEW_COMMENT = "pull_request_review_comment"
    PULL_REQUEST_TARGET = "pull_request_target"
    PUSH = "push"
    REGISTRY_PACKAGE = "registry_package"
    RELEASE = "release"
    STATUS = "status"
    WATCH = "watch"
    WORKFLOW_CALL = "workflow_call"
    WORKFLOW_DISPATCH = "workflow_dispatch"
    WORKFLOW_RUN = "workflow_run"
    REPOSITORY_DISPATCH = "repository_dispatch"


class ModelPermissionLevel(StrEnum):
    """Permission levels for models (restricted to read/none)."""

    READ = "read"
    NONE = "none"


class ShellType(StrEnum):
    """Built-in shell types."""

    BASH = "bash"
    PWSH = "pwsh"
    PYTHON = "python"
    SH = "sh"
    CMD = "cmd"
    POWERSHELL = "powershell"


class BranchProtectionRuleActivityType(StrEnum):
    """Activity types for branch_protection_rule events."""

    CREATED = "created"
    EDITED = "edited"
    DELETED = "deleted"


class CheckRunActivityType(StrEnum):
    """Activity types for check_run events."""

    CREATED = "created"
    REREQUESTED = "rerequested"
    COMPLETED = "completed"
    REQUESTED_ACTION = "requested_action"


class CheckSuiteActivityType(StrEnum):
    """Activity types for check_suite events."""

    COMPLETED = "completed"
    REQUESTED = "requested"
    REREQUESTED = "rerequested"


class DiscussionActivityType(StrEnum):
    """Activity types for discussion events."""

    CREATED = "created"
    EDITED = "edited"
    DELETED = "deleted"
    TRANSFERRED = "transferred"
    PINNED = "pinned"
    UNPINNED = "unpinned"
    LABELED = "labeled"
    UNLABELED = "unlabeled"
    LOCKED = "locked"
    UNLOCKED = "unlocked"
    CATEGORY_CHANGED = "category_changed"
    ANSWERED = "answered"
    UNANSWERED = "unanswered"


class DiscussionCommentActivityType(StrEnum):
    """Activity types for discussion_comment events."""

    CREATED = "created"
    EDITED = "edited"
    DELETED = "deleted"


class IssueCommentActivityType(StrEnum):
    """Activity types for issue_comment events."""

    CREATED = "created"
    EDITED = "edited"
    DELETED = "deleted"


class IssuesActivityType(StrEnum):
    """Activity types for issues events."""

    OPENED = "opened"
    EDITED = "edited"
    DELETED = "deleted"
    TRANSFERRED = "transferred"
    PINNED = "pinned"
    UNPINNED = "unpinned"
    CLOSED = "closed"
    REOPENED = "reopened"
    ASSIGNED = "assigned"
    UNASSIGNED = "unassigned"
    LABELED = "labeled"
    UNLABELED = "unlabeled"
    LOCKED = "locked"
    UNLOCKED = "unlocked"
    MILESTONED = "milestoned"
    DEMILESTONED = "demilestoned"


class LabelActivityType(StrEnum):
    """Activity types for label events."""

    CREATED = "created"
    EDITED = "edited"
    DELETED = "deleted"


class MergeGroupActivityType(StrEnum):
    """Activity types for merge_group events."""

    CHECKS_REQUESTED = "checks_requested"


class MilestoneActivityType(StrEnum):
    """Activity types for milestone events."""

    CREATED = "created"
    CLOSED = "closed"
    OPENED = "opened"
    EDITED = "edited"
    DELETED = "deleted"


class ProjectActivityType(StrEnum):
    """Activity types for project events."""

    CREATED = "created"
    UPDATED = "updated"
    CLOSED = "closed"
    REOPENED = "reopened"
    EDITED = "edited"
    DELETED = "deleted"


class ProjectCardActivityType(StrEnum):
    """Activity types for project_card events."""

    CREATED = "created"
    MOVED = "moved"
    CONVERTED = "converted"
    EDITED = "edited"
    DELETED = "deleted"


class ProjectColumnActivityType(StrEnum):
    """Activity types for project_column events."""

    CREATED = "created"
    UPDATED = "updated"
    MOVED = "moved"
    DELETED = "deleted"


class PullRequestActivityType(StrEnum):
    """Activity types for pull_request events."""

    ASSIGNED = "assigned"
    UNASSIGNED = "unassigned"
    LABELED = "labeled"
    UNLABELED = "unlabeled"
    OPENED = "opened"
    EDITED = "edited"
    CLOSED = "closed"
    REOPENED = "reopened"
    SYNCHRONIZE = "synchronize"
    CONVERTED_TO_DRAFT = "converted_to_draft"
    READY_FOR_REVIEW = "ready_for_review"
    LOCKED = "locked"
    UNLOCKED = "unlocked"
    MILESTONED = "milestoned"
    DEMILESTONED = "demilestoned"
    REVIEW_REQUESTED = "review_requested"
    REVIEW_REQUEST_REMOVED = "review_request_removed"
    AUTO_MERGE_ENABLED = "auto_merge_enabled"
    AUTO_MERGE_DISABLED = "auto_merge_disabled"
    ENQUEUED = "enqueued"
    DEQUEUED = "dequeued"


class PullRequestTargetActivityType(StrEnum):
    """Activity types for pull_request_target events."""

    ASSIGNED = "assigned"
    UNASSIGNED = "unassigned"
    LABELED = "labeled"
    UNLABELED = "unlabeled"
    OPENED = "opened"
    EDITED = "edited"
    CLOSED = "closed"
    REOPENED = "reopened"
    SYNCHRONIZE = "synchronize"
    CONVERTED_TO_DRAFT = "converted_to_draft"
    READY_FOR_REVIEW = "ready_for_review"
    LOCKED = "locked"
    UNLOCKED = "unlocked"
    REVIEW_REQUESTED = "review_requested"
    REVIEW_REQUEST_REMOVED = "review_request_removed"
    AUTO_MERGE_ENABLED = "auto_merge_enabled"
    AUTO_MERGE_DISABLED = "auto_merge_disabled"


class PullRequestReviewActivityType(StrEnum):
    """Activity types for pull_request_review events."""

    SUBMITTED = "submitted"
    EDITED = "edited"
    DISMISSED = "dismissed"


class PullRequestReviewCommentActivityType(StrEnum):
    """Activity types for pull_request_review_comment events."""

    CREATED = "created"
    EDITED = "edited"
    DELETED = "deleted"


class RegistryPackageActivityType(StrEnum):
    """Activity types for registry_package events."""

    PUBLISHED = "published"
    UPDATED = "updated"


class ReleaseActivityType(StrEnum):
    """Activity types for release events."""

    PUBLISHED = "published"
    UNPUBLISHED = "unpublished"
    CREATED = "created"
    EDITED = "edited"
    DELETED = "deleted"
    PRERELEASED = "prereleased"
    RELEASED = "released"


class WorkflowRunActivityType(StrEnum):
    """Activity types for workflow_run events."""

    REQUESTED = "requested"
    COMPLETED = "completed"
    IN_PROGRESS = "in_progress"


class WorkflowDispatchInputType(StrEnum):
    """Input types for workflow_dispatch events."""

    STRING = "string"
    CHOICE = "choice"
    BOOLEAN = "boolean"
    NUMBER = "number"
    ENVIRONMENT = "environment"


class WorkflowCallInputType(StrEnum):
    """Input types for workflow_call events."""

    BOOLEAN = "boolean"
    NUMBER = "number"
    STRING = "string"
