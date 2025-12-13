import click
from tabulate import tabulate
from edhelper.commom.deck_commands import DeckCommands
import edhelper.domain.deck_service as deck_service
import edhelper.domain.deck_card_service as deck_card_service


class DeckListCommands:
    @staticmethod
    def show(limit=None):
        try:
            decks = deck_service.get_decks(limit=limit)
            data = []
            headers = ["#", "Name", "Commander", "Last Modified"]
            for deck in decks:
                _, deck_cards = deck_card_service.get_deck_data_by_name(deck.name)
                for dc in deck_cards:
                    if dc.is_commander:
                        data.append(
                            [deck.id, deck.name, dc.card.name, deck.last_update]
                        )
                        break
                else:
                    data.append([deck.id, deck.name, "", deck.last_update])
            table = tabulate(data, headers=headers, tablefmt="pipe")
            click.echo(table)
        except Exception as e:
            click.echo(f"Error: {e}", err=True)
            raise e

    @staticmethod
    def import_folder():
        pass

    @staticmethod
    def export_folder(folder):
        try:
            decks = deck_service.get_decks()
            for deck in decks:
                cmd = DeckCommands.from_name(deck.name)
                cmd.export_txt(folder)
        except Exception as e:
            click.echo(f"Error: {e}", err=True)
            raise e
