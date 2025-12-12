import asyncio
import json
import logging
import os
from contextlib import asynccontextmanager
from typing import Any
from typing import TYPE_CHECKING

import anyio

from runtime.browser.extensions import build_extensions_list
from runtime.browser.extensions.intuned_extension import is_intuned_extension_enabled
from runtime.browser.extensions.intuned_extension import is_intuned_extension_loaded
from runtime.browser.extensions.intuned_extension import setup_intuned_extension
from runtime.browser.extensions.intuned_extension_server import clean_intuned_extension_server
from runtime.browser.extensions.intuned_extension_server import setup_intuned_extension_server

from .helpers import get_local_cdp_address
from .helpers import get_proxy_env
from .helpers import wait_on_cdp_address

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from playwright.async_api import Page
    from playwright.async_api import ProxySettings
    from playwright.async_api import ViewportSize


async def create_user_dir_with_preferences():
    # Create a temporary directory
    playwright_temp_dir = anyio.Path(await anyio.mkdtemp(prefix="pw-"))
    user_dir = playwright_temp_dir / "userdir"
    default_dir = user_dir / "Default"

    # Create the default directory recursively
    await default_dir.mkdir(parents=True, exist_ok=True)

    # Preferences data
    preferences = {
        "plugins": {
            "always_open_pdf_externally": True,
        }
    }

    # Write preferences to file
    async with await (default_dir / "Preferences").open("w") as f:
        await f.write(json.dumps(preferences))

    return await user_dir.absolute(), await playwright_temp_dir.absolute()


@asynccontextmanager
async def launch_chromium(
    headless: bool = True,
    timeout: int = 10,
    cdp_port: int | None = None,
    cdp_address: str | None = None,
    *,
    proxy: "ProxySettings | None" = None,
    viewport: "ViewportSize | None" = None,
    app_mode_initial_url: str | None = None,
    executable_path: os.PathLike[str] | str | None = None,
    **kwargs: Any,
):
    from playwright.async_api import async_playwright
    from playwright.async_api import Browser

    extra_args: list[str] = []
    async with async_playwright() as playwright:
        if cdp_address is not None:
            if await is_intuned_extension_enabled():
                await setup_intuned_extension_server()
            browser: Browser = await playwright.chromium.connect_over_cdp(cdp_address)
            context = browser.contexts[0]
            user_preferences_dir = None
            dir_to_clean = None
        else:
            (
                user_preferences_dir,
                dir_to_clean,
            ) = await create_user_dir_with_preferences()
            proxy = proxy or get_proxy_env()
            # Remove proxy from kwargs if it exists
            viewport = viewport or {"width": 1280, "height": 800}

            if cdp_port:
                extra_args.append(f"--remote-debugging-port={cdp_port}")

            if app_mode_initial_url:
                extra_args.append(f"--app={app_mode_initial_url}")

            args_to_ignore = [
                "--disable-extensions",
                "--disable-component-extensions-with-background-pages",
                "--disable-background-networking",
                "--disable-backgrounding-occluded-windows",
                "--disable-background-timer-throttling",
            ]
            if is_intuned_extension_loaded():
                extensions_list = build_extensions_list()
                extensions = ",".join(extensions_list)
                extra_args.append("--disable-extensions-except=" + extensions)
                extra_args.append(f"--load-extension={extensions}")

            if await is_intuned_extension_enabled():
                await setup_intuned_extension()
                if proxy:
                    extra_args.append(
                        '--proxy-bypass-list="<-loopback>"'
                    )  # This is added to bypass proxy for localhost traffic because some proxy providers block localhost traffic, and localhost traffic doesn't need proxying

            if headless:
                args_to_ignore.append("--headless=old")
                extra_args.append("--headless=new")

            if executable_path is not None:
                executable_path = await anyio.Path(executable_path).resolve()
                if not await executable_path.exists():
                    logger.warning(f"Executable path {executable_path} does not exist. Falling back to default.")
                    executable_path = None
            context = await playwright.chromium.launch_persistent_context(
                os.fspath(user_preferences_dir),
                executable_path=str(executable_path) if executable_path else None,
                headless=headless,
                viewport=viewport,
                proxy=proxy,
                ignore_default_args=args_to_ignore,
                args=extra_args,
                **kwargs,
            )

            if cdp_port:
                await wait_on_cdp_address(get_local_cdp_address(cdp_port))

        context.set_default_timeout(timeout * 1000)

        async def clean_up_after_close(*_: Any, **__: Any) -> None:
            await remove_dir_after_close()
            if await is_intuned_extension_enabled():
                await clean_intuned_extension_server()

        async def remove_dir_after_close(*_: Any, **__: Any) -> None:
            if not dir_to_clean:
                return
            if not await dir_to_clean.exists():
                return

            process = await asyncio.create_subprocess_exec(
                "rm",
                "-rf",
                os.fspath(dir_to_clean),  # Using subprocess to remove the directory
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL,
            )
            await process.wait()

        context.once("close", clean_up_after_close)

        yield context, context.pages[0]


