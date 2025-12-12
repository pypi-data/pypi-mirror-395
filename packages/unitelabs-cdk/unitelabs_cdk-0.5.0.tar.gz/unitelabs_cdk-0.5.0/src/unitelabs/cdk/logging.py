import json
import logging
import logging.config
import pathlib

import deprecated
import ruamel.yaml
import typing_extensions as typing


@deprecated.deprecated(
    version="0.2.8",
    reason=(
        "We now globally configure logging instead of configuring the individual logger instance,"
        " therefore replace `create_logger` with `logging.getLogger`."
    ),
)
def create_logger(name: str = __package__, level: int = logging.INFO) -> logging.Logger:
    """Get the app's logger and configure it if needed."""

    logger = logging.getLogger(name)
    handlers = [handler for handler in logger.handlers if not isinstance(handler, logging.NullHandler)]

    if not handlers:
        formatter = logging.Formatter("{asctime} [{levelname!s:<8}] {message!s}", style="{")

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        logger.setLevel(level)
        logger.addHandler(stream_handler)

    return logger


def configure_logging(
    config: typing.Union[None, pathlib.Path, str, dict] = None, log_level: typing.Optional[int] = None
) -> None:
    """
    Configure logging with the given config or provide a file containing the config.

    Args:
      config: Either a path containing the config or the config itself.
        See https://docs.python.org/3/library/logging.config.html#configuration-dictionary-schema
      log_level: Override the root logger's log level.
    """

    if config is None:
        # only create a basic config if no other config is provided
        logging.basicConfig(format="{asctime} [{levelname!s:<8}] {message!s}", style="{")

    if isinstance(config, (pathlib.Path, str)):
        config = pathlib.Path(config)

        if not config.exists():
            msg = f"Provided configuration file {config} does not exist."
            raise ValueError(msg)

        if config.suffix == ".json":
            config = json.loads(config.read_text(encoding="utf-8"))

        elif config.suffix in (".yaml", ".yml"):
            yaml = ruamel.yaml.YAML()
            config = yaml.load(config.read_text(encoding="utf-8"))

    if isinstance(config, dict):
        logging.config.dictConfig(config)

    elif isinstance(config, pathlib.Path):  # .ini files
        logging.config.fileConfig(config)

    if log_level is not None:
        logging.getLogger().setLevel(log_level)
