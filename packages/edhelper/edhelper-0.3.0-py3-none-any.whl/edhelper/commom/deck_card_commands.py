import click
from edhelper.domain.card import Card
from edhelper.domain.deck import Deck
import edhelper.domain.deck_card_service as deck_card_service
from edhelper.domain.deck_card import DeckCard
import edhelper.domain.card_service as card_service
from tabulate import tabulate
from .excptions import (
    CardNotFound,
    DeckNotFound,
    CardNotOnDeck,
    CardIsCommander,
    InvalidQuantity,
)


class DeckCardCommands:
    def __init__(self, deck: Deck, cards: list[DeckCard]):
        self.deck_cards = cards
        self.deck = deck

    def search(self, card_name: str):
        for deck_card in self.deck_cards:
            if deck_card.card.name == card_name:
                return deck_card
        return None

    def create(self, card_name: str, qty: int):
        if qty <= 0:
            raise InvalidQuantity(qty)
        try:
            dc = self.search(card_name)
            if dc:
                return dc
            card = card_service.get_card_by_name(card_name)
            deck_card = DeckCard(self.deck.id, card, qty, False)
            deck_card_service.add_deck_card_list([deck_card])
            self.deck_cards.append(deck_card)
            click.echo(f"Added {qty} x {card_name} to deck {self.deck.name}.")
            click.echo(
                f"Deck {self.deck.name} has {deck_card.quantidade} x {card_name} remaining."
            )
            return deck_card
        except (CardNotFound, InvalidQuantity) as e:
            raise e
        except Exception as e:
            click.echo(f"Error creating deck card: {e}", err=True)
            raise e

    def add(self, card_name: str, qty: int):
        if qty <= 0:
            raise InvalidQuantity(qty)
        dc = self.search(card_name)
        if not dc:
            return self.create(card_name, qty)
        try:
            if dc.is_commander:
                raise CardIsCommander(card_name)
            dc.quantidade = dc.quantidade + qty if dc.quantidade is not None else qty
            deck_card_service.update_deck_card_quantity(dc)
            click.echo(f"Added {qty} x {card_name} to deck {self.deck.name}.")
            click.echo(
                f"Deck {self.deck.name} has {dc.quantidade} x {card_name} remaining."
            )
        except (CardIsCommander, InvalidQuantity) as e:
            raise e
        except Exception as e:
            click.echo(f"Error adding deck card: {e}", err=True)
            raise e

    def remove(self, card_name, qty: int):
        if qty <= 0:
            raise InvalidQuantity(qty)
        dc = self.search(card_name)
        if not dc:
            assert self.deck.name is not None
            raise CardNotOnDeck(card_name, self.deck.name)
        assert dc.quantidade is not None

        try:
            if dc.quantidade <= qty:
                qty = dc.quantidade
                deck_card_service.delete_deck_card(dc)
                dc.quantidade = 0
            else:
                dc.quantidade = dc.quantidade - qty
                deck_card_service.update_deck_card_quantity(dc)
            if dc.quantidade == 0:
                click.echo(f"Removed {card_name} from deck {self.deck.name}.")
                self.deck_cards.remove(dc)
                return
            click.echo(f"Removed {qty} x {card_name} from deck {self.deck.name}.")
            click.echo(
                f"Deck {self.deck.name} has {dc.quantidade} x {card_name} remaining."
            )
        except (CardNotOnDeck, InvalidQuantity) as e:
            raise e
        except Exception as e:
            click.echo(f"Error adding deck card: {e}", err=True)
            raise e

    def edit_quantity(self, card_name: str, qty: int):
        dc = self.search(card_name)
        if not dc:
            assert self.deck.name is not None
            raise CardNotOnDeck(card_name, self.deck.name)
        assert dc.quantidade is not None
        if dc.quantidade == qty:
            click.echo(f"Deck {self.deck.name} has {qty} x {card_name}.")
            return
        if dc.quantidade > qty:
            self.remove(card_name, dc.quantidade - qty)
            return
        self.add(card_name, qty - dc.quantidade)

    def set_commander(self, card_name: str):
        dc = self.search(card_name)
        if not dc:
            assert self.deck.name is not None
            raise CardNotOnDeck(card_name, self.deck.name)
        if dc.is_commander:
            raise CardIsCommander(card_name)
        try:
            dc.quantidade = 1
            dc.is_commander = True
            deck_card_service.set_deck_commander(dc)
            click.echo(f"Set {card_name} as commander.")
        except (CardNotOnDeck, CardIsCommander) as e:
            raise e
        except Exception as e:
            click.echo(f"Error setting commander: {e}", err=True)
            raise e

    def reset_commander(self):
        assert self.deck is not None
        assert self.deck.id is not None
        try:
            deck_card_service.reset_deck_commander(self.deck.id)
            click.echo(f"Deck {self.deck.name} commander reset.")
        except Exception as e:
            click.echo(f"Error resetting commander: {e}", err=True)
            raise e

    @staticmethod
    def from_deck_name(deck_name: str):
        try:
            deck, deck_cards = deck_card_service.get_deck_data_by_name(deck_name)
            return DeckCardCommands(deck, deck_cards)
        except DeckNotFound as e:
            raise e
        except Exception as e:
            click.echo(f"Error fetching deck: {e}", err=True)
            raise e

    def show(self):
        assert self.deck is not None, "Deck should be set"
        assert self.deck_cards is not None, "Deck cards should be set"
        data = [["Qty", "Card", "Price", "Commander"]]
        for dc in self.deck_cards:
            assert dc.card is not None
            assert dc.quantidade is not None
            assert dc.is_commander is not None
            price = dc.card.price if dc.card and dc.card.price else ""
            if dc.is_commander:
                data.insert(1, [dc.quantidade, dc.card.name, price, "COMMANDER"])
                continue
            data.append([dc.quantidade, dc.card.name, price, ""])
        table = tabulate(data, headers="firstrow", tablefmt="pipe")
        click.echo(table)
