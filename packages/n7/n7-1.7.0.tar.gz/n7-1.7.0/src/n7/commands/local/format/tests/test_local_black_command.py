from unittest.mock import patch

from typer.testing import CliRunner

from n7.commands.local.format.local_black_command import local_black_command

runner = CliRunner()


class TestLocalBlackCommand:
    """Tests pour la commande black local"""

    def test_command_without_options(self):
        """command n7 pybl -> black simple"""
        with patch("n7.commands.local.format.local_black_command.subprocess.run") as mock_run:
            result = runner.invoke(local_black_command, [])

            assert result.exit_code == 0
            mock_run.assert_called_once()
            cmd = mock_run.call_args[0][0]
            assert cmd == ("black",)

    def test_command_with_path(self):
        """command n7 pybl src/"""
        with patch("n7.commands.local.format.local_black_command.subprocess.run") as mock_run:
            result = runner.invoke(local_black_command, ["src/"])

            assert result.exit_code == 0
            cmd = mock_run.call_args[0][0]
            assert cmd == ("black", "src/")

    def test_command_with_check(self):
        """command n7 pybl --check"""
        with patch("n7.commands.local.format.local_black_command.subprocess.run") as mock_run:
            result = runner.invoke(local_black_command, ["--check"])

            assert result.exit_code == 0
            cmd = mock_run.call_args[0][0]
            assert "--check" in cmd

    def test_command_with_diff(self):
        """command n7 pybl --diff"""
        with patch("n7.commands.local.format.local_black_command.subprocess.run") as mock_run:
            result = runner.invoke(local_black_command, ["--diff"])

            assert result.exit_code == 0
            cmd = mock_run.call_args[0][0]
            assert "--diff" in cmd

    def test_command_with_line_length(self):
        """command n7 pybl --line-length 100"""
        with patch("n7.commands.local.format.local_black_command.subprocess.run") as mock_run:
            result = runner.invoke(local_black_command, ["--line-length", "100"])

            assert result.exit_code == 0
            cmd = mock_run.call_args[0][0]
            assert "--line-length" in cmd
            assert "100" in cmd

    def test_command_with_target_version(self):
        """command n7 pybl --target-version py313"""
        with patch("n7.commands.local.format.local_black_command.subprocess.run") as mock_run:
            result = runner.invoke(local_black_command, ["--target-version", "py313"])

            assert result.exit_code == 0
            cmd = mock_run.call_args[0][0]
            assert "--target-version" in cmd
            assert "py313" in cmd

    def test_command_with_verbose(self):
        """command n7 pybl -v"""
        with patch("n7.commands.local.format.local_black_command.subprocess.run") as mock_run:
            result = runner.invoke(local_black_command, ["-v"])

            assert result.exit_code == 0
            cmd = mock_run.call_args[0][0]
            assert "--verbose" in cmd

    def test_command_combined_options(self):
        """command n7 pybl src/ --check --diff -v"""
        with patch("n7.commands.local.format.local_black_command.subprocess.run") as mock_run:
            result = runner.invoke(
                local_black_command,
                [
                    "--check",
                    "--diff",
                    "-v",
                    "src/",
                ],
            )

            assert result.exit_code == 0
            cmd = mock_run.call_args[0][0]
            assert "--check" in cmd
            assert "--diff" in cmd
            assert "--verbose" in cmd
            assert cmd[-1] == "src/"

    def test_command_with_formatting_options(self):
        """command n7 pybl with formatting options"""
        with patch("n7.commands.local.format.local_black_command.subprocess.run") as mock_run:
            result = runner.invoke(
                local_black_command,
                [
                    "--line-length",
                    "100",
                    "--target-version",
                    "py313",
                    "--skip-string-normalization",
                ],
            )

            assert result.exit_code == 0
            cmd = mock_run.call_args[0][0]
            assert "--line-length" in cmd
            assert "100" in cmd
            assert "--target-version" in cmd
            assert "py313" in cmd
            assert "--skip-string-normalization" in cmd
