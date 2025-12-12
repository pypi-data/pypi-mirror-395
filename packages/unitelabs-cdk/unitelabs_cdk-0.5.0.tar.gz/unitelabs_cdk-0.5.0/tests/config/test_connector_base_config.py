import dataclasses
import gc
import json
import pathlib
import uuid

import pytest
import typing_extensions as typing
from ruamel.yaml import YAML

from unitelabs.cdk.config import (
    CloudServerConfig,
    ConfigurationError,
    ConnectorBaseConfig,
    SiLAServerConfig,
    UnsupportedConfigFiletype,
    get_connector_config,
)
from unitelabs.cdk.config.config import SerializableDict

BASE_CONFIG_DEFAULT: SerializableDict = {
    "sila_server": {
        "hostname": "0.0.0.0",
        "port": 0,
        "tls": False,
        "require_client_auth": False,
        "root_certificates": None,
        "certificate_chain": None,
        "private_key": None,
        "options": {},
        "name": "SiLA Server",
        "type": "ExampleServer",
        "description": "",
        "version": "0.1",
        "vendor_url": "https://sila-standard.com",
    },
    "discovery": {"network_interfaces": [], "ip_version": "ipv4"},
    "cloud_server_endpoint": {
        "hostname": "localhost",
        "port": 50001,
        "tls": True,
        "root_certificates": None,
        "certificate_chain": None,
        "private_key": None,
        "reconnect_delay": 10000,
        "options": {},
    },
    "logging": None,
}
CERT = """
-----BEGIN CERTIFICATE-----
MIIC/jCCAeagAwIBAgIURXGhJmigNdNvgR3wMdlsv43VhCEwDQYJKoZIhvcNAQEL
BQAwEDEOMAwGA1UEAwwFU2lMQTIwHhcNMjQxMDA5MTMwNDU1WhcNMjUxMDA5MTMw
NDU1WjAQMQ4wDAYDVQQDDAVTaUxBMjCCASIwDQYJKoZIhvcNAQEBBQADggEPADCC
AQoCggEBAMCSToXHEzV76zHO3pATJ+M3zRqnbZ9KwyGJzWCA7jmZZWkCligW7QgQ
COf8AdOcf5eZawop63HeDDqkuQtAAKwOUiVjLgoPXpu9l9lxDSBo1XfquTIvgNGY
wN7i2W9zQQ0U78iBJ7+xcEbkf9m/s5yyKXGOds1apBVx184Qb2MKnGc2mK6WkRf3
uIBBj/o3JzNlEu040zIok/A/DtRimgoxOipjzbLYRq5xLtod1tpyw1lsQGctfCNi
27bYApcA2UUpy0PG8BUMbT2jkwLTkruKrfx9x4tcHL3PH9s0oXWzijKFw8seAx15
LIhoyjonygZeoKaEAkT2Rv+WzGeUDRsCAwEAAaNQME4wGgYDVR0RBBMwEYIJbG9j
YWxob3N0hwR/AAABMDAGCCsGAQQBg8lXBCQ1YThmZGI3MS1lZTIzLTQ1MmMtODM1
Yy1lMjI0ZGY3YmU5NTAwDQYJKoZIhvcNAQELBQADggEBAF9NbU6GItVjepD1w4UA
2V4UUfcrKdk9xO0FVEF/lRyPoRaoKzO08k5AJ47tmjqqqpijzYXspKta+UEMiAUE
qoCRhgLCvtrAIp7nhsCNw7fyK+i+866q1dyB2VogDbLwxyAj4nxd4o2flWNPaTqr
XgQ9xGuww3Izngr+MGFKsE9CJ7b5emq67lfGQ8UkwvfU2XhcPWPJAyHi2kQPVXFk
UmmzQoqnqELfSNpnd5zUrgdVVtABHZ+rsCJpldU0yO5OQ4pfm+f56VmS2Da2vDZt
GkEfLq/po/VTGOB6bZ1oV+kR+ZHbRpCh0mAQ+OvuUuWOAmuQ30m26nA+w7+VyLux
ht4=
-----END CERTIFICATE-----

"""
KEY = """
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAwJJOhccTNXvrMc7ekBMn4zfNGqdtn0rDIYnNYIDuOZllaQKW
KBbtCBAI5/wB05x/l5lrCinrcd4MOqS5C0AArA5SJWMuCg9em72X2XENIGjVd+q5
Mi+A0ZjA3uLZb3NBDRTvyIEnv7FwRuR/2b+znLIpcY52zVqkFXHXzhBvYwqcZzaY
rpaRF/e4gEGP+jcnM2US7TjTMiiT8D8O1GKaCjE6KmPNsthGrnEu2h3W2nLDWWxA
Zy18I2LbttgClwDZRSnLQ8bwFQxtPaOTAtOSu4qt/H3Hi1wcvc8f2zShdbOKMoXD
yx4DHXksiGjKOifKBl6gpoQCRPZG/5bMZ5QNGwIDAQABAoIBAE023PFbH2Kkq2uv
TSJr6+R5rW3wkE38xj0eahE14U+LKFRwyxCMEMLY2xlZvMnCyI5a38aVhGiF5lVl
UyUlpp9Wpq2DFSTHgOHlpYt0fxTttBp/LX7n+TkRjNRSFWlQx1adfH/i+bMtTJ3A
ZVtEOJqt/VwhCZXRsFVA7o0bne4R0VZZW/5eDH4nF9JNQsvOo2Qrcx7fRzld4khx
7Y3lbf363RQndONdJ7znPMZMd1RzFWygsjbU8vjcL2rA7bDEHLkqKc6er+RDPTWq
SgnMT2vL/+lzQxuf59JaIBU3nJA02+8jLWjMpRLSbvnNuxV/YN4j9+tzC5ChPm/4
+3HnwBECgYEA/0EtN1hl8SbwEAz+hoVB6pOhjIPOBrKqT/1xRLyPPGt5zlM3vFmc
o60LV5hcWI7dajd4TRc6mYZEYpMkWPY9FQKSANH1WmHwp9rRUwDyTCn6xvza5dk/
cV1ZnvMMjwfKi531NhZQerA4Fg/3CoiToBXIWRBl4+Vhh2Tx1mcUuA8CgYEAwSJE
+nbESRR5rbKEC1Yezc+RuxzhVqIWApOVZx29O6VLMmlL+O1ZiK6Z08YUNNno6otc
Lnhi3I5bv2O5CS4ubUpqtwLuOKKJPLdx8ZBh5aJ/1LVfEmqih58FxzYiZ3+Hfsjy
PaqSwEDp3CcShZ6Tzz8eaeJFaG9k56a659QU7jUCgYAaG2FzirAKhTAChEG4IoMG
agkY5RY6ayWuPr7KB/sic9+mca5+ri+uMfG6CNRRHnOY/IlqYRjWQPxXlLMgAjdn
IbcrLE5K6z+A+4lzUuJ1VcnXdl8xKRIrFyAmeLdtHZ/ivcopuQiMM9/YqdNbmXJ3
6iJusZWqRHjAL1vo0Ow2kwKBgQCNhKTyupA91IkMpCBphiNwP8bTSug7aO2j2azC
MGJ3EDm3qLyInLLcmsQRD7XCvGIVaySS0JfwcUf9R/9QIMzYPI1RqQ4R5deV6/3M
OjXh5F6y6GvPvN93bSj4vkwbdrE8T9ZhJVn/EhHKxb6mtnoshF2uzKR7UBSqQdv2
/8qOeQKBgQDdWqFawsUcMZmq3faoipofg0Gl8pZiKYjVOV5QBz8z2mxxUuHGB3VQ
17kBvR3rnhbyhj/kS0rq7mKib+8K9WjKeZr/ypr1oiOSXKPm5UqZTctFcAqkvgyE
Sz0JRTsDjVBHrdnbVUF6QNh+hqTkqYGMu2RcArnvmMdnQ5D1jMfe0A==
-----END RSA PRIVATE KEY-----

"""

