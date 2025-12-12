import typing_extensions as typing

import sila
from unitelabs.cdk.sila.utils.name import to_identifier

from ..common import Decorator
from ..common.errors import define_error
from ..metadata import Metadatum
from ..utils import parse_docstring, to_display_name

if typing.TYPE_CHECKING:
    from ..common import Feature


class UnobservableCommand(Decorator):
    """
    Any command for which observing the progress of execution is not possible or does not make sense.

    Args:
      name: Human readable name for the command. By default, this is
        automatically inferred by the name of the decorated method.
      identifier: Unique identifier of the command. By default, this
        equals the `name` without spaces and special characters.
      errors: A list of defined errors that may occur during command
        execution.
      enabled: Callback function that is called to determine whether
        the command is enabled or not. If not provided, the command is
        always enabled.

    Examples:
      Convert a feature method into an unobservable command:
      >>> class MyFeature(sila.Feature):
      ...   @sila.UnobservableCommand()
      ...   async def my_command(self, param_a: str, param_b: int) -> tuple[str, int]:
      ...     \"\"\"
      ...     Describe what your command does.
      ...
      ...     Args:
      ...       ParamA: Describe the purpose of param_a.
      ...       ParamB: Describe the purpose of param_b.
      ...
      ...     Returns:
      ...       ResponseA: Response value a.
      ...       ResponseB: Response value b.
      ...
      ...     Raises:
      ...       RuntimeError: If something goes wrong.
      ...     \"\"\"
      ...     return param_a, param_b
    """

    @typing.override
    def attach(self, feature: "Feature") -> bool:
        if not super().attach(feature):
            return False

        docstring = parse_docstring(self._function, feature=feature)

        self._name = self._name or to_display_name(self._function.__name__)
        self._identifier = self._identifier or to_identifier(self._name)
        self._description = docstring.description
        self._parameters = docstring.parameters
        self._responses = docstring.returns
        self._errors = [*self._errors, *docstring.raises.values()]

        self._handler = sila.server.UnobservableCommand(
            identifier=self._identifier,
            display_name=self._name,
            description=self._description,
            function=self.execute,
            errors={Error.identifier: Error for error in self._errors if (Error := define_error(error))},
            parameters=self._parameters,
            responses=self._responses,
            feature=feature,
        )
        self._metadata = Metadatum._infer_metadata(self)

        return True
