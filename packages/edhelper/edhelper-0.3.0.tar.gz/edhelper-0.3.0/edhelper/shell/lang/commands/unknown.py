from .base import BaseCommand


class UnknownCommand(BaseCommand):
    def __init__(self, word):
        self.word = word

    def run(self, ctx):
        print(f"[unknown] word={self.word}")
