from unittest.mock import Mock
from unittest.mock import patch

from intuned_cli.utils.traces import cli_trace
from runtime.types.run_types import TracingDisabled
from runtime.types.run_types import TracingEnabled


def get_mock_console():
    """Create a mock console that tracks calls."""
    mock_console = Mock()
    mock_console.print = Mock()
    return mock_console


@patch("intuned_cli.controller.authsession.console", get_mock_console())
class TestTraces:
    def test_gives_disabled_tracing_if_id_is_none(self):
        tracing = cli_trace(None).__enter__()
        assert tracing.enabled is False
        assert type(tracing) is TracingDisabled

    def test_gives_enabled_tracing_if_id_is_provided(self):
        tracing = cli_trace("some_id").__enter__()
        assert tracing.enabled is True
        assert type(tracing) is TracingEnabled
        assert "some_id" in tracing.file_path
