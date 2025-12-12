import asyncio
import datetime
import json
import time
from typing import Any
from typing import Literal
from typing import TYPE_CHECKING
from typing import Unpack

from anyio import Path
from pydantic import BaseModel
from pydantic import Field
from pydantic import ValidationError

from intuned_cli.types import BaseExecuteCommandOptions
from intuned_cli.types import BaseExecuteCommandOptionsWithoutTrace
from intuned_cli.utils.api_helpers import assert_api_file_exists
from intuned_cli.utils.browser import get_cli_run_options
from intuned_cli.utils.console import console
from intuned_cli.utils.error import CLIError
from intuned_cli.utils.error import log_automation_error
from intuned_cli.utils.get_auth_parameters import register_get_auth_session_parameters
from intuned_cli.utils.import_function import get_cli_import_function
from intuned_cli.utils.timeout import extendable_timeout
from intuned_cli.utils.traces import cli_trace
from runtime.browser.storage_state import get_storage_state
from runtime.errors.run_api_errors import AutomationError
from runtime.run.run_api import run_api
from runtime.types.run_types import Auth
from runtime.types.run_types import AutomationFunction
from runtime.types.run_types import ProxyConfig
from runtime.types.run_types import RunApiParameters
from runtime.types.run_types import StateSession
from runtime.types.run_types import StorageState

if TYPE_CHECKING:
    from playwright.async_api import ProxySettings

auth_session_instances_dirname = "auth-sessions-instances"


class AuthSessionMetadata(BaseModel):
    created_at: str = Field(alias="createdAt")
    updated_at: str = Field(alias="updatedAt")
    auth_session_id: str = Field(alias="authSessionId")
    auth_session_type: Literal["MANUAL", "API"] = Field(alias="authSessionType")
    auth_session_input: dict[str, Any] | None = Field(alias="authSessionInput", default=None)
    recorder_start_url: str | None = Field(alias="recorderStartUrl", default=None)
    recorder_end_url: str | None = Field(alias="recorderEndUrl", default=None)


async def execute_run_validate_auth_session_cli(
    *,
    id: str,
    auto_recreate: bool,
    check_retries: int,
    create_retries: int,
    **kwargs: Unpack[BaseExecuteCommandOptions],
) -> StorageState:
    """
    Validate auth session with optional auto-recreation.
    """
    console.print(f"[bold]Validating auth session with id [cyan]{id}[/cyan][/bold]")

    register_get_auth_session_parameters(id)

    # Get auth session instance and path
    instance, metadata = await load_auth_session_instance(id)

    await assert_api_file_exists("auth-sessions", "check")

    check_result = await run_check_with_retries(
        auth=instance,
        retries=check_retries,
        **kwargs,
    )

    if not check_result:
        if not auto_recreate:
            if metadata and metadata.auth_session_type == "MANUAL":
                raise CLIError("Auth session validation failed")
            raise CLIError("Auto recreate is disabled, please provide a new auth session or update it manually")

        if metadata and metadata.auth_session_type == "MANUAL":
            raise CLIError("Auth session is recorder-based, please provide a new one or update it manually")

        console.print("[bold]Auto recreate is enabled - trying to re-create it[/bold]")

        await assert_api_file_exists("auth-sessions", "create")

        auth_session_input = (metadata.auth_session_input or {}) if metadata else {}

        instance = await run_create_with_retries(
            auth_session_id=id,
            auth_session_input=auth_session_input,
            retries=create_retries,
            metadata=metadata,
            **kwargs,
        )

        # Rerun check after refresh
        check_result = await run_check_with_retries(
            auth=instance,
            retries=check_retries,
            **kwargs,
        )
        if not check_result:
            raise CLIError("Failed to re-create auth session")

    console.print("[bold][green]Auth session validated successfully[/green][/bold]")
    return instance


async def execute_run_create_auth_session_cli(
    *,
    id: str | None = None,
    input_data: Any,
    check_retries: int,
    create_retries: int,
    log: bool = True,
    metadata: AuthSessionMetadata | None = None,
    **kwargs: Unpack[BaseExecuteCommandOptions],
):
    """
    Create a new auth session.
    """
    if id is None:
        id = generate_auth_session_id()

    if log:
        console.print(f"[bold]Creating auth session with id [cyan]{id}[/cyan][/bold]")

    await assert_api_file_exists("auth-sessions", "create")
    await assert_api_file_exists("auth-sessions", "check")

    instance = await run_create_with_retries(
        auth_session_id=id,
        auth_session_input=input_data,
        retries=create_retries,
        metadata=metadata,
        **kwargs,
    )

    check_result = await run_check_with_retries(
        auth=instance,
        retries=check_retries,
        **kwargs,
    )
    if not check_result:
        raise CLIError("Failed to create auth session")

    if log:
        console.print("[bold][green]Auth session created successfully[/green][/bold]")


