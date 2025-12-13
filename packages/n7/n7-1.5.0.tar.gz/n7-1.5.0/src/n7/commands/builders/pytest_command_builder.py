class PytestCommandBuilder:
    """Build other commands pytest"""

    def __init__(self):
        self.base_cmd = "pytest"

    def build(
        self,
        path: str | None = None,
        verbose: bool = False,
        stop_first: bool = False,
        filter_tests: str | None = None,
        workers: str | None = None,
        cov: str | None = None,
        cov_report: str | None = None,
        last_failed: bool = False,
        failed_first: bool = False,
        create_db: bool = False,
        migrations: bool = False,
    ) -> tuple[str, ...]:
        """Build a pytest command with arguments"""
        cmd: tuple[str, ...] = (self.base_cmd,)

        if verbose:
            cmd = (*cmd, "-v")
        if stop_first:
            cmd = (*cmd, "-x")
        if filter_tests:
            cmd = (*cmd, "-k", filter_tests)
        if workers:
            cmd = (*cmd, "-n", workers)
        if cov:
            cmd = (*cmd, f"--cov={cov}")
        if cov_report:
            cmd = (*cmd, f"--cov-report={cov_report}")
        if last_failed:
            cmd = (*cmd, "--lf")
        if failed_first:
            cmd = (*cmd, "--ff")
        if create_db:
            cmd = (*cmd, "--create-db")
        if migrations:
            cmd = (*cmd, "--migrations")
        if path:
            cmd = (*cmd, path)

        return cmd
