from rich.live import Live
from rich.prompt import Prompt
import time
import subprocess
from super_pocket.settings import centered_spinner, display_logo


def _run_with_spinner(message: str, command: list[str], style: str = "bold blue") -> None:
    """Render a centered spinner while running a command."""

    with Live(centered_spinner(message, style), refresh_per_second=20, transient=True):
        subprocess.run(command)


def _pause(message: str = "Press Enter to continue") -> None:
    """Pause to keep output visible before re-rendering logo."""

    Prompt.ask(message, default="")


def pocket_cmd():    
    display_logo()
    with Live(centered_spinner("Loading..."), refresh_per_second=10, transient=True):
        time.sleep(2)

    while True:
        display_logo()
        user_input = Prompt.ask(
            "[bold blue]help[/] [bold orange_red1]project templates pdf web readme xml[/] [bold blue]exit/Q[/] >>>",
            default="help",
            choices=["help", "project", "templates", "pdf", "web", "readme", "xml", "exit", "quit", "q", "Q", "X", "x", "EXIT", "QUIT"],
            show_choices=False
        )

        match user_input:
            case "help":
                display_logo()
                _run_with_spinner("Loading help...", ["pocket", "--help"], "bold orange_red1")
                _pause()
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
            case "exit" | "quit" | "q" | "Q" | "X" | "x" | "EXIT" | "QUIT":
                return


def project_cmd():
    while True:
        display_logo()
        user_input = Prompt.ask(
            "[bold blue]help[/] [bold orange_red1]to-file readme req-to-date init[/] [bold blue]exit/Q[/] >>>",
            default="help", 
            choices=["help", "to-file", "readme", "req-to-date", "init", "back", "exit", "quit", "q", "Q", "X", "x", "EXIT", "QUIT"],
            show_choices=False
        )

        match user_input:
            case "help":
                display_logo()
                _run_with_spinner("Loading project help...", ["pocket", "project", "--help"])
                _pause()
            case "to-file":
                path = Prompt.ask("Project path", default=".")
                output = Prompt.ask("Output file (optional)", default="")
                exclude = Prompt.ask("Exclude (comma-separated, optional)", default="")

                command = ["pocket", "project", "to-file", "--path", path]
                if output.strip():
                    command += ["--output", output]
                if exclude.strip():
                    command += ["--exclude", exclude]

                _run_with_spinner("Exporting project...", command)
                _pause()

            case "readme":
                path = Prompt.ask("Project path", default=".")
                output = Prompt.ask("README output (optional)", default="")

                command = ["pocket", "project", "readme", "--path", path]
                if output.strip():
                    command += ["--output", output]

                _run_with_spinner("Generating README...", command)
                _pause()

            case "req-to-date":
                packages = Prompt.ask("Packages (comma list or requirements file)", default="")
                if not packages.strip():
                    continue
                command = ["pocket", "project", "req-to-date", packages]
                _run_with_spinner("Checking requirements...", command)
                _pause()

            case "init":
                # Show available templates first
                _run_with_spinner("Loading templates...", ["pocket", "project", "init", "list"])
                _pause()
                
                template = Prompt.ask("Template name (or 'back' to cancel)", default="")
                if not template.strip() or template.lower() == "back":
                    continue
                
                # Show template details
                _run_with_spinner("Loading template details...", ["pocket", "project", "init", "show", template])
                _pause()
                
                confirm = Prompt.ask("Create project with this template?", choices=["y", "n"], default="y")
                if confirm == "n":
                    continue
                
                path = Prompt.ask("Output path", default=".")
                quick = Prompt.ask("Quick mode (skip prompts)?", choices=["y", "n"], default="n")
                
                command = ["pocket", "project", "init", "new", template, "-p", path]
                if quick == "y":
                    command.append("--quick")
                
                _run_with_spinner("Creating project...", command)
                _pause()

            case "back":
                return "back"
            case "exit" | "quit" | "q" | "Q" | "X" | "x" | "EXIT" | "QUIT":
                return "exit"


def templates_cmd():
    while True:
        display_logo()
        user_input = Prompt.ask(
            "[bold blue]help[/] [bold orange_red1]list view copy init[/] [bold blue]exit/Q[/] >>>",
            default="help",
            choices=["help", "list", "view", "copy", "init", "back", "exit", "quit", "q", "Q", "X", "x", "EXIT", "QUIT"],
            show_choices=False
        )

        match user_input:
            case "help":
                display_logo()
                _run_with_spinner("Loading templates help...", ["pocket", "templates", "--help"])
                _pause()
            case "list":
                type_choice = Prompt.ask(
                    "Type", choices=["all", "templates", "cheatsheets"], default="all"
                )
                command = ["pocket", "templates", "list", "--type", type_choice]
                _run_with_spinner("Listing templates...", command)
                _pause()
            case "view":
                name = Prompt.ask("Template or cheatsheet name")
                type_choice = Prompt.ask(
                    "Type (optional)", choices=["auto", "template", "cheatsheet"], default="auto"
                )
                command = ["pocket", "templates", "view", name]
                if type_choice != "auto":
                    command += ["--type", type_choice]
                _run_with_spinner("Loading item...", command)
                _pause()
            case "copy":
                name = Prompt.ask("Template or cheatsheet name")
                output = Prompt.ask("Output path (optional)", default="")
                type_choice = Prompt.ask(
                    "Type (optional)", choices=["auto", "template", "cheatsheet"], default="auto"
                )
                force = Prompt.ask("Overwrite if exists?", choices=["y", "n"], default="y")

                command = ["pocket", "templates", "copy", name]
                if output.strip():
                    command += ["--output", output]
                if type_choice != "auto":
                    command += ["--type", type_choice]
                if force == "y":
                    command.append("--force")

                _run_with_spinner("Copying item...", command)
                _pause()
            case "init":
                output = Prompt.ask("Target directory (default .AGENTS)", default=".AGENTS")
                command = ["pocket", "templates", "init", "--output", output]
                _run_with_spinner("Initializing templates...", command)
                _pause()
            case "back":
                return "back"
            case "exit" | "quit" | "q" | "Q" | "X" | "x" | "EXIT" | "QUIT":
                return "exit"


