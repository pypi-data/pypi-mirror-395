from edhelper.commom.card_commands import CardCommands
from .base import BaseCommand


class FindCommand(BaseCommand):
    def __init__(self, query):
        self.query = query.strip()

    def run(self, ctx):
        cmd = CardCommands.from_name(self.query)
        cmd.show()
