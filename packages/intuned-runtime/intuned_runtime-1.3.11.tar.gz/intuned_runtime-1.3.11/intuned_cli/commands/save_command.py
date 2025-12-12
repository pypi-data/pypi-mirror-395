from intuned_cli.controller.save import save_project
from intuned_cli.controller.save import validate_intuned_project
from intuned_cli.controller.save import validate_project_name
from intuned_cli.utils.backend import get_intuned_api_auth_credentials
from intuned_cli.utils.error import CLIError
from intuned_cli.utils.wrapper import cli_command


@cli_command
async def save(
    project_name: str | None = None,
    /,
    *,
    workspace_id: str | None = None,
    api_key: str | None = None,
):
    """Saves the project to Intuned without deploying it.

    Args:
        project_name (str | None, optional): The name of the project to save.
        workspace_id (str | None, optional): The ID of the workspace to save to.
        api_key (str | None, optional): The API key to use for authentication.
    """
    try:
        intuned_json = await validate_intuned_project()
    except CLIError as e:
        raise CLIError(
            f"[bold red]Project to be saved is not a valid Intuned project:[/bold red][bright_red] {e}[/bright_red]\n",
            auto_color=False,
        ) from e

    project_name = project_name or intuned_json.project_name
    if not project_name:
        raise CLIError("Project name is required")

    validate_project_name(project_name)

    workspace_id, api_key = await get_intuned_api_auth_credentials(
        intuned_json=intuned_json, workspace_id=workspace_id, api_key=api_key
    )

    await save_project(
        project_name=project_name,
        workspace_id=workspace_id,
        api_key=api_key,
    )
