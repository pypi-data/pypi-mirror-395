from unittest.mock import patch

from typer.testing import CliRunner

from n7.commands.local.test.local_pytest_command import local_pytest_command

runner = CliRunner()


class TestLocalTestCommand:
    """Tests pour la commande test local"""

    def test_command_without_options(self):
        """command n7 t -> pytest simple"""
        with patch("n7.commands.local.test.local_pytest_command.subprocess.run") as mock_run:
            result = runner.invoke(local_pytest_command, [])

            assert result.exit_code == 0
            mock_run.assert_called_once()
            cmd = mock_run.call_args[0][0]
            assert cmd == ("pytest",)

    def test_command_with_path(self):
        """command n7 t users/tests/"""
        with patch("n7.commands.local.test.local_pytest_command.subprocess.run") as mock_run:
            result = runner.invoke(local_pytest_command, ["users/tests/"])

            assert result.exit_code == 0
            cmd = mock_run.call_args[0][0]
            assert cmd == ("pytest", "users/tests/")

    def test_command_with_verbose(self):
        """command n7 t -v"""
        with patch("n7.commands.local.test.local_pytest_command.subprocess.run") as mock_run:
            result = runner.invoke(local_pytest_command, ["-v"])

            assert result.exit_code == 0
            cmd = mock_run.call_args[0][0]
            assert "-v" in cmd

    def test_command_with_workers(self):
        """command n7 t -n auto"""
        with patch("n7.commands.local.test.local_pytest_command.subprocess.run") as mock_run:
            result = runner.invoke(local_pytest_command, ["-n", "auto"])

            assert result.exit_code == 0
            cmd = mock_run.call_args[0][0]
            assert "-n" in cmd
            assert "auto" in cmd

    def test_command_with_coverage(self):
        """command n7 t --cov users"""
        with patch("n7.commands.local.test.local_pytest_command.subprocess.run") as mock_run:
            result = runner.invoke(local_pytest_command, ["--cov", "users"])

            assert result.exit_code == 0
            cmd = mock_run.call_args[0][0]
            assert "--cov=users" in cmd

    def test_command_with_last_failed(self):
        """command n7 t --lf"""
        with patch("n7.commands.local.test.local_pytest_command.subprocess.run") as mock_run:
            result = runner.invoke(local_pytest_command, ["--lf"])

            assert result.exit_code == 0
            cmd = mock_run.call_args[0][0]
            assert "--lf" in cmd

    def test_command_combined_options(self):
        """command n7 t -v -n 4 --cov users users/tests/"""
        with patch("n7.commands.local.test.local_pytest_command.subprocess.run") as mock_run:
            result = runner.invoke(
                local_pytest_command,
                [
                    "-v",
                    "-n",
                    "4",
                    "--cov",
                    "users",
                    "users/tests/",
                ],
            )

            assert result.exit_code == 0
            cmd = mock_run.call_args[0][0]
            assert "-v" in cmd
            assert "-n" in cmd
            assert "4" in cmd
            assert "--cov=users" in cmd
            assert cmd[-1] == "users/tests/"
