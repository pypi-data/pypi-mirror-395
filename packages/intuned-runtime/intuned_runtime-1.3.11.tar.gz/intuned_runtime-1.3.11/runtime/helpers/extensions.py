import asyncio
import functools
import logging
from collections.abc import Awaitable
from collections.abc import Callable
from typing import Any
from typing import Optional
from typing import overload
from typing import TypeVar

from playwright.async_api import BrowserContext
from playwright.async_api import Page

from runtime.browser.extensions.intuned_extension import is_intuned_extension_enabled
from runtime.browser.extensions.intuned_extension import set_auto_solve
from runtime.browser.extensions.intuned_extension_server import CaptchaEvent
from runtime.browser.extensions.intuned_extension_server import EventRequest
from runtime.browser.extensions.intuned_extension_server import get_event_from_event_queue
from runtime.browser.extensions.intuned_extension_server import get_intuned_event_emitter

logger = logging.getLogger(__name__)

T = TypeVar("T")


# Overload 1: Direct call with page only (callable pattern)
@overload
async def wait_for_captcha_solve(
    page: Page,
    *,
    timeout: int = 10_000,
) -> None: ...


# Overload 2: Wrapper pattern with page and func
@overload
async def wait_for_captcha_solve(
    *,
    page: Page,
    func: Callable[[], Awaitable[Any]],
    timeout: int = 10_000,
) -> Any: ...


# Overload 3: Decorator without arguments
@overload
def wait_for_captcha_solve(
    func: Callable[..., Awaitable[Any]],
) -> Callable[..., Awaitable[Any]]: ...


# Overload 4: Decorator factory with arguments
@overload
def wait_for_captcha_solve(
    *,
    timeout: int = 10_000,
    wait_for_network_settled: bool = True,
) -> Callable[[Callable[..., Awaitable[Any]]], Callable[..., Awaitable[Any]]]: ...


