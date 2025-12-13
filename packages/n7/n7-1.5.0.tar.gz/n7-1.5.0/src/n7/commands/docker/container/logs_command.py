import subprocess

import typer

from n7.commands.builders import DockerComposeCommandBuilder
from n7.commands.resolver import DockerFileResolver

logs_command = typer.Typer(help="Gestion containers Docker Compose")


@logs_command.callback(invoke_without_command=True)
def logs(
    service: str = typer.Argument(
        "", help="Name of the service container (optional, all services if not specified)"
    ),
    follow: bool = typer.Option(False, "-f", "--follow", help="Do you want see live file logs"),
):
    """Show logs of Docker Compose containers"""
    # Résolution des fichiers docker
    resolver = DockerFileResolver()
    config = resolver.resolve()

    # Build commande docker compose
    docker_builder = DockerComposeCommandBuilder(
        env_file=config["env_file"] or ".env",
        compose_file=config["compose_file"] or "docker-compose.yml",
    )
    cmd = docker_builder.build_logs(service=service, follow=follow)

    # Exécution
    subprocess.run(cmd, check=True)
