# ruff: noqa: E501

import dataclasses

from unitelabs.cdk import sila


@dataclasses.dataclass
class StringMetadata(sila.Metadatum):
    """A metadata consisting of a string. It affects the full "Metadata Consumer Test" feature."""

    string_metadata: str


@dataclasses.dataclass
class TwoIntegersMetadata(sila.Metadatum):
    """
    A metadata consisting of a structure with two integers. It affects only the command "Unpack Metadata" of the "Metadata Consumer Test" feature.

    Attributes:
      FirstInteger: The first integer
      SecondInteger: The second integer
    """

    first_integer: int
    second_integer: int


class MetadataProvider(sila.Feature):
    """This feature provides SiLA Client Metadata to the "Metadata Consumer Test" feature."""

    def __init__(self):
        super().__init__(originator="org.silastandard", category="test", metadata=[StringMetadata, TwoIntegersMetadata])
