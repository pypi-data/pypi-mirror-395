import collections.abc
import inspect

import typing_extensions as typing
from sila.server import Native, SiLAError, UndefinedExecutionError

import sila

from ...subscriptions import Subscription
from ..common import Decorator
from ..common.errors import define_error
from ..metadata import Metadatum
from ..utils import parse_docstring, to_display_name, to_identifier

if typing.TYPE_CHECKING:
    from ..common import Feature

T = typing.TypeVar("T")
Stream = collections.abc.AsyncIterator[T]


class ObservableProperty(Decorator):
    """
    A property describes certain aspects of a SiLA server that do not require an action on the SiLA server.

    Args:
      name: Human readable name for the property. By default, this is
        automatically inferred by the name of the decorated method.
      identifier: Unique identifier of the property. By default, this
        equals the `name` without spaces and special characters.
      errors: A list of defined errors that may occur during property
        execution.
      enabled: Callback function that is called to determine whether
        the property is enabled or not. If not provided, the property
        is always enabled.

    Examples:
      Convert a feature method into an observable property:
      >>> class MyFeature(sila.Feature):
      ...   @sila.ObservableProperty()
      ...   async def my_property(self) -> sila.Stream[int]:
      ...     \"\"\"
      ...     Describe what your property does.
      ...
      ...     Raises:
      ...       RuntimeError: If something goes wrong.
      ...     \"\"\"
      ...     yield 0
      ...     yield 1
      ...     yield 2
    """

    @typing.override
    def attach(self, feature: "Feature") -> bool:
        if not super().attach(feature):
            return False

        docstring = parse_docstring(self._function, feature=feature)

        self._name = self._name or to_display_name(self._function.__name__.removeprefix("subscribe_"))
        self._identifier = self._identifier or to_identifier(self._name)
        self._description = docstring.description
        self._errors = [*self._errors, *docstring.raises.values()]

        element = next(iter(docstring.returns.values()))
        element.identifier = self._identifier
        element.display_name = self._name
        element.description = self._description

        self._responses = {self._identifier: element}

        self._handler = sila.server.ObservableProperty(
            identifier=self._identifier,
            display_name=self._name,
            description=self._description,
            function=self.execute,
            errors={Error.identifier: Error for error in self._errors if (Error := define_error(error))},
            data_type=element.data_type,
            feature=feature,
        )
        self._metadata = Metadatum._infer_metadata(self)

        return True

    @typing.override
    async def execute(
        self, metadata: dict[sila.MetadataIdentifier, Native], **parameters
    ) -> collections.abc.AsyncIterator[Native]:
        if not self._feature:
            raise RuntimeError

        try:
            function = self._with_metadata(self._function, metadata)
            function = self._with_parameters(function, parameters)

            responses = self._execute(function)

            async for item in responses:
                yield item
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

    @typing.override
    async def _execute(self, function: collections.abc.Callable) -> collections.abc.AsyncIterator[Native]:
        responses = function()

        if inspect.iscoroutine(responses):
            responses = await responses

        if isinstance(responses, Subscription):
            async for response in responses:
                yield {self._identifier: response}

            responses.terminate()

        elif inspect.isasyncgen(responses):
            async for response in responses:
                yield {self._identifier: response}

        elif inspect.isgenerator(responses):
            for response in responses:
                yield {self._identifier: response}
