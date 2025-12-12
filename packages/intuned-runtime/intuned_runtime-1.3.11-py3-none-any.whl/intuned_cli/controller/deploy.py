import asyncio
import json
import time
import urllib.parse
from itertools import cycle
from typing import Any
from typing import Literal

import questionary
from anyio import Path
from pydantic import BaseModel
from pydantic import Field
from pydantic import TypeAdapter

from intuned_cli.controller.save import save_project
from intuned_cli.utils.api_helpers import load_intuned_json
from intuned_cli.utils.backend import get_base_url
from intuned_cli.utils.backend import get_http_client
from intuned_cli.utils.console import console
from intuned_cli.utils.console import questionary_output
from intuned_cli.utils.error import CLIAbortError
from intuned_cli.utils.error import CLIError
from runtime.types.settings_types import IntunedJson

from .authsession import auth_session_instances_dirname
from .authsession import load_auth_session_instance

project_deploy_timeout = 10 * 60
project_deploy_check_period = 5

start_run_input_query_param_key = "startRunInput"


class DeployStatusCompleted(BaseModel):
    model_config = {"populate_by_name": True}

    status: Literal["completed"]
    projectId: str
    message: str | None = None
    default_job_id: str | None = Field(default=None, alias="defaultJobId")
    test_auth_session_id: str | None = Field(default=None, alias="testAuthSessionId")


class DeployStatusOther(BaseModel):
    status: Literal["failed", "pending"]
    message: str | None = None
    reason: str | None = None


DeployStatus = DeployStatusCompleted | DeployStatusOther


async def check_deploy_status(
    *,
    project_name: str,
    workspace_id: str,
    api_key: str,
):
    url = "deploy/result"

    async with get_http_client(
        workspace_id=workspace_id,
        project_name=project_name,
        api_key=api_key,
    ) as client:
        response = await client.get(
            url,
        )
        if response.status_code < 200 or response.status_code >= 300:
            if response.status_code == 401:
                raise CLIError("Invalid API key. Please check your API key and try again.")
            if response.status_code == 404:
                raise CLIError(f"Project '{project_name}' not found in workspace '{workspace_id}'.")
            raise CLIError(f"Failed to check deploy status for project '{project_name}': {response.text}")

    data = response.json()
    try:
        deploy_status = TypeAdapter[DeployStatus](DeployStatus).validate_python(data)
    except Exception as e:
        raise CLIError(f"Failed to parse deploy status response: {e}") from e

    return deploy_status


async def deploy_project(
    *,
    project_name: str,
    workspace_id: str,
    api_key: str,
):
    save_project_result = await save_project(
        project_name=project_name,
        workspace_id=workspace_id,
        api_key=api_key,
    )

    enable_first_run_experience = (
        save_project_result is not None and save_project_result.enable_first_run_experience is True
    )
    settings = await load_intuned_json()

    if enable_first_run_experience:
        first_run_info = await prompt_first_run_experience(settings=settings)
    else:
        first_run_info = (None, None)

    url = "deploy"

    first_run_experience_input_body: dict[str, Any] = {}
    test_auth_session_input, default_job_input = first_run_info
    if test_auth_session_input is not None:
        first_run_experience_input_body["testAuthSessionInput"] = test_auth_session_input
    if default_job_input is not None:
        first_run_experience_input_body["defaultJobInput"] = default_job_input

    async with get_http_client(
        workspace_id=workspace_id,
        project_name=project_name,
        api_key=api_key,
    ) as client:
        response = await client.post(url, json={"firstRunExperienceInput": first_run_experience_input_body})
        if response.status_code < 200 or response.status_code >= 300:
            if response.status_code == 401:
                raise CLIError("Invalid API key. Please check your API key and try again.")

            raise CLIError(
                f"[red bold]Invalid response from server:[/red bold]\n [bright_red]{response.status_code} {response.text}[/bright_red][red bold]\nProject deployment failed.[/red bold]"
            )

    start_time = time.time()

    async def update_console():
        for spinner in cycle("⠙⠹⠸⠼⠴⠦⠧⠇"):
            await asyncio.sleep(0.05)

            time_elapsed_text = f"{time.time() - start_time:.1f}"
            print("\r", end="", flush=True)
            console.print(
                f"{spinner} [cyan]Deploying[/cyan] [bright_black]({time_elapsed_text}s)[/bright_black] ", end=""
            )

    if console.is_terminal:
        update_console_task = asyncio.create_task(update_console())
    else:
        update_console_task = None
        console.print("[cyan]Deploying[/cyan]")

    try:
        while True:
            await asyncio.sleep(project_deploy_check_period)
            if not console.is_terminal:
                time_elapsed_text = f"{time.time() - start_time:.1f}"
                console.print(f"[cyan]Deploying[/cyan] [bright_black]({time_elapsed_text}s)[/bright_black]")

            try:
                deploy_status = await check_deploy_status(
                    project_name=project_name,
                    workspace_id=workspace_id,
                    api_key=api_key,
                )

                if deploy_status.status == "pending":
                    elapsed_time = time.time() - start_time
                    if elapsed_time > project_deploy_timeout:
                        raise CLIError(f"Deployment timed out after {project_deploy_timeout//60} minutes.")
                    continue

                if deploy_status.status == "completed":
                    break

                error_message = (
                    f"[red bold]Project deployment failed:[/bold red]\n{deploy_status.message or 'Unknown error'}\n"
                )
                if deploy_status.reason:
                    error_message += f"Reason: {deploy_status.reason}\n"
                error_message += "[red bold]Project deployment failed[/red bold]"
                raise CLIError(
                    error_message,
                    auto_color=False,
                )
            except Exception:
                if console.is_terminal:
                    print("\r", " " * 100, file=console.file)
                raise
    finally:
        if update_console_task:
            update_console_task.cancel()

    if console.is_terminal:
        print("\r", " " * 100, file=console.file)
    console.print("[green][bold]Project deployed successfully![/bold][/green]")

    assert isinstance(deploy_status, DeployStatusCompleted)
    project_url = f"{get_base_url()}/projects/{deploy_status.projectId}"
    runs_url = f"{project_url}/runs"
    jobs_url = f"{project_url}/jobs"
    runs_playground_url = f"{project_url}/runs?{build_runs_playground_query_params(
        settings=settings,
        enable_first_run_experience=enable_first_run_experience,
        test_auth_session_id=deploy_status.test_auth_session_id,

    )}"
    default_job_trigger_url = (
        f"{jobs_url}/{deploy_status.default_job_id}?action=trigger"
        if deploy_status.default_job_id is not None
        else None
    )
    actions = [
        ("View Project", runs_url),
        *([("Run Playground", runs_playground_url)] if settings.api_access.enabled is True else []),
        ("Manage Jobs", jobs_url),
        *([("Trigger Default Job", default_job_trigger_url)] if default_job_trigger_url is not None else []),
    ]
    terminal_supports_links = console.is_terminal and not console.legacy_windows

    for action in actions:
        label, url = action

        if terminal_supports_links:
            console.print(f"[bold][link={url}][ {label} ][/link][/bold]", end=" ")
        else:
            console.print(f"[bold]{label}:[/bold] [cyan underline]{url}[/cyan underline]")

    if terminal_supports_links:
        console.print("")


