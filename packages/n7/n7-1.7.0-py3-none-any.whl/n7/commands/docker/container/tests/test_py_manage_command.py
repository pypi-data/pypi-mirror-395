from unittest.mock import patch

from typer.testing import CliRunner

from n7.commands.docker.container.py_manage_command import py_manage_command

runner = CliRunner()


class TestManageCommand:
    """Test pour la commande qui permet d'exécuter python manage.py"""

    def test_manage_command_without_args(self):
        """test manage sans arguments"""
        with patch("n7.commands.docker.container.py_manage_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.container.py_manage_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(py_manage_command, [])

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
                    "python",
                    "manage.py",
                )

    def test_manage_command_with_single_arg(self):
        """test manage avec un argument"""
        with patch("n7.commands.docker.container.py_manage_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.container.py_manage_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(py_manage_command, ["migrate"])

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
                    "python",
                    "manage.py",
                    "migrate",
                )

    def test_manage_command_with_multiple_args(self):
        """test manage avec plusieurs arguments"""
        with patch("n7.commands.docker.container.py_manage_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.container.py_manage_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(py_manage_command, ["makemigrations", "app"])

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
                    "python",
                    "manage.py",
                    "makemigrations",
                    "app",
                )

    def test_manage_command_with_custom_service(self):
        """test manage avec service custom"""
        with patch("n7.commands.docker.container.py_manage_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.container.py_manage_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(py_manage_command, ["--service", "backend", "migrate"])

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
                    "backend",
                    "python",
                    "manage.py",
                    "migrate",
                )

    def test_manage_command_with_service_and_multiple_args(self):
        """test manage avec service custom et plusieurs arguments"""
        with patch("n7.commands.docker.container.py_manage_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.container.py_manage_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(
                    py_manage_command,
                    ["--service", "backend", "createsuperuser", "--username", "admin"],
                )

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
                    "backend",
                    "python",
                    "manage.py",
                    "createsuperuser",
                    "--username",
                    "admin",
                )
