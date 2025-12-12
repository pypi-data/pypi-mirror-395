import inspect
import traceback
from functools import wraps
from typing import Any, Callable, Coroutine, Literal, Optional, ParamSpec, TypeVar

from loguru import logger

P = ParamSpec("P")
T = TypeVar("T")


def catch_it(
    on_exception: Literal["log", "trace", ""] = "log",
) -> Callable[[Callable[P, T]], Callable[P, Optional[T]]]:
    assert on_exception in ["log", "trace", ""], "Invalid `on_exception` instruction"

    def wrapper_func_outer(func: Callable[P, T]) -> Callable[P, Optional[T]]:
        if inspect.iscoroutinefunction(func):
            raise TypeError("Unable to decorate a conroutine function!")

        @wraps(func)
        def wrapper_func_inner(*args: P.args, **kwargs: P.kwargs) -> Optional[T]:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if on_exception in ["log", "trace"]:
                    logger.error("{}", str(e))
                    if on_exception == "trace":
                        logger.debug(traceback.format_exc())
                return None

        return wrapper_func_inner

    return wrapper_func_outer


def catch_it_async(
    on_exception: Literal["log", "trace", ""] = "log",
) -> Callable[[Callable[P, Coroutine[Any, Any, T]]], Callable[P, Coroutine[Any, Any, Optional[T]]]]:
    assert on_exception in ["log", "trace", ""], "Invalid `on_exception` instruction"

    def wrapper_func_outer(coro: Callable[P, Coroutine[Any, Any, T]]) -> Callable[P, Coroutine[Any, Any, Optional[T]]]:
        if not inspect.iscoroutinefunction(coro):
            raise TypeError("Unable to decorate a non-conroutine function!")

        @wraps(coro)
        async def wrapper_func_inner(*args: P.args, **kwargs: P.kwargs) -> Optional[T]:
            try:
                return await coro(*args, **kwargs)
            except Exception as e:
                if on_exception in ["log", "trace"]:
                    logger.error("{}", str(e))
                    if on_exception == "trace":
                        logger.debug(traceback.format_exc())
                return None

        return wrapper_func_inner

    return wrapper_func_outer
