from .base import BaseCommand
from edhelper.commom.deck_card_commands import DeckCardCommands


class RemoveCommand(BaseCommand):
    def __init__(self, card, qty):
        self.card = card.strip()
        self.qty = qty

    def run(self, ctx):
        if ctx.deck is None:
            print("No deck selected")
            return
        assert ctx.deck_cards is not None
        assert ctx.deck.name is not None
        cmd = DeckCardCommands.from_deck_name(ctx.deck.name)
        cmd.remove(self.card, self.qty)
