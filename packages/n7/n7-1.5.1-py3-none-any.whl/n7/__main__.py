"""N7 CLI pour les projets N7"""

import typer
from rich.console import Console

from n7 import __version__
from n7.commands import (
    connect_shell_command,
    docker_black_command,
    docker_mypy_command,
    docker_pycheck_command,
    docker_pyqa_command,
    docker_pytest_command,
    docker_ruff_command,
    docker_uv_command,
    down_command,
    local_black_command,
    local_mypy_command,
    local_pycheck_command,
    local_pyqa_command,
    local_pytest_command,
    local_ruff_command,
    local_uv_command,
    logs_command,
    py_manage_command,
    up_command,
)

# init Typer
app = typer.Typer(
    name="n7",
    help="CLI global pour les projets N7",
    add_completion=True,
    rich_markup_mode="rich",
    context_settings={"help_option_names": ["-h", "--help"]},
    pretty_exceptions_show_locals=False,
    pretty_exceptions_short=True,
)

console = Console()

# Group docker compose
dkc_app = typer.Typer(help="Commandes Docker Compose")
dkc_app.add_typer(docker_pytest_command, name="pyt", help="Tests pytest in container")
dkc_app.add_typer(
    docker_black_command, name="pybl", help="Format Python code with Black in container"
)
dkc_app.add_typer(docker_ruff_command, name="pyrf", help="Lint Python code with Ruff in container")
dkc_app.add_typer(
    docker_mypy_command, name="pymy", help="Type check Python code with Mypy in container"
)
dkc_app.add_typer(docker_pyqa_command, name="pyqa", help="Run Python QA tools in container")
dkc_app.add_typer(
    docker_pycheck_command, name="pycheck", help="Run Python checks (Tests + QA) in container"
)
dkc_app.add_typer(docker_uv_command, name="uv", help="Run uv command in container")
dkc_app.add_typer(up_command, name="up", help="Start container")
dkc_app.add_typer(down_command, name="down", help="Stop and delete container")
dkc_app.add_typer(logs_command, name="l", help="Logs a container")
dkc_app.add_typer(connect_shell_command, name="sh", help="Start shell in container")
dkc_app.add_typer(py_manage_command, name="pymana", help="Run python manage.py in container")

app.add_typer(dkc_app, name="dkc", help="Commandes Docker Compose")

# Group local
app.add_typer(local_pytest_command, name="pyt", help="Tests pytest local")
app.add_typer(local_black_command, name="pybl", help="Format Python code with Black")
app.add_typer(local_ruff_command, name="pyrf", help="Lint Python code with Ruff")
app.add_typer(local_mypy_command, name="pymy", help="Type check Python code with Mypy")
app.add_typer(local_pyqa_command, name="pyqa", help="Run Python QA tools")
app.add_typer(local_pycheck_command, name="pycheck", help="Run Python checks (Tests + QA)")
app.add_typer(local_uv_command, name="uv", help="Run uv command")

#
# HELP => display help
#

version_option = typer.Option(
    False,
    "--version",
    "-v",
    help="Show version CLI n7",
)

debug_option = typer.Option(
    False,
    "--debug",
    help="Mode debug with traceback completed",
)


@app.callback(invoke_without_command=True)
def main_callback(version: bool = version_option, debug: bool = debug_option):
    """Callback principal pour gérer les options globales."""
    if debug:
        app.pretty_exceptions_show_locals = True
        app.pretty_exceptions_short = False

    if version:
        console.print(f"version [blue]{__version__}[/blue]")
        raise typer.Exit()


if __name__ == "__main__":
    app()
