from unittest.mock import patch

from typer.testing import CliRunner

from n7.commands.local.format.local_mypy_command import local_mypy_command

runner = CliRunner()


class TestLocalMypyCommand:
    """Tests pour la commande mypy local"""

    def test_command_without_options(self):
        """command n7 pymy -> mypy simple"""
        with patch("n7.commands.local.format.local_mypy_command.subprocess.run") as mock_run:
            result = runner.invoke(local_mypy_command, [])

            assert result.exit_code == 0
            mock_run.assert_called_once()
            cmd = mock_run.call_args[0][0]
            assert cmd == ("mypy",)

    def test_command_with_path(self):
        """command n7 pymy src/"""
        with patch("n7.commands.local.format.local_mypy_command.subprocess.run") as mock_run:
            result = runner.invoke(local_mypy_command, ["src/"])

            assert result.exit_code == 0
            cmd = mock_run.call_args[0][0]
            assert cmd == ("mypy", "src/")

    def test_command_with_strict(self):
        """command n7 pymy --strict"""
        with patch("n7.commands.local.format.local_mypy_command.subprocess.run") as mock_run:
            result = runner.invoke(local_mypy_command, ["--strict"])

            assert result.exit_code == 0
            cmd = mock_run.call_args[0][0]
            assert "--strict" in cmd

    def test_command_with_show_error_codes(self):
        """command n7 pymy --show-error-codes"""
        with patch("n7.commands.local.format.local_mypy_command.subprocess.run") as mock_run:
            result = runner.invoke(local_mypy_command, ["--show-error-codes"])

            assert result.exit_code == 0
            cmd = mock_run.call_args[0][0]
            assert "--show-error-codes" in cmd

    def test_command_with_python_version(self):
        """command n7 pymy --python-version 3.13"""
        with patch("n7.commands.local.format.local_mypy_command.subprocess.run") as mock_run:
            result = runner.invoke(local_mypy_command, ["--python-version", "3.13"])

            assert result.exit_code == 0
            cmd = mock_run.call_args[0][0]
            assert "--python-version" in cmd
            assert "3.13" in cmd

    def test_command_with_config_file(self):
        """command n7 pymy --config-file pyproject.toml"""
        with patch("n7.commands.local.format.local_mypy_command.subprocess.run") as mock_run:
            result = runner.invoke(local_mypy_command, ["--config-file", "pyproject.toml"])

            assert result.exit_code == 0
            cmd = mock_run.call_args[0][0]
            assert "--config-file" in cmd
            assert "pyproject.toml" in cmd

    def test_command_with_verbose(self):
        """command n7 pymy -v"""
        with patch("n7.commands.local.format.local_mypy_command.subprocess.run") as mock_run:
            result = runner.invoke(local_mypy_command, ["-v"])

            assert result.exit_code == 0
            cmd = mock_run.call_args[0][0]
            assert "--verbose" in cmd

    def test_command_combined_options(self):
        """command n7 pymy src/ --strict --show-error-codes -v"""
        with patch("n7.commands.local.format.local_mypy_command.subprocess.run") as mock_run:
            result = runner.invoke(
                local_mypy_command,
                [
                    "--strict",
                    "--show-error-codes",
                    "-v",
                    "src/",
                ],
            )

            assert result.exit_code == 0
            cmd = mock_run.call_args[0][0]
            assert "--strict" in cmd
            assert "--show-error-codes" in cmd
            assert "--verbose" in cmd
            assert cmd[-1] == "src/"

    def test_command_with_type_checking_options(self):
        """command n7 pymy with type checking options"""
        with patch("n7.commands.local.format.local_mypy_command.subprocess.run") as mock_run:
            result = runner.invoke(
                local_mypy_command,
                [
                    "--check-untyped-defs",
                    "--disallow-untyped-defs",
                    "--warn-return-any",
                ],
            )

            assert result.exit_code == 0
            cmd = mock_run.call_args[0][0]
            assert "--check-untyped-defs" in cmd
            assert "--disallow-untyped-defs" in cmd
            assert "--warn-return-any" in cmd
