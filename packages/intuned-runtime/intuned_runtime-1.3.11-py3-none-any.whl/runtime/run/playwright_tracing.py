from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from playwright.async_api import BrowserContext

from anyio import Path


@asynccontextmanager
async def playwright_tracing(
    *,
    context: "BrowserContext",
    trace_path: str,
    screenshots: bool = True,
    snapshots: bool = True,
    sources: bool = True,
):
    await context.tracing.start(screenshots=screenshots, snapshots=snapshots, sources=sources)
    try:
        yield
    finally:
        try:
            await context.tracing.stop(path=trace_path)
        except Exception as e:
            print("Error stopping tracing:", e)
            await Path(trace_path).unlink(missing_ok=True)
