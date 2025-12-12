"""Base models for GitHub Actions Workflows."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field, model_validator

if TYPE_CHECKING:
    from .types import Globs


class StrictModel(BaseModel):
    """Base model with strict configuration."""

    model_config = ConfigDict(extra="forbid")


class FlexibleModel(BaseModel):
    """Base model allowing additional properties."""

    model_config = ConfigDict(extra="allow")


class FilterableEventModel(StrictModel):
    """Base model for events that support branch, tag, and path filters."""

    branches: Globs | None = None
    branches_ignore: Globs | None = Field(default=None, alias="branches-ignore")
    tags: Globs | None = None
    tags_ignore: Globs | None = Field(default=None, alias="tags-ignore")
    paths: Globs | None = None
    paths_ignore: Globs | None = Field(default=None, alias="paths-ignore")

    @model_validator(mode="after")
    def check_filter_exclusivity(self) -> FilterableEventModel:
        """Validate that inclusive and exclusive filters are not used together."""
        if self.branches is not None and self.branches_ignore is not None:
            msg = "Cannot use both 'branches' and 'branches-ignore'"
            raise ValueError(msg)
        if self.tags is not None and self.tags_ignore is not None:
            msg = "Cannot use both 'tags' and 'tags-ignore'"
            raise ValueError(msg)
        if self.paths is not None and self.paths_ignore is not None:
            msg = "Cannot use both 'paths' and 'paths-ignore'"
            raise ValueError(msg)
        return self
