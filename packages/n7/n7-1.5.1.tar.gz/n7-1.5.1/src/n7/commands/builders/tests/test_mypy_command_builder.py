from n7.commands.builders import MypyCommandBuilder


class TestMypyCommandBuilder:
    def setup_method(self):
        self.builder = MypyCommandBuilder()

    def test_instance_builder(self):
        """test instance builder"""
        assert self.builder is not None
        assert self.builder.base_cmd == "mypy"

    def test_build_command_without_all(self):
        """command mypy only"""
        res = self.builder.build()
        assert res == ("mypy",)

    def test_build_command_with_path(self):
        """command mypy with path"""
        res = self.builder.build(path="my/path")
        assert res == ("mypy", "my/path")

    def test_build_with_strict(self):
        """command mypy --strict"""
        result = self.builder.build(strict=True)
        assert result == ("mypy", "--strict")

    def test_build_with_check_untyped_defs(self):
        """command mypy --check-untyped-defs"""
        result = self.builder.build(check_untyped_defs=True)
        assert result == ("mypy", "--check-untyped-defs")

    def test_build_with_disallow_untyped_defs(self):
        """command mypy --disallow-untyped-defs"""
        result = self.builder.build(disallow_untyped_defs=True)
        assert result == ("mypy", "--disallow-untyped-defs")

    def test_build_with_disallow_any_expr(self):
        """command mypy --disallow-any-expr"""
        result = self.builder.build(disallow_any_expr=True)
        assert result == ("mypy", "--disallow-any-expr")

    def test_build_with_no_implicit_optional(self):
        """command mypy --no-implicit-optional"""
        result = self.builder.build(no_implicit_optional=True)
        assert result == ("mypy", "--no-implicit-optional")

    def test_build_with_warn_return_any(self):
        """command mypy --warn-return-any"""
        result = self.builder.build(warn_return_any=True)
        assert result == ("mypy", "--warn-return-any")

    def test_build_with_warn_unused_ignores(self):
        """command mypy --warn-unused-ignores"""
        result = self.builder.build(warn_unused_ignores=True)
        assert result == ("mypy", "--warn-unused-ignores")

    def test_build_with_show_error_codes(self):
        """command mypy --show-error-codes"""
        result = self.builder.build(show_error_codes=True)
        assert result == ("mypy", "--show-error-codes")

    def test_build_with_pretty(self):
        """command mypy --pretty"""
        result = self.builder.build(pretty=True)
        assert result == ("mypy", "--pretty")

    def test_build_with_no_error_summary(self):
        """command mypy --no-error-summary"""
        result = self.builder.build(no_error_summary=True)
        assert result == ("mypy", "--no-error-summary")

    def test_build_with_config_file(self):
        """command mypy --config-file pyproject.toml"""
        result = self.builder.build(config_file="pyproject.toml")
        assert result == ("mypy", "--config-file", "pyproject.toml")

    def test_build_with_python_version(self):
        """command mypy --python-version 3.13"""
        result = self.builder.build(python_version="3.13")
        assert result == ("mypy", "--python-version", "3.13")

    def test_build_with_exclude(self):
        """command mypy --exclude venv"""
        result = self.builder.build(exclude="venv")
        assert result == ("mypy", "--exclude", "venv")

    def test_build_with_verbose(self):
        """command mypy --verbose"""
        result = self.builder.build(verbose=True)
        assert result == ("mypy", "--verbose")

    def test_build_with_quiet(self):
        """command mypy --quiet"""
        result = self.builder.build(quiet=True)
        assert result == ("mypy", "--quiet")

    def test_build_with_multiple_options(self):
        """command mypy with many options"""
        result = self.builder.build(
            path="src/",
            strict=True,
            show_error_codes=True,
            verbose=True,
        )
        assert result == ("mypy", "--strict", "--show-error-codes", "--verbose", "src/")

    def test_build_with_type_checking_options(self):
        """command mypy with type checking options"""
        result = self.builder.build(
            check_untyped_defs=True,
            disallow_untyped_defs=True,
            warn_return_any=True,
        )
        assert result == (
            "mypy",
            "--check-untyped-defs",
            "--disallow-untyped-defs",
            "--warn-return-any",
        )

    def test_path_always_last(self):
        """This path always last"""
        result = self.builder.build(
            path="src/",
            strict=True,
            python_version="3.13",
            verbose=True,
        )
        assert result[-1] == "src/"

    def test_build_full_command(self):
        """command mypy with all common options"""
        result = self.builder.build(
            path=".",
            strict=True,
            show_error_codes=True,
            pretty=True,
            verbose=True,
        )
        assert result == (
            "mypy",
            "--strict",
            "--show-error-codes",
            "--pretty",
            "--verbose",
            ".",
        )
