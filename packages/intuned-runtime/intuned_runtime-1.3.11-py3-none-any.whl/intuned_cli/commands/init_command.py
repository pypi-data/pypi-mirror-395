from typing import Any

from intuned_cli.utils.error import CLIError
from intuned_cli.utils.wrapper import cli_command


@cli_command
async def init(
    *args: Any,
):
    """
    Deprecated: Initialize a new Intuned project in the current directory.

    Returns:
        None
    """
    raise CLIError(
        "[red bold]The init command has been deprecated. Please use[/red bold] [cyan italic]npx create-intuned-project[/cyan italic] [red bold]instead.[/red bold]",
        auto_color=False,
    )
