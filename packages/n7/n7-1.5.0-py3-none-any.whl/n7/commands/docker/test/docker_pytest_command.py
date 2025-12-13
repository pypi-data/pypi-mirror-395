import subprocess

import typer

from n7.commands.builders.docker_compose_command_builder import DockerComposeCommandBuilder
from n7.commands.builders.pytest_command_builder import PytestCommandBuilder
from n7.commands.resolver.docker_file_resolver import DockerFileResolver

docker_pytest_command = typer.Typer(help="Tests pytest in container docker python")


@docker_pytest_command.callback(invoke_without_command=True)
def run(
    ctx: typer.Context,
    path: str = typer.Argument(None, help="Path of test"),
    verbose: bool = typer.Option(False, "-v", help="Mode verbose"),
    stop_first: bool = typer.Option(False, "-x", help="Stop on first failure"),
    workers: str = typer.Option(None, "-n", help="Number of workers (auto, 2, 4...)"),
    cov: str = typer.Option(None, "--cov", help="App (module python) for coverage"),
    cov_report: str = typer.Option(None, "--cov-report", help="Type rapport (html, term-missing)"),
    last_failed: bool = typer.Option(False, "--lf", help="Re try tests fails"),
    failed_first: bool = typer.Option(False, "--ff", help="Tests fails first time"),
    create_db: bool = typer.Option(False, "--create-db", help="Force create DB (test)"),
    migrations: bool = typer.Option(False, "--migrations", help="Force migrations (test)"),
    service: str = typer.Option(None, "--service", "-s", help="Service docker"),
):
    """Lance les tests pytest dans le container"""
    if ctx.invoked_subcommand is not None:
        return

    # résolution des fichiers docker
    resolver = DockerFileResolver()
    config = resolver.resolve()

    # service à utiliser
    target_service = service or config["default_service"] or "api"

    # build commande pytest
    pytest_builder = PytestCommandBuilder()
    pytest_cmd = pytest_builder.build(
        path=path,
        verbose=verbose,
        stop_first=stop_first,
        workers=workers,
        cov=cov,
        cov_report=cov_report,
        last_failed=last_failed,
        failed_first=failed_first,
        create_db=create_db,
        migrations=migrations,
    )

    # build commande docker compose
    docker_builder = DockerComposeCommandBuilder(
        env_file=config["env_file"] or ".env",
        compose_file=config["compose_file"] or "docker-compose.yml",
    )
    cmd = docker_builder.build_exec(service=target_service, cmd=pytest_cmd)

    # execution
    subprocess.run(cmd, check=True)
