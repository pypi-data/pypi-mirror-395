import click
from .base import BaseCommand
from edhelper.commom.deck_commands import DeckCommands


class CreateCommand(BaseCommand):
    def __init__(self, name):
        self.name = name

    def run(self, ctx):
        if ctx.deck:
            click.echo("Command not supported on Deck Mode")
            return
        cmd = DeckCommands.from_name(self.name)
        cmd.create()
