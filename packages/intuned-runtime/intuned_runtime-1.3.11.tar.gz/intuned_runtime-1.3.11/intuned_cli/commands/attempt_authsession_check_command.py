import pytimeparse  # type: ignore

from intuned_cli.controller.authsession import execute_attempt_check_auth_session_cli
from intuned_cli.utils.auth_session_helpers import assert_auth_enabled
from intuned_cli.utils.wrapper import cli_command


@cli_command
async def attempt__authsession__check(
    id: str,
    /,
    *,
    proxy: str | None = None,
    timeout: str = "10 min",
    headless: bool = False,
    trace: bool = False,
    keep_browser_open: bool = False,
    cdp_url: str | None = None,
):
    """Check an existing auth session

    Args:
        id (str): ID of the auth session to check
        proxy (str | None, optional): [--proxy]. Proxy URL to use for the auth session command. Defaults to None.
        timeout (str, optional): [--timeout]. Timeout for the auth session command - seconds or pytimeparse-formatted string. Defaults to "10 min".
        headless (bool, optional): [--headless]. Run the API in headless mode (default: False). This will not open a browser window.
        trace (bool, optional): [--trace]. Capture a trace of each attempt, useful for debugging. Defaults to False.
        keep_browser_open (bool, optional): [--keep-browser-open]. Keep the last browser open after execution for debugging. Defaults to False.
        cdp_url (str | None, optional): [--cdp-url]. [Experimental] Chrome DevTools Protocol URL to connect to an existing browser instance. Disables proxy, headless, keep_browser_open options. Defaults to None.
    """
    await assert_auth_enabled()

    timeout_value = pytimeparse.parse(timeout)  # type: ignore
    if timeout_value is None:
        raise ValueError(
            f"Invalid timeout format: {timeout}. Please use a valid time format like '10 min' or '600 seconds'."
        )

    await execute_attempt_check_auth_session_cli(
        id=id,
        headless=headless,
        timeout=timeout_value,
        proxy=proxy,
        trace=trace,
        keep_browser_open=keep_browser_open,
        cdp_url=cdp_url,
    )
