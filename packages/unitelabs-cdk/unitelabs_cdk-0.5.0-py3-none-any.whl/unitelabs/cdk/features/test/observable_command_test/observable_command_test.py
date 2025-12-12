# ruff: noqa: D205

import asyncio
import datetime

import typing_extensions as typing

from unitelabs.cdk import sila


class ObservableCommandTest(sila.Feature):
    """
    This is a test feature to test observable commands.
    It specifies various observable commands and returns defined answers to validate against.
    """

    def __init__(self):
        super().__init__(originator="org.silastandard", category="test")

    @sila.ObservableCommand()
    async def count(
        self,
        n: int,
        delay: typing.Annotated[
            float, sila.constraints.Unit(label="s", components=[sila.constraints.Unit.Component("Second")])
        ],
        *,
        status: sila.Status,
        intermediate: sila.Intermediate[int],
    ) -> int:
        """
        Count from 0 to N-1 and return the current number as intermediate response.

        Args:
          N: Number to count to
          Delay: The delay for each iteration

        Yields:
          CurrentIteration: The current number, from 0 to N-1 (excluded).

        Returns:
          IterationResponse: The last number (N-1)
        """

        for i in range(n):
            status.update(
                progress=i / (n - 1),
                remaining_time=datetime.timedelta(seconds=delay * (n - i - 1)),
            )
            intermediate.send(i)

            await asyncio.sleep(delay)

        return n - 1

    @sila.ObservableCommand()
    async def echo_value_after_delay(
        self,
        value: int,
        delay: typing.Annotated[
            float, sila.constraints.Unit(label="s", components=[sila.constraints.Unit.Component("Second")])
        ],
        *,
        status: sila.Status,
    ) -> int:
        """
        Echo the given value after the specified delay. The command state must be "waiting" until the delay has passed.

        Args:
          Value: The value to echo
          Delay: The delay before the command execution starts

        Returns:
          ReceivedValue: The Received Value
        """

        seconds, rest = divmod(delay, 1)
        for i in range(int(seconds)):
            await asyncio.sleep(1)
            status.update(progress=i / delay, remaining_time=datetime.timedelta(seconds=delay - i))

        await asyncio.sleep(rest)
        return value
