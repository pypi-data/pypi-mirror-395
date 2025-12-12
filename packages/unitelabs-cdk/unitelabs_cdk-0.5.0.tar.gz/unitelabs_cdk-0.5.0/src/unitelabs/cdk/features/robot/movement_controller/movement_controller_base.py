import abc
import dataclasses

import typing_extensions as typing

from unitelabs.cdk import sila


@dataclasses.dataclass
class PositionIndex(sila.CustomDataType):
    """Specifies a position via an index number, starting at 1."""

    position_index: typing.Annotated[int, sila.constraints.MinimalInclusive(value=1)]


@dataclasses.dataclass
class TargetPosition(sila.CustomDataType):
    """
    Represent a possible position of a device where the device can move to.

    Can contain a sub-position, e.g. for specifying a position in a
    rack.

    Attributes:
      Position: The name of the target position (must be unique
        within the device).
      SubPosition: The index of a sub-position within a target
        position or the number of sub-positions respectively, e.g.
        for a rack.
    """

    position: str
    sub_position: PositionIndex


class MovementControllerBase(sila.Feature, metaclass=abc.ABCMeta):
    """
    This Feature provides control over the movement of devices.

    It specifies a set of predefined positions the device can be moved to, e.g. a robot arm can be moved to positioned
    taught earlier to the robot.
    """

    def __init__(self):
        super().__init__(
            originator="io.unitelabs",
            category="robot",
            version="1.0",
            maturity_level="Draft",
        )

    @abc.abstractmethod
    @sila.UnobservableProperty()
    async def get_available_positions(self) -> list[TargetPosition]:
        """Get all positions of the device including the number of sub-positions."""

    @abc.abstractmethod
    @sila.UnobservableProperty()
    async def get_current_position(self) -> TargetPosition:
        """Get the current position of the device."""

    @abc.abstractmethod
    @sila.ObservableCommand()
    async def move_to(
        self,
        target_position: TargetPosition,
        *,
        status: sila.Status,
    ) -> None:
        """
        Move the device to the specified position.

        Args:
          TargetPosition: Indicates the position where the device will
            be moved to.
        """
