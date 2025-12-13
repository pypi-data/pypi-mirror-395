from unittest.mock import patch

from typer.testing import CliRunner

from n7.commands.local.format.local_uv_command import local_uv_command

runner = CliRunner()


class TestLocalUvCommand:
    """Tests pour la commande uv local"""

    def test_command_without_args(self):
        """command n7 uv -> uv"""
        with patch("n7.commands.local.format.local_uv_command.subprocess.run") as mock_run:
            result = runner.invoke(local_uv_command, [])

            assert result.exit_code == 0
            mock_run.assert_called_once()
            cmd = mock_run.call_args[0][0]
            assert cmd == ("uv",)

    def test_command_with_pip_install(self):
        """command n7 uv pip install requests"""
        with patch("n7.commands.local.format.local_uv_command.subprocess.run") as mock_run:
            result = runner.invoke(local_uv_command, ["pip", "install", "requests"])

            assert result.exit_code == 0
            cmd = mock_run.call_args[0][0]
            assert cmd == ("uv", "pip", "install", "requests")

    def test_command_with_sync(self):
        """command n7 uv sync"""
        with patch("n7.commands.local.format.local_uv_command.subprocess.run") as mock_run:
            result = runner.invoke(local_uv_command, ["sync"])

            assert result.exit_code == 0
            cmd = mock_run.call_args[0][0]
            assert cmd == ("uv", "sync")

    def test_command_with_lock(self):
        """command n7 uv lock"""
        with patch("n7.commands.local.format.local_uv_command.subprocess.run") as mock_run:
            result = runner.invoke(local_uv_command, ["lock"])

            assert result.exit_code == 0
            cmd = mock_run.call_args[0][0]
            assert cmd == ("uv", "lock")

    def test_command_with_options(self):
        """command n7 uv pip install requests --upgrade"""
        with patch("n7.commands.local.format.local_uv_command.subprocess.run") as mock_run:
            result = runner.invoke(local_uv_command, ["pip", "install", "requests", "--upgrade"])

            assert result.exit_code == 0
            cmd = mock_run.call_args[0][0]
            assert cmd == ("uv", "pip", "install", "requests", "--upgrade")

    def test_command_with_multiple_packages(self):
        """command n7 uv pip install requests pytest black"""
        with patch("n7.commands.local.format.local_uv_command.subprocess.run") as mock_run:
            result = runner.invoke(
                local_uv_command, ["pip", "install", "requests", "pytest", "black"]
            )

            assert result.exit_code == 0
            cmd = mock_run.call_args[0][0]
            assert cmd == ("uv", "pip", "install", "requests", "pytest", "black")

    def test_command_with_venv(self):
        """command n7 uv venv"""
        with patch("n7.commands.local.format.local_uv_command.subprocess.run") as mock_run:
            result = runner.invoke(local_uv_command, ["venv"])

            assert result.exit_code == 0
            cmd = mock_run.call_args[0][0]
            assert cmd == ("uv", "venv")
