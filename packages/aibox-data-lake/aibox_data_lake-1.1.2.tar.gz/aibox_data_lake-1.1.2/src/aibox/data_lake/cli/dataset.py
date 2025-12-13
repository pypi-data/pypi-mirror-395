"""CLI para interação
com dataset.
"""

import typer

from .utils import console, get_client

cli = typer.Typer(
    no_args_is_help=True,
    add_completion=False,
    help="Interação com metadados dos buckets.",
)


@cli.command(name="get-tabular", help="Obtém os metadados de um dataset.", no_args_is_help=True)
def get_tabular(
    bucket: str = typer.Option(help="Nome do bucket."),
    dataset_prefix: str = typer.Option(help="Prefixo do dataset."),
):
    client = get_client()
    ds = client.get_tabular_dataset(bucket, dataset_prefix)
    console.print_json(ds.info.model_dump_json(indent=2))
