# ruff: noqa: D205, D401, D415, E501

import asyncio
import dataclasses
import datetime

import typing_extensions as typing

from unitelabs.cdk import sila


@dataclasses.dataclass
class String(sila.Metadatum):
    """A string"""

    string: str


class BinaryTransferTest(sila.Feature):
    """Provides commands and properties to set or respectively get the SiLA Basic Data Type Binary via command parameters or property responses respectively."""

    def __init__(self):
        super().__init__(originator="org.silastandard", category="test", metadata=[String])

    @sila.UnobservableCommand()
    async def echo_binary_value(self, binary_value: bytes) -> bytes:
        """
        Receives a Binary value (transmitted either directly or via binary transfer) and
        returns the received value.

        Args:
          BinaryValue: The Binary value to be returned.

        Returns:
          ReceivedValue: The received Binary value transmitted in the same way it has been received.
        """

        return binary_value

    @sila.ObservableCommand()
    async def echo_binaries_observably(
        self, binaries: list[bytes], *, status: sila.Status, intermediate: sila.Intermediate[bytes]
    ) -> bytes:
        """
        Receives a list of binaries, echoes them individually as intermediate responses with a delay of 1 second, and then returns them as a single joint binary

        Args:
          Binaries: List of binaries to echo

        Yields:
          JointBinary: Single binary from the parameter list

        Returns:
          ReceivedValue: A single binary comprised of binaries received as parameter
        """

        for i, binary in enumerate(binaries):
            status.update(
                progress=(i + 1) / len(binaries),
                remaining_time=datetime.timedelta(seconds=len(binaries) - i),
            )
            intermediate.send(binary)

            await asyncio.sleep(1)

        return b"".join(binaries)

    @sila.UnobservableProperty()
    async def binary_value_directly(self) -> bytes:
        """Returns the UTF-8 encoded string 'SiLA2_Test_String_Value' directly transmitted as Binary value."""

        return b"SiLA2_Test_String_Value"

    @sila.UnobservableProperty()
    async def binary_value_download(self) -> bytes:
        """
        Returns the Binary Transfer UUID to be used to download the binary data which is the UTF-8 encoded string
        'A_slightly_longer_SiLA2_Test_String_Value_used_to_demonstrate_the_binary_download', repeated 100,000 times.
        """

        return b"A_slightly_longer_SiLA2_Test_String_Value_used_to_demonstrate_the_binary_download" * 100_000

    @sila.UnobservableCommand()
    async def echo_binary_and_metadata_string(
        self, binary: bytes, *, metadata: typing.Annotated[sila.Metadata, String]
    ) -> tuple[bytes, str]:
        """
        Receives a Binary and requires String Metadata, returns both

        Args:
          Binary: The binary to echo

        Returns:
          Binary: The received binary
          StringMetadata: The received String Metadata
        """

        return (binary, metadata[String].string)
