import click
from tabulate import tabulate
from edhelper.commom.card_commands import CardCommands
from edhelper.external.edhec import get_edhrec_cardlists
from edhelper.external.api import get_many_cards_from_api
import edhelper.domain.card_service as card_service
from .excptions import CardNotFound

CATEGORIES = [
    "New Cards",
    "Basic Lands",
    "High Synergy Cards",
    "Top Cards",
    "Game Changers",
    "Creatures",
    "Instants",
    "Sorceries",
    "Utility Artifacts",
    "Enchantments",
    "Battles",
    "Planeswalkers",
    "Utility Lands",
    "Mana Artifacts",
]


class CommanderMetaCommands:
    @staticmethod
    def get_meta(commander_name: str, category: str | None = None):
        try:
            commander_card_cmd = CardCommands.from_name(commander_name)
            if not commander_card_cmd:
                raise CardNotFound(commander_name)
            card = commander_card_cmd.card
            color_identity = card.color_identity
            card_list = get_edhrec_cardlists(commander_name)

            if not card_list:
                click.echo(
                    f"No meta data found for commander '{commander_name}'", err=True
                )
                return

            if category is None:
                available_categories = [cat for cat in CATEGORIES if cat in card_list]
                click.echo(f"\nAvailable categories for '{commander_name}':")
                for cat in available_categories:
                    click.echo(f"  - {cat}")
                click.echo(
                    "\nPlease specify a category using: deck meta <commander> <category>"
                )
                return

            if category not in card_list:
                available_categories = [cat for cat in CATEGORIES if cat in card_list]
                click.echo(f"Category '{category}' not found.", err=True)
                click.echo(
                    f"Available categories: {', '.join(available_categories)}",
                    err=True,
                )
                return

            card_names = card_list[category]
            if not card_names:
                click.echo(
                    f"No cards found in category '{category}' for '{commander_name}'"
                )
                return

            click.echo(
                f"Fetching {len(card_names)} cards from category '{category}'..."
            )

            cards = get_many_cards_from_api(card_names)

            card_service.insert_or_update_cards(cards)

            click.echo(f"Found {len(cards)} cards. Saved to database.")

            data = [
                [
                    "Name",
                    "Type Line",
                    "Color",
                    "CMC",
                    "Mana Cost",
                    "Price",
                    "Edhrec Rank",
                ]
            ]
            for card in cards:
                data.append(
                    [
                        card.name,
                        card.type_line,
                        card.colors,
                        card.cmc,
                        card.mana_cost,
                        card.price,
                        card.edhrec_rank if card.edhrec_rank is not None else "N/A",
                    ]
                )
            table = tabulate(data, headers="firstrow", tablefmt="grid")
            click.echo(table)

        except Exception as e:
            click.echo(f"Error: {e}", err=True)
            raise e
