"""
Comandos relacionados a exportação.
"""

import click
from edhelper.commom.deck_commands import DeckCommands
from edhelper.commom.deck_list_commands import DeckListCommands
from edhelper.commom.validators import validate_path
from .utils import handle_cli_exceptions, DECK_NAME


def register_export_commands(cli_group):
    """Registra todos os comandos relacionados a exportação."""

    @cli_group.group("export")
    def deck_export():
        """Export a deck."""
        pass

    @deck_export.command("txt")
    @click.argument("deck_name", type=DECK_NAME)
    @click.argument(
        "path",
        type=click.Path(
            exists=True, dir_okay=True, file_okay=False, writable=True, readable=True
        ),
    )
    @handle_cli_exceptions
    def export_txt(deck_name, path):
        if not validate_path(path):
            return
        cmd = DeckCommands.from_name(deck_name)
        cmd.export_txt(path)

    @deck_export.command("csv")
    @click.argument("deck_name", type=DECK_NAME)
    @click.argument(
        "path",
        type=click.Path(
            exists=True, dir_okay=True, file_okay=False, writable=True, readable=True
        ),
    )
    @handle_cli_exceptions
    def export_csv(deck_name, path):
        if not validate_path(path):
            return
        cmd = DeckCommands.from_name(deck_name)
        cmd.export_csv(path)

    @deck_export.command("json")
    @click.argument("deck_name", type=DECK_NAME)
    @click.argument(
        "path",
        type=click.Path(
            exists=True, dir_okay=True, file_okay=False, writable=True, readable=True
        ),
    )
    @handle_cli_exceptions
    def export_json(deck_name, path):
        if not validate_path(path):
            return
        cmd = DeckCommands.from_name(deck_name)
        cmd.export_json(path)

    @deck_export.command("all")
    @click.argument(
        "path",
        type=click.Path(
            exists=True, dir_okay=True, file_okay=False, readable=True, writable=True
        ),
    )
    def export_all(path):
        DeckListCommands.export_folder(path)
        click.echo(f"Exported everything to {path}")
