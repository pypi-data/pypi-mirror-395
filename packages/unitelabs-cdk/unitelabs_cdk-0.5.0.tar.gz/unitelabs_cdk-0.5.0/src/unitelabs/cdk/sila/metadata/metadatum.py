import collections.abc
import dataclasses
import inspect

import typing_extensions as typing
from sila.server import FeatureIdentifier, Native, SiLAError, UndefinedExecutionError

import sila

from ..common import Dataclass
from ..common.errors import define_error
from ..data_types import Any

if typing.TYPE_CHECKING:
    from ..common import Decorator, Feature

T = typing.TypeVar("T", bound=Any)


@dataclasses.dataclass
class Metadatum(typing.Generic[T], Dataclass):
    """
    Define additional metadata that is used to extend existing features with reusable functionality.

    Attributes:
      feature: The feature this metadata is registered with.

    Examples:
      Define a metadatum on the consumer:
      >>> @dataclasses.dataclass
      ... class MyMetadata(sila.Metadatum, errors=[SomeError]):
      ...   param_a: str
      ...   param_b: int
      ...
      ... class MyMetadataProvider(sila.Feature):
      ...   def __init__(self):
      ...     super().__init__(metadata=[MyMetadata])
      ...
      ... class MyFeature(sila.Feature):
      ...   @sila.UnobservableProperty()
      ...   async def my_property(self, *, metadata: typing.Annotated[sila.Metadata, MyMetadata]) -> str:
      ...     \"\"\"Describe what your property does.\"\"\"
      ...     return metadata.param_a

      Define a metadatum on the provider:
      >>> @dataclasses.dataclass
      ... class MyMetadata(sila.Metadatum):
      ...   param: str
      ...
      ...   @typing.override
      ...   @classmethod
      ...   def affects(cls) -> list[sila.identifiers.FeatureIdentifier]:
      ...     return [cls.feature.app.get_feature(MyFeature).fully_qualified_identifier]
      ...
      ...   @typing.override
      ...   async def intercept(self, context: sila.Handler) -> None:
      ...     # Optionally, intercepts the execution of the property
      ...     # and aborts it if an error is raised
      ...     pass
      ...
      ... class MyMetadataProvider(sila.Feature):
      ...   def __init__(self):
      ...     super().__init__(metadata=[MyMetadata])
      ...
      ... class MyFeature(sila.Feature):
      ...   @sila.UnobservableProperty()
      ...   async def my_property(self) -> str:
      ...     \"\"\"Describe what your property does.\"\"\"
      ...     return ""
    """

    feature: typing.ClassVar["Feature"]
    _affects: typing.ClassVar[set[str]] = set()
    _metadatum: typing.ClassVar[typing.Optional[type[sila.server.Metadata]]] = None

    def __init_subclass__(
        cls,
        /,
        *,
        identifier: typing.Optional[str] = None,
        display_name: typing.Optional[str] = None,
        name: typing.Optional[str] = None,
        errors: typing.Optional[collections.abc.Sequence[type[Exception]]] = None,
    ) -> None:
        super().__init_subclass__(identifier=identifier, display_name=display_name, name=name)

        cls._affects = set()
        cls._errors: list[type[Exception]] = list(errors or [])

    @typing.override
    @classmethod
    def attach(cls, feature: "Feature") -> type[sila.server.Metadata]:
        super().attach(feature)
        cls.feature = feature

        if cls._identifier in feature.metadata:
            cls._affects.update(cls.affects())
            feature.metadata[cls._identifier].affects = list(cls._affects)
            cls._metadatum = typing.cast(type[sila.server.Metadata], feature.metadata[cls._identifier])

            return cls._metadatum

        data_type = cls._infer_data_type(feature)
        cls._metadatum = sila.server.Metadata.create(
            identifier=cls._identifier,
            display_name=cls._name,
            description=cls._description,
            errors={Error.identifier: Error for error in cls._errors if (Error := define_error(error))},
            data_type=data_type,
            affects=list(cls._affects),
            function=cls._intercept,
            feature=feature,
        )
        return cls._metadatum

    @classmethod
    async def _intercept(cls, value: Native, context: sila.Handler) -> None:
        """Intercept method execution."""

        try:
            await cls.from_native(value).intercept(context)
        except SiLAError:
            raise
        except Exception as error:
            if type(error) in cls._errors:
                raise define_error(error)(str(error)) from None

            msg = f"{error.__class__.__name__}: {error}"
            raise UndefinedExecutionError(msg) from error

    @classmethod
    def _infer_metadata(cls, decorator: "Decorator") -> tuple[str, list[type["Metadatum"]]]:
        from .metadata import Metadata

        signature = inspect.signature(decorator._function)

        parameter: str = ""
        metadata: list[type["Metadatum"]] = []

        for param in signature.parameters.values():
            if (
                typing.get_origin(param.annotation) is typing.Annotated
                and (args := typing.get_args(param.annotation))
                and args[0] is Metadata
            ):
                parameter = param.name

                for arg in args[1:]:
                    if not issubclass(arg, Metadatum):
                        msg = (
                            f"Expected instance of `Metadatum` for metadata annotation, "
                            f"received '{arg.__name__}' for parameter '{param.name}'."
                        )
                        raise ValueError(msg)

                    if not decorator._handler:
                        raise RuntimeError

                    arg._affects.add(decorator._handler.fully_qualified_identifier)
                    if arg._metadatum:
                        arg._metadatum.affects = [
                            *arg._metadatum.affects,
                            decorator._handler.fully_qualified_identifier,
                        ]
                    metadata.append(arg)

                break

        return parameter, metadata

    @classmethod
    def from_native(cls, value: Native) -> typing.Self:
        """
        Convert a SiLA metadata value to this counterpart.

        Args:
          value: The value to parse.

        Returns:
          A new instance of this metadatum with the given value.
        """

        if cls._metadatum and issubclass(cls._metadatum.data_type, sila.Structure):
            return cls(**value)

        return cls(value)

    @classmethod
    def affects(self) -> list[FeatureIdentifier]:
        """Set the fully qualified identifiers of the handlers this metadata affects."""

        return []

    async def intercept(self, context: sila.Handler) -> None:
        """Intercept method execution."""
