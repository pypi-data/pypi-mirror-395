from edhelper.domain.deck_card import DeckCard
from edhelper.domain.card import Card
from edhelper.domain.deck import Deck
from edhelper.infra.db import transaction
from edhelper.commom.excptions import DeckNotFound, CardNotOnDeck


def get_deck_data_by_name(deck_name: str, cursor=None):
    with transaction(cursor=cursor) as t:
        deck = t.execute("SELECT * from decks WHERE nome = ?", (deck_name,)).fetchone()
        if not deck:
            raise DeckNotFound(deck_name)
        data = t.execute(
            """
                SELECT deck_cards.*, cards.*
                FROM deck_cards
                INNER JOIN cards ON cards.id = deck_cards.card_id
                INNER JOIN decks ON decks.id = deck_cards.deck_id
                WHERE decks.nome = ?
                ORDER by deck_cards.is_commander DESC
                """,
            (deck[1],),
        ).fetchall()
        deck_cards = []
        for deck_card in data:
            dc = DeckCard(
                deck_id=deck[0],
                card=Card(
                    deck_card[4],  # id
                    deck_card[5],  # name
                    deck_card[6],  # colors
                    deck_card[7],  # color_identity
                    deck_card[8],  # cmc
                    deck_card[9],  # mana_cost
                    deck_card[10],  # image
                    deck_card[11],  # art
                    deck_card[12],  # legal_commanders
                    deck_card[13],  # is_commander
                    deck_card[14],  # price
                    deck_card[15],  # edhrec_rank
                    None,  # commander_rank
                    deck_card[16] if len(deck_card) > 16 else None,  # type_line
                ),
                quantidade=deck_card[2],
                is_commander=deck_card[3] == 1,
            )
            deck_cards.append(dc)
        deck = Deck(deck[0], deck[1], deck[2])
        return deck, deck_cards


def get_deck_card(deck_id: int, card_id: str, cursor=None):
    with transaction(cursor=cursor) as t:
        deck_card = t.execute(
            """
                SELECT deck_cards.*, cards.*
                FROM deck_cards
                INNER JOIN cards ON cards.id = deck_cards.card_id
                WHERE deck_cards.deck_id = ? AND cards.id = ?
                """,
            (deck_id, card_id),
        ).fetchone()
        if not deck_card:
            return None
        card = Card(
            deck_card[4],  # id
            deck_card[5],  # name
            deck_card[6],  # colors
            deck_card[7],  # color_identity
            deck_card[8],  # cmc
            deck_card[9],  # mana_cost
            deck_card[10],  # image
            deck_card[11],  # art
            deck_card[12],  # legal_commanders
            deck_card[13],  # is_commander
            deck_card[14],  # price
            deck_card[15],  # edhrec_rank
            None,  # commander_rank
            deck_card[16] if len(deck_card) > 16 else None,  # type_line
        )
        deck_card = DeckCard(
            deck_id=deck_id,
            card=card,
            quantidade=deck_card[2],
            is_commander=deck_card[3] == 1,
        )
        return deck_card


def get_deck_commanders_name(deck_id: int, cursor=None):
    with transaction(cursor=cursor) as t:
        deck_card = t.execute(
            """
                SELECT cards.name
                FROM deck_cards
                INNER JOIN cards ON cards.id = deck_cards.card_id
                WHERE deck_cards.deck_id = ? AND deck_cards.is_commander = TRUE
                """,
            (deck_id,),
        ).fetchone()
        if not deck_card:
            return ""
        return deck_card[0]


def remove_all_deck_cards(deck_id: int, cursor=None):
    with transaction(cursor=cursor) as t:
        sql = "DELETE FROM deck_cards WHERE deck_id = ?"
        t.execute(sql, (deck_id,))


def add_deck_card_list(deck_card_list: list[DeckCard], cursor=None):
    with transaction(cursor=cursor) as t:
        sql = "INSERT INTO deck_cards (deck_id, card_id, quantidade, is_commander) VALUES (?, ?, ?, ?)"
        data = [dc.get_values_tuple() for dc in deck_card_list]
        t.executemany(sql, data)


def update_or_insert_deck_card(deck_card: DeckCard, cursor=None):
    with transaction(cursor=cursor) as t:
        sql = """
            INSERT INTO deck_cards (deck_id, card_id, quantidade, is_commander)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(deck_id, card_id)
            DO UPDATE SET 
                quantidade = deck_cards.quantidade + excluded.quantidade,
                is_commander = excluded.is_commander;
        """
        t.execute(sql, deck_card.get_values_tuple())


def update_deck_card_quantity(deck_card: DeckCard, cursor=None) -> None:
    with transaction(cursor=cursor) as t:
        sql = "UPDATE deck_cards SET quantidade = ? WHERE deck_id = ? AND card_id = ?"
        assert deck_card.card is not None
        t.execute(sql, (deck_card.quantidade, deck_card.deck_id, deck_card.card.id))


def delete_deck_card(deck_card: DeckCard, cursor=None):
    with transaction(cursor=cursor) as t:
        sql = "DELETE FROM deck_cards WHERE deck_id = ? AND card_id = ?"
        t.execute(sql, deck_card.get_values_tuple(quantidade=False, is_commander=False))


def reset_deck_commander(deck_id: int, cursor=None):
    with transaction(cursor=cursor) as t:
        sql = "UPDATE deck_cards SET is_commander = 0 WHERE deck_id = ?"
        t.execute(sql, (deck_id,))


def set_deck_commander(deck_card: DeckCard, cursor=None):
    assert deck_card.card is not None
    assert deck_card.is_commander is True
    assert deck_card.deck_id is not None
    assert deck_card.quantidade == 1
    with transaction(cursor=cursor) as t:
        reset_deck_commander(deck_card.deck_id, cursor)
        sql = "UPDATE deck_cards SET is_commander = 1, quantidade = 1 WHERE deck_id = ? AND card_id = ?"
        t.execute(sql, deck_card.get_values_tuple(quantidade=False, is_commander=False))
