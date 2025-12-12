import dataclasses

import typing_extensions as typing

import sila

T = typing.TypeVar("T", bound=dict[str, sila.Native])


@dataclasses.dataclass
class Structure(typing.Generic[T], sila.Structure[T]):
    """Structure that converts from and to a python class instead of a dictionary."""

    _class: typing.ClassVar[type] = dataclasses.field(init=None)

    @typing.override
    @classmethod
    async def from_native(
        cls,
        context: "sila.Context",
        value: typing.Optional[T] = None,
        /,
        *,
        execution: typing.Optional["sila.Execution"] = None,
    ) -> typing.Self:
        if isinstance(value, cls._class):
            value = {key: getattr(value, key, None) for key in cls.elements}

        return await super().from_native(context, value, execution=execution)

    @typing.override
    async def to_native(self, context: "sila.Context", /) -> T:
        values = await super().to_native(context)

        return self._class(**values)
