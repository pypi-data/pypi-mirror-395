"""Formatter for CLI output messages with color and style."""

from colorama import Fore, Style


class Formatter:
    """Formatter for CLI output messages."""

    def info(self, string: str) -> str:
        """Format an informational message."""
        return Fore.BLUE + string + Style.RESET_ALL  # type: ignore[return-value]

    def success(self, string: str) -> str:
        """Format a success message."""
        return Fore.GREEN + string + Style.RESET_ALL  # type: ignore[return-value]

    def warning(self, string: str) -> str:
        """Format a warning message."""
        return Fore.YELLOW + string + Style.RESET_ALL  # type: ignore[return-value]

    def fatal(self, string: str) -> str:
        """Format a fatal error message."""
        return self.bold(Fore.RED + string + Style.RESET_ALL)  # type: ignore[arg-type]

    def bold(self, string: str) -> str:
        """Format a bold message."""
        return Style.BRIGHT + string + Style.RESET_ALL  # type: ignore[return-value]
