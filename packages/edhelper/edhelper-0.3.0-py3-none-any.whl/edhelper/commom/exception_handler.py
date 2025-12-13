import click
from typing import Optional
from .excptions import (
    CardNotFound,
    DeckNotFound,
    DeckAlreadyExists,
    CardNotOnDeck,
    CardIsCommander,
    ShortPartial,
    InvalidQuantity,
)


class ExceptionHandler:
    MODE_CLI = "cli"
    MODE_SHELL = "shell"
    MODE_EDITOR = "editor"

    def __init__(self, mode: str = MODE_CLI):
        self.mode = mode

    def handle(self, exception: Exception) -> Optional[str]:
        if isinstance(exception, CardNotFound):
            return self._handle_card_not_found(exception)
        elif isinstance(exception, DeckNotFound):
            return self._handle_deck_not_found(exception)
        elif isinstance(exception, DeckAlreadyExists):
            return self._handle_deck_already_exists(exception)
        elif isinstance(exception, CardNotOnDeck):
            return self._handle_card_not_on_deck(exception)
        elif isinstance(exception, CardIsCommander):
            return self._handle_card_is_commander(exception)
        elif isinstance(exception, ShortPartial):
            return self._handle_short_partial(exception)
        elif isinstance(exception, InvalidQuantity):
            return self._handle_invalid_quantity(exception)
        return None

    def _handle_card_not_found(self, exc: CardNotFound) -> str:
        if self.mode == self.MODE_CLI:
            click.echo(f"Error: Card '{exc.card_name}' not found.", err=True)
        elif self.mode == self.MODE_SHELL:
            return f"Card '{exc.card_name}' not found"
        else:
            return exc.message
        return exc.message

    def _handle_deck_not_found(self, exc: DeckNotFound) -> str:
        if self.mode == self.MODE_CLI:
            click.echo(f"Error: Deck '{exc.deck_name}' not found.", err=True)
        elif self.mode == self.MODE_SHELL:
            return f"Deck '{exc.deck_name}' not found"
        else:
            return exc.message
        return exc.message

    def _handle_deck_already_exists(self, exc: DeckAlreadyExists) -> str:
        if self.mode == self.MODE_CLI:
            click.echo(f"Error: Deck '{exc.deck_name}' already exists.", err=True)
        elif self.mode == self.MODE_SHELL:
            return f"Deck '{exc.deck_name}' already exists"
        else:
            return exc.message
        return exc.message

    def _handle_card_not_on_deck(self, exc: CardNotOnDeck) -> str:
        if self.mode == self.MODE_CLI:
            click.echo(
                f"Error: Card '{exc.card_name}' not on deck '{exc.deck_name}'.",
                err=True,
            )
        elif self.mode == self.MODE_SHELL:
            return f"Card '{exc.card_name}' not on deck '{exc.deck_name}'"
        else:
            return exc.message
        return exc.message

    def _handle_card_is_commander(self, exc: CardIsCommander) -> str:
        if self.mode == self.MODE_CLI:
            click.echo(f"Error: Card '{exc.card_name}' is a commander.", err=True)
        elif self.mode == self.MODE_SHELL:
            return f"Card '{exc.card_name}' is a commander"
        else:
            return exc.message
        return exc.message

    def _handle_short_partial(self, exc: ShortPartial) -> str:
        if self.mode == self.MODE_CLI:
            click.echo(f"Error: {exc.message}", err=True)
        elif self.mode == self.MODE_SHELL:
            return exc.message
        else:
            return exc.message
        return exc.message

    def _handle_invalid_quantity(self, exc: InvalidQuantity) -> str:
        if self.mode == self.MODE_CLI:
            click.echo(f"Error: {exc.message}", err=True)
        elif self.mode == self.MODE_SHELL:
            return exc.message
        else:
            return exc.message
        return exc.message


cli_handler = ExceptionHandler(ExceptionHandler.MODE_CLI)
shell_handler = ExceptionHandler(ExceptionHandler.MODE_SHELL)
editor_handler = ExceptionHandler(ExceptionHandler.MODE_EDITOR)
