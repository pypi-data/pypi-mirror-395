from collections.abc import Awaitable
from collections.abc import Callable
from typing import ParamSpec
from typing import TypeVar

import arguably

from runtime.utils.anyio import run_sync

P = ParamSpec("P")
R = TypeVar("R")


def internal_cli_command(fn: Callable[P, R | Awaitable[R]]) -> Callable[P, R]:
    return arguably.command(run_sync(fn))  # type: ignore
