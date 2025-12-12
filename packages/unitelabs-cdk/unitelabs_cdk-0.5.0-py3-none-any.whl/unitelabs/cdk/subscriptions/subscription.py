import asyncio
import collections.abc
import time
import weakref

import typing_extensions as typing

from .default import _DEFAULT_VALUE, Default

if typing.TYPE_CHECKING:
    from .subject import Subject

T = typing.TypeVar("T")


class Subscription(asyncio.Queue[T], collections.abc.AsyncIterator[T]):
    """An AsyncIterable you can asynchronously add items to."""

    def __init__(self, maxsize: int, parent: "Subject") -> None:
        super().__init__(maxsize)

        self._parent: "Subject" = weakref.proxy(parent)
        self._value: typing.Union[T, Default] = typing.cast(T, _DEFAULT_VALUE)
        self._closed = asyncio.Event()

    def __repr__(self) -> str:
        name = self.__class__.__name__
        identifier = str(id(self))
        return f"{name}({identifier}, size={self.size}, closed={self._closed.is_set()})"

    @property
    def size(self) -> int:
        """The number of items in the queue."""

        return self.qsize()

    def update(self, value: "T") -> None:
        """Update the current value, if `value` is not current value."""

        if value != self._value:
            self._value = value
            self.put_nowait(value)

    def cancel(self) -> None:
        """Cancel the subscription."""

        self._closed.set()

    def terminate(self) -> None:
        """Unsubscribe the subscription from its parent."""

        self._parent.unsubscribe(self)

    def __aiter__(self) -> collections.abc.AsyncIterator[T]:
        return self

    async def __anext__(self) -> T:
        if self._closed.is_set():
            raise StopAsyncIteration

        try:
            cancellation = asyncio.create_task(self._closed.wait(), name="subscription-cancellation")
            queue_task = asyncio.create_task(super().get(), name="subscription-queue")

            done, _ = await asyncio.wait((queue_task, cancellation), return_when=asyncio.FIRST_COMPLETED)

            if cancellation in done:
                queue_task.cancel()
                raise StopAsyncIteration

            if queue_task in done:
                item = queue_task.result()
                self.task_done()
                if item is not _DEFAULT_VALUE:
                    return item
        except asyncio.CancelledError:
            raise StopAsyncIteration from None
        finally:
            self._closed.clear()

    async def get(
        self,
        predicate: typing.Callable[[T], bool] = lambda _: True,
        timeout: typing.Optional[float] = None,
    ) -> T:
        """
        Request an upcoming value that satisfies the `predicate`.

        If used without `timeout` this will block indefinitely until a value satisfies the `predicate`.

        Args:
          predicate: A filter predicate to apply.
          timeout: How many seconds to wait for new value before timing out.

        Raises:
          TimeoutError: If the `timeout` is exceeded.
        """

        start_time = time.perf_counter()

        while True:
            wait_for = timeout + start_time - time.perf_counter() if timeout is not None else None
            try:
                value = await asyncio.wait_for(super().get(), timeout=wait_for)
                self.task_done()
            except (TimeoutError, asyncio.TimeoutError):
                raise TimeoutError from None

            if value is not _DEFAULT_VALUE and predicate(value):
                return value
