import asyncio
import inspect
import traceback
from functools import wraps
from typing import Any, Callable, Coroutine, Literal, NoReturn, NotRequired, Optional, ParamSpec, Type, TypeVar

from loguru import logger

P = ParamSpec("P")


def recurring_coro(
    success_sleep: float,
    error_sleep: float = 0,
    delay: float = 0,
    on_exception: Literal["log", "trace", ""] = "trace",
) -> Callable[[Callable[P, Coroutine[Any, Any, None]]], Callable[P, Coroutine[Any, Any, None]]]:
    """Decorator to make recurring coroutine

    Example:
        >>> @recurring_coro(3)
        ... async def test():
        ...     print("test")
        ...     raise NotImplementedError
        >>> asyncio.run(test())

    Args:
        success_sleep (float): _description_
        error_sleep (float, optional): _description_. Defaults to 0.
        delay (float, optional): _description_. Defaults to 0.
        on_exception (Literal[&quot;log&quot;, &quot;trace&quot;, &quot;&quot;], optional): _description_. Defaults to "trace".
            "" - do not log on raise
            "log" - log err msg
            "trace" - log err msg and trace

    Raises:
        TypeError: _description_

    Returns:
        Callable[[Callable[P, Coroutine[Any, Any, None]]], Callable[P, Coroutine[Any, Any, None]]]: _description_
    """
    if error_sleep == 0:
        error_sleep = success_sleep

    assert on_exception in ["log", "trace", ""]

    def wrapper_func_outer(coro: Callable[P, Coroutine[Any, Any, None]]) -> Callable[P, Coroutine[Any, Any, None]]:
        assert coro is not None
        if not inspect.iscoroutinefunction(coro):
            raise TypeError("coro is not a coroutine function!")

        @wraps(coro)
        async def wrapper_func_inner(*args: P.args, **kwargs: P.kwargs) -> None:
            if delay > 0:
                await asyncio.sleep(delay)
            while True:
                try:
                    await coro(*args, **kwargs)
                    await asyncio.sleep(success_sleep)
                except (asyncio.exceptions.CancelledError, KeyboardInterrupt):
                    break
                except Exception as e:
                    try:
                        if on_exception:
                            logger.error(str(e))
                            if on_exception == "trace":
                                logger.debug(traceback.format_exc())
                        await asyncio.sleep(error_sleep)
                    except (asyncio.exceptions.CancelledError, KeyboardInterrupt):
                        break

        return wrapper_func_inner

    return wrapper_func_outer
