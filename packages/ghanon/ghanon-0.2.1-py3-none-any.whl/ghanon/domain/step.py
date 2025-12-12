"""Step-related Pydantic models for GitHub Actions Workflows."""

from __future__ import annotations

from pydantic import Field, model_validator

from .base import StrictModel
from .defaults import ShellType
from .types import EnvMapping, ExpressionSyntax

__all__ = [
    "Step",
]


class Step(StrictModel):
    """A single step in a job.

    Steps can run commands, run setup tasks, or run an action in your repository,
    a public repository, or an action published in a Docker registry.
    Not all steps run actions, but all actions run as a step.

    Each step runs in its own process in the virtual environment and has access
    to the workspace and filesystem. Because steps run in their own process,
    changes to environment variables are not preserved between steps.

    Must contain either `uses` or `run`.

    Reference: https://help.github.com/en/actions/automating-your-workflow-with-github-actions/workflow-syntax-for-github-actions#jobsjob_idsteps
    """

    id: str | None = Field(
        default=None,
        description=(
            "A unique identifier for the step. You can use the id to reference the step in contexts. "
            "For more information, see https://help.github.com/en/articles/contexts-and-expression-syntax-for-github-actions."
        ),
    )
    if_: bool | int | float | str | None = Field(
        default=None,
        alias="if",
        description=(
            "You can use the if conditional to prevent a step from running unless a condition is met. "
            "You can use any supported context and expression to create a conditional.\n"
            "Expressions in an if conditional do not require the ${{ }} syntax. "
            "For more information, see https://help.github.com/en/articles/contexts-and-expression-syntax-for-github-actions."
        ),
    )
    name: str | None = Field(
        default=None,
        description="A name for your step to display on GitHub.",
    )
    uses: str | None = Field(
        default=None,
        description=(
            "Selects an action to run as part of a step in your job. An action is a reusable unit of code. "
            "You can use an action defined in the same repository as the workflow, a public repository, "
            "or in a published Docker container image (https://hub.docker.com/).\n\n"
            "We strongly recommend that you include the version of the action you are using by specifying "
            "a Git ref, SHA, or Docker tag number. If you don't specify a version, it could break your "
            "workflows or cause unexpected behavior when the action owner publishes an update.\n\n"
            "- Using the commit SHA of a released action version is the safest for stability and security.\n"
            "- Using the specific major action version allows you to receive critical fixes and security patches.\n"
            "- Using the master branch of an action may be convenient, but if someone releases a new major version "
            "with a breaking change, your workflow could break."
        ),
    )
    run: str | None = Field(
        default=None,
        description=(
            "Runs command-line programs using the operating system's shell. If you do not provide a name, "
            "the step name will default to the text specified in the run command.\n\n"
            "Commands run using non-login shells by default. You can choose a different shell and "
            "customize the shell used to run commands.\n\n"
            "Each run keyword represents a new process and shell in the virtual environment. "
            "When you provide multi-line commands, each line runs in the same shell."
        ),
    )
    working_directory: str | None = Field(
        default=None,
        alias="working-directory",
        description=(
            "Using the working-directory keyword, you can specify the working directory of where to run the command."
        ),
    )
    shell: str | ShellType | None = Field(
        default=None,
        description=(
            "You can override the default shell settings in the runner's operating system using the shell keyword."
        ),
    )
    with_: EnvMapping | None = Field(
        default=None,
        alias="with",
        description=(
            "A map of the input parameters defined by the action. Each input parameter is a key/value pair. "
            "Input parameters are set as environment variables. The variable is prefixed with INPUT_ and "
            "converted to upper case."
        ),
    )
    env: EnvMapping | None = Field(
        default=None,
        description=(
            "Sets environment variables for steps to use in the virtual environment. "
            "You can also set environment variables for the entire workflow or a job."
        ),
    )
    continue_on_error: bool | ExpressionSyntax = Field(
        default=False,
        alias="continue-on-error",
        description=(
            "Prevents a job from failing when a step fails. Set to true to allow a job to pass when this step fails."
        ),
    )
    timeout_minutes: int | float | ExpressionSyntax | None = Field(
        default=None,
        alias="timeout-minutes",
        description="The maximum number of minutes to run the step before killing the process.",
    )

    @model_validator(mode="after")
    def check_uses_or_run(self) -> Step:
        """Validate that step has either uses or run but not both."""
        if self.uses is None and self.run is None:
            msg = "Step must contain either 'uses' or 'run'"
            raise ValueError(msg)
        if self.uses is not None and self.run is not None:
            msg = "Step cannot contain both 'uses' and 'run'"
            raise ValueError(msg)
        return self

    @model_validator(mode="after")
    def check_run_dependencies(self) -> Step:
        """Validate that shell and working-directory are only used with run."""
        if self.run is None:
            if self.working_directory is not None:
                msg = "'working-directory' requires 'run' to be specified"
                raise ValueError(msg)
            if self.shell is not None:
                msg = "'shell' requires 'run' to be specified"
                raise ValueError(msg)
        return self
