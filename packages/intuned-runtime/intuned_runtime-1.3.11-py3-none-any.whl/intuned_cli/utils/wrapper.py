import asyncio
from collections.abc import Awaitable
from collections.abc import Callable
from functools import wraps
from typing import Any
from typing import cast
from typing import ParamSpec
from typing import TypeVar

import arguably

from intuned_cli.utils.browser import close_cli_browser
from intuned_cli.utils.browser import is_cli_browser_launched
from intuned_cli.utils.console import console
from intuned_cli.utils.error import CLIAbortError
from intuned_cli.utils.error import CLIError
from intuned_cli.utils.error import CLIExit
from intuned_cli.utils.error import log_automation_error
from runtime.errors.run_api_errors import RunApiError
from runtime.stealth_setup import setup_stealth_if_enabled
from runtime.utils.anyio import run_sync

P = ParamSpec("P")
R = TypeVar("R")


def cli_command(fn: Callable[P, Awaitable[R]]) -> Callable[P, R]:
    @arguably.command  # type: ignore
    @wraps(fn)
    @run_sync
    async def wrapper(*args: Any, **kwargs: Any) -> R:
        setup_stealth_if_enabled()

        cdp_url = kwargs.get("cdp_url", None)
        keep_open = (cdp_url is None) and (bool(kwargs.get("keep_browser_open", False)))
        if keep_open:
            console.print(
                "[bold]--keep-browser-open is set, the CLI will not close the last browser after the command completes.[/bold]"
            )
        try:
            result = await fn(*args, **kwargs)
            return result
        except CLIAbortError as e:
            console.print("[bold red]Aborted[/bold red]")
            raise CLIExit(1) from e
        except CLIError as e:
            if e.auto_color:
                console.print(f"[bold red]{e.message}[/bold red]")
            else:
                console.print(e.message)
            raise CLIExit(1) from e
        except RunApiError as e:
            log_automation_error(e)
            raise CLIExit(1) from e
        except KeyboardInterrupt:
            console.print("[bold red]Aborted[/bold red]")
            raise CLIExit(1) from None
        except Exception as e:
            console.print(
                f"[red][bold]An error occurred: [/bold]{e}\n[bold]Please report this issue to the Intuned team.[/bold]"
            )
            raise CLIExit(1) from e
        finally:
            if keep_open:
                await _wait_for_user_input()
            await close_cli_browser()

    return cast(Callable[P, R], wrapper)


async def _wait_for_user_input():
    if not is_cli_browser_launched():
        return
    if not console.is_terminal:
        return
    await asyncio.to_thread(console.input, "Press Enter to continue...")