yaml_config_w_comments = """sila_server:
  hostname: 0.0.0.0
  port: 0
  tls: false # comment about tls
  require_client_auth: false
  root_certificates:
  certificate_chain:
  private_key:
  options: {}
  uuid: 3264bf7c-45d0-4fb5-9da4-d4fa53eedb6c
  name: Server Name
  type: ExampleServer
  description: Multi-line description that can span multiple lines
    if needed and still survive the round trip. This should survive
    as well.
  version: 0.1.6_rc1
  vendor_url: https://unitelabs.io/
discovery:
  network_interfaces: []
  ip_version: ipv4
cloud_server_endpoint:  # cloud server comment
  hostname: localhost
  port: 50001
  tls: false
  root_certificates:
  certificate_chain:
  private_key:
  reconnect_delay: 10000.0
  options: {}
logging:
"""


@pytest.fixture()
def config_file(tmp_path) -> pathlib.Path:
    config_path = tmp_path / "config.yaml"
    with config_path.open("w") as f:
        f.write(yaml_config_w_comments)
    yield config_path


@pytest.fixture
def cleanup():
    """Garbage collect derived Config classes to ensure `get_connector_config` finds only one subclass."""
    yield
    gc.collect()


def normalize_whitespace(s: str) -> str:
    """Remove extra whitespace from a string, while preserving comments."""
    return "\n".join("".join(map(str.rstrip, line.split("#"))) for line in s.splitlines()).rstrip()


