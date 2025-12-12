"""Default settings models for GitHub Actions workflows."""

from __future__ import annotations

from pydantic import Field, model_validator

from .base import StrictModel
from .enums import ShellType

__all__ = [
    "Defaults",
    "DefaultsRun",
]


class DefaultsRun(StrictModel):
    """Default settings for run steps."""

    shell: str | ShellType | None = Field(
        default=None,
        description=(
            "You can override the default shell settings in the runner's operating "
            "system using the shell keyword. You can use built-in shell keywords, "
            "or you can define a custom set of shell options.\n\n"
            "Reference: https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#jobsjob_idstepsshell"
        ),
    )
    working_directory: str | None = Field(
        default=None,
        alias="working-directory",
        description=(
            "Using the working-directory keyword, you can specify the working directory of where to run the command."
        ),
    )

    @model_validator(mode="after")
    def check_at_least_one_property(self) -> DefaultsRun:
        """Validate that at least one of shell or working-directory is specified."""
        if self.shell is None and self.working_directory is None:
            msg = "At least one of 'shell' or 'working-directory' must be specified"
            raise ValueError(msg)
        return self


class Defaults(StrictModel):
    """Default settings that apply to all jobs/steps.

    Reference: https://help.github.com/en/actions/reference/workflow-syntax-for-github-actions#defaults
    """

    run: DefaultsRun | None = None

    @model_validator(mode="after")
    def check_at_least_one_property(self) -> Defaults:
        """Validate that at least one property is specified in defaults."""
        if self.run is None:
            msg = "At least one property must be specified in defaults"
            raise ValueError(msg)
        return self
