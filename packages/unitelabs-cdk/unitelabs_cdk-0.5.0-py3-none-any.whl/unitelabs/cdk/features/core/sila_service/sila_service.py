# ruff: noqa: D401

import typing_extensions as typing
from sila.server import Serializer

from unitelabs.cdk import sila


class UnimplementedFeature(Exception):
    """The Feature specified by the given Feature identifier is not implemented by the server."""


class SiLAService(sila.Feature):
    """
    This Feature MUST be implemented by each SiLA Server.

    It specifies Commands and Properties to discover the Features a
    SiLA Server implements as well as details about the SiLA Server,
    like name, type, description, vendor and UUID.

    Any interaction described in this feature MUST not affect the
    behaviour of any other Feature.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(
            originator="org.silastandard",
            category="core",
            version="1.0",
            maturity_level="Normative",
            name="SiLA Service",
        )

    @sila.UnobservableProperty(name="Server UUID")
    def get_server_uuid(
        self,
    ) -> typing.Annotated[
        str,
        sila.constraints.Length(36),
        sila.constraints.Pattern(r"[0-9a-f]{8}\-[0-9a-f]{4}\-[0-9a-f]{4}\-[0-9a-f]{4}\-[0-9a-f]{12}"),
    ]:
        """
        Globally unique identifier that identifies a SiLA Server.

        The Server UUID MUST be generated once and remain the same for
        all times.
        """

        return self.server.uuid

    @sila.UnobservableProperty()
    def get_server_name(self) -> typing.Annotated[str, sila.constraints.MaximalLength(255)]:
        """
        Human readable name of the SiLA Server.

        The name can be set using the 'Set Server Name' command.
        """

        return self.server.name

    @sila.UnobservableProperty()
    def get_server_type(self) -> typing.Annotated[str, sila.constraints.Pattern(r"[A-Z][a-zA-Z0-9]*")]:
        """
        The type of this server.

        It could be, e.g., in the case of a SiLA Device, the model name.
        It is specified by the implementer of the SiLA Server and MAY not be unique.
        """

        return self.server.type

    @sila.UnobservableProperty()
    def get_server_description(self) -> str:
        """
        Description of the SiLA Server.

        This should include the use and purpose of this SiLA Server.
        """

        return self.server.description

    @sila.UnobservableProperty()
    def get_server_version(
        self,
    ) -> typing.Annotated[
        str, sila.constraints.Pattern(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(\.(0|[1-9][0-9]*))?(_[_a-zA-Z0-9]+)?")
    ]:
        """
        Returns the version of the SiLA Server.

        A "Major" and a "Minor" version number (e.g. 1.0) MUST be
        provided, a Patch version number MAY be provided. Optionally, an
        arbitrary text, separated by an underscore MAY be appended, e.g.
        "3.19.373_mighty_lab_devices".
        """

        return self.server.version

    @sila.UnobservableProperty(name="Server Vendor URL")
    def get_server_vendor_url(self) -> typing.Annotated[str, sila.constraints.Pattern(r"https?://.+")]:
        """
        Returns the URL to the website of the vendor or the website of the product of this SiLA Server.

        This URL SHOULD be accessible at all times. The URL is a Uniform
        Resource Locator as defined in RFC 1738.
        """

        return self.server.vendor_url

    @sila.UnobservableProperty()
    def get_implemented_features(
        self,
    ) -> list[typing.Annotated[str, sila.constraints.FullyQualifiedIdentifier("FeatureIdentifier")]]:
        """
        Returns a list of fully qualified Feature identifiers of all implemented Features of this SiLA Server.

        This list SHOULD remain the same throughout the lifetime of the
        SiLA Server.
        """

        return [str(feature_identifier) for feature_identifier in self.server.features]

    @sila.UnobservableCommand()
    def get_feature_definition(
        self,
        feature_identifier: typing.Annotated[str, sila.constraints.FullyQualifiedIdentifier("FeatureIdentifier")],
    ) -> typing.Annotated[
        str,
        sila.constraints.Schema(
            "Xml",
            url="https://gitlab.com/SiLA2/sila_base/raw/master/schema/FeatureDefinition.xsd",
        ),
    ]:
        """
        Get the Feature Definition of an implemented Feature by its fully qualified Feature Identifier.

        This command has no preconditions and no further dependencies and
        can be called at any time.

        Args:
          FeatureIdentifier: The fully qualified Feature identifier for
            which the Feature definition shall be retrieved.

        Returns:
          FeatureDefinition: The Feature definition in XML format
            (according to the Feature Definition Schema).

        Raises:
          UnimplementedFeature: The Feature specified by the given
            Feature identifier is not implemented by the server.
        """

        try:
            feature = self.server.get_feature(feature_identifier)
        except ValueError:
            raise UnimplementedFeature from None

        serializer = Serializer()
        feature.serialize(serializer)

        return serializer.buffer.getvalue()

    @sila.UnobservableCommand()
    def set_server_name(self, server_name: typing.Annotated[str, sila.constraints.MaximalLength(255)]) -> None:
        """
        Sets a human readable name to the Server Name Property.

        Command has no preconditions and no further dependencies and can be called at any time.

        Args:
          ServerName: The human readable name to assign to the SiLA Server.
        """

        self.server.name = server_name
