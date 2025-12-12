import asyncio
import shutil
from contextlib import asynccontextmanager
from contextlib import AsyncExitStack
from typing import AsyncContextManager
from typing import overload
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from playwright.async_api import BrowserContext
    from playwright.async_api import Page
    from playwright.async_api import ProxySettings

from runtime.env import get_browser_type
from runtime.errors.run_api_errors import AutomationError

from .launch_camoufox import launch_camoufox
from .launch_chromium import launch_chromium


@overload
def launch_browser(
    *,
    cdp_address: str,
) -> "AsyncContextManager[tuple['BrowserContext', 'Page']]": ...


@overload
def launch_browser(
    proxy: "ProxySettings | None" = None,
    headless: bool = False,
    *,
    cdp_port: int | None = None,
) -> "AsyncContextManager[tuple['BrowserContext', 'Page']]": ...


@asynccontextmanager
async def launch_browser(
    proxy: "ProxySettings | None" = None,
    headless: bool = False,
    *,
    cdp_port: int | None = None,
    cdp_address: str | None = None,
):
    browser_type = get_browser_type()
    async with AsyncExitStack() as stack:
        match browser_type:
            case "camoufox":
                if cdp_address:
                    raise AutomationError(ValueError("CDP address is not supported with Camoufox"))
                if cdp_port:
                    raise AutomationError(ValueError("CDP port is not supported with Camoufox"))
                context, page = await stack.enter_async_context(launch_camoufox(headless=headless, proxy=proxy))
            case "brave":
                brave_path = await asyncio.to_thread(shutil.which, "brave-browser-stable")
                if brave_path is None:
                    raise RuntimeError("Brave browser not found")
                context, page = await stack.enter_async_context(
                    launch_chromium(
                        headless=headless,
                        cdp_address=cdp_address,
                        cdp_port=cdp_port,
                        proxy=proxy,
                        executable_path=brave_path,
                    )
                )
            case "chromium" | _:
                context, page = await stack.enter_async_context(
                    launch_chromium(headless=headless, cdp_address=cdp_address, cdp_port=cdp_port, proxy=proxy)
                )
        try:
            yield context, page
        finally:
            from runtime.browser.extensions.intuned_extension import is_intuned_extension_enabled
            from runtime.helpers.extensions import pause_captcha_solver

            if await is_intuned_extension_enabled():
                await pause_captcha_solver(context=context)

            await context.close()
