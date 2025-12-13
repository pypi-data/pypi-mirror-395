from super_pocket.settings import click, display_logo, CONTEXT_SETTINGS
from rich.console import Console
from rich.prompt import Prompt
from super_pocket.xml.xml import (
    extract_text, format_xml, parse_custom_syntax
)


console = Console()


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('text', type=str, help='Text to process.', required=False)
@click.option('--file', '-f', type=click.Path(exists=True), help='Path to the text file.')
@click.option('--output', '-o', type=click.Path(), help='Path to the output file.')
def xml(text: str = None, file: str = None, output: str = None) -> None:
    """
    Convert custom `tag:<content>` syntax into pretty-printed XML.

    Args:
        text: Inline text to process (used if no file is provided).
        file: Path to a text file containing the custom syntax.
        output: Optional path to write the formatted XML output.

    Examples:
        pocket xml "context:<macOS 26.1, machine:<Macbook Pro>>"
        pocket xml -f ./input.txt -o ./output.xml
    """
    if file:
        text = extract_text(file)
    elif not text and not file:
        display_logo()
        text = Prompt.ask('Enter the text to process.')

    raw_xml = parse_custom_syntax(text)
    formatted_xml = format_xml(raw_xml)
    if output:
        with open(output, 'w') as f:
            f.write(formatted_xml)
    console.print(formatted_xml)


if __name__ == '__main__':
    xml()
