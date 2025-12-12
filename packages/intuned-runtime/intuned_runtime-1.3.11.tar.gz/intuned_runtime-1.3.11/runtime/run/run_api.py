import asyncio
import functools
import json
import sys
from collections.abc import Callable
from contextlib import AsyncExitStack
from importlib import import_module
from inspect import iscoroutinefunction
from typing import Any
from typing import Awaitable
from typing import cast
from typing import Optional
from typing import Protocol

from git import TYPE_CHECKING

from runtime.browser.storage_state import get_storage_state
from runtime.browser.storage_state import set_storage_state
from runtime.context import IntunedContext
from runtime.errors.run_api_errors import InvalidSessionError
from runtime.errors.run_api_errors import ResultTooBigError
from runtime.errors.run_api_errors import RunApiError
from runtime.run.playwright_context import playwright_context
from runtime.types import RunAutomationSuccessResult
from runtime.types.run_types import PayloadToAppend
from runtime.types.run_types import RunApiParameters

from ..errors import ApiNotFoundError
from ..errors import AutomationError
from ..errors import AutomationNotCoroutineError
from ..errors import NoAutomationInApiError
from .playwright_tracing import playwright_tracing
from .pydantic_encoder import PydanticEncoder
from .types import ImportFunction

if TYPE_CHECKING:
    from playwright.async_api import Page


def get_object_size_in_bytes(obj: Any) -> int:
    """Calculate the approximate size of an object in bytes."""
    try:
        return len(json.dumps(obj, cls=PydanticEncoder).encode("utf-8"))
    except (TypeError, ValueError):
        # If JSON serialization fails, return a conservative estimate
        return len(str(obj).encode("utf-8"))


def import_function_from_api_dir(
    *,
    file_path: str,
    base_dir: Optional[str] = None,
    automation_function_name: str | None = None,
) -> Callable[..., Awaitable[Any]]:
    module_path = file_path.replace("/", ".")

    def _import_module():
        if base_dir is not None:
            sys.path.insert(0, base_dir)
        return import_module(module_path)

    try:
        module = _import_module()

    except ModuleNotFoundError as e:
        # if the top-level module does not exist, it is a 404
        if e.name == module_path or e.name == module_path.split(".", 1)[0]:
            raise ApiNotFoundError(module_path) from e

        # otherwise, it is an import error inside the user code
        raise AutomationError(e) from e
    except RunApiError:
        raise
    except BaseException as e:
        raise AutomationError(e) from e

    automation_functions_to_try: list[str] = []
    if automation_function_name is not None:
        automation_functions_to_try.append(automation_function_name)
    else:
        automation_functions_to_try.append("automation")
        automation_functions_to_try.append("create")
        automation_functions_to_try.append("check")

    err: AttributeError | None = None
    automation_coroutine = None

    name = automation_functions_to_try[0]
    for n in automation_functions_to_try:
        name = n
        try:
            automation_coroutine = getattr(module, name)
        except AttributeError as e:
            err = e
        else:
            break

    if automation_coroutine is None:
        raise NoAutomationInApiError(module_path, automation_functions_to_try) from err

    if not iscoroutinefunction(automation_coroutine):
        raise AutomationNotCoroutineError(module_path)

    return automation_coroutine


class AutomationFunction(Protocol):
    def __call__(
        self, page: "Page", parameters: dict[Any, Any] | None = None, *args: Any, **kwargs: Any
    ) -> Awaitable[Any]: ...


async def run_api(
    parameters: RunApiParameters,
    *,
    import_function: ImportFunction | None = None,
) -> RunAutomationSuccessResult:
    from playwright.async_api import ProxySettings

    import_function = import_function or (
        lambda file_path, name=None: import_function_from_api_dir(file_path=file_path, automation_function_name=name)
    )

    async with AsyncExitStack() as stack:
        _initialize_playwright_context = functools.partial(
            playwright_context,
            import_function=import_function,
            api_name=parameters.automation_function.name,
            api_parameters=parameters.automation_function.params,
        )
        if parameters.run_options.environment == "standalone":
            proxy_config = parameters.run_options.proxy
            if proxy_config is not None:
                proxy = ProxySettings(
                    **proxy_config.model_dump(by_alias=True),
                )
            else:
                proxy = None

            context, page = await stack.enter_async_context(
                _initialize_playwright_context(
                    proxy=proxy,
                    headless=parameters.run_options.headless,
                )
            )

        else:
            context, page = await stack.enter_async_context(
                _initialize_playwright_context(
                    cdp_address=parameters.run_options.cdp_address,
                )
            )

        if parameters.tracing.enabled is True:
            await stack.enter_async_context(
                playwright_tracing(
                    context=context,
                    trace_path=parameters.tracing.file_path,
                    screenshots=True,
                    snapshots=True,
                    sources=True,
                )
            )

        if parameters.auth is not None and parameters.auth.session.type == "state":
            if parameters.auth.session.state is None:
                raise InvalidSessionError()
            state = parameters.auth.session.state
            await set_storage_state(
                context=context,
                state=state,
            )

        async def _run_automation():
            try:
                automation_function = cast(AutomationFunction, import_function(parameters.automation_function.name))

                automation_function = functools.partial(automation_function, page)
                if parameters.automation_function.params is None:
                    automation_result = await automation_function()
                else:
                    automation_result = await automation_function(parameters.automation_function.params)
                try:
                    automation_result = json.loads(json.dumps(automation_result, cls=PydanticEncoder))
                except TypeError as e:
                    raise AutomationError(TypeError("Result is not JSON serializable")) from e

                # Check if result size exceeds 2MB limit
                MAX_RESULT_SIZE_BYTES = 2 * 1024 * 1024  # 2MB
                result_size_in_bytes = get_object_size_in_bytes(automation_result)
                if result_size_in_bytes > MAX_RESULT_SIZE_BYTES:
                    raise ResultTooBigError(result_size_in_bytes, MAX_RESULT_SIZE_BYTES)

                response = RunAutomationSuccessResult(
                    result=automation_result,
                )
                extended_payloads = IntunedContext.current().extended_payloads
                if extended_payloads:
                    for payload in extended_payloads:
                        try:
                            payload["parameters"] = json.loads(json.dumps(payload["parameters"], cls=PydanticEncoder))
                        except TypeError as e:
                            raise AutomationError(TypeError("Parameters are not JSON serializable")) from e
                    response.payload_to_append = [
                        PayloadToAppend(
                            api_name=payload["api"],
                            parameters=payload["parameters"],
                        )
                        for payload in extended_payloads
                    ]
                if parameters.retrieve_session:
                    response.session = await get_storage_state(context)
                return response
            except RunApiError as e:
                raise e
            except Exception as e:
                # Get all public attributes of the exception
                raise AutomationError(e) from e

        automation_task = asyncio.create_task(_run_automation())
        try:
            # Shield will make the CancelledError get thrown directly here instead of inside `automation_task`
            return await asyncio.shield(automation_task)
        except asyncio.CancelledError:
            # Manually cancel the automation task
            if not automation_task.done():
                automation_task.cancel()
                try:
                    # Wait for the automation task to be cancelled for a brief moment
                    await asyncio.wait_for(automation_task, timeout=0.1)
                except (asyncio.CancelledError, asyncio.TimeoutError):
                    pass
            raise  # Re-raise the cancellation

    raise RuntimeError("Unreachable code path")
