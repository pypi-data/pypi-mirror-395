class RuffCommandBuilder:
    """Build other commands ruff"""

    def __init__(self):
        self.base_cmd = "ruff"

    def build(
        self,
        path: str | None = None,
        fix: bool = False,
        diff: bool = False,
        watch: bool = False,
        fix_only: bool = False,
        unsafe_fixes: bool = False,
        show_fixes: bool = False,
        output_format: str | None = None,
        config: str | None = None,
        select: str | None = None,
        ignore: str | None = None,
        exclude: str | None = None,
        extend_select: str | None = None,
        quiet: bool = False,
        verbose: bool = False,
    ) -> tuple[str, ...]:
        """Build a ruff command with arguments"""
        cmd: tuple[str, ...] = (self.base_cmd, "check")

        if fix:
            cmd = (*cmd, "--fix")
        if diff:
            cmd = (*cmd, "--diff")
        if watch:
            cmd = (*cmd, "--watch")
        if fix_only:
            cmd = (*cmd, "--fix-only")
        if unsafe_fixes:
            cmd = (*cmd, "--unsafe-fixes")
        if show_fixes:
            cmd = (*cmd, "--show-fixes")
        if output_format:
            cmd = (*cmd, "--output-format", output_format)
        if config:
            cmd = (*cmd, "--config", config)
        if select:
            cmd = (*cmd, "--select", select)
        if ignore:
            cmd = (*cmd, "--ignore", ignore)
        if exclude:
            cmd = (*cmd, "--exclude", exclude)
        if extend_select:
            cmd = (*cmd, "--extend-select", extend_select)
        if quiet:
            cmd = (*cmd, "--quiet")
        if verbose:
            cmd = (*cmd, "--verbose")
        if path:
            cmd = (*cmd, path)

        return cmd
