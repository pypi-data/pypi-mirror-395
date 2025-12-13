import subprocess

import typer

from n7.commands.builders import DockerComposeCommandBuilder
from n7.commands.resolver import DockerFileResolver

up_command = typer.Typer(help="Gestion containers Docker Compose")


@up_command.callback(invoke_without_command=True)
def up(
    no_detach: bool = typer.Option(
        False, "--no-detach", help="Do you want not start with detached (default : false)"
    ),
    build: bool = typer.Option(
        False, "-b", "--build", help="Do you start with build (default : false)"
    ),
):
    """Lance les containers Docker Compose"""
    # Résolution des fichiers docker
    resolver = DockerFileResolver()
    config = resolver.resolve()

    # Build commande docker compose
    docker_builder = DockerComposeCommandBuilder(
        env_file=config["env_file"] or ".env",
        compose_file=config["compose_file"] or "docker-compose.yml",
    )
    cmd = docker_builder.build_up(detach=not no_detach, build=build)

    # Exécution
    subprocess.run(cmd, check=True)
