"""CLI para configuração
da biblioteca.
"""

import typer
from rich.prompt import Confirm

from aibox.data_lake.config import Config
from aibox.data_lake.factory import get_bucket

from .utils import console, get_config

cli = typer.Typer(
    no_args_is_help=True, add_completion=False, help="Configuração de buckets & acesso."
)


@cli.command(name="show", help="Exibe a configuração atual da biblioteca.")
def show():
    config = get_config()
    console.print_json(config.model_dump_json(indent=2))


@cli.command(name="register", help="Registra um novo bucket para uso.", no_args_is_help=True)
def register(
    name: str = typer.Option(help="Nome do bucket."),
    url: str = typer.Option(help="URL do bucket."),
):
    registered_buckets = get_config().registered_buckets
    if name in registered_buckets:
        console.print("[info]Bucket já resgitrado.[/]")
        if not Confirm.ask("[warning]Deseja sobrescrever?[/]", default=True, console=console):
            return

    # Registrando bucket
    registered_buckets[name] = url
    config = Config(registered_buckets=registered_buckets)

    # Persistência
    config.save_to_file()
    console.print("[success]Configuração atualizada:[/]")
    console.print_json(config.model_dump_json(indent=2))


@cli.command(name="remove", help="Remove um bucket do registro.", no_args_is_help=True)
def remove(name: str = typer.Option("Nome do bucket.")):
    config = get_config()

    if name not in config.registered_buckets:
        console.print("[warning]Bucket não encontrado no registro.[/]")
        return

    del config.registered_buckets[name]
    config.save_to_file()
    console.print(f"[success]Bucket '{name}' removido com sucesso![/]")


@cli.command(name="validate", help="Valida as configurações atuais.")
def validate():
    config = get_config()
    for name, bucket_url in config.registered_buckets.items():
        bucket = str(bucket_url)
        try:
            get_bucket(bucket)
        except Exception as e:
            console.print(f"[error]Não foi possível accesar o bucket '{name}': {e}[/]")
            console.print(
                "[warning]Confirme que possui acesso ao bucket ou atualize as configurações.[/]"
            )
            return -1
    console.print("[info]Configurações válidas![/]")
