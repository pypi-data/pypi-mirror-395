from .base import BaseCommand
from edhelper.commom.deck_list_commands import DeckListCommands


class ExportAllCommand(BaseCommand):
    def __init__(self, path):
        self.path = path

    def run(self, ctx):
        DeckListCommands.export_folder(self.path)
