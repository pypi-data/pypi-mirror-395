from unittest.mock import patch

from typer.testing import CliRunner

from n7.commands.docker.container.connect_shell_command import connect_shell_command

runner = CliRunner()


class TestConnectShellCommand:
    """Test pour la commande qui permet de se connecter au shell du container"""

    def test_connect_shell_command(self):
        with patch("n7.commands.docker.container.connect_shell_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.container.connect_shell_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(connect_shell_command, [])

                assert result.exit_code == 0
                mock_run.assert_called_once()

                cmd = mock_run.call_args[0][0]
                assert cmd == (
                    "docker",
                    "compose",
                    "--env-file",
                    ".env",
                    "-f",
                    "docker-compose.yml",
                    "exec",
                    "api",
                    "bash",
                )

    def test_connect_shell_command_with_no_bash(self):
        with patch("n7.commands.docker.container.connect_shell_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.container.connect_shell_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(connect_shell_command, ["--no-bash"])

                assert result.exit_code == 0
                mock_run.assert_called_once()

                cmd = mock_run.call_args[0][0]
                assert cmd == (
                    "docker",
                    "compose",
                    "--env-file",
                    ".env",
                    "-f",
                    "docker-compose.yml",
                    "exec",
                    "api",
                    "sh",
                )

    def test_connect_shell_command_with_service(self):
        with patch("n7.commands.docker.container.connect_shell_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.container.connect_shell_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": None,
                }

                result = runner.invoke(connect_shell_command, ["--service", "truc"])

                assert result.exit_code == 0
                mock_run.assert_called_once()

                cmd = mock_run.call_args[0][0]
                assert cmd == (
                    "docker",
                    "compose",
                    "--env-file",
                    ".env",
                    "-f",
                    "docker-compose.yml",
                    "exec",
                    "truc",
                    "bash",
                )

    def test_connect_shell_command_with_service_with_no_bash(self):
        with patch("n7.commands.docker.container.connect_shell_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.container.connect_shell_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": None,
                }

                result = runner.invoke(connect_shell_command, ["--no-bash", "--service", "truc"])

                assert result.exit_code == 0
                mock_run.assert_called_once()

                cmd = mock_run.call_args[0][0]
                assert cmd == (
                    "docker",
                    "compose",
                    "--env-file",
                    ".env",
                    "-f",
                    "docker-compose.yml",
                    "exec",
                    "truc",
                    "sh",
                )
