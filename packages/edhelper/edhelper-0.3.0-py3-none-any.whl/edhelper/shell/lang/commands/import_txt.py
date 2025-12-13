from edhelper.commom.deck_commands import DeckCommands
from .base import BaseCommand
from edhelper.shell.repl.context import Context


class ImportTxtCommand(BaseCommand):
    def __init__(self, filename, deck_name):
        self.filename = filename
        self.deck_name = deck_name

    def run(self, ctx: Context):
        if ctx.deck is not None:
            print("Command not supported on Deck Mode")
            return
        cmd = DeckCommands.from_name(self.deck_name)
        cmd.import_txt(self.filename)
