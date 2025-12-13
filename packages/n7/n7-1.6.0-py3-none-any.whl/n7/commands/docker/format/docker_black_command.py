import subprocess

import typer

from n7.commands.builders import BlackCommandBuilder, DockerComposeCommandBuilder
from n7.commands.resolver import DockerFileResolver

docker_black_command = typer.Typer(help="Format Python code with Black in Docker container")


@docker_black_command.callback(invoke_without_command=True)
def run(
    ctx: typer.Context,
    path: str = typer.Argument(None, help="Path to format (file or directory)"),
    check: bool = typer.Option(False, "--check", help="Don't write files, just check"),
    diff: bool = typer.Option(False, "--diff", help="Show diff without writing"),
    color: bool = typer.Option(False, "--color", help="Force color output"),
    no_color: bool = typer.Option(False, "--no-color", help="Disable color output"),
    line_length: str = typer.Option(None, "--line-length", help="Line length (default: 88)"),
    target_version: str = typer.Option(
        None, "--target-version", help="Python version target (e.g. py313)"
    ),
    skip_string_normalization: bool = typer.Option(
        False, "--skip-string-normalization", help="Skip string normalization"
    ),
    quiet: bool = typer.Option(False, "-q", "--quiet", help="Quiet mode"),
    verbose: bool = typer.Option(False, "-v", "--verbose", help="Verbose mode"),
    fast: bool = typer.Option(False, "--fast", help="Fast mode (skip AST safety checks)"),
    exclude: str = typer.Option(None, "--exclude", help="Exclude pattern"),
    include: str = typer.Option(None, "--include", help="Include pattern"),
    service: str = typer.Option(None, "--service", "-s", help="Service docker"),
):
    """Format Python code with Black in Docker container"""
    if ctx.invoked_subcommand is not None:
        return

    # Résolution des fichiers docker
    resolver = DockerFileResolver()
    config = resolver.resolve()

    # Service à utiliser
    target_service = service or config["default_service"] or "api"

    # Build commande black
    black_builder = BlackCommandBuilder()
    black_cmd = black_builder.build(
        path=path,
        check=check,
        diff=diff,
        color=color,
        no_color=no_color,
        line_length=line_length,
        target_version=target_version,
        skip_string_normalization=skip_string_normalization,
        quiet=quiet,
        verbose=verbose,
        fast=fast,
        exclude=exclude,
        include=include,
    )

    # Build commande docker compose
    docker_builder = DockerComposeCommandBuilder(
        env_file=config["env_file"] or ".env",
        compose_file=config["compose_file"] or "docker-compose.yml",
    )
    cmd = docker_builder.build_exec(service=target_service, cmd=black_cmd)

    # Exécution
    subprocess.run(cmd, check=True)