async def execute_run_update_auth_session_cli(
    *,
    id: str,
    input_data: Any | None = None,
    check_retries: int,
    create_retries: int,
    **kwargs: Unpack[BaseExecuteCommandOptions],
):
    """
    Update an existing auth session.
    """
    console.print(f"[bold]Updating auth session with id [cyan]{id}[/cyan][/bold]")

    _, metadata = await load_auth_session_instance(id)
    if metadata and metadata.auth_session_type == "MANUAL":
        raise CLIError("Auth session is recorder-based, it cannot be updated.")

    if input_data is None:
        input_data = metadata.auth_session_input if metadata else {}

    await assert_api_file_exists("auth-sessions", "create")
    await assert_api_file_exists("auth-sessions", "check")

    await execute_run_create_auth_session_cli(
        id=id,
        input_data=input_data,
        check_retries=check_retries,
        create_retries=create_retries,
        log=False,
        metadata=metadata,
        **kwargs,
    )

    console.print("[bold][green]Auth session updated successfully[/green][/bold]")


async def execute_attempt_create_auth_session_cli(
    *,
    id: str | None = None,
    input_data: Any,
    **kwargs: Unpack[BaseExecuteCommandOptions],
):
    """
    Execute a single attempt to create auth session.
    """
    if id is None:
        id = generate_auth_session_id(is_attempt=True)

    console.print(f"[bold]Executing create auth session attempt with id [cyan]{id}[/cyan][/bold]")
    await assert_api_file_exists("auth-sessions", "create")
    await run_create_with_retries(
        auth_session_id=id,
        auth_session_input=input_data,
        retries=None,
        **kwargs,
    )


async def execute_attempt_check_auth_session_cli(*, id: str, **kwargs: Unpack[BaseExecuteCommandOptions]):
    """
    Execute a single attempt to check auth session.
    """
    console.print(f"[bold]Executing check auth session attempt with id [cyan]{id}[/cyan][/bold]")
    await assert_api_file_exists("auth-sessions", "check")

    register_get_auth_session_parameters(id)

    instance, _ = await load_auth_session_instance(id)

    check_result = await run_check_with_retries(
        auth=instance,
        retries=None,
        **kwargs,
    )

    if not check_result:
        raise CLIError("Check failed")

    console.print("[bold green]Auth session check successful[/bold green]")


async def run_check(
    *, auth: StorageState, trace_id: str | None = None, **kwargs: Unpack[BaseExecuteCommandOptionsWithoutTrace]
) -> bool:
    """
    Run auth session check.
    """
    timeout = kwargs.get("timeout")
    headless = kwargs.get("headless")
    proxy = kwargs.get("proxy")
    keep_browser_open = kwargs.get("keep_browser_open")
    cdp_url = kwargs.get("cdp_url")
    with cli_trace(trace_id) as tracing:
        async with extendable_timeout(timeout):
            result = await run_api(
                RunApiParameters(
                    automation_function=AutomationFunction(
                        name="auth-sessions/check",
                        params=None,
                    ),
                    run_options=await get_cli_run_options(
                        headless=headless,
                        proxy=ProxyConfig.parse_from_str(proxy) if proxy else None,
                        keep_browser_open=keep_browser_open,
                        cdp_url=cdp_url,
                    ),
                    auth=Auth(
                        session=StateSession(
                            state=auth,
                        ),
                    ),
                    tracing=tracing,
                ),
                import_function=await get_cli_import_function(),
            )

            if not result.result:
                return False

            return bool(result.result)


