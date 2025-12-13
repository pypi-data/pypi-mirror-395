"""
Comandos relacionados a decks.
"""

import click
from edhelper.commom.deck_commands import DeckCommands
from edhelper.commom.deck_card_commands import DeckCardCommands
from edhelper.commom.commander_meta_commands import CommanderMetaCommands
from edhelper.commom.deck_list_commands import DeckListCommands
from edhelper.commom.validators import validate_path
from .utils import handle_cli_exceptions, DECK_NAME, TXT_FILE


def register_deck_commands(cli_group):
    """Registra todos os comandos relacionados a decks."""

    @cli_group.group()
    def deck():
        """Manage EDH decks."""
        pass

    @deck.command("open")
    @click.argument("deck_name", type=DECK_NAME)
    @click.argument("commander", required=False)
    @handle_cli_exceptions
    def open_or_create(deck_name, commander):
        cmd = DeckCommands.from_name(deck_name)
        if not cmd.exists():
            click.echo(f"Creating deck '{deck_name}'...")
            if commander:
                cmd.create_with_commander(commander)
            else:
                cmd.create()
        click.echo(f"Opening deck '{deck_name}'...")

    @deck.command("create")
    @click.argument("deck_name", type=DECK_NAME)
    @click.argument("commander", required=False)
    @handle_cli_exceptions
    def create_deck(deck_name, commander):
        """Create an empty deck or with a commander."""
        cmd = DeckCommands.from_name(deck_name)
        if commander:
            cmd.create_with_commander(commander)
        else:
            cmd.create()

    @deck.command("import-txt")
    @click.argument("file", type=TXT_FILE)
    @click.argument("deck_name", type=DECK_NAME)
    @handle_cli_exceptions
    def create_deck_from_file(deck_name, file):
        """Create a new deck from a .txt list."""
        if not validate_path(file, ".txt"):
            return
        cmd = DeckCommands.from_name(deck_name)
        cmd.import_txt(file)

    @deck.command("delete")
    @click.argument("deck_name", type=DECK_NAME)
    @handle_cli_exceptions
    def delete_deck(deck_name):
        cmd = DeckCommands.from_name(deck_name)
        cmd.delete()

    @deck.command("rename")
    @click.argument("old", type=DECK_NAME)
    @click.argument("new", type=DECK_NAME)
    @handle_cli_exceptions
    def rename_deck(old, new):
        cmd = DeckCommands.from_name(old)
        cmd.rename(new)

    @deck.command("copy")
    @click.argument("source", type=DECK_NAME)
    @click.argument("new", type=DECK_NAME)
    @handle_cli_exceptions
    def copy_deck(source, new):
        cmd = DeckCommands.from_name(source)
        cmd.copy(new)

    @deck.command("list")
    @click.argument("limit", type=int, required=False)
    def list_decks(limit):
        DeckListCommands.show(limit)

    @deck.command("show")
    @click.argument("deck_name", type=DECK_NAME)
    @handle_cli_exceptions
    def show_deck(deck_name):
        cmd = DeckCardCommands.from_deck_name(deck_name)
        cmd.show()

    @deck.command("set-commander")
    @click.argument("deck_name", type=DECK_NAME)
    @click.argument("commander", type=DECK_NAME)
    @handle_cli_exceptions
    def set_commander(deck_name, commander):
        cmd = DeckCardCommands.from_deck_name(deck_name)
        cmd.set_commander(commander)

    @deck.command("reset-commander")
    @click.argument("deck_name", type=DECK_NAME)
    @handle_cli_exceptions
    def reset_commander(deck_name):
        cmd = DeckCardCommands.from_deck_name(deck_name)
        cmd.reset_commander()

    @deck.command("meta")
    @click.argument("commander_name", type=str)
    @click.argument("category", type=str, required=False)
    @handle_cli_exceptions
    def deck_meta(commander_name, category):
        """Get meta cards for a commander from EDHREC."""
        CommanderMetaCommands.get_meta(commander_name, category)

    @deck.command("add")
    @click.argument("deck_name", type=DECK_NAME)
    @click.argument("card_name", type=DECK_NAME)
    @click.argument("qty", type=int, required=False, default=1)
    @handle_cli_exceptions
    def deck_add_card(deck_name, card_name, qty):
        cmd = DeckCardCommands.from_deck_name(deck_name)
        cmd.add(card_name, qty)

    @deck.command("remove")
    @click.argument("deck_name", type=DECK_NAME)
    @click.argument("card_name", required=True)
    @click.argument("qty", type=int, required=False, default=1)
    @handle_cli_exceptions
    def deck_remove_card(deck_name, card_name, qty):
        cmd = DeckCardCommands.from_deck_name(deck_name)
        cmd.remove(card_name, qty)

    @deck.command("set")
    @click.argument("deck_name", type=DECK_NAME)
    @click.argument("card_name", required=True)
    @click.option("--qty", type=int, required=False, default=1)
    @handle_cli_exceptions
    def deck_set_card_qty(deck_name, card_name, qty):
        cmd = DeckCardCommands.from_deck_name(deck_name)
        cmd.edit_quantity(card_name, qty)

    @deck.command("analyze")
    @click.argument("deck_name", type=DECK_NAME)
    @handle_cli_exceptions
    def analyze_deck(deck_name):
        """Analyze if deck follows Commander format rules."""
        cmd = DeckCommands.from_name(deck_name)
        cmd.analyze()
