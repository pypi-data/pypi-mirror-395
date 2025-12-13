from edhelper.domain.card_service import get_card_names
from edhelper.domain.deck import Deck
from edhelper.domain.deck_service import get_deck_names


class Context:
    def __init__(self, deck=None, deck_cards=None):
        assert isinstance(deck, Deck | None)
        assert isinstance(deck_cards, list | None)

        self.deck = deck
        self.deck_cards = deck_cards
        self.deck_names = []

    def set_deck(self, deck):
        assert isinstance(deck, Deck | None)
        self.deck = deck

    def set_deck_cards(self, deck_cards):
        assert isinstance(deck_cards, list | None)
        self.deck_cards = deck_cards

    def get_deck_names(self):
        return get_deck_names()

    def get_saved_card_names(self):
        return get_card_names()