class TestInnerTypes:
    def test_sila_server_conversion(self):
        default = ConnectorBaseConfig().to_dict()
        instance = ConnectorBaseConfig(**default)
        assert isinstance(instance.sila_server, SiLAServerConfig)

    @pytest.mark.parametrize(
        "path,content,key", [("cert.pem", CERT, "certificate_chain"), ("key.pem", KEY, "private_key")]
    )
    def test_sila_server_cert_key_conversion(self, tmp_path, path, content, key):
        path = tmp_path / path
        path.touch()
        path.write_bytes(content.encode("ascii"))

        default = ConnectorBaseConfig().to_dict()
        default["sila_server"][key] = path

        config = ConnectorBaseConfig(**default)
        assert isinstance(getattr(config.sila_server, key), bytes)
        assert getattr(config.sila_server, key).decode("ascii") == content

    def test_cloud_server_endpoint_conversion(self):
        default = ConnectorBaseConfig().to_dict()
        instance = ConnectorBaseConfig(**default)
        assert isinstance(instance.cloud_server_endpoint, CloudServerConfig)

    @pytest.mark.parametrize(
        "path,content,key", [("cert.pem", CERT, "certificate_chain"), ("key.pem", KEY, "private_key")]
    )
    def test_cloud_server_endpoint_cert_key_conversion(self, tmp_path, path, content, key):
        path = tmp_path / path
        path.touch()
        path.write_bytes(content.encode("ascii"))

        default = ConnectorBaseConfig().to_dict()
        default["cloud_server_endpoint"][key] = path

        config = ConnectorBaseConfig(**default)
        assert isinstance(getattr(config.cloud_server_endpoint, key), bytes)
        assert getattr(config.cloud_server_endpoint, key).decode("ascii") == content

    @pytest.mark.parametrize("key,name", [("certificate_chain", "Certificate chain"), ("private_key", "Private key")])
    def test_sila_server_cert_key_file_not_found(self, key, name):
        default = ConnectorBaseConfig().to_dict()
        path = pathlib.Path("path.json")
        default.update({"sila_server": {f"{key}": path}})
        with pytest.raises(FileNotFoundError, match=rf"File at path '{path.resolve()}' not found."):
            ConnectorBaseConfig(**default)

    @pytest.mark.parametrize("key,name", [("certificate_chain", "Certificate chain"), ("private_key", "Private key")])
    def test_cloud_server_endpoint_cert_key_file_not_found(self, key, name):
        default = ConnectorBaseConfig().to_dict()
        path = pathlib.Path("path.json")
        default.update({"cloud_server_endpoint": {f"{key}": path}})

        with pytest.raises(FileNotFoundError, match=rf"File at path '{path.resolve()}' not found."):
            ConnectorBaseConfig(**default)

    def test_should_not_allow_neither_sila_server_nor_cloud_server(self):
        default = ConnectorBaseConfig().to_dict()
        default["sila_server"] = None
        default["cloud_server_endpoint"] = None

        with pytest.raises(
            ConfigurationError,
            match=r"At least one of 'sila_server' or 'cloud_server_endpoint' must be configured.",
        ):
            ConnectorBaseConfig(**default)


class TestSchema:
    def test_schema(self, cleanup):
        @dataclasses.dataclass
        class ExampleConfig(ConnectorBaseConfig):
            complex: bool = False
            """Whether or not the complex configuration is enabled."""
            complex_name: typing.Optional[str] = ""
            """The name of the complex configuration."""

        schema = ExampleConfig.schema()

        assert schema


class TestFromDict:
    def test_type_conversion(self):
        default = ConnectorBaseConfig().to_dict()
        instance = ConnectorBaseConfig.from_dict(default)
        assert isinstance(instance.sila_server, SiLAServerConfig)
        assert isinstance(instance.cloud_server_endpoint, CloudServerConfig)

    def test_should_allow_arbitrary_fields(self):
        default = ConnectorBaseConfig().to_dict()
        default["this"] = "that"
        instance = ConnectorBaseConfig.from_dict(default)
        assert instance.this == "that"

    def test_should_validate_known_fields(self):
        default: SerializableDict = ConnectorBaseConfig().to_dict()
        default["sila_server"]["port"] = "invalid"
        with pytest.raises(
            ConfigurationError,
            match=r"Invalid configuration for ConnectorBaseConfig: "
            "1 validation error for ConnectorBaseConfig\n"
            "sila_server.port\n  "
            "Input should be a valid integer, unable to parse string as an integer",
        ):
            ConnectorBaseConfig.from_dict(default)


