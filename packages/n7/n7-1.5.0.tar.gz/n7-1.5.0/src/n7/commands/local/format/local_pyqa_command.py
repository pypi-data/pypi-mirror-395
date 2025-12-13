import subprocess

import typer

from n7.commands.builders import BlackCommandBuilder, MypyCommandBuilder, RuffCommandBuilder

local_pyqa_command = typer.Typer(help="Run Python QA tools (Black, Ruff, Mypy)")


@local_pyqa_command.callback(invoke_without_command=True)
def run(
    ctx: typer.Context,
    path: str = typer.Argument(None, help="Path to check (file or directory)"),
    fix: bool = typer.Option(False, "--fix", help="Apply fixes (Black format, Ruff --fix)"),
    parallel: bool = typer.Option(False, "--parallel", help="Run tools in parallel"),
):
    """Run Python QA tools: Black, Ruff, and Mypy"""
    if ctx.invoked_subcommand is not None:
        return

    # Utiliser "." comme path par défaut si aucun path n'est spécifié
    target_path = path or "."

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
        subprocess.run(black_cmd, check=True)
        subprocess.run(ruff_cmd, check=True)
        subprocess.run(mypy_cmd, check=True)
