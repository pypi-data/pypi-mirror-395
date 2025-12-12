from intuned_cli.utils.console import console
from intuned_cli.utils.error import CLIExit
from intuned_cli.utils.help import print_help_and_exit
from intuned_cli.utils.wrapper import cli_command


@cli_command
async def __root__(
    *,
    version: bool = False,
):
    """Intuned CLI to initialize, develop and deploy Intuned projects.

    This command is the entry point for the Intuned CLI. It provides various subcommands
    for managing Intuned projects, including initialization, development, and deployment.

    Args:
        version (bool, optional): [-v/--version] Show version information. Defaults to False.
    """

    if version:
        console.print("1.0.0")  # todo: better version handling
        raise CLIExit(0)

    print_help_and_exit()