async def dangerous_launch_chromium(
    headless: bool = True,
    timeout: int = 10,
    cdp_url: str | None = None,
    port: int | None = None,
    **kwargs: Any,
):
    from playwright.async_api import async_playwright
    from playwright.async_api import Browser

    temp_dir = await anyio.gettempdir()

    extra_args = [
        "--no-first-run",
        "--disable-sync",
        "--disable-translate",
        "--disable-features=TranslateUI",
        "--disable-features=NetworkService",
        "--lang=en",
        "--disable-blink-features=AutomationControlled",
        "--disable-dev-shm-usage",
        f"--disk-cache-dir={temp_dir}/chrome-cache",
    ]
    playwright = await async_playwright().start()
    if cdp_url is not None:
        if await is_intuned_extension_enabled():
            await setup_intuned_extension_server()
        logging.info(f"Connecting to cdp: {cdp_url}")
        browser: Browser = await playwright.chromium.connect_over_cdp(cdp_url)
        browser.on("disconnected", lambda _: logging.info("Browser Session disconnected"))
        context = browser.contexts[0]
        # set view port for the already existing pages and any new pages
        for page in context.pages:
            await page.set_viewport_size(kwargs.get("viewport", {"width": 1280, "height": 800}))

        async def set_viewport_size(page: "Page"):
            # check if the page is already closed
            if page.is_closed():
                return
            try:
                await page.set_viewport_size(kwargs.get("viewport", {"width": 1280, "height": 800}))
            except Exception as e:
                # check if the error because page closed then we don't need to raise an error
                if page.is_closed():
                    return
                else:
                    raise e

        context.on("page", set_viewport_size)
        user_preferences_dir = None
        dir_to_clean = None
    else:
        logging.info("Launching local browser")
        user_preferences_dir, dir_to_clean = await create_user_dir_with_preferences()
        logging.info(f"Using user data directory: {user_preferences_dir}")
        if kwargs.get("proxy") is None:
            proxy_env = get_proxy_env()
        else:
            proxy_env = kwargs.get("proxy")
        # Remove proxy from kwargs if it exists
        kwargs.pop("proxy", None)
        viewport = kwargs.get("viewport", {"width": 1280, "height": 800})
        kwargs.pop("viewport", None)

        if headless:
            extra_args.append("--headless=new")

        if port:
            extra_args.append(f"--remote-debugging-port={port}")

        if is_intuned_extension_loaded():
            extensions_list = build_extensions_list()
            extensions = ",".join(extensions_list)
            extra_args.append("--disable-extensions-except=" + extensions)
            extra_args.append(f"--load-extension={extensions}")

        if await is_intuned_extension_enabled():
            await setup_intuned_extension()
            if proxy_env:
                extra_args.append('--proxy-bypass-list="<-loopback>"')

        context = await playwright.chromium.launch_persistent_context(
            os.fspath(user_preferences_dir),
            headless=headless,
            viewport=viewport,
            proxy=proxy_env,
            args=extra_args,
            **kwargs,
        )
        context.set_default_timeout(timeout * 1000)

        async def clean_up_after_close(*_: Any, **__: Any) -> None:
            await remove_dir_after_close()
            if await is_intuned_extension_enabled():
                await clean_intuned_extension_server()

        async def remove_dir_after_close(*_: Any, **__: Any) -> None:
            if not dir_to_clean:
                return
            if not await dir_to_clean.exists():
                return

            process = await asyncio.create_subprocess_exec(
                "rm",
                "-rf",
                os.fspath(dir_to_clean),  # Using subprocess to remove the directory
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL,
            )
            await process.wait()

        context.once("close", clean_up_after_close)
    return playwright, context
