import asyncio
import collections.abc
import inspect
import time


def set_interval(function: collections.abc.Callable, delay: float = 1) -> asyncio.Task:
    """Repeatedly call a function or execute a codesnippet, with a fixed time delay between each call."""
    delay_ns = delay * 10**9
    timer = time.perf_counter_ns()

    async def interval(timer: float) -> None:
        while True:
            response = function()
            if inspect.isawaitable(response):
                await response

            timer += delay_ns
            await asyncio.sleep((timer - time.perf_counter_ns()) / 10**9)

    return asyncio.create_task(interval(timer))


def clear_interval(interval: asyncio.Task) -> None:
    """Cancel a timed, repeating action which was previously established by a call to set_interval()."""
    interval.cancel()
