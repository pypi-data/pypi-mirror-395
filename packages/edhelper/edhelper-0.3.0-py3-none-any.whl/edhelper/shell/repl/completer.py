import os
from prompt_toolkit.completion import Completer, Completion, PathCompleter
from prompt_toolkit.document import Document


ROOT_COMMANDS = [
    "select",
    "cd",
    "create",
    "mk",
    "rename",
    "mv",
    "delete",
    "del",
    "copy",
    "cp",
    "export_all",
    "export_txt",
    "export_csv",
    "export_json",
    "import_txt",
    "find",
    "search",
    "meta",
    "top-commanders",
    "sync-db",
    "exit",
    "clear",
    "cls",
    "analyze",
]

DECK_COMMANDS = [
    "add",
    "remove",
    "rmc",
    "reset-commander",
    "set-commander",
    "commander",
    "find",
    "search",
    "export_txt",
    "export_csv",
    "export_json",
    "analyze",
    "find",
    "search",
    "list",
    "ls",
    "exit",
    "clear",
    "cls",
]


def quote_if_needed(name: str) -> str:
    if " " in name and not (name.startswith('"') and name.endswith('"')):
        return f'"{name}"'
    return name


class ShellCompleter(Completer):
    def __init__(self, ctx):
        self.ctx = ctx
        self.path_completer = PathCompleter(expanduser=True)

    def available_commands(self):
        return ROOT_COMMANDS if self.ctx.deck is None else DECK_COMMANDS

    def complete_path(self, arg, complete_event):
        """
        Para path completion funcionar, precisamos fingir
        que o usuário digitou apenas o path, não o comando.
        """
        fake = Document(arg, cursor_position=len(arg))
        yield from self.path_completer.get_completions(fake, complete_event)

    def complete_deck_names(self, arg, start_position):
        needle = arg.strip('"')
        for deck in self.ctx.get_deck_names():
            if deck.startswith(needle):
                yield Completion(quote_if_needed(deck), start_position=start_position)

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor.strip()
        commands = self.available_commands()

        if not text:
            for cmd in commands:
                yield Completion(cmd + " ", start_position=0)
            return

        tokens = text.split()
        cmd = tokens[0]

        if len(tokens) == 1:
            for c in commands:
                if c.startswith(cmd):
                    yield Completion(c + " ", start_position=-len(cmd))
            return

        arg = tokens[-1]
        start = -len(arg)

        DECK_1ARG = ["select", "cd", "export_all", "analyze"]
        if cmd in DECK_1ARG:
            yield from self.complete_deck_names(arg, start)
            return

        DECK_2ARG = ["rename", "mv", "copy", "cp", "delete", "del"]
        if cmd in DECK_2ARG:
            yield from self.complete_deck_names(arg, start)
            return

        CARD_CMDS = ["add", "remove", "rmc", "find", "search", "set-commander"]
        if cmd in CARD_CMDS:
            for card in self.ctx.get_saved_card_names():
                if card.lower().startswith(arg.lower()):
                    yield Completion(card, start_position=start)
            return

        if cmd in ["export_txt", "export_csv", "export_json"]:
            if len(tokens) == 2:
                yield from self.complete_path(arg, complete_event)
                return
            if len(tokens) == 3:
                yield from self.complete_deck_names(arg, start)
                return

        if cmd == "export_all":
            if len(tokens) == 2:
                yield from self.complete_path(arg, complete_event)
            return

        if cmd == "import_txt":
            if len(tokens) == 2:
                yield from self.complete_path(arg, complete_event)
                return
            if len(tokens) == 3:
                yield from self.complete_deck_names(arg, start)
                return

        return
