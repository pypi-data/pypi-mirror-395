import functools
import inspect
from functools import wraps
from typing import Any
from typing import Callable
from typing import TypeVar

import anyio

T = TypeVar("T")


def run_sync(func: Callable[..., T]) -> Callable[..., T]:
    """
    Wrapper that runs a function synchronously.
    If the function is async, it will be run using anyio.run instead of asyncio.run.
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        if inspect.iscoroutinefunction(func):
            func_with_args_kwargs = functools.partial(func, *args, **kwargs)
            return anyio.run(func_with_args_kwargs, backend="asyncio")
        return func(*args, **kwargs)

    return wrapper
