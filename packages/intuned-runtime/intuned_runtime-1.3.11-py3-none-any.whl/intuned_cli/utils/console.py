import sys

from prompt_toolkit.output import create_output
from rich.console import Console

output_file = sys.stderr

console = Console(
    highlight=False,
    file=output_file,
)


questionary_output = create_output(
    stdout=output_file,
)
