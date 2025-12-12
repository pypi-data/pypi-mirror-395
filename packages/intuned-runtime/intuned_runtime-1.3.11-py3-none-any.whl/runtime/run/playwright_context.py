import asyncio
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from contextlib import AsyncExitStack
from typing import Any
from typing import AsyncContextManager
from typing import overload
from typing import TYPE_CHECKING
from typing import TypedDict
from typing import Unpack

from ..browser.helpers import get_local_cdp_address
from ..browser.launch_browser import launch_browser
from ..errors.run_api_errors import AutomationError
from ..errors.run_api_errors import InvalidAPIError
from ..run.types import ImportFunction
from .setup_context_hook import load_setup_context_hook
from .setup_context_hook import setup_context_hook_function_name

if TYPE_CHECKING:
    from playwright.async_api import BrowserContext
    from playwright.async_api import Page
    from playwright.async_api import ProxySettings


class _CommonKwargs(TypedDict):
    import_function: "ImportFunction"
    api_name: str
    api_parameters: Any


@overload
def playwright_context(
    *,
    proxy: "ProxySettings | None" = None,
    headless: bool = False,
    **kwargs: Unpack[_CommonKwargs],
) -> "AsyncContextManager[tuple[BrowserContext, Page]]": ...
@overload
def playwright_context(
    *,
    cdp_address: str | None = None,
    **kwargs: Unpack[_CommonKwargs],
) -> "AsyncContextManager[tuple[BrowserContext, Page]]": ...


@asynccontextmanager
async def playwright_context(
    *,
    proxy: "ProxySettings | None" = None,
    headless: bool = False,
    cdp_address: str | None = None,
    **kwargs: Unpack[_CommonKwargs],
) -> "AsyncGenerator[tuple[BrowserContext, Page], None]":
    setup_context_hook = load_setup_context_hook(import_function=kwargs["import_function"])

    if setup_context_hook is None:
        if cdp_address:
            async with launch_browser(
                cdp_address=cdp_address,
            ) as (context, page):
                yield context, page
        else:
            async with launch_browser(
                proxy=proxy,
                headless=headless,
            ) as (context, page):
                yield context, page
        return

    if cdp_address is not None:
        cdp_port = None
        hook_cdp_url = cdp_address
    else:
        cdp_port = await get_random_free_port()
        hook_cdp_url = get_local_cdp_address(cdp_port)

    async with AsyncExitStack() as stack:
        if cdp_address:
            context, page = await stack.enter_async_context(
                launch_browser(
                    cdp_address=cdp_address,
                )
            )
        else:
            context, page = await stack.enter_async_context(
                launch_browser(
                    proxy=proxy,
                    headless=headless,
                    cdp_port=cdp_port,
                )
            )
        try:
            hook_result = await setup_context_hook(
                api_name=kwargs["api_name"],
                api_parameters=kwargs["api_parameters"],
                cdp_url=hook_cdp_url,
            )
        except Exception as e:
            raise AutomationError(e) from e

        if hook_result is None:
            yield context, page
            return

        new_context: "BrowserContext | None" = None  # noqa: UP037
        try:
            if not isinstance(hook_result, tuple):
                new_context = hook_result
                yield new_context, page
                return

            if len(hook_result) == 2:
                new_context, new_page = hook_result

                yield new_context, new_page or page
                return

            if len(hook_result) == 3:
                new_context, new_page, cleanup = hook_result

                try:
                    yield new_context, new_page or page
                    return
                finally:
                    try:
                        await cleanup()
                    except Exception as e:
                        raise AutomationError(e) from e

            raise InvalidAPIError(
                f"{setup_context_hook_function_name} hook returned an invalid value. Return value must be one of: None, BrowserContext, (BrowserContext, Page | None), (BrowserContext, Page | None, Callable[..., Awaitable[None]])"
            )
        finally:
            if new_context is not None and new_context != context:
                await new_context.close()


async def get_random_free_port() -> int:
    def get_random_free_port_sync():
        import socket

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("", 0))
            return s.getsockname()[1]

    return await asyncio.to_thread(get_random_free_port_sync)
