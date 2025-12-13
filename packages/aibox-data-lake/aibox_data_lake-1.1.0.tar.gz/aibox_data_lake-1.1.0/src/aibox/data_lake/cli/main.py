"""CLI da biblioteca."""

import typer

from .bucket import cli as bucket
from .config import cli as config
from .dataset import cli as dataset

cli = typer.Typer(no_args_is_help=True, add_completion=False, help="CLI do AiBox Data Lake.")


cli.add_typer(config, name="config")
cli.add_typer(bucket, name="bucket")
cli.add_typer(dataset, name="dataset")


if __name__ == "__main__":
    cli()
