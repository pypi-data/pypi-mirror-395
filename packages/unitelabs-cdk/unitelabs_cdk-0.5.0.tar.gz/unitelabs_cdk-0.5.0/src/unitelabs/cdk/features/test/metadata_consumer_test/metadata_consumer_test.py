# ruff: noqa: D401, E501

import typing_extensions as typing

from unitelabs.cdk import sila

from ..metadata_provider import StringMetadata
from ..metadata_provider.metadata_provider import TwoIntegersMetadata


class MetadataConsumerTest(sila.Feature):
    """Provides commands and properties to set or respectively get SiLA Any Type values via command parameters or property responses respectively."""

    def __init__(self):
        super().__init__(originator="org.silastandard", category="test")

    @sila.UnobservableCommand()
    async def echo_string_metadata(self, *, metadata: typing.Annotated[sila.Metadata, StringMetadata]) -> str:
        """
        Expects the "String Metadata" metadata from the "Metadata Provider" feature and responds with the metadata value.

        Returns:
          ReceivedStringMetadata: The received string metadata
        """

        return metadata[StringMetadata].string_metadata

    @sila.UnobservableCommand()
    async def unpack_metadata(
        self, *, metadata: typing.Annotated[sila.Metadata, StringMetadata, TwoIntegersMetadata]
    ) -> tuple[str, int, int]:
        """
        Expects the "String Metadata" and "Two Integers Metadata" metadata from the "Metadata Provider" feature and responds with all three data items.

        Returns:
          ReceivedString: The received string (via "String Metadata")
          FirstReceivedInteger: The first element of the received integer structure (via "Two Integers Metadata")
          SecondReceivedInteger: The second element of the received integer structure (via "Two Integers Metadata")
        """

        return (
            metadata[StringMetadata].string_metadata,
            metadata[TwoIntegersMetadata].first_integer,
            metadata[TwoIntegersMetadata].second_integer,
        )

    @sila.UnobservableProperty()
    async def received_string_metadata(self, *, metadata: typing.Annotated[sila.Metadata, StringMetadata]) -> str:
        """Expects the "String Metadata" metadata from the "Metadata Provider" feature and returns the metadata value."""

        return metadata[StringMetadata].string_metadata

    @sila.ObservableProperty()
    async def received_string_metadata_as_characters(
        self, *, metadata: typing.Annotated[sila.Metadata, StringMetadata]
    ) -> sila.Stream[typing.Annotated[str, sila.constraints.Length(1)]]:
        """Expects the "String Metadata" metadata from the "Metadata Provider" feature and returns all characters of its string value as separate responses."""

        for char in metadata[StringMetadata].string_metadata:
            yield char
