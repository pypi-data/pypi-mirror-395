import abc

from unitelabs.cdk import sila


class StartSimulationModeFailed(Exception):
    """
    The server cannot change to Simulation Mode.

    This error can, e.g., be thrown, if a real-world process needs to be ended before switching to simulation
    mode.
    """


class StartRealModeFailed(Exception):
    """
    The server cannot change to Real Mode.

    This error can, e.g., be thrown, if a device is not ready to change into Real Mode.
    """


class SimulationControllerBase(sila.Feature, metaclass=abc.ABCMeta):
    """
    This Feature provides control over the simulation behaviour of a SiLA Server.

    A SiLA Server can run in two modes:
    (a) Real Mode - with real activities, e.g. addressing or controlling real hardware,
        e.g. through serial/CANBus commands, writing to real databases, moving real objects etc.
    (b) Simulation Mode - where every command is only simulated and responses are just example returns.

    Note that certain commands and properties might not be affected by this feature if they
    do not interact with the real world.
    """

    _simulation_mode = False

    def __init__(self):
        super().__init__(
            originator="org.silastandard",
            category="core",
            version="1.0",
            maturity_level="Verified",
        )

    @abc.abstractmethod
    @sila.UnobservableCommand()
    async def start_simulation_mode(self) -> None:
        """
        Set the SiLA Server to run in Simulation Mode, i.e. all following commands are executed in simulation mode.

        The Simulation Mode can only be entered, if all hardware operations have been safely terminated
        or are in a controlled, safe state.

        The simulation mode can be stopped by issuing the 'Start Real Mode' command.

        Raises:
          StartSimulationModeFailed: If the server cannot change to Simulation Mode.
        """

    @abc.abstractmethod
    @sila.UnobservableCommand()
    async def start_real_mode(self) -> None:
        """
        Set the SiLA Server to run in real mode.

        In real-mode all following commands are executed with real-world
        interactions, like serial port/CAN communication, motor actions etc.

        If the server is in Simulation Mode it can be interrupted at any time. A re-initialization of
        the hardware might be required. The Real Mode can be stopped by issuing the 'Start Simulation Mode' command.

        Raises:
          StartRealModeFailed: If the server cannot change to Real Mode.
        """

    @abc.abstractmethod
    @sila.UnobservableProperty(name="SimulationMode")
    async def simulation_mode(self) -> bool:
        """Whether or not the SiLA Server is in Simulation Mode."""
