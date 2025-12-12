"""Logger module for CLI output messages."""

from typing import NoReturn

from click import Abort, echo

from ghanon.formatter import Formatter


class Logger:
    """Logger for CLI output messages."""

    def __init__(self, formatter: Formatter) -> None:
        """Initialize the Logger with a Formatter."""
        self.formatter = formatter

    def log(self, *messages: str) -> None:
        """Log a generic message."""
        echo(" ".join(messages), color=True)

    def info(self, string: str) -> None:
        """Log an informational message."""
        self.log(self.formatter.info(string))

    def success(self, string: str) -> None:
        """Log a success message."""
        self.log(self.formatter.success(string))

    def error(self, string: str) -> None:
        """Log an error message."""
        self.log(self.formatter.fatal(string))

    def fatal(self, string: str) -> NoReturn:
        """Log a fatal error message and abort execution."""
        self.log(self.formatter.fatal(string))
        raise Abort
