from collections.abc import Callable
from typing import Any
from typing import Awaitable
from typing import Optional
from typing import Protocol


class ImportFunction(Protocol):
    def __call__(self, file_path: str, name: Optional[str] = None, /) -> Callable[..., Awaitable[Any]]: ...
