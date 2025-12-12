from collections.abc import Callable
from typing import Any
from typing import Awaitable
from typing import cast
from typing import Protocol
from typing import TYPE_CHECKING
from typing import Union

from runtime.errors.run_api_errors import ApiNotFoundError

from .types import ImportFunction

if TYPE_CHECKING:
    from playwright.async_api import BrowserContext
    from playwright.async_api import Page


setup_context_hook_path = "hooks/setup_context"
setup_context_hook_function_name = "setup_context"

SetupContextHookReturn = Union[
    "None",
    "BrowserContext",
    "tuple[BrowserContext, Page | None]",
    "tuple[BrowserContext, Page | None, Callable[..., Awaitable[None]]]",
]


class SetupContextHook(Protocol):
    def __call__(self, *, cdp_url: str, api_name: str, api_parameters: Any) -> Awaitable[SetupContextHookReturn]: ...


def load_setup_context_hook(*, import_function: ImportFunction):
    try:
        setup_context_hook = cast(
            SetupContextHook, import_function(setup_context_hook_path, setup_context_hook_function_name)
        )
        return setup_context_hook
    except ApiNotFoundError:
        return None
