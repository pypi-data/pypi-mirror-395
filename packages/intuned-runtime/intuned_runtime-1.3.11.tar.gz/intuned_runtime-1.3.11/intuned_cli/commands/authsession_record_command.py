import pytimeparse  # type: ignore

from intuned_cli.controller.authsession import execute_record_auth_session_cli
from intuned_cli.utils.auth_session_helpers import assert_auth_enabled
from intuned_cli.utils.auth_session_helpers import get_auth_session_recorder_parameters
from intuned_cli.utils.wrapper import cli_command
from runtime.env import get_is_auth_session_recorder_enabled

if get_is_auth_session_recorder_enabled():

    @cli_command
    async def authsession__record(
        *,
        id: str | None = None,
        check_attempts: int = 1,
        proxy: str | None = None,
        timeout: str = "10 min",
        headless: bool = False,
        trace: bool = False,
        keep_browser_open: bool = False,
        cdp_url: str | None = None,
    ):
        """Record a recorder-based auth session and then execute an AuthSession:Validate run to validate it

        Args:
            id (str | None, optional): ID of the auth session to record. If not provided, a new ID will be generated.
            check_attempts (int, optional): [--check-attempts]. Number of attempts to check the auth session validity after it is created. Defaults to 1.
            proxy (str | None, optional): [--proxy]. Proxy URL to use for recorder session and validation. Defaults to None.
            timeout (str, optional): [--timeout]. Timeout for the auth session command - seconds or pytimeparse-formatted string. Defaults to "10 min".
            headless (bool, optional): [--headless]. Run the auth session validation in headless mode (default: False). This will not open a browser window. The recorder will always be non-headless.
            trace (bool, optional): [--trace]. Capture a trace of each attempt, useful for debugging. Defaults to False.
            keep_browser_open (bool, optional): [--keep-browser-open]. Keep the last browser open after execution for debugging. Defaults to False.
            cdp_url (str | None, optional): [--cdp-url]. [Experimental] Chrome DevTools Protocol URL to connect to an existing browser instance. Disables proxy, headless, keep_browser_open options. Defaults to None.
        """

        await assert_auth_enabled(auth_type="MANUAL")

        timeout_value = pytimeparse.parse(timeout)  # type: ignore
        if timeout_value is None:
            raise ValueError(
                f"Invalid timeout format: {timeout}. Please use a valid time format like '10 min' or '600 seconds'."
            )

        start_url, finish_url = await get_auth_session_recorder_parameters()

        await execute_record_auth_session_cli(
            start_url=start_url,
            finish_url=finish_url,
            id=id,
            check_retries=check_attempts,
            headless=headless,
            proxy=proxy,
            timeout=timeout_value,
            trace=trace,
            keep_browser_open=keep_browser_open,
            cdp_url=cdp_url,
        )
else:
    authsession__record = None  # type: ignore
