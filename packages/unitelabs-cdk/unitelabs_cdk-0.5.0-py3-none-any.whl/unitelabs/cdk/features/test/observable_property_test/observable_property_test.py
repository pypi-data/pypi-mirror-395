# ruff: noqa: D401, D415

import asyncio

from unitelabs.cdk import sila, subscriptions


class ObservablePropertyTest(sila.Feature):
    """This is a test feature to test observable properties."""

    def __init__(self):
        super().__init__(originator="org.silastandard", category="test")

        self.alternating = False
        self.alternating_publisher = subscriptions.Publisher(self._update_alternating, interval=1)

        self.value: int = 1
        self.value_event = asyncio.Event()

    async def _update_alternating(self) -> bool:
        self.alternating = not self.alternating

        return self.alternating

    @sila.ObservableProperty()
    async def subscribe_fixed_value(self) -> sila.Stream[int]:
        """Always returns 42 and never changes."""

        yield 42

    @sila.ObservableProperty()
    async def subscribe_alternating(self) -> sila.Stream[bool]:
        """Switches every second between true and false"""

        return self.alternating_publisher.subscribe()

    @sila.ObservableProperty()
    async def subscribe_editable(self) -> sila.Stream[int]:
        """Can be set through SetValue command"""

        while True:
            self.value_event.clear()
            yield self.value
            await self.value_event.wait()

    @sila.UnobservableCommand()
    def set_value(self, value: int) -> None:
        """
        Changes the value of Editable

        Args:
          Value: The new value
        """

        self.value = value
        self.value_event.set()
