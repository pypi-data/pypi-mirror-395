import abc

import typing_extensions as typing

from unitelabs.cdk import sila, subscriptions

KELVIN = sila.constraints.Unit(label="K", components=[sila.constraints.UnitComponent(unit="Kelvin")])


class TemperatureNotReachable(Exception):
    """The ambient conditions prohibit the device from reaching the target temperature."""


class ControlInterrupted(Exception):
    """The control of temperature could not be finished as it has been interrupted by another 'Control Temperature' command."""  # noqa: E501


class TemperatureController(sila.Feature, metaclass=abc.ABCMeta):
    """
    This is a simple example of a generic Feature for controlling and retrieving the temperature.

    A new target temperature can be set anytime with the 'Control Temperature' Command.
    The temperature range has been limited to prevent major damages of a device.
    In case the first target temperature has not been reached, a ControlInterrupted Error should be thrown.
    """

    def __init__(self):
        super().__init__(
            originator="org.silastandard",
            category="examples",
            version="1.0",
            maturity_level="Verified",
        )

        self.current_temperature = 21.0
        self.target_temperature = self.current_temperature
        self.source = subscriptions.Publisher(source=self._change_temperature, interval=1)

    def _change_temperature(self) -> float:
        return self.current_temperature

    @sila.ObservableProperty()
    async def subscribe_current_temperature(self) -> sila.Stream[typing.Annotated[float, KELVIN]]:
        """Subscribe the current temperature as measured by the controller."""

        return self.source.subscribe()

    @sila.ObservableCommand()
    async def control_temperature(
        self,
        target_temperature: typing.Annotated[
            float, KELVIN, sila.constraints.MaximalInclusive(363.0), sila.constraints.MinimalExclusive(277.0)
        ],
        *,
        status: sila.Status,
    ) -> None:
        """
        Control the temperature gradually to a set target.

        It is RECOMMENDED to use an oscillation free control system.

        Args:
          TargetTemperature: The target temperature that the server will
            try to reach. Note that the command might be completed at a
            temperature that it evaluates to be close enough. If the
            temperature cannot be reached, a 'Temperature Not Reachable'
            error will be thrown.

        Raises:
          TemperatureNotReachable: The ambient conditions prohibit the
            device from reaching the target temperature.
          ControlInterrupted: The control of temperature could not be
            finished as it has been interrupted by another 'Control
            Temperature' command.
        """
