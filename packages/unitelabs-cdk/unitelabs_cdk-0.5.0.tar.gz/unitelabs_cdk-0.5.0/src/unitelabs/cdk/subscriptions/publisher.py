import asyncio
import collections.abc
import inspect

import typing_extensions as typing

from ..sila.utils import clear_interval, set_interval
from .default import _DEFAULT_VALUE
from .subject import IN, OUT, PipeFunction, Subject

if typing.TYPE_CHECKING:
    from .subject import PipeFunction
    from .subscription import Subscription


class Publisher(typing.Generic[IN, OUT], Subject[IN, OUT]):
    """
    An observable which updates itself by polling a data source.

    Args:
      source: A function or coroutine that will be called at a fixed interval as the data source of the subscription.
      interval: How many seconds to wait between polling calls to `source`.
      maxsize: The maximum number of messages to track in the queue.

    Examples:
      Subscribe to a publisher which will call `method` every 2 seconds:
      >>> publisher = Publisher[str](source=method, interval=2, maxsize=10)
      >>> async for state in publisher.subscribe():
      >>>     yield state
    """

    def __init__(
        self,
        source: typing.Union[
            typing.Callable[[], collections.abc.Awaitable[IN]],
            typing.Callable[[], IN],
        ],
        interval: float = 5,
        maxsize: int = 0,
        pipe: typing.Optional[PipeFunction[IN, OUT]] = None,
    ) -> None:
        super().__init__(maxsize=maxsize, pipe=pipe)

        self._update_task: typing.Optional[asyncio.Task] = None
        self._source = source
        self._interval = interval

    @typing.override
    def on_subscribe(self) -> None:
        self._set()

    @typing.override
    def _on_subscribe(self, subscription: "Subscription") -> None:
        super()._on_subscribe(subscription)
        if self.current is not _DEFAULT_VALUE:
            subscription.update(typing.cast("OUT", self.current))

    @typing.override
    def on_unsubscribe(self) -> None:
        self._unset()

    def _set(self) -> None:
        """
        Create a background task to poll the data `source` and update the current value.

        Task will be destroyed when all subscriptions to the `Publisher` are removed.
        """
        if not self._update_task:
            self._update_task = set_interval(self.__self_update, delay=self._interval)

    def _unset(self) -> None:
        """
        Stop the background task that polls the data `source`.

        This is called when all subscriptions to the `Publisher` are removed.
        """
        if self._update_task:
            clear_interval(self._update_task)
            self._update_task = None
            self._value = _DEFAULT_VALUE

    async def __self_update(self) -> None:
        new_value = self._source()
        if inspect.isawaitable(new_value):
            new_value = await new_value
        self.update(typing.cast("IN", new_value))
