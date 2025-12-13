import click
from edhelper.shell.repl.context import Context
from .base import BaseCommand
from edhelper.commom.deck_commands import DeckCommands


class ExportTxtCommand(BaseCommand):
    def __init__(self, path, deck=None):
        self.deck = deck
        self.path = path

    def run(self, ctx: Context):
        if ctx.deck is not None:
            if self.deck is not None:
                click.echo("On Deck Mode, export-txt only needs a path")
                return
            self.deck = ctx.deck.name
        if self.deck is None:
            click.echo("Outside Deck Mode, export-txt needs a deck name")
            return
        assert self.deck is not None
        cmd = DeckCommands.from_name(self.deck)
        if not cmd:
            return
        cmd.export_txt(self.path)
