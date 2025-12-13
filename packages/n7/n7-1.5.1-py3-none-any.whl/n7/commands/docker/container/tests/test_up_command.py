from unittest.mock import patch

from typer.testing import CliRunner

from n7.commands.docker.container.up_command import up_command

runner = CliRunner()


class TestUpCommand:
    """Tests pour la commande docker compose up"""

    def test_up_default(self):
        """command n7 dkc up -> docker compose up -d"""
        with patch("n7.commands.docker.container.up_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.container.up_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": None,
                }

                result = runner.invoke(up_command, [])

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
                    "up",
                    "-d",
                )

    def test_up_without_detach(self):
        """command n7 dkc up --no-detach"""
        with patch("n7.commands.docker.container.up_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.container.up_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": None,
                }

                result = runner.invoke(up_command, ["--no-detach"])

                assert result.exit_code == 0
                cmd = mock_run.call_args[0][0]
                assert "-d" not in cmd
                assert cmd[-1] == "up"

    def test_up_custom_files(self):
        """n7 dkc up avec fichiers custom via n7.yaml"""
        with patch("n7.commands.docker.container.up_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.container.up_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env.prod",
                    "compose_file": "docker-compose.prod.yml",
                    "default_service": None,
                }

                result = runner.invoke(up_command, [])

                assert result.exit_code == 0
                cmd = mock_run.call_args[0][0]
                assert ".env.prod" in cmd
                assert "docker-compose.prod.yml" in cmd
