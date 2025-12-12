"""Parser functions for GitHub Actions Workflow schema."""

from __future__ import annotations

from dataclasses import dataclass, field

import yaml
from pydantic_core import ErrorDetails, ValidationError

from .domain.workflow import Workflow
from .yaml import YamlLoader

__all__ = [
    "ParsingResult",
    "WorkflowParser",
]


@dataclass
class ParsingResult:
    """Result of parsing a GitHub Actions workflow."""

    workflow: Workflow | None = None
    success: bool = False
    errors: list[ErrorDetails] = field(default_factory=list)
    line_map: dict[str, int] = field(default_factory=dict)

    @classmethod
    def with_success(cls, workflow: Workflow) -> ParsingResult:
        """Create a successful ParsingResult."""
        return cls(workflow=workflow, success=True, errors=[])

    @classmethod
    def with_errors(cls, errors: list[ErrorDetails], line_map: dict[str, int] | None = None) -> ParsingResult:
        """Create a failed ParsingResult."""
        return cls(workflow=None, success=False, errors=errors, line_map=line_map or {})


class WorkflowParser:
    """Parser for GitHub Actions Workflows."""

    loader: YamlLoader

    def __init__(self) -> None:
        """Initialize the parser with a YAML loader."""
        self.loader = YamlLoader()

    def parse(self, yaml_content: str) -> ParsingResult:
        """Parse a workflow dictionary into a ParsingResult."""
        line_map = self.loader.build_line_map(yaml_content)

        try:
            data = self.loader.load(yaml_content)
        except yaml.YAMLError as error:
            return self._yaml_parsing_error(yaml_content, line_map, error)

        try:
            workflow = Workflow.model_validate(data)
            return ParsingResult.with_success(workflow)
        except ValidationError as error:
            return ParsingResult.with_errors(error.errors(), line_map)

    def _yaml_parsing_error(self, content: str, line_map: dict[str, int], error: Exception) -> ParsingResult:
        errors: list[ErrorDetails] = [
            {
                "type": "yaml_error",
                "loc": (),
                "msg": f"Error parsing YAML: {error}",
                "input": content,
            },
        ]

        return ParsingResult.with_errors(errors, line_map)
