import re
from pygments.lexer import RegexLexer
from pygments.token import Keyword

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

ROOT_COMMANDS_PATTERN = "|".join(ROOT_COMMANDS)
DECK_COMMANDS_PATTERN = "|".join(DECK_COMMANDS)


class ShellLexer(RegexLexer):
    name = "CustomShell"
    flags = re.UNICODE

    tokens = {
        "root": [
            (rf"({ROOT_COMMANDS_PATTERN})\b", Keyword),
            (rf"({DECK_COMMANDS_PATTERN})\b", Keyword),
        ]
    }
