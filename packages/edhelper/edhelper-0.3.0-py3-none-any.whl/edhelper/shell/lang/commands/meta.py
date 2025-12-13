from .base import BaseCommand
from edhelper.commom.commander_meta_commands import CommanderMetaCommands


class MetaCommand(BaseCommand):
    def __init__(self, commander_name, category=None):
        self.commander_name = commander_name.strip()
        self.category = category.strip() if category else None

    def run(self, ctx):
        CommanderMetaCommands.get_meta(self.commander_name, self.category)
