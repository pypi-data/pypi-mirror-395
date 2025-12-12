import dataclasses

import typing_extensions as typing

import sila

T = typing.TypeVar("T", bound=sila.Native)


@dataclasses.dataclass
class Custom(typing.Generic[T], sila.Custom[T]):
    """Custom data type that converts from and to a python class instead of a dictionary."""

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
            fields = dataclasses.fields(cls._class)
            value = {field.name: getattr(value, field.name) for field in fields}

            if not issubclass(cls.data_type, sila.Structure):
                field = fields[0]
                value = value.get(field.name, None)

        return await super().from_native(context, value, execution=execution)

    @typing.override
    async def to_native(self, context: "sila.Context", /) -> T:
        values = await super().to_native(context)

        if issubclass(self.data_type, sila.Structure):
            return self._class(**values)

        return self._class(values)
