import click
import edhelper.domain.card_service as card_service
from edhelper.external.api import get_many_cards_from_api


class SyncDbCommands:
    @staticmethod
    def sync_database():
        """Sync all cards in database with API."""
        click.echo("Fetching all card names from database...")
        card_names = card_service.get_card_names()

        if not card_names:
            click.echo("No cards found in database.")
            return

        click.echo(f"Found {len(card_names)} cards. Updating from API...")

        try:
            # Fetch updated cards from API
            updated_cards = get_many_cards_from_api(card_names)

            # Update database
            card_service.insert_or_update_cards(updated_cards)

            click.echo(f"Successfully updated {len(updated_cards)} cards.")
        except Exception as e:
            click.echo(f"Error syncing database: {e}", err=True)
            raise

    @staticmethod
    def sync_database_shell():
        """Sync all cards in database with API (for shell)."""
        print("Fetching all card names from database...")
        card_names = card_service.get_card_names()

        if not card_names:
            print("No cards found in database.")
            return

        print(f"Found {len(card_names)} cards. Updating from API...")

        try:
            # Fetch updated cards from API
            updated_cards = get_many_cards_from_api(card_names)

            # Update database
            card_service.insert_or_update_cards(updated_cards)

            print(f"Successfully updated {len(updated_cards)} cards.")
        except Exception as e:
            print(f"Error syncing database: {e}")
            raise
