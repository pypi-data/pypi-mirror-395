import abc

from unitelabs.cdk import sila


class Unstable(Exception):
    """Command understood but timeout for stable reading was reached."""


class Overloaded(Exception):
    """Device in overload range."""


class Underloaded(Exception):
    """Device in underload range."""


class WeighingServiceBase(sila.Feature, metaclass=abc.ABCMeta):
    """
    This feature contains commands and properties used for common functions required when weighing things.

    The feature enables access to the current net weight (stable and dynamic) and the tare weight. Commands for zeroing
    and taring are provided.
    """

    def __init__(self, **kwarg):
        super().__init__(
            originator="io.unitelabs",
            category="weighing",
            version="1.0",
            maturity_level="Draft",
            **kwarg,
        )

    @abc.abstractmethod
    @sila.ObservableProperty()
    async def subscribe_weight(self) -> sila.Stream[float]:
        """
        Subscribe to the current net weight in gram, accessed immediately.

        Raises:
          Overloaded: Device in overload range.
          Underloaded: Device in underload range.
        """

    @abc.abstractmethod
    @sila.ObservableProperty()
    async def subscribe_tare_weight(self) -> sila.Stream[float]:
        """Subscribe to the stored tare weight in gram."""

    @abc.abstractmethod
    @sila.UnobservableCommand()
    def get_stable_weight(self) -> float:
        """
        Get the stable net weight in gram.

        Returns:
          Weight: The stable net weight in gram.

        Raises:
          Unstable: Command understood but timeout for stable reading was reached.
          Overloaded: Device in overload range.
          Underloaded: Device in underload range.
        """

    @abc.abstractmethod
    @sila.UnobservableCommand()
    def tare(self) -> float:
        """
        Tare with the current net weight, executed immediately (Not stable).

        Returns:
          TareWeight: The stored tare weight in gram.
        """

    @abc.abstractmethod
    @sila.UnobservableCommand()
    def tare_stable(self) -> float:
        """
        Tare with the stable net weight.

        Returns:
          TareWeight: The stored tare weight in gram.

        Raises:
          Unstable: Command understood but timeout for stable reading was reached.
        """

    @abc.abstractmethod
    @sila.UnobservableCommand()
    def set_tare_weight(self, tare_weight: float) -> None:
        """
        Set a new, custom tare weight in gram.

        Args:
          TareWeight: The tare weight to be stored in gram.
        """

    @abc.abstractmethod
    @sila.UnobservableCommand()
    def clear_tare_weight(self) -> None:
        """Clear the currently stored tare weight."""

    @abc.abstractmethod
    @sila.UnobservableCommand()
    def zero(self) -> None:
        """Zero the balance immediately."""

    @abc.abstractmethod
    @sila.UnobservableCommand()
    def zero_stable(self) -> None:
        """
        Zero the balance with a stable measurement.

        Raises:
          Unstable: Command understood but timeout for stable reading was reached.
        """
