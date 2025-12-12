import weakref

import typing_extensions as typing
from sila.server import CommandExecution, Element

from ..data_types import to_sila

T = typing.TypeVar("T")


class Intermediate(typing.Generic[T]):
    """A class representing an intermediate response in a command execution."""

    def __init__(self, command_execution: CommandExecution, responses: dict[str, Element]):
        self.command_execution: CommandExecution = weakref.proxy(command_execution)
        self.responses = responses

    def send(self, *responses: T) -> None:
        """Send an intermediate response."""

        self.command_execution.send_intermediate_responses(to_sila(responses, self.responses))
