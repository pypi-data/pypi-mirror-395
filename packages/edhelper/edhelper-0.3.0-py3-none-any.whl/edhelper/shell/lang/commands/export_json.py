from .base import BaseCommand
import click
from edhelper.commom.deck_commands import DeckCommands


class ExportJsonCommand(BaseCommand):
    def __init__(self, path, deck=None):
        self.deck = deck
        self.path = path

    def run(self, ctx):
        if ctx.deck is not None:
            if self.deck is not None:
                click.echo("On Deck Mode, export-json only needs a path")
                return
            self.deck = ctx.deck.name
        if self.deck is None:
            click.echo("Outside Deck Mode, export-json needs a deck name")
            return
        assert self.deck is not None
        cmd = DeckCommands.from_name(self.deck)
        if not cmd:
            return
        cmd.export_json(self.path)
