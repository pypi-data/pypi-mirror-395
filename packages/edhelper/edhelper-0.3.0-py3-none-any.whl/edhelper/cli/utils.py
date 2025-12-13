"""
Utilitários e tipos para comandos CLI.
"""

import click
import re
from functools import wraps
from edhelper.commom.exception_handler import cli_handler
from edhelper.commom.excptions import (
    CardNotFound,
    DeckNotFound,
    DeckAlreadyExists,
    CardNotOnDeck,
    CardIsCommander,
    ShortPartial,
    InvalidQuantity,
)


def handle_cli_exceptions(func):
    """Decorator para tratar exceções customizadas no CLI."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (
            CardNotFound,
            DeckNotFound,
            DeckAlreadyExists,
            CardNotOnDeck,
            CardIsCommander,
            ShortPartial,
            InvalidQuantity,
        ) as e:
            cli_handler.handle(e)
            return
        except Exception as e:
            click.echo(f"Unexpected error: {e}", err=True)
            raise

    return wrapper


class TxtFile(click.ParamType):
    name = "txtfile"

    def convert(self, value, param, ctx):
        if not value.lower().endswith(".txt"):
            self.fail("O arquivo deve ser .txt", param, ctx)
        return value


TXT_FILE = TxtFile()


class DeckNameType(click.ParamType):
    name = "deck_name"

    pattern = re.compile(r"^[0-9A-Za-z _+\-]+$")

    def sanitize(self, value):
        return "".join(c for c in value if re.match(r"[0-9A-Za-z _+\-]", c))

    def convert(self, value, param, ctx):
        if not value:
            self.fail("Deck name cannot be empty.", param, ctx)

        sanitized = self.sanitize(value)

        if not self.pattern.match(sanitized):
            self.fail(
                f"Invalid deck name after sanitization: '{sanitized}'",
                param,
                ctx,
            )

        return sanitized


DECK_NAME = DeckNameType()
