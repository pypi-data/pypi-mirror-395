import click
import subprocess
import sys
from tabulate import tabulate
from edhelper.external.api import get_commanders_from_api
import edhelper.domain.card_service as card_service


class TopCommandersCommands:
    @staticmethod
    def show_top_commanders(use_pager: bool = True):
        try:
            click.echo("Fetching top 100 commanders...")
            commanders = get_commanders_from_api()

            card_service.insert_or_update_cards(commanders)

            click.echo(f"Found {len(commanders)} commanders. Saved to database.")

            data = [
                [
                    "Rank",
                    "Name",
                    "Color",
                    "CMC",
                    "Mana Cost",
                    "Price",
                    "Edhrec Rank",
                ]
            ]
            for idx, commander in enumerate(commanders, 1):
                data.append(
                    [
                        idx,
                        commander.name,
                        commander.colors,
                        commander.cmc,
                        commander.mana_cost,
                        commander.price,
                        commander.edhrec_rank
                        if commander.edhrec_rank is not None
                        else "N/A",
                    ]
                )

            table = tabulate(data, headers="firstrow", tablefmt="grid")

            if use_pager:
                click.echo_via_pager(table)
            else:
                click.echo(table)

        except Exception as e:
            click.echo(f"Error: {e}", err=True)
            raise e

    @staticmethod
    def show_top_commanders_shell():
        try:
            print("Fetching top 100 commanders...")
            commanders = get_commanders_from_api()

            card_service.insert_or_update_cards(commanders)

            print(f"Found {len(commanders)} commanders. Saved to database.")

            data = [
                [
                    "Rank",
                    "Name",
                    "Color",
                    "CMC",
                    "Mana Cost",
                    "Price",
                    "Edhrec Rank",
                ]
            ]
            for idx, commander in enumerate(commanders, 1):
                data.append(
                    [
                        idx,
                        commander.name,
                        commander.colors,
                        commander.cmc,
                        commander.mana_cost,
                        commander.price,
                        commander.edhrec_rank
                        if commander.edhrec_rank is not None
                        else "N/A",
                    ]
                )

            table = tabulate(data, headers="firstrow", tablefmt="grid")

            try:
                pager = subprocess.Popen(
                    ["less", "-R"],
                    stdin=subprocess.PIPE,
                    stdout=sys.stdout,
                    stderr=sys.stderr,
                    text=True,
                )
                pager.stdin.write(table)
                pager.stdin.close()
                pager.wait()
            except FileNotFoundError:
                try:
                    pager = subprocess.Popen(
                        ["more"],
                        stdin=subprocess.PIPE,
                        stdout=sys.stdout,
                        stderr=sys.stderr,
                        text=True,
                    )
                    pager.stdin.write(table)
                    pager.stdin.close()
                    pager.wait()
                except FileNotFoundError:
                    print(table)

        except Exception as e:
            print(f"Error: {e}")
            raise e