def wait_for_captcha_solve(
    *args: Any,
    **kwargs: Any,
) -> Any:
    """
    Wait for CAPTCHA solve after performing an action or by itself.

    Usage patterns:
    1. Callable: await wait_for_captcha_solve(page, timeout=10_000)
    2. Wrapper: await wait_for_captcha_solve(page=page, func=my_func, timeout=10_000)
    3. Decorator: @wait_for_captcha_solve or @wait_for_captcha_solve()
    4. Decorator with options: @wait_for_captcha_solve(timeout=10_000, wait_for_network_settled=True)

    Args:
        page: Playwright Page object
        func: Optional callable to execute before waiting for captcha solve
        timeout: Maximum time to wait in milliseconds (default: 10_000)
        wait_for_network_settled: Whether to wait for network idle before checking captcha (default: True)
    """

    # Case 1a: Direct call with page only (callable pattern - positional)
    # await wait_for_captcha_solve(page, timeout=10_000)
    if len(args) == 1 and isinstance(args[0], Page):
        page = args[0]
        timeout = kwargs.get("timeout", 10_000)
        return _wait_for_captcha_solve_core(
            page=page,
            func=None,
            timeout=timeout,
            wait_for_network_settled=False,
        )

    # Case 1b: Direct call with page only (callable pattern - keyword)
    # await wait_for_captcha_solve(page=page, timeout=10_000)
    if "page" in kwargs and "func" not in kwargs and len(args) == 0:
        page = kwargs["page"]
        timeout = kwargs.get("timeout", 10_000)

        if not isinstance(page, Page):
            raise ValueError(
                "No Page object found in function arguments. 'page' parameter must be a Playwright Page object."
            )

        return _wait_for_captcha_solve_core(
            page=page,
            func=None,
            timeout=timeout,
            wait_for_network_settled=False,
        )

    # Case 2: Wrapper pattern with page and func as keyword arguments
    # await wait_for_captcha_solve(page=page, func=func, timeout=10_000)
    if "page" in kwargs and "func" in kwargs:
        page = kwargs["page"]
        func = kwargs["func"]
        timeout = kwargs.get("timeout", 10_000)
        wait_for_network_settled = kwargs.get("wait_for_network_settled", True)

        if not isinstance(page, Page):
            raise ValueError(
                "No Page object found in function arguments. 'page' parameter must be a Playwright Page object."
            )

        return _wait_for_captcha_solve_core(
            page=page,
            func=func,
            timeout=timeout,
            wait_for_network_settled=wait_for_network_settled,
        )

    # Case 3: Decorator without arguments
    # @wait_for_captcha_solve
    if len(args) == 1 and callable(args[0]) and not isinstance(args[0], Page):
        func = args[0]
        return _create_decorated_function(func, timeout=10_000, wait_for_network_settled=True)  # type: ignore

    # Case 4: Decorator factory with arguments (including empty parentheses)
    # @wait_for_captcha_solve() or @wait_for_captcha_solve(timeout=10_000, wait_for_network_settled=True)
    if len(args) == 0 and "page" not in kwargs and "func" not in kwargs:
        timeout = kwargs.get("timeout", 10_000)
        wait_for_network_settled = kwargs.get("wait_for_network_settled", True)

        def decorator(func: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
            return _create_decorated_function(func, timeout=timeout, wait_for_network_settled=wait_for_network_settled)

        return decorator

    raise ValueError(
        "Invalid usage. Valid patterns:\n"
        "1. await wait_for_captcha_solve(page, timeout=10_000) or await wait_for_captcha_solve(page=page, timeout=10_000)\n"
        "2. await wait_for_captcha_solve(page=page, func=func, timeout=10_000)\n"
        "3. @wait_for_captcha_solve or @wait_for_captcha_solve()\n"
        "4. @wait_for_captcha_solve(timeout=10_000, wait_for_network_settled=True)"
    )


def _create_decorated_function(
    func: Callable[..., Awaitable[Any]],
    timeout: int,
    wait_for_network_settled: bool,
) -> Callable[..., Awaitable[Any]]:
    """Helper to create a decorated function with captcha solve waiting."""

    @functools.wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        # Find the page object in function arguments
        page = next((arg for arg in args if isinstance(arg, Page)), None)
        if page is None:
            page = kwargs.get("page")

        if not page or not isinstance(page, Page):
            logger.error(
                "No Page object found in function arguments. The decorated function must have a 'page' parameter or receive a Page object as an argument."
            )
            raise ValueError(
                "No Page object found in function arguments. The decorated function must have a 'page' parameter or receive a Page object as an argument."
            )

        async def func_with_args():
            return await func(*args, **kwargs)

        return await _wait_for_captcha_solve_core(
            page=page,
            func=func_with_args,
            timeout=timeout,
            wait_for_network_settled=wait_for_network_settled,
        )

    return wrapper


async def _wait_for_captcha_solve_core(
    *,
    page: Page,
    func: Optional[Callable[..., Awaitable[Any]]],
    timeout: int = 10_000,
    wait_for_network_settled: bool = True,
):
    """Core implementation of captcha solve waiting logic."""
    if not isinstance(page, Page):
        raise ValueError("No Page object found in function arguments. Page parameter must be a Playwright Page object.")

    logger.debug(f"Page object: {page}")

    result = None
    if func is not None:
        result = await func()

    if wait_for_network_settled:
        try:
            await page.wait_for_load_state("networkidle", timeout=timeout)
        except Exception as e:
            logger.debug(f"Network idle wait failed: {e}")

    detection_event: EventRequest
    try:
        detection_event = await wait_for_captcha_event("CAPTCHA_DETECTED", timeout=timeout)
    except asyncio.TimeoutError:
        logger.info("CAPTCHA Detection timed out")
        return result
    except Exception as e:
        logger.error(f"Error while waiting for captcha: {e}")
        raise e

    logger.info("CAPTCHA Detected, awaiting result...")
    if detection_event.session_id is None:
        raise RuntimeError("CAPTCHA_DETECTED event missing session ID")
    try:
        solved_task = asyncio.create_task(
            wait_for_captcha_event("CAPTCHA_SOLVED", session_id=detection_event.session_id, timeout=timeout)
        )
        max_retries_task = asyncio.create_task(
            wait_for_captcha_event("MAX_RETRIES_EXHAUSTED", session_id=detection_event.session_id, timeout=timeout)
        )
        error_task = asyncio.create_task(
            wait_for_captcha_event("ERROR", session_id=detection_event.session_id, timeout=timeout)
        )
        hit_limit_task = asyncio.create_task(
            wait_for_captcha_event("HIT_LIMIT", session_id=detection_event.session_id, timeout=timeout)
        )

        done, pending = await asyncio.wait(
            [solved_task, max_retries_task, error_task, hit_limit_task], return_when=asyncio.FIRST_COMPLETED
        )

        # Cancel pending tasks
        for task in pending:
            task.cancel()

        # Get the completed task
        completed = done.pop()
        exception = completed.exception()
        if exception:
            raise exception

        # Check which task completed
        if completed == max_retries_task:
            raise RuntimeError("Reached maximum retries on solving captcha")
        elif completed == error_task:
            raise RuntimeError("Captcha error")
        elif completed == hit_limit_task:
            raise RuntimeError("Insufficient resource credits to execute the captcha solve")

        logger.info("CAPTCHA solved successfully")

    except asyncio.TimeoutError as e:
        logger.error("CAPTCHA Result timeout")
        raise RuntimeError("CAPTCHA Solving timeout") from e
    except Exception as e:
        logger.error(f"CAPTCHA solve error: {e}")
        raise

    return result


def remove_captcha_event_listener(
    event: CaptchaEvent,
    f: Callable[..., Awaitable[None] | None],
):
    """
    Detach a callback from a captcha event.

    Args:
        event: The captcha event to listen for
        f: The callback function to execute
    """
    event_emitter = get_intuned_event_emitter()

    event_emitter.remove_listener(event, f)


def on_captcha_event(
    event: CaptchaEvent,
    f: Callable[..., Awaitable[None] | None],
    *args,
    **kwargs,
):
    """
    Register a callback for a captcha event.

    Args:
        event: The captcha event to listen for
        f: The callback function to execute
        *args: Additional arguments to pass to the callback
        **kwargs: Additional keyword arguments to pass to the callback
    """
    event_emitter = get_intuned_event_emitter()

    async def wrapper(*_, **__):
        result = f(*args, **kwargs)
        if asyncio.iscoroutine(result):
            await result

    event_emitter.on(event, wrapper)


def once_captcha_event(
    event: CaptchaEvent,
    f: Callable[..., Awaitable[None] | None],
    *args,
    **kwargs,
):
    """
    Register a one-time callback for a captcha event.

    Args:
        event: The captcha event to listen for
        f: The callback function to execute
        *args: Additional arguments to pass to the callback
        **kwargs: Additional keyword arguments to pass to the callback
    """
    event_emitter = get_intuned_event_emitter()

    async def wrapper(*_, **__):
        result = f(*args, **kwargs)
        if asyncio.iscoroutine(result):
            await result

    event_emitter.once(event, wrapper)


async def wait_for_captcha_event(event: CaptchaEvent, session_id: str = "", timeout: int = 10_000) -> EventRequest:
    """
    Wait for a captcha event to be emitted.

    Args:
        event: Event name to wait for
        session_id: ID for the captcha solve session
        timeout: Optional timeout in milliseconds (default: 10_000)

    Returns:
        The event payload

    Raises:
        RuntimeError: If the event emitter is not initialized
        asyncio.TimeoutError: If the timeout is reached before the event fires
    """

    # Check if event was already fired before attaching the listener
    event_from_queue = get_event_from_event_queue(
        event=event, tab_id="page-0", session_id=session_id
    )  # For now we stick with page-0, will revisit on multi page support
    if event_from_queue is not None:
        return event_from_queue

    emitter = get_intuned_event_emitter()
    if emitter is None:
        raise RuntimeError("Intuned Extensions listener is not initialized")

    loop = asyncio.get_event_loop()
    future: asyncio.Future = asyncio.Future()

    def handler(*_, **__):
        if not future.done():
            consumed_event = get_event_from_event_queue(session_id=session_id, event=event)
            loop.call_soon_threadsafe(future.set_result, consumed_event)

    emitter.once(event, handler)

    try:
        if timeout:
            return await asyncio.wait_for(future, timeout=timeout / 1000)
        else:
            return await future
    except (asyncio.TimeoutError, asyncio.CancelledError):
        emitter.remove_listener(event, handler)
        raise


async def pause_captcha_solver(context: BrowserContext) -> None:
    """
    Pause the captcha solver by setting autoSolve flag to false.

    This will disable automatic captcha solving in the browser extension
    while preserving all other settings.

    Args:
        context: Playwright browser context

    Raises:
        RuntimeError: If extension is not enabled or settings cannot be updated
    """
    if not await is_intuned_extension_enabled():
        raise RuntimeError("Intuned extension is not enabled. Cannot pause captcha solver.")

    await set_auto_solve(context, False)


async def resume_captcha_solver(context: BrowserContext) -> None:
    """
    Resume the captcha solver by setting autoSolve flag to true.

    This will re-enable automatic captcha solving in the browser extension.

    Args:
        context: Playwright browser context

    Raises:
        RuntimeError: If extension is not enabled or settings cannot be updated
    """
    if not await is_intuned_extension_enabled():
        raise RuntimeError("Intuned extension is not enabled. Cannot resume captcha solver.")

    await set_auto_solve(context, True)
