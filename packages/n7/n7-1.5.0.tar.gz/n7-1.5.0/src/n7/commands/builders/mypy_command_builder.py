class MypyCommandBuilder:
    """Build other commands mypy"""

    def __init__(self):
        self.base_cmd = "mypy"

    def build(
        self,
        path: str | None = None,
        strict: bool = False,
        check_untyped_defs: bool = False,
        disallow_untyped_defs: bool = False,
        disallow_any_expr: bool = False,
        no_implicit_optional: bool = False,
        warn_return_any: bool = False,
        warn_unused_ignores: bool = False,
        show_error_codes: bool = False,
        pretty: bool = False,
        no_error_summary: bool = False,
        config_file: str | None = None,
        python_version: str | None = None,
        exclude: str | None = None,
        verbose: bool = False,
        quiet: bool = False,
    ) -> tuple[str, ...]:
        """Build a mypy command with arguments"""
        cmd: tuple[str, ...] = (self.base_cmd,)

        if strict:
            cmd = (*cmd, "--strict")
        if check_untyped_defs:
            cmd = (*cmd, "--check-untyped-defs")
        if disallow_untyped_defs:
            cmd = (*cmd, "--disallow-untyped-defs")
        if disallow_any_expr:
            cmd = (*cmd, "--disallow-any-expr")
        if no_implicit_optional:
            cmd = (*cmd, "--no-implicit-optional")
        if warn_return_any:
            cmd = (*cmd, "--warn-return-any")
        if warn_unused_ignores:
            cmd = (*cmd, "--warn-unused-ignores")
        if show_error_codes:
            cmd = (*cmd, "--show-error-codes")
        if pretty:
            cmd = (*cmd, "--pretty")
        if no_error_summary:
            cmd = (*cmd, "--no-error-summary")
        if config_file:
            cmd = (*cmd, "--config-file", config_file)
        if python_version:
            cmd = (*cmd, "--python-version", python_version)
        if exclude:
            cmd = (*cmd, "--exclude", exclude)
        if verbose:
            cmd = (*cmd, "--verbose")
        if quiet:
            cmd = (*cmd, "--quiet")
        if path:
            cmd = (*cmd, path)

        return cmd
