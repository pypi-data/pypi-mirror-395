from rich.console import Console

console = Console()

def print_error(error: Exception, custom=False, message: str = None) -> None:
    error_message = "Error" if not custom else message
    console.print(f"\n\n[red]{error_message}:[/red] {error}\n\n", style="bold", justify="center")