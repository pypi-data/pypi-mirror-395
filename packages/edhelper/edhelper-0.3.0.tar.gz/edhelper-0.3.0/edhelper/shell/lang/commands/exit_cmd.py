from .base import BaseCommand
from edhelper.shell.repl.context import Context


class ExitCommand(BaseCommand):
    def run(self, ctx: Context):
        if ctx.deck:
            print("Leaving Deck Mode...")
            ctx.set_deck(None)
            ctx.set_deck_cards(None)
            return
        print("Leaving REPL Mode...")
        raise EOFError
