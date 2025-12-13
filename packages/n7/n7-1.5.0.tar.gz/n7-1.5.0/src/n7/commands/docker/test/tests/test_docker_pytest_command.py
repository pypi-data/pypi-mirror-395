from unittest.mock import patch

from typer.testing import CliRunner

from n7.commands.docker.test.docker_pytest_command import docker_pytest_command

runner = CliRunner()


class TestDockerTestCommand:
    """Tests pour la commande docker test"""

    def test_command_without_options(self):
        """n7 dkc t -> pytest simple dans container"""
        with patch("n7.commands.docker.test.docker_pytest_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.test.docker_pytest_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(docker_pytest_command, [])

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
                    "-T",
                    "api",
                    "pytest",
                )

    def test_command_with_path(self):
        """n7 dkc t users/tests/"""
        with patch("n7.commands.docker.test.docker_pytest_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.test.docker_pytest_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(docker_pytest_command, ["users/tests/"])

                assert result.exit_code == 0
                cmd = mock_run.call_args[0][0]
                assert cmd[-1] == "users/tests/"

    def test_command_with_verbose(self):
        """n7 dkc t -v"""
        with patch("n7.commands.docker.test.docker_pytest_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.test.docker_pytest_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(docker_pytest_command, ["-v"])

                assert result.exit_code == 0
                cmd = mock_run.call_args[0][0]
                assert "-v" in cmd

    def test_command_with_workers(self):
        """n7 dkc t -n auto"""
        with patch("n7.commands.docker.test.docker_pytest_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.test.docker_pytest_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(docker_pytest_command, ["-n", "auto"])

                assert result.exit_code == 0
                cmd = mock_run.call_args[0][0]
                assert "-n" in cmd
                assert "auto" in cmd

    def test_command_with_coverage(self):
        """n7 dkc t --cov users"""
        with patch("n7.commands.docker.test.docker_pytest_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.test.docker_pytest_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(docker_pytest_command, ["--cov", "users"])

                assert result.exit_code == 0
                cmd = mock_run.call_args[0][0]
                assert "--cov=users" in cmd

    def test_command_with_last_failed(self):
        """n7 dkc t --lf"""
        with patch("n7.commands.docker.test.docker_pytest_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.test.docker_pytest_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(docker_pytest_command, ["--lf"])

                assert result.exit_code == 0
                cmd = mock_run.call_args[0][0]
                assert "--lf" in cmd

    def test_command_with_custom_service(self):
        """n7 dkc t --service worker"""
        with patch("n7.commands.docker.test.docker_pytest_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.test.docker_pytest_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(docker_pytest_command, ["--service", "worker"])

                assert result.exit_code == 0
                cmd = mock_run.call_args[0][0]
                assert "worker" in cmd

    def test_command_combined_options(self):
        """n7 dkc t users/tests/ -v -n 4 --cov users"""
        with patch("n7.commands.docker.test.docker_pytest_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.test.docker_pytest_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(
                    docker_pytest_command,
                    [
                        "-v",
                        "-n",
                        "4",
                        "--cov",
                        "users",
                        "users/tests/",  # path à la fin
                    ],
                )

                assert result.exit_code == 0
                cmd = mock_run.call_args[0][0]
                assert "-v" in cmd
                assert "-n" in cmd
                assert "4" in cmd
                assert "--cov=users" in cmd
                assert cmd[-1] == "users/tests/"
