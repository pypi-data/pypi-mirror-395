import dataclasses
import errno
import pathlib
import uuid

import pydantic
import pydantic_core
import typing_extensions as typing
from pydantic import Field
from pydantic.json_schema import JsonSchemaValue

import sila

from ..sila.utils import parse_version
from .config import Config, ConfigurationError

URIString = typing.Annotated[
    str,
    pydantic.WithJsonSchema({"type": "string", "format": "uri"}),
]

UUIDString = typing.Annotated[
    str,
    pydantic.WithJsonSchema({"type": "string", "format": "uuid"}),
]


def read_bytes_if_path_and_exists(path: typing.Union[str, pathlib.Path, None]) -> typing.Optional[bytes]:
    """
    Read the byte-contents of the given `path`, if it is a path or a string-representation of a path.

    If the path-string's resolved `Path` does not exist, it is treated as a base64-encoded ASCII-string
    and decoded to bytes.

    Args:
      path: A string-representation of a path, or a path, from which to read the contents,
        or base64-encoded ASCII-string, which is decoded to bytes,
        or None, which is returned immediately.

    Returns:
      The byte-contents from `path` or None.

    Raises:
      FileNotFoundError: If `path` is a valid path but does not exist.
    """

    if not isinstance(path, (str, pathlib.Path)):
        return path

    path_str = None
    if isinstance(path, str):
        path_str = path
        path = pathlib.Path(path).resolve()

    try:
        if not path.resolve().exists():
            if path_str is not None and path_str.startswith("-----BEGIN "):
                return path_str.encode("ascii")
            msg = f"File at path '{path.resolve()}' not found."
            raise FileNotFoundError(msg)
    except OSError as err:
        if err.errno != errno.ENAMETOOLONG:
            # Platform-specific errors: File name too long
            raise

        # assumed to be a base64-encoded string of the certificate/key
        return path_str.encode("ascii")

    return path.read_bytes()


@dataclasses.dataclass
class SiLAServerConfig(sila.server.ServerConfig, Config):
    """Configuration for a SiLA server."""

    root_certificates: typing.Union[str, pathlib.Path, bytes, None] = None
    """
    A path to, or the bytestring contents of, the PEM-encoded root certificates, or `None` if no
    root certificates should be used.
    Note: TLS must be set to True to activate encryption with this certificate.
    """

    certificate_chain: typing.Union[str, pathlib.Path, bytes, None] = None
    """
    A path to, or the bytestring contents of, the PEM-encoded certificate chain, or `None`
    if no certificate chain should be used.
    Note: TLS must be set to True to activate encryption with this certificate.
    """

    private_key: typing.Union[str, pathlib.Path, bytes, None] = None
    """
    A path to, or the bytestring contents of, the PEM-encoded private key, or `None` if no
    private key should be used.
    Note: TLS must be set to True to activate encryption with this key.
    """

    options: dict = dataclasses.field(default_factory=dict)
    uuid: UUIDString = dataclasses.field(default_factory=lambda: str(uuid.uuid4()))
    name: typing.Annotated[str, Field(max_length=255)] = "SiLA Server"
    vendor_url: URIString = "https://sila-standard.com"

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: pydantic_core.core_schema.CoreSchema, handler: pydantic.GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        json_schema = handler(core_schema)
        json_schema["required"] = ["uuid"]
        return json_schema

    def __post_init__(self):
        self.certificate_chain = (
            read_bytes_if_path_and_exists(self.certificate_chain)
            if not isinstance(self.certificate_chain, (bytes, bytearray, memoryview))
            else self.certificate_chain
        )
        self.private_key = (
            read_bytes_if_path_and_exists(self.private_key)
            if not isinstance(self.private_key, (bytes, bytearray, memoryview))
            else self.private_key
        )
        self.version = parse_version(self.version)


@dataclasses.dataclass
class CloudServerConfig(sila.server.CloudServerConfig, Config):
    """Configuration for a gRPC Cloud Server."""

    port: typing.Annotated[int, Field(ge=1, le=65_535)] = 50_000

    root_certificates: typing.Union[str, pathlib.Path, bytes, None] = None
    """
    A path to, or the bytestring contents of, the PEM-encoded root certificates, or `None` if no
    root certificates should be used.
    Note: TLS must be set to True to activate encryption with this certificate.
    """

    certificate_chain: typing.Union[str, pathlib.Path, bytes, None] = None
    """
    A path to, or the bytestring contents of, the PEM-encoded certificate chain, or `None` if no
    certificate chain should be used.
    Note: TLS must be set to True to activate encryption with this certificate.
    """

    private_key: typing.Union[str, pathlib.Path, bytes, None] = None
    """
    A path to, or the bytestring contents of, the PEM-encoded private key, or `None` if no
    private key should be used.
    Note: TLS must be set to True to activate encryption with this key.
    """
    options: dict = dataclasses.field(default_factory=dict)

    def __post_init__(self):
        self.certificate_chain = (
            read_bytes_if_path_and_exists(self.certificate_chain)
            if not isinstance(self.certificate_chain, (bytes, bytearray, memoryview))
            else self.certificate_chain
        )
        self.private_key = (
            read_bytes_if_path_and_exists(self.private_key)
            if not isinstance(self.private_key, (bytes, bytearray, memoryview))
            else self.private_key
        )


@dataclasses.dataclass
class DiscoveryConfig(sila.server.discovery.DiscoveryConfig, Config):
    """Configuration for network broadcast of a server."""


@dataclasses.dataclass
class ConnectorBaseConfig(Config):
    """Base configuration for a UniteLabs SiLA2 Connector."""

    sila_server: typing.Optional[SiLAServerConfig] = dataclasses.field(default_factory=SiLAServerConfig)
    cloud_server_endpoint: typing.Optional[CloudServerConfig] = dataclasses.field(default_factory=CloudServerConfig)
    discovery: typing.Optional[DiscoveryConfig] = dataclasses.field(default_factory=DiscoveryConfig)
    logging: typing.Optional[dict] = dataclasses.field(default=None)
    """
    A python `logging.config` which is passed into `dictConfig`.
    Check the official documentation for more information about the logging config schema:
    https://docs.python.org/3/library/logging.config.html#logging-config-dictschema
    """

    def __post_init__(self):
        if isinstance(self.sila_server, dict):
            self.sila_server = SiLAServerConfig(**self.sila_server)
        if isinstance(self.cloud_server_endpoint, dict):
            self.cloud_server_endpoint = CloudServerConfig(**self.cloud_server_endpoint)
        if isinstance(self.discovery, dict):
            self.discovery = DiscoveryConfig(**self.discovery)
        if self.cloud_server_endpoint is None and self.sila_server is None:
            msg = "At least one of 'sila_server' or 'cloud_server_endpoint' must be configured."
            raise ConfigurationError(msg)


def get_connector_config() -> type[ConnectorBaseConfig]:
    """Get the current connector configuration."""
    derived_configs = {c for c in ConnectorBaseConfig.__subclasses__() if c.__name__ != "ConnectorBaseConfig"}
    if len(derived_configs) > 1 and len({c.__name__ for c in derived_configs}) > 1:
        msg = (
            f"Multiple configurations ({', '.join([c.__name__ for c in derived_configs])}) found. "
            "Please ensure only one subclass of ConnectorBaseConfig exists."
        )
        raise ConfigurationError(msg)

    return derived_configs.pop() if derived_configs else ConnectorBaseConfig


__all__ = [
    "CloudServerConfig",
    "ConnectorBaseConfig",
    "SiLAServerConfig",
    "get_connector_config",
]
