import collections.abc
import inspect

import typing_extensions as typing
from sila.server import Native

import sila
from unitelabs.cdk.sila.utils.name import to_identifier

from ..common import Decorator
from ..common.errors import define_error
from ..metadata import Metadatum
from ..utils import parse_docstring, to_display_name

if typing.TYPE_CHECKING:
    from ..common import Feature


class UnobservableProperty(Decorator):
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
      Convert a feature method into an unobservable property:
      >>> class MyFeature(sila.Feature):
      ...   @sila.UnobservableProperty()
      ...   async def my_property(self) -> str:
      ...     \"\"\"
      ...     Describe what your property does.
      ...
      ...     Raises:
      ...       RuntimeError: If something goes wrong.
      ...     \"\"\"
      ...     return "Hello, World!"
    """

    @typing.override
    def attach(self, feature: "Feature") -> bool:
        if not super().attach(feature):
            return False

        docstring = parse_docstring(self._function, feature=feature)

        self._name = self._name or to_display_name(self._function.__name__.removeprefix("get_"))
        self._identifier = self._identifier or to_identifier(self._name)
        self._description = docstring.description
        self._errors = [*self._errors, *docstring.raises.values()]

        element = next(iter(docstring.returns.values()))
        element.identifier = self._identifier
        element.display_name = self._name
        element.description = self._description

        self._responses = {self._identifier: element}

        self._handler = sila.server.UnobservableProperty(
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
    async def _execute(self, function: collections.abc.Callable) -> Native:
        responses: Native = function()

        if inspect.isawaitable(responses):
            responses = await responses

        return {self._identifier: responses}
