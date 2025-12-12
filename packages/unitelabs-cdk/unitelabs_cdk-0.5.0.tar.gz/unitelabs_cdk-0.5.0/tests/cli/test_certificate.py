import json
import pathlib
import typing
import uuid

import pytest
from click.testing import CliRunner

from unitelabs.cdk.cli.certificate import MutuallyExclusiveOptions
from unitelabs.cdk.config import ConnectorBaseConfig


@pytest.fixture
def create_temp_config(tmp_path) -> typing.Callable[[str], tuple[ConnectorBaseConfig, pathlib.Path]]:
    def config(ext: str) -> tuple[ConnectorBaseConfig, pathlib.Path]:
        config_path = tmp_path / f"config.{ext}"
        config = ConnectorBaseConfig()
        config.dump(config_path)
        return (config, config_path)

    return config


@pytest.fixture
def temp_config_with_comment(
    create_temp_config,
) -> typing.Generator[tuple[ConnectorBaseConfig, pathlib.Path], None, None]:
    config, config_path = create_temp_config("yaml")
    with config_path.open("a") as f:
        f.write("# comment\n")
    yield (config, config_path)


class TestGenerate:
    @pytest.mark.parametrize("ext", ["json", "yaml", "yml"])
    def test_should_accept_config_file(self, create_temp_config, ext):
        from unitelabs.cdk.cli import certificate

        runner = CliRunner()
        config, config_path = create_temp_config(ext)

        result = runner.invoke(
            certificate, ["generate", "--config-path", config_path, "--target", config_path.parent], input="n"
        )
        assert result.exit_code == 0

        config_file_contents = ConnectorBaseConfig.load(config_path)

        assert config_file_contents == config

    @pytest.mark.parametrize("ext", ["json", "yaml", "yml"])
    def test_should_update_config_file_with_prompt(self, create_temp_config, ext):
        from unitelabs.cdk.cli import certificate

        runner = CliRunner()
        config, config_path = create_temp_config(ext)

        result = runner.invoke(
            certificate, ["generate", "--config-path", config_path, "--target", config_path.parent], input="y"
        )
        assert result.exit_code == 0

        config_file_contents = ConnectorBaseConfig.load(config_path)

        # cert, key, and tls values have been updated
        assert config_file_contents.sila_server
        assert config_file_contents.sila_server.tls
        assert isinstance(config_file_contents.sila_server.certificate_chain, bytes)
        assert isinstance(config_file_contents.sila_server.private_key, bytes)

        # all other values are the same
        assert config_file_contents != config

        config_file_contents.sila_server.certificate_chain = None
        config_file_contents.sila_server.private_key = None
        config_file_contents.sila_server.tls = False

        assert config_file_contents == config

    @pytest.mark.parametrize("ext", ["json", "yaml", "yml"])
    def test_update_should_suppress_prompt_and_update_config(self, create_temp_config, ext):
        from unitelabs.cdk.cli import certificate

        runner = CliRunner()
        config, config_path = create_temp_config(ext)

        result = runner.invoke(
            certificate, ["generate", "--config-path", config_path, "--target", config_path.parent, "-y"]
        )
        assert result.exit_code == 0

        config_file_contents = ConnectorBaseConfig.load(config_path)

        # cert, key, and tls values have been updated
        assert config_file_contents.sila_server
        assert config_file_contents.sila_server.tls
        assert isinstance(config_file_contents.sila_server.certificate_chain, bytes)
        assert isinstance(config_file_contents.sila_server.private_key, bytes)

        # all other values are the same
        assert config_file_contents != config

        config_file_contents.sila_server.certificate_chain = None
        config_file_contents.sila_server.private_key = None
        config_file_contents.sila_server.tls = False

        assert config_file_contents == config

    def test_uuid_and_host_should_generate_certs(self, tmp_path):
        from unitelabs.cdk.cli import certificate

        cert_path = tmp_path / "cert.pem"
        key_path = tmp_path / "key.pem"

        assert not cert_path.exists()
        assert not key_path.exists()

        runner = CliRunner()
        result = runner.invoke(
            certificate, ["generate", "--uuid", str(uuid.uuid4()), "--host", "localhost", "--target", tmp_path]
        )
        assert result.exit_code == 0

        assert cert_path.exists()
        assert key_path.exists()

    def test_should_not_allow_config_path_and_uuid(self, create_temp_config):
        from unitelabs.cdk.cli import certificate

        _, config_path = create_temp_config("json")

        runner = CliRunner()
        result = runner.invoke(certificate, ["generate", "--config-path", config_path, "--uuid", str(uuid.uuid4())])

        assert result.exit_code == 1
        assert result.exc_info
        assert result.exc_info[0] == MutuallyExclusiveOptions

    def test_should_not_allow_config_path_and_host(self, create_temp_config):
        from unitelabs.cdk.cli import certificate

        _, config_path = create_temp_config("json")

        runner = CliRunner()
        result = runner.invoke(certificate, ["generate", "--config-path", config_path, "--host", "localhost"])

        assert result.exit_code == 1
        assert result.exc_info
        assert result.exc_info[0] == MutuallyExclusiveOptions

    def test_should_not_allow_config_path_and_uuid_and_host(self, create_temp_config):
        from unitelabs.cdk.cli import certificate

        _, config_path = create_temp_config("json")

        runner = CliRunner()
        result = runner.invoke(
            certificate, ["generate", "--config-path", config_path, "--uuid", str(uuid.uuid4()), "--host", "localhost"]
        )

        assert result.exit_code == 1
        assert result.exc_info
        assert result.exc_info[0] == MutuallyExclusiveOptions

    def test_should_not_allow_embed_and_target(self, create_temp_config):
        from unitelabs.cdk.cli import certificate

        _, config_path = create_temp_config("json")

        runner = CliRunner()
        result = runner.invoke(
            certificate,
            [
                "generate",
                "--config-path",
                config_path,
                "--embed",
                "--target",
                config_path.parent,
            ],
        )

        assert result.exit_code == 1
        assert result.exc_info
        assert result.exc_info[0] == MutuallyExclusiveOptions

    @pytest.mark.parametrize("ext", ["json", "yaml", "yml"])
    def test_should_embed_certificate_and_key_in_config(self, create_temp_config, ext):
        from unitelabs.cdk.cli import certificate

        _, config_path = create_temp_config(ext)

        runner = CliRunner()
        result = runner.invoke(
            certificate,
            [
                "generate",
                "--config-path",
                config_path,
                "--embed",
            ],
        )
        assert result.exit_code == 0

        config_file_contents = ConnectorBaseConfig.load(config_path)

        # cert, key, and tls values have been updated
        assert config_file_contents.sila_server
        assert config_file_contents.sila_server.tls
        assert isinstance(config_file_contents.sila_server.certificate_chain, bytes)
        assert isinstance(config_file_contents.sila_server.private_key, bytes)

    def test_should_preserve_unknown_config_keys(self, tmp_path):
        from unitelabs.cdk.cli import certificate

        config_data = ConnectorBaseConfig().to_dict()
        config_data["simple"] = True

        config_path = tmp_path / "config.json"
        with config_path.open("w") as f:
            f.write(json.dumps(config_data))

        runner = CliRunner()
        result = runner.invoke(
            certificate, ["generate", "--config-path", config_path, "--target", config_path.parent, "-y"]
        )
        assert result.exit_code == 0

        with config_path.open("r") as f:
            updated = json.load(f)

        assert "simple" in updated

    def test_should_preserve_comments(self, temp_config_with_comment):
        from unitelabs.cdk.cli import certificate

        _, config_path = temp_config_with_comment

        runner = CliRunner()
        result = runner.invoke(
            certificate, ["generate", "--config-path", config_path, "--target", config_path.parent, "-y"]
        )
        assert result.exit_code == 0

        with config_path.open("r") as f:
            updated = f.read()

        assert "# comment\n" in updated
