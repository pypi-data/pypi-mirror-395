import collections.abc
import copy
import functools
import inspect
import warnings
import weakref

import typing_extensions as typing
from sila.server import CommandExecution, Handler, Native, SiLAError, UndefinedExecutionError

from sila import Element, MetadataIdentifier

from ..data_types import to_sila
from ..metadata import Metadatum
from ..utils import parse_docstring, to_display_name, to_identifier
from .errors import define_error

if typing.TYPE_CHECKING:
    from .feature import Feature


class Decorator:
    """Base class for decorator based SiLA annotations."""

    def __init__(
        self,
        /,
        *,
        identifier: typing.Optional[str] = None,
        display_name: typing.Optional[str] = None,
        name: typing.Optional[str] = None,
        errors: typing.Optional[collections.abc.Sequence[type[Exception]]] = None,
        enabled: typing.Union[bool, collections.abc.Callable[..., bool]] = True,
    ) -> None:
        if display_name is not None:
            msg = "Using `display_name` is deprecated, use `name` instead."
            warnings.warn(msg, stacklevel=2)
            name = display_name

        self._identifier = identifier or ""
        self._name = name or ""
        self._description = ""
        self._enabled = enabled
        self._parameters: dict[str, Element] = {}
        self._responses: dict[str, Element] = {}
        self._intermediate_responses: dict[str, Element] = {}
        self._handler: typing.Optional[Handler] = None
        self._metadata: tuple[str, list[type[Metadatum]]] = ("", [])
        self._errors: list[type[Exception]] = list(errors or [])
        self._function: collections.abc.Callable = lambda: ...
        self._feature: typing.Optional["Feature"] = None

    def __call__(self, function: collections.abc.Callable) -> collections.abc.Callable:
        """Call the decorator to wrap the given method."""

        self._function = weakref.proxy(function)
        setattr(function, "__handler", self)

        return function

    def is_enabled(self, feature: "Feature") -> bool:
        """Whether the handler is enabled or not."""

        if callable(self._enabled):
            return self._enabled(feature)

        return self._enabled

    def clone(self) -> "Decorator":
        """Create a copy of this decorator."""

        return copy.copy(self)

    def attach(self, feature: "Feature") -> bool:
        """
        Create and attach a handler to the `feature`.

        Args:
          feature: The `Feature` to which the handler will be attached.

        Returns:
          Whether the handler was attached or not.
        """

        if not self.is_enabled(feature):
            return False

        if self.__class__ is Decorator:
            docstring = parse_docstring(self._function, feature=feature)
            self._name = self._name or to_display_name(self._function.__name__)
            self._identifier = self._identifier or to_identifier(self._name)
            self._description = docstring.description

        self._feature = weakref.proxy(feature)

        return True

    async def execute(self, metadata: dict[MetadataIdentifier, Native], **parameters) -> Native:
        """
        Execute a given function with the provided keyword arguments.

        Args:
          metadata: Additional metadata sent from client to server.

        Returns:
          The result of the `function` execution.

        Raises:
          DefinedExecutionError: If the error type is in the list of defined errors.
          UndefinedExecutionError: If an unexpected error occurs during execution.
        """

        if not self._feature:
            raise RuntimeError

        try:
            function = self._with_metadata(self._function, metadata)
            function = self._with_parameters(function, parameters)

            return await self._execute(function)
        except SiLAError:
            raise
        except Exception as error:
            import traceback

            traceback.print_exc()

            error_name = error.__name__ if inspect.isclass(error) else error.__class__.__name__
            if any(error_name in e.__name__ for e in self._errors):
                raise define_error(error)(str(error)) from None

            msg = f"{error.__class__.__name__}: {error}"
            raise UndefinedExecutionError(msg) from error

    async def _execute(self, function: collections.abc.Callable) -> Native:
        responses = function()

        if inspect.isawaitable(responses):
            responses = await responses

        return to_sila(responses, self._responses)

    def _with_metadata(
        self, function: collections.abc.Callable, metadata: dict[MetadataIdentifier, Native]
    ) -> collections.abc.Callable:
        if self._metadata[0]:
            function = functools.partial(
                function,
                **{
                    self._metadata[0]: {
                        metadatum: metadatum.from_native(metadata[metadatum._metadatum.fully_qualified_identifier()])
                        for metadatum in self._metadata[1]
                        if metadatum._metadatum
                    }
                },
            )

        return function

    def _with_parameters(
        self,
        function: collections.abc.Callable,
        parameters: collections.abc.Mapping[str, typing.Union[Native, CommandExecution]],
    ) -> collections.abc.Callable:
        if not self._feature:
            raise RuntimeError

        parameters = dict(parameters)
        command_execution = parameters.pop("command_execution", None)
        parameters = typing.cast(dict[str, Native], parameters)

        if command_execution and isinstance(command_execution, CommandExecution):
            from ..command import Intermediate, Status

            signature = inspect.signature(function)
            for param in signature.parameters.values():
                annotation = typing.get_origin(param.annotation) or param.annotation
                if annotation is Status:
                    function = functools.partial(function, **{param.name: Status(command_execution)})
                if annotation is Intermediate:
                    function = functools.partial(
                        function, **{param.name: Intermediate(command_execution, self._intermediate_responses)}
                    )

        return functools.partial(function, **parameters)
