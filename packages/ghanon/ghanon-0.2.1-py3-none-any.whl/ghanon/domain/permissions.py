"""Pydantic models for GitHub Actions Permissions."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import Field, model_validator

from .base import StrictModel
from .enums import ErrorMessage, ModelPermissionLevel, PermissionAccess, PermissionLevel

if TYPE_CHECKING:
    from .jobs import NormalJob, ReusableWorkflowCallJob
    from .workflow import Workflow

__all__ = [
    "Permissions",
    "PermissionsEvent",
]


class PermissionsEvent(StrictModel):
    """Fine-grained permissions for GITHUB_TOKEN.

    You can modify the default permissions granted to the GITHUB_TOKEN,
    adding or removing access as required, so that you only allow the
    minimum required access.

    Reference: https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#permissions
    """

    actions: PermissionLevel | None = None
    attestations: PermissionLevel | None = None
    checks: PermissionLevel | None = None
    contents: PermissionLevel | None = None
    deployments: PermissionLevel | None = None
    discussions: PermissionLevel | None = None
    id_token: PermissionLevel | None = Field(default=None, alias="id-token")
    issues: PermissionLevel | None = None
    models: ModelPermissionLevel | None = None
    packages: PermissionLevel | None = None
    pages: PermissionLevel | None = None
    pull_requests: PermissionLevel | None = Field(default=None, alias="pull-requests")
    repository_projects: PermissionLevel | None = Field(default=None, alias="repository-projects")
    security_events: PermissionLevel | None = Field(default=None, alias="security-events")
    statuses: PermissionLevel | None = None

    @model_validator(mode="after")
    def check_contents_read(self) -> PermissionsEvent:
        """Validate that 'contents' permission is explicitly set when customizing permissions.

        When defining custom permissions, the contents permission must be explicitly
        specified to follow the principle of least privilege.
        """
        if self.contents is None:
            raise ValueError(ErrorMessage.NO_CONTENTS_PERMISSION)
        return self


Permissions = PermissionAccess | PermissionsEvent
"""
Permissions can be either a global access level ('read-all' or 'write-all')
or fine-grained per-scope permissions.
"""


def rebuild_models_with_permissions(
    normal_job: type[NormalJob],
    reusable_workflow_call_job: type[ReusableWorkflowCallJob],
    workflow: type[Workflow],
) -> None:
    """Rebuild Pydantic models with proper Permissions type namespace.

    This function must be called after all models are defined to ensure
    forward references to Permissions are properly resolved.
    """
    normal_job.model_rebuild(_types_namespace={"Permissions": Permissions})
    reusable_workflow_call_job.model_rebuild(_types_namespace={"Permissions": Permissions})
    workflow.model_rebuild(_types_namespace={"Permissions": Permissions})
