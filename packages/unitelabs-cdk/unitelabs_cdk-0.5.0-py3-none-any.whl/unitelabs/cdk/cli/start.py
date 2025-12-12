import logging
import pathlib

import click

from unitelabs.cdk import utils
from unitelabs.cdk.config import read_config_file
from unitelabs.cdk.logging import configure_logging

from ..main import run


class TLSConfigurationError(Exception):
    """TLS Configuration is invalid."""


@click.command()
@click.option(
    "--app",
    type=str,
    metavar="IMPORT",
    default=utils.find_factory,
    show_default=False,
    help="The application factory function to load, in the form 'module:name'.",
    envvar="UNITELABS_CDK_APP",
)
@click.option(
    "-cfg",
    "--config-path",
    type=click.Path(path_type=pathlib.Path),
    default=pathlib.Path("./config.json"),
    help="Path to the configuration file.",
)
@click.option(
    "-v",
    "--verbose",
    count=True,
    help=(
        "Increase the verbosity of the default logger. "
        "Use a custom log-config for fine grained handling."
        "When used together with a log-config, this will override the root logger's level."
    ),
)
@utils.coroutine
async def start(app, config_path: pathlib.Path, verbose: int) -> None:  # noqa: ANN001
    """Application Entrypoint."""

    config = read_config_file(config_path)

    log_level = logging.ERROR - verbose * 10 if verbose else None
    log_config = config.get("logging", None)
    configure_logging(log_config, log_level=log_level)

    await run(app, config=config)
