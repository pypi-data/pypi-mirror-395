from functools import WRAPPER_ASSIGNMENTS
from functools import wraps

import pytimeparse  # type: ignore

from intuned_cli.controller.authsession import execute_run_update_auth_session_cli
from intuned_cli.utils.auth_session_helpers import assert_auth_enabled
from intuned_cli.utils.auth_session_helpers import load_parameters
from intuned_cli.utils.wrapper import cli_command


async def _run_update_authsession_impl(
    id: str,
    /,
    *,
    parameters: str | None = None,
    check_attempts: int = 1,
    create_attempts: int = 1,
    proxy: str | None = None,
    timeout: str = "10 min",
    headless: bool = False,
    trace: bool = False,
    keep_browser_open: bool = False,
    cdp_url: str | None = None,
):
    """Execute an AuthSession:Update run to update an existing auth session

    Args:
        id (str): ID of the auth session to update
        parameters (str | None, optional): [--parameters]. Parameters for the auth session command. If not provided, it will use the existing parameters.
        check_attempts (int, optional): [--check-attempts]. Number of attempts to check the auth session validity. Defaults to 1.
        create_attempts (int, optional): [--create-attempts]. Number of attempts to create a new auth session if it is invalid. Defaults to 1.
        proxy (str | None, optional): [--proxy]. Proxy URL to use for the auth session command. Defaults to None.
        timeout (str, optional): [--timeout]. Timeout for the auth session command - seconds or pytimeparse-formatted string. Defaults to "10 min".
        headless (bool, optional): [--headless]. Run the API in headless mode (default: False). This will not open a browser window.
        trace (bool, optional): [--trace]. Capture a trace of each attempt, useful for debugging. Defaults to False.
        keep_browser_open (bool, optional): [--keep-browser-open]. Keep the last browser open after execution for debugging. Defaults to False.
        cdp_url (str | None, optional): [--cdp-url]. [Experimental] Chrome DevTools Protocol URL to connect to an existing browser instance. Disables proxy, headless, keep_browser_open options. Defaults to None.
    """
    await assert_auth_enabled(auth_type="API")

    auth_session_input = None
    if parameters:
        auth_session_input = await load_parameters(parameters)

    timeout_value = pytimeparse.parse(timeout)  # type: ignore
    if timeout_value is None:
        raise ValueError(
            f"Invalid timeout format: {timeout}. Please use a valid time format like '10 min' or '600 seconds'."
        )

    await execute_run_update_auth_session_cli(
        id=id,
        input_data=auth_session_input,
        check_retries=check_attempts,
        create_retries=create_attempts,
        headless=headless,
        proxy=proxy,
        timeout=timeout_value,
        trace=trace,
        keep_browser_open=keep_browser_open,
        cdp_url=cdp_url,
    )


@cli_command
@wraps(_run_update_authsession_impl, (a for a in WRAPPER_ASSIGNMENTS if a != "__name__"))
async def run__authsession__update(
    *args,  # type: ignore
    **kwargs,  # type: ignore
):
    return await _run_update_authsession_impl(*args, **kwargs)  # type: ignore


@cli_command
@wraps(_run_update_authsession_impl, (a for a in WRAPPER_ASSIGNMENTS if a != "__name__"))
async def authsession__update(
    *args,  # type: ignore
    **kwargs,  # type: ignore
):
    return await _run_update_authsession_impl(*args, **kwargs)  # type: ignore
