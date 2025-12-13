import subprocess

import typer

from n7.commands.builders import DockerComposeCommandBuilder
from n7.commands.resolver import DockerFileResolver

connect_shell_command = typer.Typer(help="Start shell in container")


@connect_shell_command.callback(invoke_without_command=True)
def shell_command(
    no_bash: bool = typer.Option(False, "--no-bash", help="no shell bash, shell becomes 'sh'"),
    service: str = typer.Option(None, "--service", "-s", help="Service docker"),
):
    resolver = DockerFileResolver()
    config = resolver.resolve()

    target_service = service or config["default_service"] or "api"

    # Build commande docker compose
    docker_builder = DockerComposeCommandBuilder(
        env_file=config["env_file"] or ".env",
        compose_file=config["compose_file"] or "docker-compose.yml",
    )

    command = ("bash",)
    if no_bash:
        command = ("sh",)

    cmd = docker_builder.build_exec(service=target_service, cmd=command, disable_tty=False)

    subprocess.run(cmd, check=True)
