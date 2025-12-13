from .base import BaseCommand
from edhelper.shell.repl.context import Context
from edhelper.domain.deck_service import get_deck_by_name, rename_deck


class RenameCommand(BaseCommand):
    def __init__(self, old, new):
        self.old = old
        self.new = new

    def run(self, ctx):
        if ctx.deck:
            print("Command not supported on Deck Mode")
        try:
            deck = get_deck_by_name(self.old)
            if not deck:
                print(f"Deck {self.old} not found")
                return
            new_deck = get_deck_by_name(self.new)
            if new_deck:
                print(f"Deck {self.new} already exists")
                return
            rename_deck(self.old, self.new)
            print(f"Deck {self.old} renamed to {self.new}")
        except Exception as e:
            print("An error occurred while trying to rename deck")
