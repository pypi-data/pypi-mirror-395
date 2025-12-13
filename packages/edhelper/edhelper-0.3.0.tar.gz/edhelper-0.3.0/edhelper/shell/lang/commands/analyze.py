from edhelper.shell.repl.context import Context
from .base import BaseCommand
from edhelper.commom.deck_commands import DeckCommands
from edhelper.commom.excptions import DeckNotFound


class AnalizeCommand(BaseCommand):
    def __init__(self, name: str | None = None):
        self.name = name

    def run(self, ctx: Context):
        if self.name is None and ctx.deck is None:
            print("Error: Outside Deck Mode ou must provide a deck name or a deck file")
            return
        if self.name is not None and ctx.deck is not None:
            print("Error: On deck mode you can't provide a deck name")
            return
        if self.name is None:
            assert ctx.deck is not None
            self.name = ctx.deck.name
        try:
            assert self.name is not None
            cmd = DeckCommands.from_name(self.name)
            cmd.analyze()
        except DeckNotFound as e:
            print(f"Error: {e.message}")
        except Exception as e:
            print(f"Error: {e}")