async def run_create(
    *,
    auth_session_input: dict[str, Any],
    trace_id: str | None = None,
    **kwargs: Unpack[BaseExecuteCommandOptionsWithoutTrace],
) -> StorageState:
    """
    Run auth session create.
    """

    timeout = kwargs.get("timeout")
    headless = kwargs.get("headless")
    proxy = kwargs.get("proxy")
    keep_browser_open = kwargs.get("keep_browser_open")
    cdp_url = kwargs.get("cdp_url")
    with cli_trace(trace_id) as tracing:
        async with extendable_timeout(timeout):
            result = await run_api(
                RunApiParameters(
                    automation_function=AutomationFunction(
                        name="auth-sessions/create",
                        params=auth_session_input,
                    ),
                    run_options=await get_cli_run_options(
                        headless=headless,
                        proxy=ProxyConfig.parse_from_str(proxy) if proxy else None,
                        keep_browser_open=keep_browser_open,
                        cdp_url=cdp_url,
                    ),
                    retrieve_session=True,
                    tracing=tracing,
                ),
                import_function=await get_cli_import_function(),
            )
            if not result.session:
                raise Exception("Auth session create did not return a session")
            return result.session


async def run_check_with_retries(
    *,
    auth: StorageState,
    retries: int | None,
    trace: bool,
    **kwargs: Unpack[BaseExecuteCommandOptionsWithoutTrace],
) -> bool:
    """
    Run auth session check with retries.
    """
    for i in range(retries or 1):
        attempt_text = "" if i == 0 else f" [italic](Attempt {i + 1})[/italic]"
        console.print(f"\n[bold]Running [cyan]auth session check[/cyan]{attempt_text}...[/bold]\n")

        try:
            trace_id: str | None = None
            if trace:
                trace_id = "authsession-check-attempt"
                if retries is not None:
                    trace_id += f"-{i+1}"
            check_result = await run_check(
                auth=auth,
                trace_id=trace_id,
                **kwargs,
            )

            if check_result:
                console.print("[bold][green]Auth session check passed[/green][/bold]")
                return True
        except AutomationError as e:
            log_automation_error(e)
            continue

    console.print(f"[bold][red]Auth session check failed after {retries} attempt(s)[/red][/bold]")
    return False


async def run_create_with_retries(
    *,
    auth_session_id: str,
    auth_session_input: dict[str, Any],
    retries: int | None,
    metadata: AuthSessionMetadata | None = None,
    trace: bool,
    **kwargs: Unpack[BaseExecuteCommandOptionsWithoutTrace],
):
    """
    Run auth session create with retries.
    """
    new_auth_session_instance: StorageState | None = None

    for i in range(retries or 1):
        attempt_text = "" if i == 0 else f" [italic](Attempt {i + 1})[/italic]"
        console.print(f"\n[bold]Running [cyan]auth session create[/cyan]{attempt_text}...[/bold]\n")

        try:
            trace_id: str | None = None
            if trace:
                trace_id = "authsession-create-attempt"
                if retries is not None:
                    trace_id += f"-{i+1}"

            new_auth_session_instance = await run_create(
                auth_session_input=auth_session_input,
                trace_id=trace_id,
                **kwargs,
            )
            console.print("[bold][green]Auth session create succeeded[/green][/bold]")
            break
        except AutomationError as e:
            log_automation_error(e)
            continue

    if not new_auth_session_instance:
        raise CLIError(f"Failed to create auth session after {retries} attempt(s)")

    await store_auth_session_instance(new_auth_session_instance, auth_session_id, auth_session_input, metadata=metadata)

    return new_auth_session_instance


async def load_auth_session_instance(auth_session_id: str) -> tuple[StorageState, AuthSessionMetadata]:
    """
    Retrieve auth session instance storage path by ID.
    """
    # Placeholder implementation - will be replaced with actual retrieval logic
    auth_session_instances_path = get_auth_session_path(auth_session_id)

    instance_path = auth_session_instances_path / "auth-session.json"

    if not await instance_path.exists():
        raise CLIError(f"Auth session instance with ID {auth_session_id} not found")

    metadata_path = auth_session_instances_path / "metadata.json"

    if not await metadata_path.exists():
        raise CLIError(f"Metadata for auth session instance with ID {auth_session_id} not found")

    try:
        instance_text_content = await instance_path.read_text()

        instance = StorageState.model_validate_json(instance_text_content)

        metadata_text_content = await metadata_path.read_text()

        metadata = AuthSessionMetadata.model_validate_json(metadata_text_content)
    except ValidationError as e:
        raise CLIError(f"Failed to parse auth session instance or metadata: {e}") from e

    return instance, metadata


