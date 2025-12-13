import subprocess
from typing import List

import typer

from n7.commands.builders import DockerComposeCommandBuilder
from n7.commands.resolver import DockerFileResolver

docker_uv_command = typer.Typer(
    help="Run uv command with any arguments in Docker container",
    invoke_without_command=True,
    no_args_is_help=False,
)


@docker_uv_command.callback()
def run(
    args: List[str] = typer.Argument(None, help="Arguments to pass to uv command"),
    service: str = typer.Option(None, "--service", "-s", help="Service docker"),
):
    """Run uv command with any arguments in Docker container"""
    # Récupérer tous les arguments passés à uv
    uv_args = args if args else []

    # Résolution des fichiers docker
    resolver = DockerFileResolver()
    config_docker = resolver.resolve()

    # Service à utiliser
    target_service = service or config_docker["default_service"] or "api"

    # Build command uv
    uv_cmd = ("uv", *uv_args)

    # Build commande docker compose
    docker_builder = DockerComposeCommandBuilder(
        env_file=config_docker["env_file"] or ".env",
        compose_file=config_docker["compose_file"] or "docker-compose.yml",
    )

    # Build docker command
    docker_cmd = docker_builder.build_exec(service=target_service, cmd=uv_cmd)

    # Exécution dans le container
    subprocess.run(docker_cmd, check=True)
