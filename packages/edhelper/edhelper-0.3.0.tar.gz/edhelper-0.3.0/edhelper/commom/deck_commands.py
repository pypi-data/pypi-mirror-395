import json
import click
from edhelper.domain.deck import Deck
from edhelper.domain.deck_card import DeckCard
import edhelper.domain.deck_service as deck_service
from .validators import validate_txt
import edhelper.domain.card_service as card_service
import edhelper.domain.deck_card_service as deck_card_service
import os
import csv
from .excptions import DeckNotFound, DeckAlreadyExists, CardNotFound


class DeckCommands:
    def __init__(self, deck: Deck):
        self.deck = deck

    def show(self):
        assert self.deck is not None
        click.echo(f"Deck: {self.deck.name}")
        click.echo(f"Last update: {self.deck.last_update}")

    def create(self):
        assert self.deck is not None
        try:
            if self.exists():
                raise DeckAlreadyExists(self.deck.name)
            click.echo("Creating deck...")
            deck = deck_service.create_deck(self.deck)
            click.echo("Deck created")
            self.deck = deck
            self.show()
        except (DeckAlreadyExists, DeckNotFound) as e:
            raise e
        except Exception as e:
            click.echo(f"Error: {e}", err=True)
            raise e

    def create_with_commander(self, commander_name: str):
        assert self.deck is not None
        assert self.deck.name is not None
        try:
            if self.exists():
                raise DeckAlreadyExists(self.deck.name)

            click.echo("Creating deck...")
            card = card_service.get_card_by_name(commander_name)
            deck_card = DeckCard(deck_id=self.deck.id, card=card, quantidade=1)
            deck_service.create_deck_with_cards(self.deck.name, [deck_card])
            click.echo("Deck created")
        except (DeckAlreadyExists, CardNotFound) as e:
            raise e
        except Exception as e:
            click.echo(f"Error: {e}", err=True)
            raise e

    def rename(self, new_name: str):
        assert self.deck is not None
        assert self.deck.name is not None
        try:
            if not self.exists():
                raise DeckNotFound(self.deck.name)
            if DeckCommands(Deck(name=new_name)).exists():
                raise DeckAlreadyExists(new_name)
            click.echo(f"Renaming deck {self.deck.name} to {new_name}")
            deck_service.rename_deck(self.deck.name, new_name)
            click.echo("Deck renamed")
        except (DeckNotFound, DeckAlreadyExists) as e:
            raise e
        except Exception as e:
            click.echo(f"Error: {e}", err=True)
            raise e

    def delete(self):
        assert self.deck is not None
        assert self.deck.name is not None
        try:
            if not self.exists():
                raise DeckNotFound(self.deck.name)
            click.echo(f"Deleting deck {self.deck.name}")
            deck_service.delete_deck(self.deck.name)
            click.echo("Deck deleted")
        except DeckNotFound as e:
            raise e
        except Exception as e:
            click.echo(f"Error: {e}", err=True)
            raise e

    def exists(self, create=True):
        assert self.deck is not None
        assert self.deck.name is not None
        deck = deck_service.get_deck_by_name(self.deck.name)
        if deck is None:
            return False
        if create:
            self.deck = deck
        return True

    def export_txt(self, path):
        assert self.deck is not None
        assert self.deck.name is not None
        try:
            if not self.exists():
                raise DeckNotFound(self.deck.name)
            deck, deck_cards = deck_card_service.get_deck_data_by_name(self.deck.name)
            output = os.path.join(path, f"{deck.name}.txt")

            with open(output, "w") as f:
                text = []
                for dc in deck_cards:
                    qty = dc.quantidade
                    name = dc.card.name
                    if dc.is_commander:
                        text.insert(0, f"{qty} {name}")
                    else:
                        text.append(f"{qty} {name}")
                f.write("\n".join(text))

            click.echo(f"Written: {output}")

        except DeckNotFound as e:
            raise e
        except Exception as e:
            click.echo(f"Error: {e}", err=True)
            raise e

    def export_csv(self, path):
        assert self.deck is not None
        assert self.deck.name is not None
        try:
            if not self.exists():
                raise DeckNotFound(self.deck.name)
            deck, deck_cards = deck_card_service.get_deck_data_by_name(self.deck.name)
            output = os.path.join(path, f"{deck.name}.csv")

            with open(output, "w") as f:
                text = []
                writer = csv.writer(f)
                writer.writerow(["Qty", "Card"])
                for dc in deck_cards:
                    qty = dc.quantidade
                    name = dc.card.name
                    if dc.is_commander:
                        writer.writerow([qty, name])
                    else:
                        text.append([qty, name])
                writer.writerows(text)

            click.echo(f"Written: {output}")

        except DeckNotFound as e:
            raise e
        except Exception as e:
            click.echo(f"Error: {e}", err=True)
            raise e

    def export_json(self, path):
        assert self.deck is not None
        assert self.deck.name is not None
        try:
            if not self.exists():
                raise DeckNotFound(self.deck.name)
            deck, deck_cards = deck_card_service.get_deck_data_by_name(self.deck.name)
            output = os.path.join(path, f"{deck.name}.json")

            with open(output, "w") as f:
                text = []
                for dc in deck_cards:
                    qty = dc.quantidade
                    name = dc.card.name
                    is_commander = dc.is_commander
                    if dc.is_commander:
                        text.insert(
                            0, {"qty": qty, "name": name, "is_commander": is_commander}
                        )
                    else:
                        text.append(
                            {"qty": qty, "name": name, "is_commander": is_commander}
                        )
                json.dump(text, f, indent=2)

            click.echo(f"Written: {output}")

        except DeckNotFound as e:
            raise e
        except Exception as e:
            click.echo(f"Error: {e}", err=True)
            raise e

    def import_txt(self, filename):
        cards, errors = validate_txt(filename)
        if errors:
            click.echo("Found errors in file:\n" + "\n".join(errors), err=True)
            return
        try:
            if self.exists():
                raise DeckAlreadyExists(self.deck.name)
            card_names = [card[1] for card in cards]
            card_data = card_service.get_cards_by_name(card_names)
            if len(card_data) != len(card_names):
                card_data_names = [card.name for card in card_data]
                extra_cards = [
                    card for card in card_names if card not in card_data_names
                ]
                extra_card_data = card_service.get_many_cards_from_api(extra_cards)
                card_service.insert_or_update_cards(extra_card_data)
                card_data.extend(extra_card_data)
            click.echo(f"Found {len(card_data)} cards")
            card_list = []
            for card in card_data:
                for qty, name in cards:
                    if card.name == name:
                        card_list.append({"card": card, "quantidade": int(qty)})
                        break
                else:
                    click.echo(f"Card not found: {card.name}")
            assert self.deck is not None
            assert self.deck.name is not None
            deck_service.create_deck_with_cards(self.deck.name, card_list)
            click.echo(f"Deck {self.deck.name} created")
        except Exception as e:
            click.echo(f"Error: {e}", err=True)

    @staticmethod
    def from_name(deck_name: str):
        try:
            deck = deck_service.get_deck_by_name(deck_name)
            if deck is None:
                deck = Deck(name=deck_name)
                return DeckCommands(deck)
            return DeckCommands(deck)

        except Exception as e:
            click.echo(f"Error: {e}", err=True)
            raise e

    def copy(self, dest):
        assert self.deck is not None
        assert self.deck.name is not None
        try:
            if not self.exists():
                raise DeckNotFound(self.deck.name)
            other = DeckCommands.from_name(dest)
            if other.exists():
                raise DeckAlreadyExists(dest)
            click.echo(f"Copying deck {self.deck.name} ")
            deck_service.copy_deck(self.deck, dest)
            click.echo(f"Deck {self.deck.name} copied to {dest}")
        except (DeckNotFound, DeckAlreadyExists) as e:
            raise e
        except Exception as e:
            click.echo(f"Error: {e}", err=True)
            raise e

    def analyze(self):
        assert self.deck is not None
        assert self.deck.name is not None
        try:
            if not self.exists():
                raise DeckNotFound(self.deck.name)
            from edhelper.commom.deck_analyzer import analyze_commander_rules

            deck, deck_cards = deck_card_service.get_deck_data_by_name(self.deck.name)
            if deck is None:
                raise DeckNotFound(self.deck.name)
            result = analyze_commander_rules(deck_cards)

            click.echo(f"Commander: {result['commander']}")
            click.echo(f"Color Identity: {result.get('commander_color_identity')}")
            click.echo(f"Total Cards: {result['total_cards']}")
            click.echo(f"Valid: {'Yes' if result['valid'] else 'No'}")

            if result["errors"]:
                click.echo("\nErrors:", err=True)
                for error in result["errors"]:
                    click.echo(f"  - {error}", err=True)

            if result["warnings"]:
                click.echo("\nWarnings:")
                for warning in result["warnings"]:
                    click.echo(f"  - {warning}")
        except DeckNotFound as e:
            raise e
        except Exception as e:
            click.echo(f"Error: {e}", err=True)
            raise e
