import rich_click as click
from rich.panel import Panel
from rich.text import Text
from rich.spinner import Spinner
from rich.align import Align
from rich.console import Console

console = Console()


click.rich_click.STYLE_OPTION = "bold blue"
click.rich_click.STYLE_ARGUMENT = "bold orange_red1"
click.rich_click.STYLE_COMMAND = "bold orange_red1"
click.rich_click.STYLE_SWITCH = "blue"
click.rich_click.STYLE_METAVAR = "orange_red1"
click.rich_click.STYLE_METAVAR_SEPARATOR = ""
click.rich_click.STYLE_USAGE = "bold grey100"
click.rich_click.STYLE_USAGE_COMMAND = "bold bright_blue"
click.rich_click.STYLE_HELPTEXT_FIRST_LINE = "bold"
click.rich_click.STYLE_HELPTEXT = "dim italic"
click.rich_click.STYLE_OPTION_DEFAULT = "blue"
click.rich_click.STYLE_REQUIRED_SHORT = "orange_red1"
click.rich_click.STYLE_REQUIRED_LONG = "orange_red1"
click.rich_click.STYLE_OPTIONS_PANEL_BORDER = "orange_red1"
click.rich_click.STYLE_COMMANDS_PANEL_BORDER = "blue"
click.rich_click.STYLE_OPTIONS_TABLE_BOX = "SIMPLE"


click.rich_click.STYLE_OPTIONS_PANEL_BOX = "SIMPLE_HEAD"

click.rich_click.STYLE_OPTIONS_PANEL_TITLE_STYLE = "bold grey100"

click.rich_click.STYLE_OPTIONS_TABLE_LEADING: int = 1
click.rich_click.STYLE_COMMANDS_PANEL_BOX = "SIMPLE_HEAD"
click.rich_click.STYLE_COMMANDS_PANEL_TITLE_STYLE = "bold grey100"
click.rich_click.STYLE_COMMANDS_TABLE_BOX = "SIMPLE"

def centered_spinner(message: str = "Loading...", style: str = "bold blue"):
    text = Text(message, style=style)
    return Align.center(Spinner("dots12", text=text, style=style))


def display_logo():
    logo = Align.center(
        Panel.fit(
            Text(
                """
░█▀█░█▀█░█▀▀░█░█░█▀▀░▀█▀
░█▀▀░█░█░█░░░█▀▄░█▀▀░░█░
░▀░░░▀▀▀░▀▀▀░▀░▀░▀▀▀░░▀░
                """,
                style="bold orange_red1"
            ), 
            padding=(1, 6), 
            border_style="blue"
        )
    )
    console.clear()
    console.print(logo)