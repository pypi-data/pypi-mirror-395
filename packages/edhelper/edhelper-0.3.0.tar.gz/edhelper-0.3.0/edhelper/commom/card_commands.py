import edhelper.domain.card_service as card_service
from edhelper.domain.card import Card
import click
from tabulate import tabulate
from .excptions import CardNotFound, ShortPartial


class CardCommands:
    def __init__(self, card: Card):
        self.card: Card = card

    @staticmethod
    def search(partial: str):
        if len(partial) < 3:
            raise ShortPartial(partial)
        try:
            cards = card_service.get_autocomplete_from_api(partial=partial)
            card_service.insert_or_update_cards(cards)
            data = [
                [
                    "ID",
                    "Name",
                    "Type Line",
                    "Color",
                    "CMC",
                    "Mana Cost",
                    "Legal Commanders",
                    "Is Commander",
                    "Price",
                    "Edhrec Rank",
                ]
            ]
            for card in cards:
                data.append(
                    [
                        card.id,
                        card.name,
                        card.type_line,
                        card.colors,
                        card.cmc,
                        card.mana_cost,
                        card.legal_commanders,
                        card.is_commander,
                        card.price,
                        card.edhrec_rank,
                    ]
                )
            table = tabulate(data, headers="firstrow")
            click.echo(table)
        except Exception as e:
            click.echo(f"Error: {e}", err=True)
            raise e

    def __find(self):
        assert self.card is not None
        assert self.card.name is not None
        card = card_service.get_card_by_name(self.card.name)
        if not card:
            raise CardNotFound(self.card.name)
        self.card = card

    @staticmethod
    def from_name(card_name: str):
        card = CardCommands(Card(name=card_name))
        card.__find()
        return card

    def show(self):
        table = [
            ["ID", self.card.id if self.card.id is not None else ""],
            ["Name", self.card.name],
            [
                "Type Line",
                self.card.type_line if self.card.type_line is not None else "",
            ],
            ["Color", self.card.colors],
            ["Color Identity", self.card.color_identity],
            ["CMC", self.card.cmc],
            ["Mana Cost", self.card.mana_cost],
            ["Image URL", self.card.image],
            ["Art URL", self.card.art],
            ["Legal Commands", self.card.legal_commanders == 1],
            ["Is Commander", self.card.is_commander == 1],
            ["Price", self.card.price],
            [
                "Edhrec Rank",
                self.card.edhrec_rank if self.card.edhrec_rank is not None else "N/A",
            ],
        ]
        table = tabulate(table, headers="firstrow", tablefmt="fancy_grid")
        click.echo(table)
