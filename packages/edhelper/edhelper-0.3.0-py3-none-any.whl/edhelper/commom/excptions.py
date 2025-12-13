class CardNotFound(Exception):
    def __init__(self, card_name):
        self.card_name = card_name
        self.message = f"Card {card_name} not found"
        super().__init__(self.message)


class DeckNotFound(Exception):
    def __init__(self, deck_name):
        self.deck_name = deck_name
        self.message = f"Deck {deck_name} not found"
        super().__init__(self.message)


class DeckAlreadyExists(Exception):
    def __init__(self, deck_name):
        self.deck_name = deck_name
        self.message = f"Deck {deck_name} already exists"
        super().__init__(self.message)


class CardNotOnDeck(Exception):
    def __init__(self, card_name, deck_name):
        self.card_name = card_name
        self.deck_name = deck_name
        self.message = f"Card {card_name} not on deck {deck_name}"
        super().__init__(self.message)


class CardIsCommander(Exception):
    def __init__(self, card_name):
        self.card_name = card_name
        self.message = f"Card {card_name} is a commander"
        super().__init__(self.message)


class ShortPartial(Exception):
    def __init__(self, partial):
        self.partial = partial
        self.message = (
            f"Partial must be at least 3 characters long, received {len(partial)}"
        )
        super().__init__(self.message)


class InvalidQuantity(Exception):
    def __init__(self, qty):
        self.qty = qty
        self.message = f"Quantity must be a number, received {qty}"
        super().__init__(self.message)
