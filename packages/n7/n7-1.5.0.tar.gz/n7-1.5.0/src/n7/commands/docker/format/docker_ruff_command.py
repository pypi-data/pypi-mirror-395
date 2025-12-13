import subprocess

import typer

from n7.commands.builders import DockerComposeCommandBuilder, RuffCommandBuilder
from n7.commands.resolver import DockerFileResolver

docker_ruff_command = typer.Typer(help="Lint Python code with Ruff in Docker container")


@docker_ruff_command.callback(invoke_without_command=True)
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
    service: str = typer.Option(None, "--service", "-s", help="Service docker"),
):
    """Lint Python code with Ruff in Docker container"""
    if ctx.invoked_subcommand is not None:
        return

    # Résolution des fichiers docker
    resolver = DockerFileResolver()
    config_docker = resolver.resolve()

    # Service à utiliser
    target_service = service or config_docker["default_service"] or "api"

    # Build commande ruff
    ruff_builder = RuffCommandBuilder()
    ruff_cmd = ruff_builder.build(
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

    # Build commande docker compose
    docker_builder = DockerComposeCommandBuilder(
        env_file=config_docker["env_file"] or ".env",
        compose_file=config_docker["compose_file"] or "docker-compose.yml",
    )
    cmd = docker_builder.build_exec(service=target_service, cmd=ruff_cmd)

    # Exécution
    subprocess.run(cmd, check=True)
