from .base import BaseCommand
from edhelper.commom.sync_db_commands import SyncDbCommands


class SyncDbCommand(BaseCommand):
    def run(self, ctx):
        try:
            SyncDbCommands.sync_database_shell()
        except Exception as e:
            print(f"Error: {e}")

