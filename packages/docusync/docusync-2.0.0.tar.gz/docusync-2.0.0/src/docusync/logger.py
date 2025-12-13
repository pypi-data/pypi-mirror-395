"""Beautiful logging utilities for DocuSync."""

from enum import Enum
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from docusync.constants import LOG_COLORS


class LogLevel(Enum):
    """Log levels for user-facing messages."""

    DEBUG = LOG_COLORS["DEBUG"]
    INFO = LOG_COLORS["INFO"]
    SUCCESS = LOG_COLORS["SUCCESS"]
    WARNING = LOG_COLORS["WARNING"]
    ERROR = LOG_COLORS["ERROR"]


class UserLogger:
    """Beautiful logger for user-facing messages using Rich."""

    def __init__(self, verbose: bool = False) -> None:
        """Initialize the logger.

        :param verbose: Enable verbose (debug) output
        """
        self.console = Console()
        self.verbose = verbose

    def _log(
        self,
        level: LogLevel,
        message: str,
        **kwargs: Any,
    ) -> None:
        """Internal logging method.

        :param level: Log level
        :param message: Message to log
        :param kwargs: Additional arguments for console.print
        """
        color = level.value

        if level == LogLevel.DEBUG and not self.verbose:
            return

        self.console.print(f"[{color}]{message}[/{color}]", **kwargs)

    def debug(self, message: str) -> None:
        """Log debug message (only in verbose mode).

        :param message: Debug message
        """
        self._log(LogLevel.DEBUG, message)

    def info(self, message: str) -> None:
        """Log info message.

        :param message: Info message
        """
        self._log(LogLevel.INFO, message)

    def success(self, message: str) -> None:
        """Log success message.

        :param message: Success message
        """
        self._log(LogLevel.SUCCESS, message)

    def warning(self, message: str) -> None:
        """Log warning message.

        :param message: Warning message
        """
        self._log(LogLevel.WARNING, message)

    def error(self, message: str) -> None:
        """Log error message.

        :param message: Error message
        """
        self._log(LogLevel.ERROR, message)

    def header(self, title: str, subtitle: str = "") -> None:
        """Display a beautiful header.

        :param title: Header title
        :param subtitle: Optional subtitle
        """
        text = Text()
        text.append(title, style="bold blue")
        if subtitle:
            text.append(f"\n{subtitle}", style="dim")

        panel = Panel(text, border_style="blue")
        self.console.print(panel)

    def section(self, title: str) -> None:
        """Display a section header.

        :param title: Section title
        """
        self.console.print(f"\n[bold cyan]═══ {title} ═══[/bold cyan]\n")

    def step(self, step_num: int, total: int, message: str) -> None:
        """Display a step in a process.

        :param step_num: Current step number
        :param total: Total number of steps
        :param message: Step message
        """
        self.console.print(
            f"[bold blue][{step_num}/{total}][/bold blue] {message}"
        )

    def table_repositories(
        self,
        repositories: list[Any],
    ) -> None:
        """Display repositories in a beautiful table.

        :param repositories: List of repository objects
        """
        table = Table(
            title="Configured Repositories",
            show_header=True,
            header_style="bold cyan",
        )

        table.add_column("#", style="dim", width=4)
        table.add_column("Name", style="bold")
        table.add_column("GitHub Path")
        table.add_column("Docs Path", style="dim")
        table.add_column("Description", style="italic")

        for repo in repositories:
            table.add_row(
                str(repo.position),
                repo.display_name,
                repo.github_path,
                repo.docs_path,
                repo.description,
            )

        self.console.print(table)

    def progress_message(
        self,
        action: str,
        target: str,
    ) -> None:
        """Display a progress message.

        :param action: Action being performed
        :param target: Target of the action
        """
        self.console.print(f"[cyan]→[/cyan] {action} [bold]{target}[/bold]...")

    def command_output(self, command: str) -> None:
        """Display a command being executed.

        :param command: Command string
        """
        if self.verbose:
            self.console.print(f"[dim]$ {command}[/dim]")

    def newline(self) -> None:
        """Print a newline."""
        self.console.print()


# Global logger instance for user-facing messages
USER_LOG = UserLogger(verbose=False)
