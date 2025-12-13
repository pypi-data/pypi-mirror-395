import subprocess

import typer

from n7.commands.builders import (
    BlackCommandBuilder,
    DockerComposeCommandBuilder,
    MypyCommandBuilder,
    PytestCommandBuilder,
    RuffCommandBuilder,
)
from n7.commands.resolver import DockerFileResolver

docker_pycheck_command = typer.Typer(
    help="Run Python checks (Pytest, Black, Ruff, Mypy) in Docker container"
)


@docker_pycheck_command.callback(invoke_without_command=True)
def run(
    ctx: typer.Context,
    path: str = typer.Argument(None, help="Path to check (file or directory)"),
    fix: bool = typer.Option(False, "--fix", help="Apply fixes (Black format, Ruff --fix)"),
    verbose: bool = typer.Option(False, "-v", "--verbose", help="Verbose pytest output"),
    stop_first: bool = typer.Option(
        False, "-x", "--stop-first", help="Stop pytest at first failure"
    ),
    filter_tests: str = typer.Option(None, "-k", help="Filter pytest by test name expression"),
    parallel: bool = typer.Option(False, "--parallel", help="Run tools in parallel"),
    service: str = typer.Option(None, "--service", "-s", help="Service docker"),
):
    """Run Python checks: Pytest, Black, Ruff, and Mypy in Docker container"""
    if ctx.invoked_subcommand is not None:
        return

    # Utiliser "." comme path par défaut si aucun path n'est spécifié
    target_path = path or "."

    # Résolution des fichiers docker
    resolver = DockerFileResolver()
    config_docker = resolver.resolve()

    # Service à utiliser
    target_service = service or config_docker["default_service"] or "api"

    # Build Pytest command
    pytest_builder = PytestCommandBuilder()
    pytest_cmd = pytest_builder.build(
        path=path, verbose=verbose, stop_first=stop_first, filter_tests=filter_tests
    )

    # Build Black command
    black_builder = BlackCommandBuilder()
    if fix:
        # Mode format: pas de --check
        black_cmd = black_builder.build(path=target_path)
    else:
        # Mode check: avec --check
        black_cmd = black_builder.build(path=target_path, check=True)

    # Build Ruff command
    ruff_builder = RuffCommandBuilder()
    ruff_cmd = ruff_builder.build(path=target_path, fix=fix)

    # Build Mypy command
    mypy_builder = MypyCommandBuilder()
    mypy_cmd = mypy_builder.build(path=target_path)

    # Build commande docker compose
    docker_builder = DockerComposeCommandBuilder(
        env_file=config_docker["env_file"] or ".env",
        compose_file=config_docker["compose_file"] or "docker-compose.yml",
    )

    # Build docker commands
    pytest_docker_cmd = docker_builder.build_exec(service=target_service, cmd=pytest_cmd)
    black_docker_cmd = docker_builder.build_exec(service=target_service, cmd=black_cmd)
    ruff_docker_cmd = docker_builder.build_exec(service=target_service, cmd=ruff_cmd)
    mypy_docker_cmd = docker_builder.build_exec(service=target_service, cmd=mypy_cmd)

    if parallel:
        # Exécution parallèle dans le container
        processes = []
        processes.append(subprocess.Popen(pytest_docker_cmd))
        processes.append(subprocess.Popen(black_docker_cmd))
        processes.append(subprocess.Popen(ruff_docker_cmd))
        processes.append(subprocess.Popen(mypy_docker_cmd))

        # Attendre que tous les processus se terminent
        exit_codes = [p.wait() for p in processes]

        # Si un processus a échoué, lever une erreur
        if any(code != 0 for code in exit_codes):
            raise subprocess.CalledProcessError(max(exit_codes), "parallel execution")
    else:
        # Exécution séquentielle dans le container
        subprocess.run(pytest_docker_cmd, check=True)
        subprocess.run(black_docker_cmd, check=True)
        subprocess.run(ruff_docker_cmd, check=True)
        subprocess.run(mypy_docker_cmd, check=True)
