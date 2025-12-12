"""Pydantic models for GitHub Actions workflow schema."""

from .jobs import NormalJob, ReusableWorkflowCallJob
from .permissions import rebuild_models_with_permissions
from .workflow import Workflow

rebuild_models_with_permissions(NormalJob, ReusableWorkflowCallJob, Workflow)
