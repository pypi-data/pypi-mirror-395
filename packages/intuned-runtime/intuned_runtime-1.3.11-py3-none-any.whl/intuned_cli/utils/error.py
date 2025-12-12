import traceback

from intuned_cli.utils.console import console
from runtime.errors.run_api_errors import AutomationError
from runtime.errors.run_api_errors import RunApiError


class CLIError(Exception):
    """Base class for CLI errors."""

    def __init__(self, message: str, auto_color: bool = True):
        """
        Initialize the CLIError.

        Args:
            message (str): The error message.
            auto_color (bool): Whether to automatically color the error message.
        """
        super().__init__(message)
        self.message = message
        self.auto_color = auto_color


class CLIAbortError(Exception):
    """Exception to signal CLI abortion without an error message."""

    pass


def log_automation_error(e: RunApiError):
    console.print("[bold red]An error occurred while running the API:[/bold red]")

    if isinstance(e, AutomationError):
        stack_trace = traceback.format_exception(type(e.error), value=e.error, tb=e.error.__traceback__)
        console.print(f"[red]{''.join(stack_trace)}[/red]")
    else:
        console.print(f"[red]{e}[/red]")


class CLIExit(BaseException):
    """Exception to signal CLI exit with a specific code."""

    def __init__(self, code: int):
        """
        Initialize the CLIExit.

        Args:
            code (int): The exit code.
        """
        super().__init__()
        self.code = code
