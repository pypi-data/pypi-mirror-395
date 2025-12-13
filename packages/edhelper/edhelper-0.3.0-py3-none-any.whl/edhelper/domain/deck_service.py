from edhelper.infra.db import transaction
from edhelper.domain.deck import Deck
from edhelper.domain.deck_card import DeckCard
import edhelper.domain.deck_card_service as deck_card_service
from edhelper.commom.excptions import DeckNotFound, DeckAlreadyExists


def save_deck(deck: Deck, cursor=None):
    with transaction(cursor=cursor) as t:
        t.execute(
            "INSERT OR REPLACE INTO decks (id, nome, last_update) VALUES (?, ?, ?);",
            deck.get_values_tuple(),
        )
        return t.execute("SELECT * FROM decks WHERE id = ?", (deck.id,)).fetchone()


def create_deck(deck: Deck, cursor=None):
    with transaction(cursor=cursor) as t:
        t.execute(
            "INSERT INTO decks (nome, last_update) VALUES (?, ?);",
            deck.get_values_tuple(id=False),
        )
        deck_data = t.execute(
            "SELECT * FROM decks WHERE nome = ?", (deck.name,)
        ).fetchone()
        deck = Deck(deck_data[0], deck_data[1], deck_data[2])
        return deck


def get_deck_by_name(deck_name: str, cursor=None):
    with transaction(cursor=cursor) as t:
        deck_data = t.execute(
            "SELECT * FROM decks WHERE nome = ?", (deck_name,)
        ).fetchone()
        if not deck_data:
            return None
        deck = Deck(deck_data[0], deck_data[1], deck_data[2])
        return deck


def get_deck_by_id(deck_id: int, cursor=None):
    with transaction(cursor=cursor) as t:
        deck_data = t.execute("SELECT * FROM decks WHERE id = ?", (deck_id,)).fetchone()
        if not deck_data:
            raise DeckNotFound(str(deck_id))
        deck = Deck(deck_data[0], deck_data[1], deck_data[2])
        return deck


def get_decks(limit=None, cursor=None):
    with transaction(cursor=cursor) as t:
        sql = "SELECT * FROM decks ORDER BY last_update DESC"
        if limit:
            sql += f" LIMIT {limit}"
        decks_data = t.execute(sql).fetchall()
        decks = []
        for deck_data in decks_data:
            decks.append(Deck(deck_data[0], deck_data[1], deck_data[2]))
        return decks


def copy_deck(source: Deck, new_name: str, cursor=None):
    with transaction(cursor=cursor) as t:
        assert source.name is not None
        new_deck = Deck(name=new_name)
        new_deck.update()
        new_deck = create_deck(new_deck, cursor=t)
        source_deck, deck_cards = deck_card_service.get_deck_data_by_name(
            source.name, cursor=t
        )
        assert source_deck.name == source.name
        assert new_deck.id is not None
        deck_card_service.remove_all_deck_cards(new_deck.id, cursor=t)
        for deck_card in deck_cards:
            deck_card.deck_id = new_deck.id
        deck_card_service.add_deck_card_list(deck_cards, cursor=t)


def delete_deck(deck_name: str, cursor=None):
    with transaction(cursor=cursor) as t:
        sql = "DELETE FROM decks WHERE nome = ?"
        t.execute(sql, (deck_name,))


def rename_deck(old_name: str, new_name: str, cursor=None):
    with transaction(cursor=cursor) as t:
        sql = "UPDATE decks SET nome = ? WHERE nome = ?"
        t.execute(sql, (new_name, old_name))


def create_deck_with_cards(deck_name: str, cards, cursor=None):
    with transaction(cursor=cursor) as t:
        deck = Deck(name=deck_name)
        deck.update()
        deck = create_deck(deck, cursor=t)
        deck_cards = []
        for card in cards:
            dc = DeckCard(
                deck_id=deck.id,
                card=card["card"],
                quantidade=card["quantidade"],
                is_commander=False,
            )
            deck_cards.append(dc)
        deck_card_service.add_deck_card_list(deck_cards, cursor=t)
        deck_data = t.execute(
            "SELECT * FROM decks WHERE nome = ?", (deck.name,)
        ).fetchone()
        deck = Deck(deck_data[0], deck_data[1], deck_data[2])
        return deck


def get_deck_names():
    with transaction(cursor=None) as t:
        deck_names = t.execute("SELECT nome FROM decks").fetchall()
        return [deck[0] for deck in deck_names]
