from n7.commands.builders import RuffCommandBuilder


class TestRuffCommandBuilder:
    def setup_method(self):
        self.builder = RuffCommandBuilder()

    def test_instance_builder(self):
        """test instance builder"""
        assert self.builder is not None
        assert self.builder.base_cmd == "ruff"

    def test_build_command_without_all(self):
        """command ruff check only"""
        res = self.builder.build()
        assert res == ("ruff", "check")

    def test_build_command_with_path(self):
        """command ruff check with path"""
        res = self.builder.build(path="my/path")
        assert res == ("ruff", "check", "my/path")

    def test_build_with_fix(self):
        """command ruff check --fix"""
        result = self.builder.build(fix=True)
        assert result == ("ruff", "check", "--fix")

    def test_build_with_diff(self):
        """command ruff check --diff"""
        result = self.builder.build(diff=True)
        assert result == ("ruff", "check", "--diff")

    def test_build_with_watch(self):
        """command ruff check --watch"""
        result = self.builder.build(watch=True)
        assert result == ("ruff", "check", "--watch")

    def test_build_with_fix_only(self):
        """command ruff check --fix-only"""
        result = self.builder.build(fix_only=True)
        assert result == ("ruff", "check", "--fix-only")

    def test_build_with_unsafe_fixes(self):
        """command ruff check --unsafe-fixes"""
        result = self.builder.build(unsafe_fixes=True)
        assert result == ("ruff", "check", "--unsafe-fixes")

    def test_build_with_show_fixes(self):
        """command ruff check --show-fixes"""
        result = self.builder.build(show_fixes=True)
        assert result == ("ruff", "check", "--show-fixes")

    def test_build_with_output_format(self):
        """command ruff check --output-format json"""
        result = self.builder.build(output_format="json")
        assert result == ("ruff", "check", "--output-format", "json")

    def test_build_with_config(self):
        """command ruff check --config pyproject.toml"""
        result = self.builder.build(config="pyproject.toml")
        assert result == ("ruff", "check", "--config", "pyproject.toml")

    def test_build_with_select(self):
        """command ruff check --select E,F"""
        result = self.builder.build(select="E,F")
        assert result == ("ruff", "check", "--select", "E,F")

    def test_build_with_ignore(self):
        """command ruff check --ignore E501"""
        result = self.builder.build(ignore="E501")
        assert result == ("ruff", "check", "--ignore", "E501")

    def test_build_with_exclude(self):
        """command ruff check --exclude venv"""
        result = self.builder.build(exclude="venv")
        assert result == ("ruff", "check", "--exclude", "venv")

    def test_build_with_extend_select(self):
        """command ruff check --extend-select B"""
        result = self.builder.build(extend_select="B")
        assert result == ("ruff", "check", "--extend-select", "B")

    def test_build_with_quiet(self):
        """command ruff check --quiet"""
        result = self.builder.build(quiet=True)
        assert result == ("ruff", "check", "--quiet")

    def test_build_with_verbose(self):
        """command ruff check --verbose"""
        result = self.builder.build(verbose=True)
        assert result == ("ruff", "check", "--verbose")

    def test_build_with_multiple_options(self):
        """command ruff check with many options"""
        result = self.builder.build(
            path="src/",
            fix=True,
            diff=True,
            verbose=True,
        )
        assert result == ("ruff", "check", "--fix", "--diff", "--verbose", "src/")

    def test_build_with_rules_options(self):
        """command ruff check with rules options"""
        result = self.builder.build(
            select="E,F",
            ignore="E501",
            extend_select="B",
        )
        assert result == (
            "ruff",
            "check",
            "--select",
            "E,F",
            "--ignore",
            "E501",
            "--extend-select",
            "B",
        )

    def test_path_always_last(self):
        """This path always last"""
        result = self.builder.build(
            path="src/",
            fix=True,
            select="E,F",
            verbose=True,
        )
        assert result[-1] == "src/"

    def test_build_full_command(self):
        """command ruff check with all common options"""
        result = self.builder.build(
            path=".",
            fix=True,
            diff=True,
            select="E,F",
            verbose=True,
        )
        assert result == (
            "ruff",
            "check",
            "--fix",
            "--diff",
            "--select",
            "E,F",
            "--verbose",
            ".",
        )