async def store_auth_session_instance(
    auth_session_instance: StorageState,
    auth_session_id: str,
    auth_session_input: dict[str, Any] | None = None,
    metadata: AuthSessionMetadata | None = None,
):
    """
    Store auth session instance with metadata.
    """

    # Create directory path
    auth_session_path = get_auth_session_path(auth_session_id)
    await auth_session_path.mkdir(parents=True, exist_ok=True)

    # Store the session data
    instance_file_path = auth_session_path / "auth-session.json"
    instance_json = json.dumps(auth_session_instance.model_dump(by_alias=True), indent=2)
    await instance_file_path.write_text(instance_json)
    # Store metadata
    metadata = AuthSessionMetadata(
        createdAt=metadata.created_at if metadata else datetime.datetime.now().isoformat(),
        updatedAt=datetime.datetime.now().isoformat(),
        authSessionId=auth_session_id,
        authSessionInput=auth_session_input,
        authSessionType=metadata.auth_session_type if metadata else "API",
    )
    metadata_file_path = auth_session_path / "metadata.json"

    metadata_json = json.dumps(metadata.model_dump(by_alias=True, exclude_none=True), indent=2)
    await metadata_file_path.write_text(metadata_json)


def get_auth_session_path(auth_session_id: str):
    return Path(auth_session_instances_dirname) / auth_session_id


async def execute_record_auth_session_cli(
    *,
    start_url: str,
    finish_url: str,
    id: str | None = None,
    check_retries: int = 1,
    **kwargs: Unpack[BaseExecuteCommandOptions],
):
    """
    Record a new auth session using a browser.
    """

    from playwright.async_api import ProxySettings

    if id is None:
        id = generate_auth_session_id()

    console.print(f"[bold]Recording auth session with id [cyan]{id}[/cyan][/bold]")
    proxy = kwargs.get("proxy")

    proxy_settings: ProxySettings | None = None
    if proxy:
        proxy_settings = ProxySettings(server=proxy)

    try:
        auth_session = await record_auth_session(
            start_url=start_url,
            finish_url=finish_url,
            timeout=kwargs.get("timeout"),
            proxy=proxy_settings,
        )
    except CLIError as e:
        raise CLIError(f"Failed to record auth session: {e}") from e

    await store_auth_session_instance(
        auth_session_instance=auth_session,
        auth_session_id=id,
        metadata=AuthSessionMetadata(
            createdAt=datetime.datetime.now().isoformat(),
            updatedAt=datetime.datetime.now().isoformat(),
            authSessionId=id,
            authSessionInput=None,
            authSessionType="MANUAL",
            recorderStartUrl=start_url,
            recorderEndUrl=finish_url,
        ),
    )

    await execute_run_validate_auth_session_cli(
        id=id,
        create_retries=1,
        check_retries=check_retries,
        auto_recreate=False,
        **kwargs,
    )

    console.print(f"[bold][green]Auth session [cyan]{id}[/cyan] recorded successfully[/green][/bold]")


async def record_auth_session(
    *,
    start_url: str,
    finish_url: str,
    timeout: float = 300,
    proxy: "ProxySettings | None" = None,
):
    from runtime.browser import launch_chromium

    async with launch_chromium(
        proxy=proxy,
        headless=False,
        app_mode_initial_url=start_url,
    ) as (context, page):
        if not page.url.startswith(start_url):
            await page.goto(start_url)
        console.print(f"[bold]Navigated to[/bold] [underline]{start_url}[/underline]")
        console.print(f"[bold]Waiting for[/bold] [underline]{finish_url}[/underline]...")

        try:
            async with asyncio.timeout(timeout):
                while True:
                    if len(context.pages) == 0:
                        raise CLIError("Browser was closed before reaching the finish URL")
                    if context.pages[0].url.startswith(finish_url):
                        break
                    await asyncio.sleep(1)

            console.print("[bold]Finish URL reached, capturing auth session...[/bold]")
            await page.wait_for_load_state("load")
            auth_session = await get_storage_state(context)
            return auth_session
        except asyncio.TimeoutError as e:
            raise CLIError("Timeout waiting for finish URL") from e


def generate_auth_session_id(is_attempt: bool = False) -> str:
    timestamp = int(time.time() * 1000)
    if is_attempt:
        return f"auth-session-attempt-{timestamp}"
    return f"auth-session-{timestamp}"
