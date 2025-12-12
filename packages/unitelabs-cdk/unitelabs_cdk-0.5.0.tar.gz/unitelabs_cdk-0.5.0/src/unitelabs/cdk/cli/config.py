import json
import pathlib
import typing

import click

from unitelabs.cdk import utils
from unitelabs.cdk.config import get_connector_config
from unitelabs.cdk.main import load


@click.group(context_settings=dict(show_default=True))
def config() -> click.Group:
    """Configure a connector."""


@config.command()
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
    "-p",
    "--path",
    type=click.Path(
        exists=False,
        dir_okay=False,
        writable=True,
        resolve_path=True,
        path_type=pathlib.Path,
    ),
    default=None,
    required=False,
    help="Path to the configuration schema file.",
)
@utils.coroutine
async def schema(app, path: typing.Optional[pathlib.Path]) -> None:  # noqa: ANN001
    """Create a configuration jsonschema."""
    await load(app)
    config = get_connector_config()
    if not path:
        click.echo(json.dumps(config.schema(), indent=2))
        return

    with path.open("w") as file:
        json.dump(config.schema(), file, indent=2)


@config.command()
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
    "-o",
    "--output",
    type=str,
    required=False,
    help="The name of the field in the schema to output information about, otherwise the entire schema is shown.",
)
@utils.coroutine
async def show(app, output: typing.Optional[str] = None) -> None:  # noqa: ANN001
    """Visualize the configuration options."""
    await load(app)
    config = get_connector_config()
    description = config.describe(output)

    from rich.console import Console
    from rich.table import Column, Table

    table = Table(
        Column("Field", justify="left"),
        Column("Type", justify="right"),
        Column("Description", justify="right"),
        Column("Example", justify="right"),
        title=f"{config.__name__} Definition",
        show_lines=True,
    )

    for name, values in description.items():
        if not isinstance(values, dict):
            table.add_row(output, *description.values())
            break
        if "values" not in values:
            table.add_row(name, *values.values())
        else:
            table.add_row(name, values["type"], values["description"], values["default"])

    console = Console()
    console.print(table)


@config.command()
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
    "--path",
    type=click.Path(
        exists=False,
        dir_okay=False,
        writable=True,
        resolve_path=True,
        path_type=pathlib.Path,
    ),
    default=pathlib.Path("./config.json"),
    help="Path to the configuration file.",
)
@click.option(
    "--force",
    "-f",
    is_flag=True,
    default=False,
    help="Whether to override an existing configuration file.",
)
@utils.coroutine
async def create(app: str, path: pathlib.Path, force: bool) -> None:
    """Create a configuration file."""
    await load(app)
    if path.exists() and not force:
        msg = (
            f"Config file already exists at: '{path}'. "
            "To force an overwrite of the existing config file, use the '--force' flag."
        )
        raise FileExistsError(msg)
    config = get_connector_config()
    config().dump(path)


if __name__ == "__main__":
    config()
