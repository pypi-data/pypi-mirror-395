from .base import BaseCommand
from edhelper.shell.repl.context import Context
from edhelper.domain.deck_service import get_decks
from edhelper.domain.deck_card_service import get_deck_commanders_name
from tabulate import tabulate
from edhelper.commom.deck_list_commands import DeckListCommands
from edhelper.commom.deck_card_commands import DeckCardCommands


class ListCommand(BaseCommand):
    def __init__(self, qty):
        self.qty = qty

    def run(self, ctx: Context):
        if ctx.deck:
            assert ctx.deck_cards is not None
            assert ctx.deck.name is not None
            cmd = DeckCardCommands.from_deck_name(ctx.deck.name)
            if not cmd:
                return
            cmd.show()
            return
        DeckListCommands.show(self.qty)
