from rich.__main__ import make_test_card
from rich.console import Console
from rich.panel import Panel

__version__ = "v0.1.15"


def run():
    console = Console()  # noqa
    panel = Panel(
        make_test_card(),
        title=rf"[[b]Rich Demo[/b]] [gray30]{__version__}",
        padding=(2, 0),
        style="default on gray7",
        width=120,
        expand=False,
    )
    console.print(panel)


if __name__ == "__main__":
    run()
