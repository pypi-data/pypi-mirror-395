import arguably

from intuned_cli.utils.error import CLIExit


def print_help_and_exit():
    if arguably.is_target():
        arguably._context.context._current_parser.print_help()  # type: ignore
        raise CLIExit(0)
