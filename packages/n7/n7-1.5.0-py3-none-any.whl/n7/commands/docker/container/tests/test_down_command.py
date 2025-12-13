from unittest.mock import patch

from typer.testing import CliRunner

from n7.commands.docker.container.down_command import down_command

runner = CliRunner()


class TestDownCommand:
    """Tests pour la commande docker compose down"""

    def test_down_default(self):
        """command n7 dkc down -> docker compose down"""
        with patch("n7.commands.docker.container.down_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.container.down_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": None,
                }

                result = runner.invoke(down_command, [])

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
                    "down",
                )

    def test_down_with_volumes(self):
        """command n7 dkc down -> docker compose down"""
        with patch("n7.commands.docker.container.down_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.container.down_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": None,
                }

                result = runner.invoke(down_command, ["--volumes"])

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
                    "down",
                    "-v",
                )

    def test_down_with_v(self):
        """command n7 dkc down -> docker compose down"""
        with patch("n7.commands.docker.container.down_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.container.down_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": None,
                }

                result = runner.invoke(down_command, ["-v"])

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
                    "down",
                    "-v",
                )

    def test_down_custom_files(self):
        """n7 dkc down avec fichiers custom via n7.yaml"""
        with patch("n7.commands.docker.container.down_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.container.down_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env.prod",
                    "compose_file": "docker-compose.prod.yml",
                    "default_service": None,
                }

                result = runner.invoke(down_command, [])

                assert result.exit_code == 0
                cmd = mock_run.call_args[0][0]
                assert ".env.prod" in cmd
                assert "docker-compose.prod.yml" in cmd
