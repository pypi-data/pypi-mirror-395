from edhelper.external.api import (
    get_card_from_api,
    get_many_cards_from_api,
    get_autocomplete_from_api,
)
from edhelper.infra.db import transaction
from edhelper.domain.card import Card
from edhelper.commom.excptions import CardNotFound


def get_card_by_name(card_name: str, cursor=None):
    with transaction(cursor=cursor) as t:
        card_data = t.execute(
            "SELECT * FROM cards WHERE name = ?", (card_name,)
        ).fetchone()
        if card_data is None:
            try:
                card = get_card_from_api(card_name)
            except Exception:
                raise CardNotFound(card_name)

            t.execute(
                "INSERT INTO cards (id, name, colors, color_identity, cmc, mana_cost, image, art, legal_commanders, is_commander, price, edhrec_rank, type_line) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                card.get_values_tuple(),
            )

        else:
            card = Card(
                card_data[0],
                card_data[1],
                card_data[2],
                card_data[3],
                card_data[4],
                card_data[5],
                card_data[6],
                card_data[7],
                card_data[8],
                card_data[9],
                card_data[10],
                card_data[11],
                None,
                card_data[12],
            )
        return card


def get_card_by_id(card_id: str, cursor=None):
    with transaction(cursor=cursor) as t:
        card_data = t.execute("SELECT * FROM cards WHERE id = ?", (card_id,)).fetchone()
        if not card_data:
            raise CardNotFound(card_id)
        card = Card(
            card_data[0],
            card_data[1],
            card_data[2],
            card_data[3],
            card_data[4],
            card_data[5],
            card_data[6],
            card_data[7],
            card_data[8],
            card_data[9],
            card_data[10],
            card_data[11],
            None,
            card_data[12],
        )
        return card


def insert_or_update_card(card: Card, cursor=None):
    with transaction(cursor=cursor) as t:
        sql = """
        INSERT INTO cards 
        (id, name, colors, color_identity, cmc, mana_cost, image, art, legal_commanders, is_commander, price, edhrec_rank, type_line) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id)
        DO UPDATE SET
            name = excluded.name,
            colors = excluded.colors,
            color_identity = excluded.color_identity,
            cmc = excluded.cmc,
            mana_cost = excluded.mana_cost,
            price = excluded.price,
            image = excluded.image,
            art = excluded.art,
            legal_commanders = excluded.legal_commanders,
            is_commander = excluded.is_commander,
            edhrec_rank = excluded.edhrec_rank,
            type_line = excluded.type_line;
        """
        t.execute(sql, card.get_values_tuple())


def fetch_many_cards(cards: list, cursor=None):
    with transaction(cursor=cursor) as t:
        card_data = get_many_cards_from_api(cards)
        insert_or_update_cards(card_data, cursor=t)
        return card_data


def get_cards_by_name(card_names: list[str], cursor=None):
    with transaction(cursor=cursor) as t:
        sql = (
            "SELECT * FROM cards WHERE name IN ("
            + ", ".join("?" * len(card_names))
            + ")"
        )
        card_data = t.execute(sql, card_names).fetchall()
        cards = []
        for card in card_data:
            cards.append(
                Card(
                    card[0],
                    card[1],
                    card[2],
                    card[3],
                    card[4],
                    card[5],
                    card[6],
                    card[7],
                    card[8],
                    card[9],
                    card[10],
                    card[11],
                    card[12] if len(card) > 12 else None,
                )
            )
        return cards


def insert_or_update_cards(cards: list, cursor=None):
    with transaction(cursor=cursor) as t:
        sql = """
        INSERT INTO cards 
        (id, name, colors, color_identity, cmc, mana_cost, image, art, legal_commanders, is_commander, price, edhrec_rank, type_line) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id)
        DO UPDATE SET
            name = excluded.name,
            colors = excluded.colors,
            color_identity = excluded.color_identity,
            cmc = excluded.cmc,
            mana_cost = excluded.mana_cost,
            price = excluded.price,
            image = excluded.image,
            art = excluded.art,
            legal_commanders = excluded.legal_commanders,
            is_commander = excluded.is_commander,
            price = excluded.price,
            edhrec_rank = excluded.edhrec_rank,
            type_line = excluded.type_line;
        """
        cards = [card.get_values_tuple() for card in cards]
        t.executemany(sql, cards)


def get_by_autocomplete(card_name: str, cursor=None):
    from edhelper.commom.excptions import ShortPartial

    if len(card_name) < 3:
        raise ShortPartial(card_name)
    with transaction(cursor=cursor) as t:
        cards = get_autocomplete_from_api(card_name)
        insert_or_update_cards(cards, cursor=t)
        return cards


def get_card_names():
    with transaction(cursor=None) as t:
        card_names = t.execute("SELECT name FROM cards").fetchall()
        return [card[0] for card in card_names]
