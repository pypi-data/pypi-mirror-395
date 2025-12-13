import subprocess
from typing import List

import typer

local_uv_command = typer.Typer(
    help="Run uv command with any arguments",
    invoke_without_command=True,
    no_args_is_help=False,
)


@local_uv_command.callback()
def run(
    args: List[str] = typer.Argument(None, help="Arguments to pass to uv command"),
):
    """Run uv command with any arguments"""
    # Build command uv
    uv_args = args if args else []
    cmd = ("uv", *uv_args)

    # Exécution
    subprocess.run(cmd, check=True)
