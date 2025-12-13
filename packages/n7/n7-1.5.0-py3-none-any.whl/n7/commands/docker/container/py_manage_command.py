import subprocess
from typing import Annotated

import typer

from n7.commands.builders import DockerComposeCommandBuilder
from n7.commands.resolver import DockerFileResolver

py_manage_command = typer.Typer(help="Run python manage.py in container")


@py_manage_command.callback(invoke_without_command=True)
def manage(
    args: Annotated[list[str] | None, typer.Argument(help="Arguments for manage.py")] = None,
    service: Annotated[str | None, typer.Option("--service", "-s", help="Service docker")] = None,
):
    resolver = DockerFileResolver()
    config = resolver.resolve()

    target_service = service or config["default_service"] or "api"

    # Build commande docker compose
    docker_builder = DockerComposeCommandBuilder(
        env_file=config["env_file"] or ".env",
        compose_file=config["compose_file"] or "docker-compose.yml",
    )

    # Construire la commande manage.py
    command = ["python", "manage.py"]
    if args:
        command.extend(args)

    cmd = docker_builder.build_exec(service=target_service, cmd=tuple(command), disable_tty=False)

    subprocess.run(cmd, check=True)
