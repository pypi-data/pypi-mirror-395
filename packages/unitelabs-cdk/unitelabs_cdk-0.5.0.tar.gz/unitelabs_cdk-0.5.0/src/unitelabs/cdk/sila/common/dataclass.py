import dataclasses
import inspect
import warnings
import weakref

import typing_extensions as typing
from sila.server import DataType, Structure

from ..utils import parse_docstring, to_display_name, to_identifier

if typing.TYPE_CHECKING:
    from ..common import Feature


@dataclasses.dataclass
class Dataclass:
    """Base class for dataclass based SiLA annotations."""

    _identifier: typing.ClassVar[str] = ""
    _name: typing.ClassVar[str] = ""
    _description: typing.ClassVar[str] = ""

    def __init_subclass__(
        cls,
        /,
        *,
        identifier: typing.Optional[str] = None,
        display_name: typing.Optional[str] = None,
        name: typing.Optional[str] = None,
    ) -> None:
        super().__init_subclass__()

        if display_name is not None:
            msg = "Using `display_name` is deprecated, use `name` instead."
            warnings.warn(msg, stacklevel=2)
            name = display_name

        cls._name = name or to_display_name(cls.__name__)
        cls._identifier = identifier or to_identifier(cls._name)
        cls._description = inspect.getdoc(cls)
        cls._feature: typing.Optional["Feature"] = None

    @classmethod
    def attach(cls, feature: "Feature") -> None:
        """
        Create and attach a dataclass to the `feature`.

        Args:
          feature: The `Feature` to which the dataclass will be attached.
        """

        cls._feature = weakref.proxy(feature)

    @classmethod
    def _infer_data_type(cls, feature: "Feature") -> type[DataType]:
        docstring = parse_docstring(cls, feature=feature)
        cls._description = docstring.description

        if len(docstring.parameters) == 0:
            msg = (
                f"Could not detect any fields on '{cls._identifier}'. "
                "Did you forget to annotated your data type definition with `@dataclasses.dataclass`?"
            )
            raise ValueError(msg)
        if (
            len(docstring.parameters) == 1
            and (item := next(iter(docstring.parameters.values()), None))
            and item.identifier == cls._identifier
        ):
            data_type = item.data_type
        else:
            data_type = Structure.create(
                elements=docstring.parameters, name=cls.__name__, description=docstring.description
            )

        return data_type
