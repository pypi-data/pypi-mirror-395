import subprocess

import typer

from n7.commands.builders import DockerComposeCommandBuilder
from n7.commands.resolver import DockerFileResolver

connect_postgres_command = typer.Typer(help="Connect to PostgreSQL database in container")


@connect_postgres_command.callback(invoke_without_command=True)
def postgres_command(
    service: str = typer.Option(None, "--service", "-s", help="Service docker"),
    user: str = typer.Option(None, "--user", "-u", help="PostgreSQL user"),
    database: str = typer.Option(None, "--database", "-d", help="PostgreSQL database"),
):
    """Connect to PostgreSQL database using psql"""
    resolver = DockerFileResolver()
    config = resolver.resolve()

    target_service = service or "db"

    # Build commande docker compose
    docker_builder = DockerComposeCommandBuilder(
        env_file=config["env_file"] or ".env",
        compose_file=config["compose_file"] or "docker-compose.yml",
    )

    # Build psql command
    command = ["psql"]
    if user:
        command.extend(["-U", user])
    if database:
        command.extend(["-d", database])

    cmd = docker_builder.build_exec(service=target_service, cmd=tuple(command), disable_tty=False)

    subprocess.run(cmd, check=True)
