import subprocess

import typer

from n7.commands.builders import PytestCommandBuilder

local_pytest_command = typer.Typer(help="Tests pytest en local")


@local_pytest_command.callback(invoke_without_command=True)
def run(
    ctx: typer.Context,
    path: str = typer.Argument(None, help="Path of test"),
    verbose: bool = typer.Option(False, "-v", help="Mode verbose"),
    stop_first: bool = typer.Option(False, "-x", help="Stop first failure"),
    workers: str = typer.Option(None, "-n", help="number of workers (auto, 2, 4...)"),
    cov: str = typer.Option(None, "--cov", help="App for coverage"),
    cov_report: str = typer.Option(None, "--cov-report", help="Type rapport (html, term-missing)"),
    last_failed: bool = typer.Option(False, "--lf", help="Re try tests fails"),
    failed_first: bool = typer.Option(False, "--ff", help="Tests fails first time"),
    create_db: bool = typer.Option(False, "--create-db", help="Force create DB (test)"),
    migrations: bool = typer.Option(False, "--migrations", help="Force migrations (test)"),
):
    """Lance les tests pytest en local"""
    if ctx.invoked_subcommand is not None:
        return

    # Build commande pytest
    pytest_builder = PytestCommandBuilder()
    cmd = pytest_builder.build(
        path=path,
        verbose=verbose,
        stop_first=stop_first,
        workers=workers,
        cov=cov,
        cov_report=cov_report,
        last_failed=last_failed,
        failed_first=failed_first,
        create_db=create_db,
        migrations=migrations,
    )

    # Exécution
    subprocess.run(cmd, check=True)
