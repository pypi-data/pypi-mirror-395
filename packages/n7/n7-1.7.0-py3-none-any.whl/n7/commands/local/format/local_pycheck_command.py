import subprocess

import typer

from n7.commands.builders import (
    BlackCommandBuilder,
    MypyCommandBuilder,
    PytestCommandBuilder,
    RuffCommandBuilder,
)

local_pycheck_command = typer.Typer(help="Run Python checks (Pytest, Black, Ruff, Mypy)")


@local_pycheck_command.callback(invoke_without_command=True)
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
):
    """Run Python checks: Pytest, Black, Ruff, and Mypy"""
    if ctx.invoked_subcommand is not None:
        return

    # Utiliser "." comme path par défaut si aucun path n'est spécifié
    target_path = path or "."

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

    if parallel:
        # Exécution parallèle
        processes = []
        processes.append(subprocess.Popen(pytest_cmd))
        processes.append(subprocess.Popen(black_cmd))
        processes.append(subprocess.Popen(ruff_cmd))
        processes.append(subprocess.Popen(mypy_cmd))

        # Attendre que tous les processus se terminent
        exit_codes = [p.wait() for p in processes]

        # Si un processus a échoué, lever une erreur
        if any(code != 0 for code in exit_codes):
            raise subprocess.CalledProcessError(max(exit_codes), "parallel execution")
    else:
        # Exécution séquentielle
        subprocess.run(pytest_cmd, check=True)
        subprocess.run(black_cmd, check=True)
        subprocess.run(ruff_cmd, check=True)
        subprocess.run(mypy_cmd, check=True)
