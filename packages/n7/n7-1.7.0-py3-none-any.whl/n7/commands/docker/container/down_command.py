import subprocess

import typer

from n7.commands.builders import DockerComposeCommandBuilder
from n7.commands.resolver import DockerFileResolver

down_command = typer.Typer(help="Gestion containers Docker Compose")


@down_command.callback(invoke_without_command=True)
def down(
    volumes: bool = typer.Option(
        False,
        "-v",
        "--volumes",
        help="Do you want delete all volume for containers (default: False)",
    ),
):
    """Stop les containers Docker Compose"""
    # Résolution des fichiers docker
    resolver = DockerFileResolver()
    config = resolver.resolve()

    # Build commande docker compose
    docker_builder = DockerComposeCommandBuilder(
        env_file=config["env_file"] or ".env",
        compose_file=config["compose_file"] or "docker-compose.yml",
    )
    cmd = docker_builder.build_down(volumes=volumes)

    # Exécution
    subprocess.run(cmd, check=True)
