from prompt_toolkit import PromptSession
from edhelper.shell.lang.parser import transformer, parser
from .context import Context
from prompt_toolkit.completion import Completer
from .completer import ShellCompleter
from edhelper.commom.exception_handler import shell_handler
from edhelper.commom.excptions import (
    CardNotFound,
    DeckNotFound,
    DeckAlreadyExists,
    CardNotOnDeck,
    CardIsCommander,
    ShortPartial,
    InvalidQuantity,
)

from prompt_toolkit.lexers import PygmentsLexer
from .highlighter import ShellLexer
from prompt_toolkit.styles import Style

style = Style.from_dict(
    {
        "pygments.keyword": "bold #00afff",
        "pygments.string": "#afff00",
        "pygments.name": "#ffaf00",
    }
)

session = PromptSession(
    lexer=PygmentsLexer(ShellLexer),
    style=style,
)


def repl():
    ctx = Context()
    completer = ShellCompleter(ctx)

    count = 1

    while True:
        try:
            s = f"[ {count} ] > "
            if ctx.deck:
                s = f"[ {count} ] : [ {ctx.deck.name} ] > "

            line = session.prompt(s, completer=completer)

            if not line:
                continue

            tree = parser.parse(line)
            cmd = transformer.transform(tree)
            cmd.run(ctx)

            count += 1
            print("\n")

        except KeyboardInterrupt:
            print("\nbye")
            break

        except SystemExit:
            print("\nbye")
            break

        except EOFError:
            print("\nbye")
            break

        except (
            CardNotFound,
            DeckNotFound,
            DeckAlreadyExists,
            CardNotOnDeck,
            CardIsCommander,
            ShortPartial,
            InvalidQuantity,
        ) as e:
            message = shell_handler.handle(e)
            if message:
                print(message)
        except Exception as e:
            print("Erro:", e)
