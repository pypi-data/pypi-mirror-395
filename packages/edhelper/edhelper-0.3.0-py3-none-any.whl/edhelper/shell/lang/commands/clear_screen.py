from .base import BaseCommand
from edhelper.commom.utils import clear_screen


class ClearCommand(BaseCommand):
    def run(self, ctx):
        clear_screen()