def pdf_cmd():
    while True:
        display_logo()
        user_input = Prompt.ask(
            "[bold blue]help[/] [bold orange_red1]convert[/] [bold blue]exit/Q[/] >>>",
            default="help",
            choices=["help", "convert", "back", "exit", "quit", "q", "Q", "X", "x", "EXIT", "QUIT"],
            show_choices=False
        )

        match user_input:
            case "help":
                display_logo()
                _run_with_spinner("Loading PDF help...", ["pocket", "pdf", "--help"])
                _pause()
            case "convert":
                input_file = Prompt.ask("Input file")
                output_file = Prompt.ask("Output file (optional)", default="")
                command = ["pocket", "pdf", "convert", input_file]
                if output_file.strip():
                    command += ["--output", output_file]
                _run_with_spinner("Converting to PDF...", command)
                _pause()
            case "back":
                return "back"
            case "exit" | "quit" | "q" | "Q" | "X" | "x" | "EXIT" | "QUIT":
                return "exit"


def web_cmd():
    while True:
        display_logo()
        user_input = Prompt.ask(
            "[bold blue]help[/] [bold orange_red1]favicon job-search[/] [bold blue]exit/Q[/] >>>",
            default="help",
            choices=["help", "favicon", "job-search", "back", "exit", "quit", "q", "Q", "X", "x", "EXIT", "QUIT"],
            show_choices=False
        )

        match user_input:
            case "help":
                display_logo()
                _run_with_spinner("Loading web help...", ["pocket", "web", "--help"])
                _pause()
            case "favicon":
                input_file = Prompt.ask("Input image")
                output_file = Prompt.ask("Output ico (optional)", default="")
                sizes = Prompt.ask("Sizes (optional: 64x64,32x32)", default="")
                command = ["pocket", "web", "favicon", input_file]
                if output_file.strip():
                    command += ["--output", output_file]
                if sizes.strip():
                    command += ["--sizes", sizes]
                _run_with_spinner("Generating favicon...", command)
                _pause()
            case "job-search":
                query = Prompt.ask("Search query", default="Python developer")
                page = Prompt.ask("Start page", default="1")
                num_pages = Prompt.ask("Number of pages", default="10")
                country = Prompt.ask("Country code", default="fr")
                language = Prompt.ask("Language", default="fr")
                date_posted = Prompt.ask(
                    "Date posted", choices=["all", "today", "3days", "week", "month"], default="month"
                )
                employment_types = Prompt.ask(
                    "Employment types", default="FULLTIME"
                )
                job_requirements = Prompt.ask("Job requirements", default="no_experience")
                work_from_home = Prompt.ask("Work from home?", choices=["y", "n"], default="n")
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

                _run_with_spinner("Searching jobs...", command)
                _pause()
            case "back":
                return "back"
            case "exit" | "quit" | "q" | "Q" | "X" | "x" | "EXIT" | "QUIT":
                return "exit"


def readme_cmd():
    while True:
        display_logo()
        user_input = Prompt.ask(
            "[bold blue]help[/] [bold orange_red1]analyze generate[/] [bold blue]exit/Q[/] >>>",
            default="help",
            choices=["help", "analyze", "generate", "back", "exit", "quit", "q", "Q", "X", "x", "EXIT", "QUIT"],
            show_choices=False
        )

        match user_input:
            case "help":
                display_logo()
                _run_with_spinner("Loading README help...", ["pocket", "readme", "--help"])
                _pause()
            case "analyze":
                path = Prompt.ask("Project path", default=".")
                command = ["pocket", "readme", "analyze", path]
                _run_with_spinner("Analyzing project...", command)
                _pause()
            case "generate":
                path = Prompt.ask("Project path", default=".")
                output = Prompt.ask("Output file", default="README.md")
                command = ["pocket", "readme", "generate", "--path", path, "--output", output]
                _run_with_spinner("Generating README...", command)
                _pause()
            case "back":
                return "back"
            case "exit" | "quit" | "q" | "Q" | "X" | "x" | "EXIT" | "QUIT":
                return "exit"


def xml_cmd():
    while True:
        display_logo()
        user_input = Prompt.ask(
            "[bold blue]help[/] [bold orange_red1]convert[/] [bold blue]exit/Q[/] >>>",
            default="help",
            choices=["help", "convert", "back", "exit", "quit", "q", "Q", "X", "x", "EXIT", "QUIT"],
            show_choices=False
        )

        match user_input:
            case "help":
                display_logo()
                _run_with_spinner("Loading XML help...", ["pocket", "xml", "--help"])
                _pause()
            case "convert":
                source_type = Prompt.ask(
                    "Source type", choices=["text", "file"], default="text"
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
                
                _run_with_spinner("Converting to XML...", command)
                _pause()
            case "back":
                return "back"
            case "exit" | "quit" | "q" | "Q" | "X" | "x" | "EXIT" | "QUIT":
                return "exit"


if __name__ == "__main__":
    pocket_cmd()
