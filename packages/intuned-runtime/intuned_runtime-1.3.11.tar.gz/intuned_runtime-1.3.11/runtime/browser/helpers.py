import asyncio
import os
from typing import Optional
from typing import TYPE_CHECKING

import tenacity as tx
from httpx import AsyncClient
from playwright.async_api import ProxySettings

if TYPE_CHECKING:
    from playwright.async_api import ProxySettings


def get_proxy_env() -> Optional["ProxySettings"]:
    server = os.getenv("PROXY_SERVER")
    username = os.getenv("PROXY_USERNAME")
    password = os.getenv("PROXY_PASSWORD")
    if server is None or username is None or password is None:
        return None
    return {
        "server": server,
        "username": username,
        "password": password,
    }


def get_local_cdp_address(port: int) -> str:
    return f"http://localhost:{port}"


async def wait_on_cdp_address(cdp_address: str) -> None:
    cdp_address_without_protocol = (
        cdp_address.replace("http://", "").replace("https://", "").replace("localhost", "127.0.0.1")
    )

    @tx.retry(stop=tx.stop_after_delay(5), wait=tx.wait_fixed(0.1))
    async def _check_cdp() -> None:
        async with AsyncClient(timeout=1) as client:
            response = await client.get(f"http://{cdp_address_without_protocol}/json/version")
            response.raise_for_status()

    await asyncio.sleep(0.1)
    await _check_cdp()
