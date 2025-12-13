class BlackCommandBuilder:
    """Build other commands black"""

    def __init__(self):
        self.base_cmd = "black"

    def build(
        self,
        path: str | None = None,
        check: bool = False,
        diff: bool = False,
        color: bool = False,
        no_color: bool = False,
        line_length: str | None = None,
        target_version: str | None = None,
        skip_string_normalization: bool = False,
        quiet: bool = False,
        verbose: bool = False,
        fast: bool = False,
        exclude: str | None = None,
        include: str | None = None,
    ) -> tuple[str, ...]:
        """Build a black command with arguments"""
        cmd: tuple[str, ...] = (self.base_cmd,)

        if check:
            cmd = (*cmd, "--check")
        if diff:
            cmd = (*cmd, "--diff")
        # color takes precedence over no_color
        if color:
            cmd = (*cmd, "--color")
        elif no_color:
            cmd = (*cmd, "--no-color")
        if line_length:
            cmd = (*cmd, "--line-length", line_length)
        if target_version:
            cmd = (*cmd, "--target-version", target_version)
        if skip_string_normalization:
            cmd = (*cmd, "--skip-string-normalization")
        if quiet:
            cmd = (*cmd, "--quiet")
        if verbose:
            cmd = (*cmd, "--verbose")
        if fast:
            cmd = (*cmd, "--fast")
        if exclude:
            cmd = (*cmd, "--exclude", exclude)
        if include:
            cmd = (*cmd, "--include", include)
        if path:
            cmd = (*cmd, path)

        return cmd
