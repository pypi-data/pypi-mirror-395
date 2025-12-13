# transformer.py
from lark import Transformer
from edhelper.shell.lang.commands.select import SelectCommand
from edhelper.shell.lang.commands.create import CreateCommand
from edhelper.shell.lang.commands.rename import RenameCommand
from edhelper.shell.lang.commands.delete import DeleteCommand
from edhelper.shell.lang.commands.copy import CopyCommand
from edhelper.shell.lang.commands.export_txt import ExportTxtCommand
from edhelper.shell.lang.commands.export_csv import ExportCsvCommand
from edhelper.shell.lang.commands.export_json import ExportJsonCommand
from edhelper.shell.lang.commands.import_txt import ImportTxtCommand
from edhelper.shell.lang.commands.export_all import ExportAllCommand
from edhelper.shell.lang.commands.add import AddCommand
from edhelper.shell.lang.commands.remove import RemoveCommand
from edhelper.shell.lang.commands.reset_commander import ResetCommanderCommand
from edhelper.shell.lang.commands.set_commander import SetCommanderCommand
from edhelper.shell.lang.commands.list_cmd import ListCommand
from edhelper.shell.lang.commands.find import FindCommand
from edhelper.shell.lang.commands.search import SearchCommand
from edhelper.shell.lang.commands.unknown import UnknownCommand
from edhelper.shell.lang.commands.commander import CommanderCommand
from edhelper.shell.lang.commands.exit_cmd import ExitCommand
from edhelper.shell.lang.commands.base import BaseCommand
from edhelper.shell.lang.commands.clear_screen import ClearCommand
from edhelper.shell.lang.commands.meta import MetaCommand
from edhelper.shell.lang.commands.top_commanders import TopCommandersCommand
from edhelper.shell.lang.commands.analyze import AnalizeCommand
from edhelper.shell.lang.commands.sync_db import SyncDbCommand
from edhelper.commom.validators import validate_path
import ast


class CommandTransformer(Transformer):
    WORD = str

    def DECKNAME(self, token):
        s = str(token)
        if s.startswith('"') or s.startswith("'"):
            return ast.literal_eval(s)  # remove quotes corretamente
        return s

    INT = int

    def select_cmd(self, items):
        return SelectCommand(items[0])

    def create_cmd(self, items):
        return CreateCommand(items[0])

    def rename_cmd(self, items):
        return RenameCommand(items[0], items[1])

    def delete_cmd(self, items):
        return DeleteCommand(items[0])

    def copy_cmd(self, items):
        return CopyCommand(items[0], items[1])

    def export_txt_cmd(self, items):
        if not validate_path(items[0]):
            return BaseCommand()
        if len(items) > 1:
            return ExportTxtCommand(items[0], items[1])
        return ExportTxtCommand(items[0])

    def export_csv_cmd(self, items):
        if not validate_path(items[0]):
            return BaseCommand()
        if len(items) > 1:
            return ExportCsvCommand(items[0], items[1])
        return ExportCsvCommand(items[0])

    def export_json_cmd(self, items):
        if not validate_path(items[0]):
            return BaseCommand()
        if len(items) > 1:
            return ExportJsonCommand(items[0], items[1])
        return ExportJsonCommand(items[0])

    def import_txt_cmd(self, items):
        if not validate_path(items[0], extension=".txt"):
            return BaseCommand()
        return ImportTxtCommand(items[0], items[1])

    def export_all_cmd(self, items):
        if not validate_path(items[0]):
            return BaseCommand()
        return ExportAllCommand(items[0])

    def add_cmd(self, items):
        card = items[0]
        qty = items[1] if len(items) > 1 else 1
        return AddCommand(card, qty)

    def remove_cmd(self, items):
        card = items[0]
        qty = items[1] if len(items) > 1 else 1
        return RemoveCommand(card, qty)

    def reset_cmd(self, _):
        return ResetCommanderCommand()

    def set_cmd(self, items):
        return SetCommanderCommand(items[0])

    def list_cmd(self, items):
        if len(items) == 0:
            return ListCommand(None)
        return ListCommand(items[0])

    def find_cmd(self, items):
        return FindCommand(items[0])

    def search_cmd(self, items):
        return SearchCommand(items[0])

    def unknown(self, items):
        return UnknownCommand(items[0])

    def command(self, items):
        return items[0]

    def start(self, items):
        return items[0]

    def commander_cmd(self, _):
        return CommanderCommand()

    def meta_cmd(self, items):
        if len(items) > 1:
            return MetaCommand(items[0], items[1])
        return MetaCommand(items[0])

    def top_commanders_cmd(self, _):
        return TopCommandersCommand()

    def exit_cmd(self, _):
        return ExitCommand()

    def clear_cmd(self, _):
        return ClearCommand()

    def analyze_cmd(self, items):
        if len(items) == 0:
            return AnalizeCommand()
        return AnalizeCommand(items[0])

    def sync_db_cmd(self, _):
        return SyncDbCommand()
