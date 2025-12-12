"""Ghanon CLI implementation."""

import os
from pathlib import Path
from typing import TYPE_CHECKING

import click
from pydantic_core import ErrorDetails

from ghanon.formatter import Formatter
from ghanon.logger import Logger
from ghanon.parser import ParsingResult, WorkflowParser

if TYPE_CHECKING:
    from collections.abc import Iterator


class ErrorHandler:
    """Handles formatting and logging of validation errors."""

    def __init__(self, formatter: Formatter, logger: Logger) -> None:
        """Initialize the error handler.

        Args:
            formatter: Formatter instance for styling output.
            logger: Logger instance for outputting messages.

        """
        self.formatter = formatter
        self.logger = logger

    def handle(self, result: ParsingResult, workflow: Path) -> None:
        """Handle validation errors by logging them and aborting.

        Args:
            result: Parsing result containing errors.
            workflow: Path to the workflow file being validated.

        """
        self.logger.error(
            f"Error parsing workflow file {workflow}. Found {len(result.errors)} error(s).{os.linesep}",
        )
        for error in result.errors:
            msg = self._format_error(error, workflow, result.line_map)
            self.logger.log(msg, os.linesep)

        raise click.Abort

    def _format_error(self, error: ErrorDetails, workflow: Path, line_map: dict[str, int]) -> str:
        """Format a Pydantic error for display.

        Args:
            error: Error details from Pydantic validation.
            workflow: Path to the workflow file being validated.
            line_map: Dictionary mapping paths to line numbers.

        Returns:
            Formatted error message.

        """
        msg = error["msg"]
        loc = error["loc"]
        message = f"{self.formatter.bold(msg)} {os.linesep}  --> {self.formatter.warning(str(workflow))}"

        if not loc:
            return message

        location = ".".join(str(segment) for segment in loc) if isinstance(loc, tuple) else loc
        line_info = self._get_line_info(location, line_map)

        return f"{message}:{line_info} at `{location}`"

    def _get_line_info(self, location: str, line_map: dict[str, int]) -> int:
        """Get line number information for a given location path.

        Finds the most specific (longest) matching path in the line map.
        This helps point to the deepest nested field causing validation errors.

        Args:
            location: Dotted path location from error details.
            line_map: Dictionary mapping paths to line numbers.

        Returns:
            Line number suffix (e.g., ":42") or empty string if not found.

        """
        # Pydantic error locations include model class names not present in the YAML line map,
        # so we search for partial path matches by progressively shortening the location path.
        # Valid errors always have at least one matching partial path (e.g., root keys like "on", "jobs").
        path_parts = location.split(".")
        for i in range(len(path_parts), 0, -1):
            partial_path = ".".join(path_parts[:i])
            if partial_path in line_map:
                return line_map[partial_path]

        # Fallback for edge cases where no path matches (should not occur with valid workflow errors)
        return 0  # pragma: no cover


class Ghanon:
    """Ghanon CLI for validating GitHub Actions workflows."""

    verbose: bool

    def __init__(self, verbose: bool) -> None:
        """Initialize the CLI.

        Args:
            verbose: Whether to enable verbose output.

        """
        self.formatter = Formatter()
        self.logger = Logger(self.formatter)
        self.parser = WorkflowParser()
        self.error_handler = ErrorHandler(self.formatter, self.logger)
        self.set_options(verbose=verbose)

    def set_options(self, **kwargs: str | bool) -> None:
        """Set CLI options dynamically.

        Args:
            **kwargs: CLI option flags (e.g., verbose=True).

        """
        for key, value in kwargs.items():
            setattr(self, key, value)

    def run(self, workflows: tuple[str, ...]) -> None:
        """Run the CLI with the given workflow paths.

        Args:
            workflows: Tuple of workflow paths from command line arguments.

        """
        workflow_paths = self._get_workflow_paths(workflows)

        for workflow in workflow_paths:
            self._validate_workflow(workflow)

    def _get_workflow_paths(self, workflows: tuple[str, ...]) -> Iterator[Path]:
        """Get list of workflow paths to validate.

        Args:
            workflows: Tuple of workflow paths from command line arguments.

        Returns:
            List of Path objects to validate.

        """
        if workflows:
            return (Path(workflow) for workflow in workflows)

        workflows_dir = Path.cwd() / ".github" / "workflows"

        return workflows_dir.glob("*.yml")

    def _validate_workflow(self, workflow: Path) -> None:
        """Validate a single workflow file.

        Args:
            workflow: Path to the workflow file to validate.

        """
        if not workflow.is_file():
            self.logger.fatal(f"File '{workflow}' does not exist")

        if self.verbose:
            self.logger.info(f"Parsing workflow file: {workflow}")

        result = self._parse(workflow)

        if result.success:
            return self.logger.success(f"{workflow.name} is a valid workflow.")

        return self.error_handler.handle(result, workflow)

    def _parse(self, filepath: Path) -> ParsingResult:
        """Parse a workflow file and return the parsing result.

        Args:
            filepath: Path to the workflow file to parse.

        Returns:
            Parsing result containing success status and any errors.

        """
        return self.parser.parse(filepath.read_text())


@click.command()
@click.argument("workflows", type=click.Path(), required=False, nargs=-1)
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output.")
def main(workflows: tuple[str, ...], verbose: bool) -> None:
    """Run Ghanon CLI."""
    cli = Ghanon(verbose=verbose)
    cli.run(workflows)
