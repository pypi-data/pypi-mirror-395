import pytimeparse  # type: ignore

from intuned_cli.controller.api import execute_attempt_api_cli
from intuned_cli.utils.auth_session_helpers import assert_auth_consistent
from intuned_cli.utils.auth_session_helpers import load_parameters
from intuned_cli.utils.wrapper import cli_command


@cli_command
async def attempt__api(
    api_name: str,
    parameters: str,
    /,
    *,
    auth_session: str | None = None,
    proxy: str | None = None,
    timeout: str = "10 min",
    headless: bool = False,
    output_file: str | None = None,
    trace: bool = False,
    keep_browser_open: bool = False,
    cdp_url: str | None = None,
):
    """Executes an Intuned API attempt with parameters

    Args:
        api_name (str): Name of the API.
        parameters (str): Path to JSON file containing API parameters or the parameters as a JSON string.
        auth_session (str | None, optional): [-a/--auth-session]. ID of the auth session to use for the API. This is expected to be in ./auth-sessions-instances/<id>
        proxy (str | None, optional): [--proxy]. Proxy URL to use. Defaults to None.
        timeout (str, optional): [--timeout]. Timeout - seconds or pytimeparse-formatted string. Defaults to "10 min".
        headless (bool, optional): [--headless]. Run the API in headless mode (default: False). This will not open a browser window.
        output_file (str | None, optional): [-o/--output-file]. Output file path. Defaults to None.
        trace (bool, optional): [--trace]. Capture a trace of each attempt, useful for debugging. Defaults to False.
        keep_browser_open (bool, optional): [--keep-browser-open]. Keep the last browser open after execution for debugging. Defaults to False.
        cdp_url (str | None, optional): [--cdp-url]. [Experimental] Chrome DevTools Protocol URL to connect to an existing browser instance. Disables proxy, headless, keep_browser_open options. Defaults to None.
    """

    await assert_auth_consistent(auth_session)

    input_data = await load_parameters(parameters)

    timeout_value = pytimeparse.parse(timeout)  # type: ignore
    if timeout_value is None:
        raise ValueError(
            f"Invalid timeout format: {timeout}. Please use a valid time format like '10 min' or '600 seconds'."
        )

    await execute_attempt_api_cli(
        api_name=api_name,
        input_data=input_data,
        proxy=proxy,
        auth_session_id=auth_session,
        timeout=timeout_value,
        headless=headless,
        output_file=output_file,
        trace=trace,
        keep_browser_open=keep_browser_open,
        cdp_url=cdp_url,
    )
