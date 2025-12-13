from edhelper.domain.card import Card


class DeckCard:
    def __init__(self, deck_id=None, card=None, quantidade=None, is_commander=None):
        assert isinstance(deck_id, int | None)
        assert isinstance(card, Card | None)
        assert isinstance(quantidade, int | None)
        assert quantidade is None or quantidade >= 0
        assert isinstance(is_commander, bool | None)
        self.deck_id = deck_id
        self.card = card
        self.quantidade = quantidade
        self.is_commander = is_commander

    def get_values_tuple(
        self, deck=True, card=True, quantidade=True, is_commander=True
    ):
        values = []
        if deck:
            values.append(self.deck_id)
        if card:
            if self.card:
                values.append(self.card.id)
            else:
                values.append(None)
        if quantidade:
            values.append(self.quantidade)
        if is_commander:
            values.append(self.is_commander)
        return tuple(values)

    def __hash__(self):
        return hash(self.get_values_tuple())

    def get_list_row(self):
        if not self.card:
            return None
        return [
            self.quantidade,
            self.card.name,
            "COMMANDER" if self.is_commander else "",
        ]
