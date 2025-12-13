from unittest.mock import patch

from typer.testing import CliRunner

from n7.commands.docker.format.docker_mypy_command import docker_mypy_command

runner = CliRunner()


class TestDockerMypyCommand:
    """Tests pour la commande docker mypy"""

    def test_command_without_options(self):
        """n7 dkc pymy -> mypy simple dans container"""
        with patch("n7.commands.docker.format.docker_mypy_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.format.docker_mypy_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(docker_mypy_command, [])

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
                    "mypy",
                )

    def test_command_with_path(self):
        """n7 dkc pymy src/"""
        with patch("n7.commands.docker.format.docker_mypy_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.format.docker_mypy_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(docker_mypy_command, ["src/"])

                assert result.exit_code == 0
                cmd = mock_run.call_args[0][0]
                assert cmd[-1] == "src/"

    def test_command_with_strict(self):
        """n7 dkc pymy --strict"""
        with patch("n7.commands.docker.format.docker_mypy_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.format.docker_mypy_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(docker_mypy_command, ["--strict"])

                assert result.exit_code == 0
                cmd = mock_run.call_args[0][0]
                assert "--strict" in cmd

    def test_command_with_show_error_codes(self):
        """n7 dkc pymy --show-error-codes"""
        with patch("n7.commands.docker.format.docker_mypy_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.format.docker_mypy_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(docker_mypy_command, ["--show-error-codes"])

                assert result.exit_code == 0
                cmd = mock_run.call_args[0][0]
                assert "--show-error-codes" in cmd

    def test_command_with_python_version(self):
        """n7 dkc pymy --python-version 3.13"""
        with patch("n7.commands.docker.format.docker_mypy_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.format.docker_mypy_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(docker_mypy_command, ["--python-version", "3.13"])

                assert result.exit_code == 0
                cmd = mock_run.call_args[0][0]
                assert "--python-version" in cmd
                assert "3.13" in cmd

    def test_command_with_config_file(self):
        """n7 dkc pymy --config-file pyproject.toml"""
        with patch("n7.commands.docker.format.docker_mypy_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.format.docker_mypy_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(docker_mypy_command, ["--config-file", "pyproject.toml"])

                assert result.exit_code == 0
                cmd = mock_run.call_args[0][0]
                assert "--config-file" in cmd
                assert "pyproject.toml" in cmd

    def test_command_with_verbose(self):
        """n7 dkc pymy -v"""
        with patch("n7.commands.docker.format.docker_mypy_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.format.docker_mypy_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(docker_mypy_command, ["-v"])

                assert result.exit_code == 0
                cmd = mock_run.call_args[0][0]
                assert "--verbose" in cmd

    def test_command_with_custom_service(self):
        """n7 dkc pymy --service backend"""
        with patch("n7.commands.docker.format.docker_mypy_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.format.docker_mypy_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(docker_mypy_command, ["--service", "backend"])

                assert result.exit_code == 0
                cmd = mock_run.call_args[0][0]
                assert "backend" in cmd

    def test_command_combined_options(self):
        """n7 dkc pymy src/ --strict --show-error-codes -v"""
        with patch("n7.commands.docker.format.docker_mypy_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.format.docker_mypy_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(
                    docker_mypy_command,
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
        """n7 dkc pymy with type checking options"""
        with patch("n7.commands.docker.format.docker_mypy_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.format.docker_mypy_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(
                    docker_mypy_command,
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
