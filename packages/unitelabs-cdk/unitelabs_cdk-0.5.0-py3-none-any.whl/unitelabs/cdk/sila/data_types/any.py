import dataclasses

import typing_extensions as typing

import sila


@dataclasses.dataclass
class Any(sila.Any):
    """Any data type that converts to its native python type."""

    @typing.override
    async def to_native(self, context: "sila.Context", /) -> sila.Native:
        return await self.value.to_native(context)
