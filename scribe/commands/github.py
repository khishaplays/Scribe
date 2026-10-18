
import httpx
import typer

from rich.console import Console
from rich.table import Table

from scribe.services.github import GitHubService


app = typer.Typer(help="Explore GitHub repositories.")
console = Console()


@app.command()
def repos(username: str):
    """Display a user's public GitHub repositories."""

    github = GitHubService()

    try:
        repositories = github.get_repositories(username)
    except httpx.HTTPStatusError as error:
        console.print(
            f"[red]GitHub API error: "
            f"{error.response.status_code}[/red]"
        )
        raise typer.Exit(code=1)
    except httpx.RequestError:
        console.print("[red]Unable to reach GitHub.[/red]")
        raise typer.Exit(code=1)
    finally:
        github.close()

    if not repositories:
        console.print("[dim]No public repositories found.[/dim]")
        return

    table = Table(
        title=f"GITHUB REPOSITORIES — @{username}",
        border_style="bright_black",
    )

    table.add_column("#", style="dim", justify="right")
    table.add_column("Repository", style="bold")
    table.add_column("Language")
    table.add_column("Updated")

    for index, repo in enumerate(repositories, start=1):
        table.add_row(
            str(index),
            repo["name"],
            repo.get("language") or "—",
            repo["updated_at"][:10],
        )

    console.print()
    console.print(table)
    console.print(
        f"\n[dim]{len(repositories)} public repositories found.[/dim]\n"
    )
