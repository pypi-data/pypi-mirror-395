from intuned_cli.utils.help import print_help_and_exit
from intuned_cli.utils.wrapper import cli_command


@cli_command
async def attempt__authsession():
    """Execute san Intuned authsession attempt"""

    print_help_and_exit()
