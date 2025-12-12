from __future__ import annotations

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from . import __version__
from .roadmap import PLAN, by_sprint

app = typer.Typer(no_args_is_help=True, add_completion=True)
auth_app = typer.Typer(no_args_is_help=True)
ctx_app = typer.Typer(no_args_is_help=True)
ws_app = typer.Typer(no_args_is_help=True)
proj_app = typer.Typer(no_args_is_help=True)
file_app = typer.Typer(no_args_is_help=True)
sdk_app = typer.Typer(no_args_is_help=True)

app.add_typer(auth_app, name="auth")
app.add_typer(ctx_app, name="context")
app.add_typer(ws_app, name="workspace")
app.add_typer(proj_app, name="project")
app.add_typer(file_app, name="file")
app.add_typer(sdk_app, name="sdk")

console = Console()

def coming_soon(cmd: str) -> None:
    plan = PLAN.get(cmd)
    if not plan:
        console.print(Panel.fit(f"[yellow]Planned[/yellow]\ncommand: [bold]{cmd}[/bold]\nsprint: [bold]TBD[/bold]\nintent: TBD"))
        raise typer.Exit(code=0)

    console.print(
        Panel.fit(
            f"[yellow]Planned (not implemented yet)[/yellow]\n"
            f"command: [bold]{plan.command}[/bold]\n"
            f"sprint: [bold]Sprint {plan.sprint}[/bold]\n"
            f"intent: {plan.intent}"
        )
    )
    raise typer.Exit(code=0)

@app.command()
def roadmap() -> None:
    """Show the command roadmap and sprint plan."""
    groups = by_sprint()
    for sprint, items in groups.items():
        table = Table(title=f"Sprint {sprint}")
        table.add_column("Command", style="bold")
        table.add_column("Intent")
        for p in items:
            table.add_row(p.command, p.intent)
        console.print(table)

@app.command()
def version() -> None:
    """Print CLI version."""
    console.print(Panel.fit(f"[green]aiel[/green] version [bold]{__version__}[/bold]"))
    # Requirement: every command returns a sprint plan too
    coming_soon("aiel version")

# ----- Sprint 1 -----
@app.command()
def init() -> None:
    coming_soon("aiel init")

@auth_app.command("login")
def auth_login() -> None:
    coming_soon("aiel auth login")

@auth_app.command("status")
def auth_status() -> None:
    coming_soon("aiel auth status")

@auth_app.command("logout")
def auth_logout() -> None:
    coming_soon("aiel auth logout")

@ctx_app.command("show")
def context_show() -> None:
    coming_soon("aiel context show")

@ctx_app.command("set")
def context_set() -> None:
    coming_soon("aiel context set")

# ----- Sprint 2 -----
@ws_app.command("ls")
def workspace_ls() -> None:
    coming_soon("aiel workspace ls")

@ws_app.command("use")
def workspace_use() -> None:
    coming_soon("aiel workspace use")

@proj_app.command("ls")
def project_ls() -> None:
    coming_soon("aiel project ls")

@proj_app.command("create")
def project_create() -> None:
    coming_soon("aiel project create")

# ----- Sprint 3 -----
@file_app.command("ls")
def file_ls() -> None:
    coming_soon("aiel file ls")

@file_app.command("cat")
def file_cat() -> None:
    coming_soon("aiel file cat")

@file_app.command("write")
def file_write() -> None:
    coming_soon("aiel file write")

@file_app.command("rm")
def file_rm() -> None:
    coming_soon("aiel file rm")

@sdk_app.command("pin")
def sdk_pin() -> None:
    coming_soon("aiel sdk pin")

@sdk_app.command("status")
def sdk_status() -> None:
    coming_soon("aiel sdk status")

# ----- Sprint 4 -----
@app.command()
def run() -> None:
    coming_soon("aiel run")

@app.command()
def logs() -> None:
    coming_soon("aiel logs")

@app.command()
def doctor() -> None:
    coming_soon("aiel doctor")
