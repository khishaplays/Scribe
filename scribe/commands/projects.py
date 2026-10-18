
import typer
from rich.console import Console
from rich.table import Table
from sqlalchemy import select

from scribe.database.connection import SessionLocal
from scribe.models.project import Project

app = typer.Typer(help="Manage development projects.")
console = Console()


@app.command()
def add(
    name: str = typer.Argument(..., help="Project name"),
    project_type: str = typer.Option(
        "personal", "--type", help="personal or team"
    ),
):
    """Add a new development project."""

    if project_type not in ("personal", "team"):
        console.print("[red]Type must be personal or team.[/red]")
        raise typer.Exit(code=1)

    with SessionLocal() as db:
        project = Project(
            name=name,
            project_type=project_type,
        )

        db.add(project)
        db.commit()
        db.refresh(project)

        console.print(
            f"\n[green]✓[/green] Added {project.name} "
            f"({project.project_type})\n"
        )


@app.command("list")
def list_projects():
    """Display saved projects."""

    with SessionLocal() as db:
        projects = db.scalars(
            select(Project).order_by(Project.name)
        ).all()

    if not projects:
        console.print("\n[dim]No projects recorded yet.[/dim]\n")
        return

    for project_type in ("personal", "team"):
        matching = [
            project for project in projects
            if project.project_type == project_type
        ]

        if not matching:
            continue

        table = Table(
            title=f"{project_type.upper()} PROJECTS",
            border_style="bright_black",
        )

        table.add_column("ID", style="dim")
        table.add_column("Project", style="bold")
        table.add_column("Status")

        for project in matching:
            table.add_row(
                str(project.id),
                project.name,
                project.status,
            )

        console.print(table)
