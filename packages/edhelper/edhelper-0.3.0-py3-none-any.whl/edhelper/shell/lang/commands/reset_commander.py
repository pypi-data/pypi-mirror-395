import click
from edhelper.shell.repl.context import Context
from .base import BaseCommand
from edhelper.commom.deck_card_commands import DeckCardCommands


class ResetCommanderCommand(BaseCommand):
    def run(self, ctx: Context):
        if ctx.deck is None:
            click.echo("Command not supported outside Deck Mode")
            return
        assert ctx.deck_cards is not None
        assert ctx.deck.name is not None
        cmd = DeckCardCommands.from_deck_name(ctx.deck.name)
        if not cmd:
            return
        cmd.reset_commander()
        ctx.deck_cards = cmd.deck_cards
