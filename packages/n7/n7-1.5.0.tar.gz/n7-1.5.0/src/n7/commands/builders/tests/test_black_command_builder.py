from n7.commands.builders import BlackCommandBuilder


class TestBlackCommandBuilder:
    def setup_method(self):
        self.builder = BlackCommandBuilder()

    def test_instance_builder(self):
        """test instance builder"""
        assert self.builder is not None
        assert self.builder.base_cmd == "black"

    def test_build_command_without_all(self):
        """command black only"""
        res = self.builder.build()
        assert res == ("black",)

    def test_build_command_with_path(self):
        """command black with path"""
        res = self.builder.build(path="my/path")
        assert res == ("black", "my/path")

    def test_build_with_check(self):
        """command black --check"""
        result = self.builder.build(check=True)
        assert result == ("black", "--check")

    def test_build_with_diff(self):
        """command black --diff"""
        result = self.builder.build(diff=True)
        assert result == ("black", "--diff")

    def test_build_with_color(self):
        """command black --color"""
        result = self.builder.build(color=True)
        assert result == ("black", "--color")

    def test_build_with_no_color(self):
        """command black --no-color"""
        result = self.builder.build(no_color=True)
        assert result == ("black", "--no-color")

    def test_build_with_line_length(self):
        """command black --line-length 100"""
        result = self.builder.build(line_length="100")
        assert result == ("black", "--line-length", "100")

    def test_build_with_line_length_default(self):
        """command black --line-length 88"""
        result = self.builder.build(line_length="88")
        assert result == ("black", "--line-length", "88")

    def test_build_with_target_version(self):
        """command black --target-version py313"""
        result = self.builder.build(target_version="py313")
        assert result == ("black", "--target-version", "py313")

    def test_build_with_skip_string_normalization(self):
        """command black --skip-string-normalization"""
        result = self.builder.build(skip_string_normalization=True)
        assert result == ("black", "--skip-string-normalization")

    def test_build_with_quiet(self):
        """command black --quiet"""
        result = self.builder.build(quiet=True)
        assert result == ("black", "--quiet")

    def test_build_with_verbose(self):
        """command black --verbose"""
        result = self.builder.build(verbose=True)
        assert result == ("black", "--verbose")

    def test_build_with_fast(self):
        """command black --fast"""
        result = self.builder.build(fast=True)
        assert result == ("black", "--fast")

    def test_build_with_exclude(self):
        """command black --exclude pattern"""
        result = self.builder.build(exclude="venv")
        assert result == ("black", "--exclude", "venv")

    def test_build_with_include(self):
        """command black --include pattern"""
        result = self.builder.build(include="\\.pyi?$")
        assert result == ("black", "--include", "\\.pyi?$")

    def test_build_with_multiple_options(self):
        """command black with many options"""
        result = self.builder.build(
            path="src/",
            check=True,
            diff=True,
            verbose=True,
        )
        assert result == ("black", "--check", "--diff", "--verbose", "src/")

    def test_build_with_formatting_options(self):
        """command black with formatting options"""
        result = self.builder.build(
            line_length="100",
            target_version="py313",
            skip_string_normalization=True,
        )
        assert result == (
            "black",
            "--line-length",
            "100",
            "--target-version",
            "py313",
            "--skip-string-normalization",
        )

    def test_path_always_last(self):
        """This path always last"""
        result = self.builder.build(
            path="src/",
            check=True,
            line_length="100",
            verbose=True,
        )
        assert result[-1] == "src/"

    def test_build_full_command(self):
        """command black with all common options"""
        result = self.builder.build(
            path=".",
            check=True,
            diff=True,
            color=True,
            line_length="100",
            target_version="py313",
            verbose=True,
        )
        assert result == (
            "black",
            "--check",
            "--diff",
            "--color",
            "--line-length",
            "100",
            "--target-version",
            "py313",
            "--verbose",
            ".",
        )

    def test_color_and_no_color_not_both(self):
        """test that color takes precedence over no_color if both are set"""
        # Dans l'implémentation, on gérera ce cas en donnant la priorité à color
        result = self.builder.build(color=True, no_color=True)
        assert "--color" in result
        assert "--no-color" not in result
