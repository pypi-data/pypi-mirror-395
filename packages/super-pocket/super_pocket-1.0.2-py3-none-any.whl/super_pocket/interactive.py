import subprocess
import time
from typing import Iterable

from rich.live import Live
from rich.prompt import Prompt

from super_pocket.settings import centered_spinner, display_logo


EXIT_KEYWORDS = {"exit", "quit", "q", "x"}
EXIT_CHOICES = ["exit", "quit", "q", "Q", "X", "x", "EXIT", "QUIT"]


def _run_with_spinner(message: str, command: list[str], style: str = "bold blue") -> None:
    """Render a centered spinner while running a command."""
    with Live(centered_spinner(message, style), refresh_per_second=20, transient=True):
        subprocess.run(command)


def _pause(message: str = "Press Enter to continue") -> None:
    """Pause to keep output visible before re-rendering logo."""
    Prompt.ask(message, default="")


def _run_with_spinner_and_pause(
    message: str,
    command: list[str],
    style: str = "bold blue",
) -> None:
    """Run a command with spinner, then pause."""
    _run_with_spinner(message, command, style)
    _pause()


def _handle_common_navigation(choice: str, allow_back: bool = False) -> str | None:
    """
    Handle common navigation keywords like 'exit', 'quit', 'q', 'x' and optionally 'back'.

    Returns:
        "exit" | "back" | None
    """
    normalized = choice.lower()

    if normalized in EXIT_KEYWORDS:
        return "exit"

    if allow_back and normalized == "back":
        return "back"

    return None


def _prompt_with_choices(
    prompt: str,
    base_choices: Iterable[str],
    default: str = "help",
    allow_back: bool = True,
) -> str:
    """
    Wrapper around Prompt.ask to avoid repeating choices wiring.

    - Adds 'back' if allow_back is True.
    - Always appends EXIT_CHOICES.
    - Hides choices from the UI.
    """
    choices = list(base_choices)

    if allow_back and "back" not in choices:
        choices.append("back")

    # Ensure all exit aliases are present only once
    for exit_choice in EXIT_CHOICES:
        if exit_choice not in choices:
            choices.append(exit_choice)

    return Prompt.ask(
        prompt,
        default=default,
        choices=choices,
        show_choices=False,
    )


def _show_help(section: str, message: str) -> None:
    """Standardized help renderer for a given section."""
    display_logo()
    _run_with_spinner_and_pause(
        message=message,
        command=["pocket", section, "--help"],
        style="bold orange_red1",
    )


def pocket_cmd() -> None:
    display_logo()
    with Live(
        centered_spinner("Loading..."),
        refresh_per_second=10,
        transient=True,
    ):
        time.sleep(2)

    base_choices = ["help", "project", "templates", "pdf", "web", "readme", "xml"]

    while True:
        display_logo()
        user_input = Prompt.ask(
            "[bold blue]help -[/] "
            "[bold orange_red1] - project  - templates - pdf - web - readme - xml[/] "
            "[bold blue]- exit/Q[/] >>>",
            default="help",
            choices=base_choices + EXIT_CHOICES,
            show_choices=False,
        )

        nav = _handle_common_navigation(user_input, allow_back=False)
        if nav == "exit":
            return

        match user_input:
            case "help":
                display_logo()
                _run_with_spinner_and_pause(
                    "Loading help...",
                    ["pocket", "--help"],
                    style="bold orange_red1",
                )

            case "project":
                if project_cmd() == "exit":
                    return

            case "templates":
                if templates_cmd() == "exit":
                    return

            case "pdf":
                if pdf_cmd() == "exit":
                    return

            case "web":
                if web_cmd() == "exit":
                    return

            case "readme":
                if readme_cmd() == "exit":
                    return

            case "xml":
                if xml_cmd() == "exit":
                    return


