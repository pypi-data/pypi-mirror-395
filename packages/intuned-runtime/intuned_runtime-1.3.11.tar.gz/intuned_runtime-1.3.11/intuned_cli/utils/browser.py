from typing import Any
from typing import AsyncContextManager
from typing import TYPE_CHECKING

from runtime.types.run_types import CDPRunOptions
from runtime.types.run_types import ProxyConfig
from runtime.types.run_types import StandaloneRunOptions

if TYPE_CHECKING:
    from playwright.async_api import BrowserContext

_current_browser_context_manager: AsyncContextManager[Any] | None = None
_current_browser_context: "BrowserContext | None" = None


async def get_cli_run_options(
    headless: bool = False,
    proxy: ProxyConfig | None = None,
    keep_browser_open: bool = False,
    cdp_url: str | None = None,
):
    global _current_browser_context_manager, _current_browser_context
    if cdp_url is not None:
        await close_cli_browser()
        return CDPRunOptions(
            cdp_address=cdp_url,
        )
    if not keep_browser_open:
        return StandaloneRunOptions(
            headless=headless,
            proxy=proxy,
        )
    from playwright.async_api import ProxySettings

    from runtime.browser.launch_chromium import launch_chromium
    from runtime.run.playwright_context import get_random_free_port

    await close_cli_browser()
    port = await get_random_free_port()
    acm = launch_chromium(
        headless=headless,
        cdp_port=port,
        proxy=ProxySettings(
            **proxy.model_dump(by_alias=True),
        )
        if proxy
        else None,
    )

    _current_browser_context_manager = acm
    _current_browser_context, _ = await _current_browser_context_manager.__aenter__()

    return CDPRunOptions(
        cdp_address=f"http://localhost:{port}",
    )


def is_cli_browser_launched():
    global _current_browser_context_manager
    return _current_browser_context_manager is not None and _current_browser_context is not None


async def close_cli_browser():
    global _current_browser_context_manager, _current_browser_context
    if _current_browser_context_manager is not None:
        await _current_browser_context_manager.__aexit__(None, None, None)
        _current_browser_context_manager = None
    if _current_browser_context is not None:
        _current_browser_context = None
