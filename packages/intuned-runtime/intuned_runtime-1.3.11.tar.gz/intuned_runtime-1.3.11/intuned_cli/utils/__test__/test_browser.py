from dataclasses import dataclass
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

import pytest
import pytest_asyncio

from intuned_cli.utils.browser import close_cli_browser
from intuned_cli.utils.browser import get_cli_run_options
from runtime.types.run_types import CDPRunOptions
from runtime.types.run_types import StandaloneRunOptions


@dataclass
class BrowserMocks:
    launch_chromium: AsyncMock


@pytest_asyncio.fixture
async def browser_mocks():
    """Mock dependencies for execute_record_auth_session_cli tests."""

    _mock_launch_chromium = patch("runtime.browser.launch_chromium.launch_chromium")
    _mock_get_free_port = patch("runtime.run.playwright_context.get_random_free_port", new_callable=AsyncMock)

    with (
        _mock_launch_chromium as mock_launch_chromium,
        _mock_get_free_port as _mock_get_free_port,
    ):
        mock_launch_chromium_return_value = Mock()

        async def create_context_and_page():
            return (MagicMock(), MagicMock())

        mock_launch_chromium_return_value.__aenter__ = AsyncMock(side_effect=create_context_and_page)
        mock_launch_chromium_return_value.__aexit__ = AsyncMock(return_value=None)
        mock_launch_chromium.return_value = mock_launch_chromium_return_value

        _mock_get_free_port.return_value = 1234

        yield BrowserMocks(
            launch_chromium=mock_launch_chromium,
        )

        await close_cli_browser()


class TestBrowser:
    @pytest.mark.asyncio
    @pytest.mark.asyncio
    async def test_returns_cdp_options_if_cdp_url_is_passed(self, browser_mocks: BrowserMocks):
        from intuned_cli.utils.browser import get_cli_run_options

        options = await get_cli_run_options(
            cdp_url="cdp_url",
        )
        assert options.environment == "cdp"
        assert type(options) is CDPRunOptions
        assert options.cdp_address == "cdp_url"

    @pytest.mark.asyncio
    async def test_returns_standalone_options_if_keep_browser_open_is_false(self, browser_mocks: BrowserMocks):
        from intuned_cli.utils.browser import get_cli_run_options

        options = await get_cli_run_options(
            keep_browser_open=False,
            headless=False,
        )
        assert options.environment == "standalone"
        assert type(options) is StandaloneRunOptions
        assert options.headless is False

    @pytest.mark.asyncio
    async def test_launches_browser_and_returns_cdp_options_if_keep_browser_open_is_true(
        self, browser_mocks: BrowserMocks
    ):
        options = await get_cli_run_options(
            keep_browser_open=True,
            headless=False,
        )
        assert options.environment == "cdp"
        assert type(options) is CDPRunOptions
        assert options.cdp_address == "http://localhost:1234"

        browser_mocks.launch_chromium.assert_called_with(
            headless=False,
            cdp_port=1234,
            proxy=None,
        )

    @pytest.mark.asyncio
    async def test_keeps_context_open_until_new_context_if_keep_browser_open_is_true(self, browser_mocks: BrowserMocks):
        options = await get_cli_run_options(
            keep_browser_open=True,
            headless=False,
        )
        assert options.environment == "cdp"
        assert type(options) is CDPRunOptions
        assert options.cdp_address == "http://localhost:1234"

        from intuned_cli.utils.browser import _current_browser_context  # type: ignore

        first_context = _current_browser_context
        assert first_context is not None

        assert browser_mocks.launch_chromium.call_count == 1

        options = await get_cli_run_options(
            keep_browser_open=True,
            headless=False,
        )

        from intuned_cli.utils.browser import _current_browser_context  # type: ignore

        second_context = _current_browser_context
        assert second_context is not None
        assert first_context != second_context
        assert browser_mocks.launch_chromium.call_count == 2

    @pytest.mark.asyncio
    async def test_keeps_context_open_until_explicitly_closed_if_keep_browser_open_is_true(
        self, browser_mocks: BrowserMocks
    ):
        options = await get_cli_run_options(
            keep_browser_open=True,
            headless=False,
        )
        assert options.environment == "cdp"
        assert type(options) is CDPRunOptions
        assert options.cdp_address == "http://localhost:1234"

        from intuned_cli.utils.browser import _current_browser_context  # type: ignore

        assert _current_browser_context is not None

        assert browser_mocks.launch_chromium.call_count == 1

        await close_cli_browser()

        from intuned_cli.utils.browser import _current_browser_context  # type: ignore

        assert _current_browser_context is None