class TestLoad:
    def test_should_load_yaml_file(self, tmp_path):
        config_file_path = tmp_path / "config.yaml"
        config = BASE_CONFIG_DEFAULT.copy()
        config["sila_server"]["uuid"] = str(uuid.uuid4())
        with config_file_path.open("w") as f:
            YAML().dump(config, f)

        instance = ConnectorBaseConfig.load(config_file_path)
        data = dataclasses.asdict(instance)
        assert data == config

    def test_should_load_json_file(self, tmp_path):
        config_file_path = tmp_path / "config.json"
        config = BASE_CONFIG_DEFAULT.copy()
        config["sila_server"]["uuid"] = str(uuid.uuid4())
        with config_file_path.open("w") as f:
            json.dump(config, f)

        instance = ConnectorBaseConfig.load(config_file_path)
        data = dataclasses.asdict(instance)
        assert data == config


class TestDump:
    def test_should_dump_yaml_file(self, tmp_path):
        config_file_path = tmp_path / "config.yaml"
        config = BASE_CONFIG_DEFAULT.copy()
        config["sila_server"]["uuid"] = str(uuid.uuid4())

        ConnectorBaseConfig.from_dict(config).dump(config_file_path)

        with config_file_path.open("r") as f:
            data = YAML().load(f)

        assert data == config

    def test_should_dump_json_file(self, tmp_path):
        config_file_path = tmp_path / "config.json"
        config = BASE_CONFIG_DEFAULT.copy()
        config["sila_server"]["uuid"] = str(uuid.uuid4())

        ConnectorBaseConfig.from_dict(config).dump(config_file_path)

        with config_file_path.open("r") as f:
            data = json.load(f)

        assert data == config

    @pytest.mark.parametrize("ext", ["toml", "ini"])
    def test_should_raise_unsupported_filetype(self, tmp_path, ext):
        config_file_path = tmp_path / f"config.{ext}"
        config_file_path.touch()

        config = BASE_CONFIG_DEFAULT.copy()
        config["sila_server"]["uuid"] = str(uuid.uuid4())

        instance = ConnectorBaseConfig.from_dict(config)
        with pytest.raises(
            UnsupportedConfigFiletype,
            match=f"Cannot write file to {config_file_path.resolve()}. Only yaml and json filetypes are supported.",
        ):
            instance.dump(config_file_path)

    def test_yaml_comment_preservation(self, config_file, tmp_path):
        config = ConnectorBaseConfig.load(config_file)
        test_path = tmp_path / "dump.yaml"
        config.dump(test_path)

        round_trip_data: str = test_path.read_text()

        # Compare while ignoring trailing whitespace differences per line

        assert normalize_whitespace(round_trip_data) == normalize_whitespace(yaml_config_w_comments)

    def test_should_preserve_comment_on_updated_value_line(self, config_file, tmp_path):
        config = ConnectorBaseConfig.load(config_file)
        config.sila_server.tls = True
        out_path = tmp_path / "out.yaml"
        config.dump(out_path)

        assert ConnectorBaseConfig.load(out_path).sila_server.tls
        assert normalize_whitespace(out_path.read_text()) == normalize_whitespace(
            yaml_config_w_comments.replace("tls: false # comment about tls", "tls: true # comment about tls")
        )


class TestGetConnectorConfig:
    def test_should_return_base_if_no_derived_config_exists(self):
        assert get_connector_config() == ConnectorBaseConfig

    def test_should_find_derived_config(self, cleanup):
        @dataclasses.dataclass
        class ExampleConfig(ConnectorBaseConfig):
            value: bool = False

        assert get_connector_config() == ExampleConfig

    def test_should_raise_for_multiple_configs(self, cleanup):
        @dataclasses.dataclass
        class ExampleConfig(ConnectorBaseConfig):
            simple: bool = False

        @dataclasses.dataclass
        class SecondaryExampleConfig(ConnectorBaseConfig):
            simple: bool = True

        with pytest.raises(
            ConfigurationError,
            match=r"Please ensure only one subclass of ConnectorBaseConfig exists.",
        ):
            get_connector_config()
