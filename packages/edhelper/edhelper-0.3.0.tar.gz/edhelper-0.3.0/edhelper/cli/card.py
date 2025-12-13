"""
Comandos relacionados a cards.
"""

import click
from edhelper.commom.card_commands import CardCommands
from edhelper.commom.top_commanders_commands import TopCommandersCommands
from edhelper.commom.sync_db_commands import SyncDbCommands
from .utils import handle_cli_exceptions


def register_card_commands(cli_group):
    """Registra todos os comandos relacionados a cards."""

    @cli_group.group()
    def card():
        """Card utilities."""
        pass

    @card.command("find")
    @click.argument("name")
    @handle_cli_exceptions
    def card_show(name):
        cmd = CardCommands.from_name(name)
        cmd.show()

    @card.command("search")
    @click.argument("partial", type=str)
    @handle_cli_exceptions
    def card_search(partial):
        CardCommands.search(partial)

    @card.command("top-commanders")
    @handle_cli_exceptions
    def top_commanders():
        """List the top 100 commanders."""
        TopCommandersCommands.show_top_commanders()

    @card.command("sync-db")
    @handle_cli_exceptions
    def sync_db():
        """Sync all cards in database with API."""
        SyncDbCommands.sync_database()
