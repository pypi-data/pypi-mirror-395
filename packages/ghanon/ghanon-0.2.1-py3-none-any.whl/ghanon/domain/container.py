"""Container models for GitHub Actions workflows."""

from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel, Field

from .base import StrictModel

__all__ = [
    "Container",
    "ContainerCredentials",
]


EnvVarValue = str | int | float | bool
"""Valid types for environment variable values."""

EnvMapping = dict[str, EnvVarValue] | str
"""
Environment variables mapping.

To set custom environment variables, you need to specify the variables in the workflow file.
You can define environment variables for a step, job, or entire workflow using the
jobs.<job_id>.steps[*].env, jobs.<job_id>.env, and env keywords.

Reference: https://docs.github.com/en/actions/learn-github-actions/environment-variables
"""


class ContainerCredentials(BaseModel):
    """Container registry credentials for docker login."""

    username: str | None = None
    password: str | None = None


class Container(StrictModel):
    """Container configuration for running jobs.

    Reference: https://help.github.com/en/actions/automating-your-workflow-with-github-actions/workflow-syntax-for-github-actions#jobsjob_idcontainer
    """

    image: str = Field(
        ...,
        description=(
            "The Docker image to use as the container to run the action. "
            "The value can be the Docker Hub image name or a registry name."
        ),
    )
    credentials: ContainerCredentials | None = Field(
        default=None,
        description=(
            "If the image's container registry requires authentication to pull the image, "
            "you can use credentials to set a map of the username and password. "
            "The credentials are the same values that you would provide to the `docker login` command.\n\n"
            "Reference: https://docs.github.com/en/free-pro-team@latest/actions/reference/workflow-syntax-for-github-actions#jobsjob_idcontainercredentials"
        ),
    )
    env: EnvMapping | None = Field(
        default=None,
        description="Sets an array of environment variables in the container.",
    )
    ports: Annotated[list[int | str], Field(min_length=1)] | None = Field(
        default=None,
        description="Sets an array of ports to expose on the container.",
    )
    volumes: Annotated[list[str], Field(min_length=1)] | None = Field(
        default=None,
        description=(
            "Sets an array of volumes for the container to use. You can use volumes to share data "
            "between services or other steps in a job. You can specify named Docker volumes, "
            "anonymous Docker volumes, or bind mounts on the host.\n"
            "To specify a volume, you specify the source and destination path: <source>:<destinationPath>\n"
            "The <source> is a volume name or an absolute path on the host machine, "
            "and <destinationPath> is an absolute path in the container."
        ),
    )
    options: str | None = Field(
        default=None,
        description=(
            "Additional Docker container resource options. "
            "For a list of options, see https://docs.docker.com/engine/reference/commandline/create/#options."
        ),
    )
