from unittest.mock import patch

from typer.testing import CliRunner

from n7.commands.docker.format.docker_uv_command import docker_uv_command

runner = CliRunner()


class TestDockerUvCommand:
    """Tests pour la commande docker uv"""

    def test_command_without_args(self):
        """n7 dkc uv -> uv dans container"""
        with patch("n7.commands.docker.format.docker_uv_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.format.docker_uv_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(docker_uv_command, [])

                assert result.exit_code == 0
                mock_run.assert_called_once()
                cmd = mock_run.call_args[0][0]
                assert cmd[0:6] == (
                    "docker",
                    "compose",
                    "--env-file",
                    ".env",
                    "-f",
                    "docker-compose.yml",
                )
                assert "api" in cmd
                assert "uv" in cmd

    def test_command_with_pip_install(self):
        """n7 dkc uv pip install requests"""
        with patch("n7.commands.docker.format.docker_uv_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.format.docker_uv_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(docker_uv_command, ["pip", "install", "requests"])

                assert result.exit_code == 0
                cmd = mock_run.call_args[0][0]
                assert "uv" in cmd
                assert "pip" in cmd
                assert "install" in cmd
                assert "requests" in cmd

    def test_command_with_sync(self):
        """n7 dkc uv sync"""
        with patch("n7.commands.docker.format.docker_uv_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.format.docker_uv_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(docker_uv_command, ["sync"])

                assert result.exit_code == 0
                cmd = mock_run.call_args[0][0]
                assert "uv" in cmd
                assert "sync" in cmd

    def test_command_with_lock(self):
        """n7 dkc uv lock"""
        with patch("n7.commands.docker.format.docker_uv_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.format.docker_uv_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(docker_uv_command, ["lock"])

                assert result.exit_code == 0
                cmd = mock_run.call_args[0][0]
                assert "uv" in cmd
                assert "lock" in cmd

    def test_command_with_options(self):
        """n7 dkc uv pip install requests --upgrade"""
        with patch("n7.commands.docker.format.docker_uv_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.format.docker_uv_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(
                    docker_uv_command, ["pip", "install", "requests", "--upgrade"]
                )

                assert result.exit_code == 0
                cmd = mock_run.call_args[0][0]
                assert "uv" in cmd
                assert "pip" in cmd
                assert "install" in cmd
                assert "requests" in cmd
                assert "--upgrade" in cmd

    def test_command_with_custom_service(self):
        """n7 dkc uv --service backend sync"""
        with patch("n7.commands.docker.format.docker_uv_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.format.docker_uv_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(docker_uv_command, ["--service", "backend", "sync"])

                assert result.exit_code == 0
                cmd = mock_run.call_args[0][0]
                assert "backend" in cmd
                assert "uv" in cmd
                assert "sync" in cmd

    def test_command_with_venv(self):
        """n7 dkc uv venv"""
        with patch("n7.commands.docker.format.docker_uv_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.format.docker_uv_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(docker_uv_command, ["venv"])

                assert result.exit_code == 0
                cmd = mock_run.call_args[0][0]
                assert "uv" in cmd
                assert "venv" in cmd
