import subprocess

import typer

from n7.commands.builders import DockerComposeCommandBuilder, MypyCommandBuilder
from n7.commands.resolver import DockerFileResolver

docker_mypy_command = typer.Typer(help="Type check Python code with Mypy in Docker container")


@docker_mypy_command.callback(invoke_without_command=True)
def run(
    ctx: typer.Context,
    path: str = typer.Argument(None, help="Path to type check (file or directory)"),
    strict: bool = typer.Option(False, "--strict", help="Strict mode"),
    check_untyped_defs: bool = typer.Option(
        False, "--check-untyped-defs", help="Check untyped functions"
    ),
    disallow_untyped_defs: bool = typer.Option(
        False, "--disallow-untyped-defs", help="Disallow untyped functions"
    ),
    disallow_any_expr: bool = typer.Option(False, "--disallow-any-expr", help="Disallow Any"),
    no_implicit_optional: bool = typer.Option(
        False, "--no-implicit-optional", help="No implicit optional"
    ),
    warn_return_any: bool = typer.Option(False, "--warn-return-any", help="Warn on return Any"),
    warn_unused_ignores: bool = typer.Option(
        False, "--warn-unused-ignores", help="Warn on unused ignores"
    ),
    show_error_codes: bool = typer.Option(False, "--show-error-codes", help="Show error codes"),
    pretty: bool = typer.Option(False, "--pretty", help="Pretty output"),
    no_error_summary: bool = typer.Option(False, "--no-error-summary", help="No error summary"),
    config_file: str = typer.Option(None, "--config-file", help="Config file path"),
    python_version: str = typer.Option(None, "--python-version", help="Python version (e.g. 3.13)"),
    exclude: str = typer.Option(None, "--exclude", help="Exclude pattern"),
    verbose: bool = typer.Option(False, "-v", "--verbose", help="Verbose mode"),
    quiet: bool = typer.Option(False, "-q", "--quiet", help="Quiet mode"),
    service: str = typer.Option(None, "--service", "-s", help="Service docker"),
):
    """Type check Python code with Mypy in Docker container"""
    if ctx.invoked_subcommand is not None:
        return

    # Résolution des fichiers docker
    resolver = DockerFileResolver()
    config_docker = resolver.resolve()

    # Service à utiliser
    target_service = service or config_docker["default_service"] or "api"

    # Build commande mypy
    mypy_builder = MypyCommandBuilder()
    mypy_cmd = mypy_builder.build(
        path=path,
        strict=strict,
        check_untyped_defs=check_untyped_defs,
        disallow_untyped_defs=disallow_untyped_defs,
        disallow_any_expr=disallow_any_expr,
        no_implicit_optional=no_implicit_optional,
        warn_return_any=warn_return_any,
        warn_unused_ignores=warn_unused_ignores,
        show_error_codes=show_error_codes,
        pretty=pretty,
        no_error_summary=no_error_summary,
        config_file=config_file,
        python_version=python_version,
        exclude=exclude,
        verbose=verbose,
        quiet=quiet,
    )

    # Build commande docker compose
    docker_builder = DockerComposeCommandBuilder(
        env_file=config_docker["env_file"] or ".env",
        compose_file=config_docker["compose_file"] or "docker-compose.yml",
    )
    cmd = docker_builder.build_exec(service=target_service, cmd=mypy_cmd)

    # Exécution
    subprocess.run(cmd, check=True)
