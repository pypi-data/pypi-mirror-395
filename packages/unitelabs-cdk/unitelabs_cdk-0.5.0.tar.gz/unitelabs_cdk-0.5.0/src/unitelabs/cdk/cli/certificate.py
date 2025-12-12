import pathlib
import typing

import click

import sila
from unitelabs.cdk.config import get_connector_config


class MutuallyExclusiveOptions(Exception):
    """Two mutually exclusive options were used together."""


@click.group()
def certificate() -> None:
    """Handle certificates for TLS encryption."""


@certificate.command()
@click.option(
    "-cfg",
    "--config-path",
    type=click.Path(path_type=pathlib.Path, exists=True),
    default=None,
    required=False,
    help=(
        "The path to the configuration file which contains the UUID and host for the generated certificate, "
        "defaults to ./config.json if uuid and host not provided."
    ),
)
@click.option(
    "--uuid",
    type=str,
    required=False,
    help="The SiLA server's uuid.",
)
@click.option(
    "--host",
    type=str,
    required=False,
    help="The SiLA server's host address.",
)
@click.option(
    "--target",
    "-t",
    type=str,
    help="The output directory in which to store the certificate files.",
)
@click.option(
    "--embed",
    "-e",
    type=bool,
    is_flag=True,
    default=False,
    help=(
        "Whether or not to embed the certificate and key into the config file. "
        "Mutually exclusive with usage of '--target'."
        "Implies --non-interactive."
    ),
)
@click.option(
    "--non-interactive",
    "-y",
    type=bool,
    is_flag=True,
    default=False,
    help=(
        "When using the `--config-path` option: "
        "suppress the input prompt and automatically update the config file's TLS values."
    ),
)
def generate(
    config_path: typing.Optional[pathlib.Path],
    uuid: typing.Optional[str],
    host: typing.Optional[str],
    target: typing.Optional[str],
    embed: bool,
    non_interactive: bool,
) -> None:
    """
    Generate a new self-signed certificate according to the SiLA 2 specification.

    Create a certificate with provided UUID and host.
    ```certificate generate --uuid <UUID> --host <host name>```

    Create a certificate using the UUID and host from the provided config file.
    ```certificate generate --config-path <path to config>```

    Create a certificate from a config file and update the config to enable TLS encryption.
    ```certificate generate --config-path <path to config> -y```

    Embed the generated certificate and key into the config file rather than writing to files on disk.
    ```certificate generate --config-path <path to config> --embed```

    The option `--config-path` cannot be used in combination with either `--host` or `--uuid`.
    The option `--target` cannot be used in combination with `--embed`.

    If no `config-path`, `uuid`, or `host` is provided, searches the default config file locations:
    `./config.json`, `./config.yaml`, and `./config.yml` for an existing config file.
    If no config file is found in any of the default locations, a `FileNotFoundError` is raised.
    """
    config_cls = get_connector_config()

    if target and embed:
        msg = "The option '--target' cannot be used with '--embed'."
        raise MutuallyExclusiveOptions(msg)

    if config_path and (uuid or host):
        msg = "The option '--config-path' cannot be used with '--uuid' or '--host'."
        raise MutuallyExclusiveOptions(msg)

    if not (uuid or host) and (config_path or config_path is None):
        config = config_cls.load(config_path)
        config_path = config_path or config._source_path

        uuid = config.sila_server.uuid
        host = config.sila_server.hostname

    key, cert = sila.server.generate_certificate(uuid, host)

    if not embed:
        target = target or "."
        click.echo(f"Writing certificate and key to directory: {target}")
        directory = pathlib.Path(target)
        directory.mkdir(parents=True, exist_ok=True)

        cert_path = directory / "cert.pem"
        cert_path.write_bytes(cert)
        cert = str(cert_path.resolve())

        key_path = directory / "key.pem"
        key_path.write_bytes(key)
        key = str(key_path.resolve())

    else:
        key = key.decode("ascii")
        cert = cert.decode("ascii")

    if config_path:
        if not non_interactive and not embed:
            response = click.prompt("Do you want to update your configuration file to enable TLS encryption? Enter Y/N")
            if response.lower() not in ["y", "yes"]:
                return

        config.sila_server.tls = True
        config.sila_server.private_key = key
        config.sila_server.certificate_chain = cert
        click.echo(f"Updating configuration file at: {config_path}.")
        config.dump(config_path)


if __name__ == "__main__":
    certificate()
