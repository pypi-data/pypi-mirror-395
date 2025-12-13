from lark import Lark
from edhelper.shell.lang.transformer import CommandTransformer
from pathlib import Path
from edhelper.infra.config import settings
import os

# Get the path to grammar.lark relative to this file
grammar_path = Path(__file__).parent / "grammar.lark"
if not grammar_path.exists():
    # Fallback to BASE_PATH if not found relative to file
    grammar_path = Path(settings.BASE_PATH) / "edhelper" / "shell" / "lang" / "grammar.lark"

grammar = grammar_path.read_text()
parser = Lark(grammar, parser="lalr")

transformer = CommandTransformer()


def parse_command(input_str):
    tree = parser.parse(input_str)
    return transformer.transform(tree)
