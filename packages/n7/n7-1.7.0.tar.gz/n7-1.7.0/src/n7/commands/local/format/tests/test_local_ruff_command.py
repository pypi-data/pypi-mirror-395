from unittest.mock import patch

from typer.testing import CliRunner

from n7.commands.local.format.local_ruff_command import local_ruff_command

runner = CliRunner()


class TestLocalRuffCommand:
    """Tests pour la commande ruff local"""

    def test_command_without_options(self):
        """command n7 pyrf -> ruff check simple"""
        with patch("n7.commands.local.format.local_ruff_command.subprocess.run") as mock_run:
            result = runner.invoke(local_ruff_command, [])

            assert result.exit_code == 0
            mock_run.assert_called_once()
            cmd = mock_run.call_args[0][0]
            assert cmd == ("ruff", "check")

    def test_command_with_path(self):
        """command n7 pyrf src/"""
        with patch("n7.commands.local.format.local_ruff_command.subprocess.run") as mock_run:
            result = runner.invoke(local_ruff_command, ["src/"])

            assert result.exit_code == 0
            cmd = mock_run.call_args[0][0]
            assert cmd == ("ruff", "check", "src/")

    def test_command_with_fix(self):
        """command n7 pyrf --fix"""
        with patch("n7.commands.local.format.local_ruff_command.subprocess.run") as mock_run:
            result = runner.invoke(local_ruff_command, ["--fix"])

            assert result.exit_code == 0
            cmd = mock_run.call_args[0][0]
            assert "--fix" in cmd

    def test_command_with_diff(self):
        """command n7 pyrf --diff"""
        with patch("n7.commands.local.format.local_ruff_command.subprocess.run") as mock_run:
            result = runner.invoke(local_ruff_command, ["--diff"])

            assert result.exit_code == 0
            cmd = mock_run.call_args[0][0]
            assert "--diff" in cmd

    def test_command_with_select(self):
        """command n7 pyrf --select E,F"""
        with patch("n7.commands.local.format.local_ruff_command.subprocess.run") as mock_run:
            result = runner.invoke(local_ruff_command, ["--select", "E,F"])

            assert result.exit_code == 0
            cmd = mock_run.call_args[0][0]
            assert "--select" in cmd
            assert "E,F" in cmd

    def test_command_with_ignore(self):
        """command n7 pyrf --ignore E501"""
        with patch("n7.commands.local.format.local_ruff_command.subprocess.run") as mock_run:
            result = runner.invoke(local_ruff_command, ["--ignore", "E501"])

            assert result.exit_code == 0
            cmd = mock_run.call_args[0][0]
            assert "--ignore" in cmd
            assert "E501" in cmd

    def test_command_with_verbose(self):
        """command n7 pyrf -v"""
        with patch("n7.commands.local.format.local_ruff_command.subprocess.run") as mock_run:
            result = runner.invoke(local_ruff_command, ["-v"])

            assert result.exit_code == 0
            cmd = mock_run.call_args[0][0]
            assert "--verbose" in cmd

    def test_command_combined_options(self):
        """command n7 pyrf src/ --fix --diff -v"""
        with patch("n7.commands.local.format.local_ruff_command.subprocess.run") as mock_run:
            result = runner.invoke(
                local_ruff_command,
                [
                    "--fix",
                    "--diff",
                    "-v",
                    "src/",
                ],
            )

            assert result.exit_code == 0
            cmd = mock_run.call_args[0][0]
            assert "--fix" in cmd
            assert "--diff" in cmd
            assert "--verbose" in cmd
            assert cmd[-1] == "src/"

    def test_command_with_rules_options(self):
        """command n7 pyrf with rules options"""
        with patch("n7.commands.local.format.local_ruff_command.subprocess.run") as mock_run:
            result = runner.invoke(
                local_ruff_command,
                [
                    "--select",
                    "E,F",
                    "--ignore",
                    "E501",
                    "--extend-select",
                    "B",
                ],
            )

            assert result.exit_code == 0
            cmd = mock_run.call_args[0][0]
            assert "--select" in cmd
            assert "E,F" in cmd
            assert "--ignore" in cmd
            assert "E501" in cmd
            assert "--extend-select" in cmd
            assert "B" in cmd
