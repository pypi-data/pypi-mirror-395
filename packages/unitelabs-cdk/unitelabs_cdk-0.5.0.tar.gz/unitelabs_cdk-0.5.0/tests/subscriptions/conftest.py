import asyncio
import typing

import pytest

ONE_OP_TIME = 0.01
DEFAULT_VALUE = "default"


async def bg_cancel(cancel_event: asyncio.Event):
    """Set the cancel event after a delay of ~5 operations."""
    await asyncio.sleep(ONE_OP_TIME * 5)
    cancel_event.set()


@pytest.fixture
def create_task() -> typing.Generator[asyncio.Task, None, None]:
    tasks = set()

    def _create_task(
        method: typing.Coroutine[typing.Awaitable, None, None],
    ) -> typing.Generator[asyncio.Task, None, None]:
        name = f"subscription-{method.__name__}"
        task = asyncio.create_task(method, name=name)
        tasks.add(task)
        task.add_done_callback(tasks.discard)

        yield task

        task.cancel()
        tasks.discard(task)

    yield _create_task

    for task in tasks:
        task.cancel()
        tasks.discard(task)
