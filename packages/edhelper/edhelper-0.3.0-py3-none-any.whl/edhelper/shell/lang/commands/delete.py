import click
from edhelper.commom.deck_commands import DeckCommands
from .base import BaseCommand
import edhelper.domain.deck_service as deck_service
from edhelper.shell.repl.context import Context


class DeleteCommand(BaseCommand):
    def __init__(self, name):
        self.name = name

    def run(self, ctx: Context):
        if ctx.deck:
            click.echo("Command not supported on Deck Mode")
            return
        cmd = DeckCommands.from_name(self.name)
        if not cmd:
            click.echo(f"Deck {self.name} not found")
            return
        cmd.delete()
