from edhelper.shell.repl.context import Context
from .base import BaseCommand
from edhelper.commom.deck_card_commands import DeckCardCommands


class AddCommand(BaseCommand):
    def __init__(self, card, qty):
        self.card = card.strip()
        self.qty = qty

    def run(self, ctx: Context):
        if ctx.deck is None:
            print("No deck selected")
            return
        assert ctx.deck.name is not None
        cmd = DeckCardCommands.from_deck_name(ctx.deck.name)
        cmd.add(self.card, self.qty)
        ctx.deck_cards = cmd.deck_cards
