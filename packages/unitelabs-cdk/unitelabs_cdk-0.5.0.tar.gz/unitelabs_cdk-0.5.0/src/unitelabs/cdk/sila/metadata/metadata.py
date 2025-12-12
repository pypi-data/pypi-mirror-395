import collections.abc

import typing_extensions as typing

from .metadatum import Metadatum

T = typing.TypeVar("T", bound=Metadatum)


class Metadata(collections.abc.Mapping):
    """Collection of the metadata sent by the client."""

    def __getitem__(self, key: type[T]) -> T:
        return super().__getitem__(key)  # type: ignore
