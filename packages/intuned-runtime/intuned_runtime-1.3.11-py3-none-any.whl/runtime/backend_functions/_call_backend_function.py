import json
from typing import Any
from typing import Literal

from httpx import AsyncClient
from pydantic import BaseModel

from runtime.constants import api_key_header_name
from runtime.context.context import IntunedContext
from runtime.env import get_api_key
from runtime.env import get_functions_domain
from runtime.env import get_is_running_in_cli
from runtime.env import get_project_id
from runtime.env import get_workspace_id


async def call_backend_function[T: BaseModel](
    name: str,
    validation_model: type[T],
    *,
    method: Literal["GET", "POST"] = "GET",
    params: BaseModel | None = None,
) -> T:
    """
    Get the auth session parameters from the IntunedContext.
    """
    functions_domain, workspace_id, project_id = get_functions_domain(), get_workspace_id(), get_project_id()

    if functions_domain is None or workspace_id is None or project_id is None:
        if get_is_running_in_cli():
            raise Exception(
                "API credentials not set - make sure to save your project to Intuned to set up the correct API credentials."
            )

        raise Exception("No workspace ID or project ID found.")

    context = IntunedContext.current()

    async with AsyncClient() as client:
        api_key = get_api_key()
        if api_key is not None:
            client.headers[api_key_header_name] = api_key

        if context.functions_token:
            client.headers["Authorization"] = f"Bearer {context.functions_token}"
        if params:
            client.headers["Content-Type"] = "application/json"
        path = f"{functions_domain}/api/{workspace_id}/functions/{project_id}/{name}"
        body = params.model_dump() if params else None

        response = await client.request(
            method,
            path,
            json=body,
        )
        try:
            response_json = response.json()
        except json.JSONDecodeError as e:
            raise CallBackendException(
                response.status_code,
                f"Expected JSON response, but got: {response.text}",
            ) from e
        if not isinstance(response_json, dict):
            raise CallBackendException(
                response.status_code,
                f"Expected JSON object, but got: {response_json}",
            )
        if 200 <= response.status_code < 300:
            return validation_model.model_validate(response_json)
        if response.status_code == 401 and get_is_running_in_cli():
            raise CallBackendException(
                response.status_code,
                "Unauthorized backend function call - make sure to save your project to Intuned to set up the correct API credentials",
            )
        raise CallBackendException(
            response.status_code,
            f"Calling backend function errored with status {response.status_code}: {response_json}",
        )


class CallBackendException(Exception):
    def __init__(self, status_code: int, body: str | dict[str, Any]):
        message = "Unknown error"
        if isinstance(body, str):
            message = body
        else:
            body_message = body.get("message") or body.get("error")
            if body_message:
                message = str(body_message)
            else:
                message = json.dumps(body)
        super().__init__(message)
        self.status_code = status_code
        self.body = body
