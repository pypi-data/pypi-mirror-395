from unittest.mock import patch

from typer.testing import CliRunner

from n7.commands.docker.container.logs_command import logs_command

runner = CliRunner()


class TestLogsCommand:
    """Tests pour la commande docker compose logs"""

    def test_logs_without_service(self):
        """n7 dkc logs -> docker compose logs (tous les services)"""
        with patch("n7.commands.docker.container.logs_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.container.logs_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": None,
                }

                result = runner.invoke(logs_command, [])

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
                    "logs",
                    "",
                )

    def test_logs_with_service(self):
        """n7 dkc logs api"""
        with patch("n7.commands.docker.container.logs_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.container.logs_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": None,
                }

                result = runner.invoke(logs_command, ["api"])

                assert result.exit_code == 0
                cmd = mock_run.call_args[0][0]
                assert "api" in cmd
                assert cmd == (
                    "docker",
                    "compose",
                    "--env-file",
                    ".env",
                    "-f",
                    "docker-compose.yml",
                    "logs",
                    "api",
                )

    def test_logs_with_multiple_services(self):
        """n7 dkc logs worker"""
        with patch("n7.commands.docker.container.logs_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.container.logs_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": None,
                }

                result = runner.invoke(logs_command, ["worker"])

                assert result.exit_code == 0
                cmd = mock_run.call_args[0][0]
                assert "worker" in cmd

    def test_logs_with_follow(self):
        """n7 dkc logs --follow"""
        with patch("n7.commands.docker.container.logs_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.container.logs_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": None,
                }

                result = runner.invoke(logs_command, ["--follow"])

                assert result.exit_code == 0
                cmd = mock_run.call_args[0][0]
                assert "-f" in cmd
                assert cmd == (
                    "docker",
                    "compose",
                    "--env-file",
                    ".env",
                    "-f",
                    "docker-compose.yml",
                    "logs",
                    "-f",
                    "",
                )

    def test_logs_with_follow_short_option(self):
        """n7 dkc logs -f"""
        with patch("n7.commands.docker.container.logs_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.container.logs_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": None,
                }

                result = runner.invoke(logs_command, ["-f"])

                assert result.exit_code == 0
                cmd = mock_run.call_args[0][0]
                assert "-f" in cmd

    def test_logs_with_service_and_follow(self):
        """n7 dkc logs --follow api"""
        with patch("n7.commands.docker.container.logs_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.container.logs_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": None,
                }

                result = runner.invoke(logs_command, ["--follow", "api"])

                assert result.exit_code == 0
                cmd = mock_run.call_args[0][0]
                assert "api" in cmd
                assert "-f" in cmd
                assert cmd == (
                    "docker",
                    "compose",
                    "--env-file",
                    ".env",
                    "-f",
                    "docker-compose.yml",
                    "logs",
                    "-f",
                    "api",
                )

    def test_logs_with_service_and_follow_short_option(self):
        """n7 dkc logs -f api"""
        with patch("n7.commands.docker.container.logs_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.container.logs_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": None,
                }

                result = runner.invoke(logs_command, ["-f", "api"])

                assert result.exit_code == 0
                cmd = mock_run.call_args[0][0]
                assert "api" in cmd
                assert "-f" in cmd

    def test_logs_custom_files(self):
        """n7 dkc logs worker avec fichiers custom via n7.yaml"""
        with patch("n7.commands.docker.container.logs_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.container.logs_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env.prod",
                    "compose_file": "docker-compose.prod.yml",
                    "default_service": None,
                }

                result = runner.invoke(logs_command, ["worker"])

                assert result.exit_code == 0
                cmd = mock_run.call_args[0][0]
                assert ".env.prod" in cmd
                assert "docker-compose.prod.yml" in cmd
                assert "worker" in cmd