async def prompt_first_run_experience(settings: IntunedJson):
    test_auth_session_input: Any | None = None
    should_prompt_test_auth_session = settings.auth_sessions.enabled is True and settings.auth_sessions.type == "API"

    metadata = settings.metadata

    default_job_input = metadata.default_job_input if metadata else None
    should_prompt_for_default_job = default_job_input is not None
    if should_prompt_test_auth_session:
        test_auth_session_input = await prompt_first_run_experience_test_auth_session_parameters(
            should_prompt_for_default_job=should_prompt_for_default_job
        )
        if test_auth_session_input is None:
            return None, None

    if should_prompt_for_default_job:
        default_job_input = await prompt_first_run_experience_default_job_parameters(
            default_job_input=default_job_input
        )

    return test_auth_session_input, default_job_input


async def prompt_first_run_experience_test_auth_session_parameters(*, should_prompt_for_default_job: bool):
    global auth_session_instances_dirname
    auth_session_instances_path = Path(auth_session_instances_dirname)

    if not await auth_session_instances_path.exists():
        return

    auth_session_dirs = [d async for d in auth_session_instances_path.iterdir() if await d.is_dir()]

    if len(auth_session_dirs) == 0:
        return

    auth_session_id = auth_session_dirs[0].name

    _, metadata = await load_auth_session_instance(auth_session_id)

    if should_prompt_for_default_job:
        message = f"Create a test auth session using {auth_session_id} parameters? (required for creating default job)"
    else:
        message = f"Create a test auth session using {auth_session_id} parameters?"

    result: bool | None = await questionary.confirm(message=message, default=True, output=questionary_output).ask_async(
        kbi_msg=""
    )

    if result is None:
        raise CLIAbortError()

    return metadata.auth_session_input


async def prompt_first_run_experience_default_job_parameters(default_job_input: dict[str, Any]):
    pass
    result: bool | None = await questionary.confirm(
        message="Create a default job with sample parameters?", default=True, output=questionary_output
    ).ask_async(kbi_msg="")

    if result is None:
        raise CLIAbortError()
    if result is True:
        return default_job_input
    return None


async def get_default_job_exists(
    *,
    project_name: str,
    workspace_id: str,
    api_key: str,
):
    async with get_http_client(
        workspace_id=workspace_id,
        project_name=project_name,
        api_key=api_key,
    ) as client:
        response = await client.get(
            "jobs/default",
        )
        if response.status_code == 404:
            return False
        if response.status_code < 200 or response.status_code >= 300:
            raise CLIError(f"Failed to check default job existence for project '{project_name}': {response.text}")
    return True


def build_runs_playground_query_params(
    *,
    enable_first_run_experience: bool = False,
    settings: IntunedJson,
    test_auth_session_id: str | None = None,
):
    def get_params():
        params: dict[str, str] = {start_run_input_query_param_key: "{}"}
        if not settings.metadata:
            return params
        if not enable_first_run_experience:
            return params
        input = settings.metadata.default_run_playground_input or {}
        if test_auth_session_id:
            input["authSessionId"] = test_auth_session_id
        params = {start_run_input_query_param_key: json.dumps(input)}

        return params

    return urllib.parse.urlencode(get_params())