def project_cmd() -> str | None:
    base_choices = ["help", "to-file", "readme", "req-to-date", "init"]

    while True:
        display_logo()
        user_input = _prompt_with_choices(
            "[bold blue]help - [/][bold orange_red1]"
            "to-file - readme - req-to-date - init[/] "
            "[bold blue]- exit/Q[/] >>>",
            base_choices=base_choices,
            default="help",
            allow_back=True,
        )

        nav = _handle_common_navigation(user_input, allow_back=True)
        if nav == "exit":
            return "exit"
        if nav == "back":
            return "back"

        match user_input:
            case "help":
                _show_help("project", "Loading project help...")

            case "to-file":
                path = Prompt.ask("Project path", default=".")
                output = Prompt.ask("Output file (optional)", default="")
                exclude = Prompt.ask("Exclude (comma-separated, optional)", default="")

                command = ["pocket", "project", "to-file", "--path", path]
                if output.strip():
                    command += ["--output", output]
                if exclude.strip():
                    command += ["--exclude", exclude]

                _run_with_spinner_and_pause("Exporting project...", command)

            case "readme":
                path = Prompt.ask("Project path", default=".")
                output = Prompt.ask("README output (optional)", default="")

                command = ["pocket", "project", "readme", "--path", path]
                if output.strip():
                    command += ["--output", output]

                _run_with_spinner_and_pause("Generating README...", command)

            case "req-to-date":
                packages = Prompt.ask(
                    "Packages (comma list or requirements file)",
                    default="",
                )
                if not packages.strip():
                    continue

                command = ["pocket", "project", "req-to-date", packages]
                _run_with_spinner_and_pause("Checking requirements...", command)

            case "init":
                _run_with_spinner_and_pause(
                    "Loading templates...",
                    ["pocket", "project", "init", "list"],
                )

                template = Prompt.ask(
                    "Template name (or 'back' to cancel)",
                    default="",
                )
                if not template.strip() or template.lower() == "back":
                    continue

                _run_with_spinner_and_pause(
                    "Loading template details...",
                    ["pocket", "project", "init", "show", template],
                )

                confirm = Prompt.ask(
                    "Create project with this template?",
                    choices=["y", "n"],
                    default="y",
                )
                if confirm.strip().lower() == "n":
                    continue

                path = Prompt.ask("Output path", default=".")
                quick = Prompt.ask(
                    "Quick mode (skip prompts)?",
                    choices=["y", "n"],
                    default="n",
                )

                command = [
                    "pocket",
                    "project",
                    "init",
                    "new",
                    template,
                    "-p",
                    path,
                ]
                if quick == "y":
                    command.append("--quick")

                _run_with_spinner_and_pause("Creating project...", command)


def templates_cmd() -> str | None:
    base_choices = ["help", "list", "view", "copy", "init"]

    while True:
        display_logo()
        user_input = _prompt_with_choices(
            "[bold blue]help -[/] [bold orange_red1]list - view - copy - init[/]"
            "[bold blue]- exit/Q[/] >>>",
            base_choices=base_choices,
            default="help",
            allow_back=True,
        )

        nav = _handle_common_navigation(user_input, allow_back=True)
        if nav == "exit":
            return "exit"
        if nav == "back":
            return "back"

        match user_input:
            case "help":
                _show_help("templates", "Loading templates help...")

            case "list":
                type_choice = Prompt.ask(
                    "Type",
                    choices=["all", "templates", "cheatsheets"],
                    default="all",
                )
                command = ["pocket", "templates", "list", "--type", type_choice]
                _run_with_spinner_and_pause("Listing templates...", command)

            case "view":
                name = Prompt.ask("Template or cheatsheet name")
                type_choice = Prompt.ask(
                    "Type (optional)",
                    choices=["auto", "template", "cheatsheet"],
                    default="auto",
                )
                command = ["pocket", "templates", "view", name]
                if type_choice != "auto":
                    command += ["--type", type_choice]
                _run_with_spinner_and_pause("Loading item...", command)

            case "copy":
                name = Prompt.ask("Template or cheatsheet name")
                output = Prompt.ask("Output path (optional)", default="")
                type_choice = Prompt.ask(
                    "Type (optional)",
                    choices=["auto", "template", "cheatsheet"],
                    default="auto",
                )
                force = Prompt.ask(
                    "Overwrite if exists?",
                    choices=["y", "n"],
                    default="y",
                )

                command = ["pocket", "templates", "copy", name]
                if output.strip():
                    command += ["--output", output]
                if type_choice != "auto":
                    command += ["--type", type_choice]
                if force == "y":
                    command.append("--force")

                _run_with_spinner_and_pause("Copying item...", command)

            case "init":
                output = Prompt.ask(
                    "Target directory (default .AGENTS)",
                    default=".AGENTS",
                )
                command = ["pocket", "templates", "init", "--output", output]
                _run_with_spinner_and_pause("Initializing templates...", command)


def pdf_cmd() -> str | None:
    base_choices = ["help", "convert"]

    while True:
        display_logo()
        user_input = _prompt_with_choices(
            "[bold blue]help -[/] [bold orange_red1]convert[/] "
            "[bold blue]- exit/Q[/] >>>",
            base_choices=base_choices,
            default="help",
            allow_back=True,
        )

        nav = _handle_common_navigation(user_input, allow_back=True)
        if nav == "exit":
            return "exit"
        if nav == "back":
            return "back"

        match user_input:
            case "help":
                _show_help("pdf", "Loading PDF help...")

            case "convert":
                input_file = Prompt.ask("Input file")
                output_file = Prompt.ask("Output file (optional)", default="")
                command = ["pocket", "pdf", "convert", input_file]
                if output_file.strip():
                    command += ["--output", output_file]
                _run_with_spinner_and_pause("Converting to PDF...", command)


