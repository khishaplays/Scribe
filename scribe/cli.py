
import typer

from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from scribe.commands.github import app as github_app
from scribe.commands.projects import (
    app as projects_app,
    list_projects,
)


# Initialize Scribe CLI
app = typer.Typer(
    name="scribe",
    help="Your development, documented.",
    no_args_is_help=False,
)

console = Console()

# Register project management commands
app.add_typer(projects_app, name="project")
app.add_typer(github_app, name="github")
def show_home():
    """Display the Scribe welcome screen."""

    title = Text("S C R I B E", style="bold")
    subtitle = Text(
        "your development, documented.",
        style="dim",
    )

    header = Text()
    header.append(title)
    header.append("\n")
    header.append(subtitle)

    console.print()
    console.print(
        Panel(
            Align.center(header),
            padding=(1, 8),
            border_style="bright_black",
        )
    )
    console.print()
    console.print(
        "  Welcome to your developer space.",
        style="dim",
    )
    console.print()


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """Scribe — your developer command center."""

    if ctx.invoked_subcommand is None:
        show_home()


@app.command()
def today():
    """View today's development activity."""

    console.print()
    console.print("  TODAY", style="bold")
    console.print(
        "  ─────────────────────────────────────",
        style="dim",
    )
    console.print()
    console.print(
        "  No activity recorded yet.",
        style="dim",
    )
    console.print()


@app.command()
def projects():
    """View all saved development projects."""

    list_projects()


if __name__ == "__main__":
    app()
