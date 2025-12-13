import click
from .base import BaseCommand
from edhelper.commom.deck_card_commands import DeckCardCommands
from edhelper.shell.repl.context import Context


class SetCommanderCommand(BaseCommand):
    def __init__(self, name):
        self.name = name.strip()

    def run(self, ctx: Context):
        if ctx.deck is None:
            click.echo("Command not supported outside Deck Mode")
            return
        assert ctx.deck_cards is not None
        assert ctx.deck.name is not None
        cmd = DeckCardCommands.from_deck_name(ctx.deck.name)
        if not cmd:
            return
        cmd.set_commander(self.name)
        ctx.deck_cards = cmd.deck_cards
