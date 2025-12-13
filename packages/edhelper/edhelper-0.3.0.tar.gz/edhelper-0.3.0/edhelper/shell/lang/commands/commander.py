from .base import BaseCommand
from edhelper.shell.repl.context import Context


class CommanderCommand(BaseCommand):
    def run(self, ctx: Context):
        if ctx.deck is None:
            print("No deck selected")
            return
        assert ctx.deck_cards is not None

        for dc in ctx.deck_cards:
            if dc.is_commander:
                print(f"Commander: {dc.card.name}")
                dc.card.show()
                return
