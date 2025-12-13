from typing import Awaitable, TypeVar
import inspect

T = TypeVar("T")

async def maybe_await(x: T | Awaitable[T]) -> T:
    if inspect.isawaitable(x):
        return await x
    else:
        return x