import subprocess

import typer

from n7.commands.builders import RuffCommandBuilder

local_ruff_command = typer.Typer(help="Lint Python code with Ruff")


@local_ruff_command.callback(invoke_without_command=True)
def run(
    ctx: typer.Context,
    path: str = typer.Argument(None, help="Path to lint (file or directory)"),
    fix: bool = typer.Option(False, "--fix", help="Fix linting errors automatically"),
    diff: bool = typer.Option(False, "--diff", help="Show diff of fixes"),
    watch: bool = typer.Option(False, "--watch", help="Watch mode"),
    fix_only: bool = typer.Option(False, "--fix-only", help="Apply fixes without reporting"),
    unsafe_fixes: bool = typer.Option(False, "--unsafe-fixes", help="Apply unsafe fixes"),
    show_fixes: bool = typer.Option(False, "--show-fixes", help="Show available fixes"),
    output_format: str = typer.Option(
        None, "--output-format", help="Output format (text, json, etc.)"
    ),
    config: str = typer.Option(None, "--config", help="Config file path"),
    select: str = typer.Option(None, "--select", help="Select rules (e.g., E,F)"),
    ignore: str = typer.Option(None, "--ignore", help="Ignore rules (e.g., E501)"),
    exclude: str = typer.Option(None, "--exclude", help="Exclude pattern"),
    extend_select: str = typer.Option(None, "--extend-select", help="Extend selected rules"),
    quiet: bool = typer.Option(False, "-q", "--quiet", help="Quiet mode"),
    verbose: bool = typer.Option(False, "-v", "--verbose", help="Verbose mode"),
):
    """Lint Python code with Ruff"""
    if ctx.invoked_subcommand is not None:
        return

    # Build commande ruff
    ruff_builder = RuffCommandBuilder()
    cmd = ruff_builder.build(
        path=path,
        fix=fix,
        diff=diff,
        watch=watch,
        fix_only=fix_only,
        unsafe_fixes=unsafe_fixes,
        show_fixes=show_fixes,
        output_format=output_format,
        config=config,
        select=select,
        ignore=ignore,
        exclude=exclude,
        extend_select=extend_select,
        quiet=quiet,
        verbose=verbose,
    )

    # Exécution
    subprocess.run(cmd, check=True)