def web_cmd() -> str | None:
    base_choices = ["help", "favicon", "job-search"]

    while True:
        display_logo()
        user_input = _prompt_with_choices(
            "[bold blue]help -[/] [bold orange_red1]favicon - job-search[/]"
            "[bold blue] - exit/Q[/] >>>",
            base_choices=base_choices,
            default="help",
            allow_back=True,
        )

        nav = _handle_common_navigation(user_input, allow_back=True)
        if nav == "exit":
            return "exit"
        if nav == "back":
            return "back"

        match user_input:
            case "help":
                _show_help("web", "Loading web help...")

            case "favicon":
                input_file = Prompt.ask("Input image")
                output_file = Prompt.ask("Output ico (optional)", default="")
                sizes = Prompt.ask("Sizes (optional: 64x64,32x32)", default="")
                command = ["pocket", "web", "favicon", input_file]
                if output_file.strip():
                    command += ["--output", output_file]
                if sizes.strip():
                    command += ["--sizes", sizes]
                _run_with_spinner_and_pause("Generating favicon...", command)

            case "job-search":
                query = Prompt.ask("Search query", default="Python developer")
                page = Prompt.ask("Start page", default="1")
                num_pages = Prompt.ask("Number of pages", default="10")
                country = Prompt.ask("Country code", default="fr")
                language = Prompt.ask("Language", default="fr")
                date_posted = Prompt.ask(
                    "Date posted",
                    choices=["all", "today", "3days", "week", "month"],
                    default="month",
                )
                employment_types = Prompt.ask(
                    "Employment types",
                    default="FULLTIME",
                )
                job_requirements = Prompt.ask(
                    "Job requirements",
                    default="no_experience",
                )
                work_from_home = Prompt.ask(
                    "Work from home?",
                    choices=["y", "n"],
                    default="n",
                )
                output = Prompt.ask("Output file", default="jobs.json")

                command = [
                    "pocket",
                    "web",
                    "job-search",
                    query,
                    "--page",
                    page,
                    "--num_pages",
                    num_pages,
                    "--country",
                    country,
                    "--language",
                    language,
                    "--date_posted",
                    date_posted,
                    "--employment_types",
                    employment_types,
                    "--job_requirements",
                    job_requirements,
                ]

                if work_from_home == "y":
                    command.append("--work_from_home")

                command += ["--output", output]

                _run_with_spinner_and_pause("Searching jobs...", command)


def readme_cmd() -> str | None:
    base_choices = ["help", "analyze", "generate"]

    while True:
        display_logo()
        user_input = _prompt_with_choices(
            "[bold blue]help -[/] [bold orange_red1]analyze - generate[/] "
            "[bold blue]- exit/Q[/] >>>",
            base_choices=base_choices,
            default="help",
            allow_back=True,
        )

        nav = _handle_common_navigation(user_input, allow_back=True)
        if nav == "exit":
            return "exit"
        if nav == "back":
            return "back"

        match user_input:
            case "help":
                _show_help("readme", "Loading README help...")

            case "analyze":
                path = Prompt.ask("Project path", default=".")
                command = ["pocket", "readme", "analyze", path]
                _run_with_spinner_and_pause("Analyzing project...", command)

            case "generate":
                path = Prompt.ask("Project path", default=".")
                output = Prompt.ask("Output file", default="README.md")
                command = [
                    "pocket",
                    "readme",
                    "generate",
                    "--path",
                    path,
                    "--output",
                    output,
                ]
                _run_with_spinner_and_pause("Generating README...", command)


def xml_cmd() -> str | None:
    base_choices = ["help", "convert"]

    while True:
        display_logo()
        user_input = _prompt_with_choices(
            "[bold blue]help -[/] [bold orange_red1]convert[/] "
            "[bold blue]- exit/Q[/] >>>",
            base_choices=base_choices,
            default="help",
            allow_back=True,
        )

        nav = _handle_common_navigation(user_input, allow_back=True)
        if nav == "exit":
            return "exit"
        if nav == "back":
            return "back"

        match user_input:
            case "help":
                _show_help("xml", "Loading XML help...")

            case "convert":
                source_type = Prompt.ask(
                    "Source type",
                    choices=["text", "file"],
                    default="text",
                )

                if source_type == "text":
                    text = Prompt.ask("Text to convert (custom tag syntax)")
                    output = Prompt.ask("Output file (optional)", default="")

                    command = ["pocket", "xml", text]
                    if output.strip():
                        command += ["--output", output]
                else:
                    input_file = Prompt.ask("Input file path")
                    output = Prompt.ask("Output file (optional)", default="")

                    command = ["pocket", "xml", "--file", input_file]
                    if output.strip():
                        command += ["--output", output]

                _run_with_spinner_and_pause("Converting to XML...", command)


if __name__ == "__main__":
    pocket_cmd()
