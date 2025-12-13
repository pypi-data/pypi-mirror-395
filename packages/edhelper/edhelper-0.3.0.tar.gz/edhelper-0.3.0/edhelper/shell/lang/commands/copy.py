import click
from edhelper.commom.deck_commands import DeckCommands
from .base import BaseCommand
from edhelper.shell.repl.context import Context


class CopyCommand(BaseCommand):
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest

    def run(self, ctx: Context):
        if ctx.deck:
            click.echo(f"Deck {self.src} already exists")
            return
        cmd = DeckCommands.from_name(self.src)
        if not cmd:
            click.echo(f"Deck {self.src} not found")
            return
        cmd.copy(self.dest)
