from unittest.mock import patch

from typer.testing import CliRunner

from n7.commands.docker.format.docker_black_command import docker_black_command

runner = CliRunner()


class TestDockerBlackCommand:
    """Tests pour la commande docker black"""

    def test_command_without_options(self):
        """n7 dkc pybl -> black simple dans container"""
        with patch("n7.commands.docker.format.docker_black_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.format.docker_black_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(docker_black_command, [])

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
                    "black",
                )

    def test_command_with_path(self):
        """n7 dkc pybl src/"""
        with patch("n7.commands.docker.format.docker_black_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.format.docker_black_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(docker_black_command, ["src/"])

                assert result.exit_code == 0
                cmd = mock_run.call_args[0][0]
                assert cmd[-1] == "src/"

    def test_command_with_check(self):
        """n7 dkc pybl --check"""
        with patch("n7.commands.docker.format.docker_black_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.format.docker_black_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(docker_black_command, ["--check"])

                assert result.exit_code == 0
                cmd = mock_run.call_args[0][0]
                assert "--check" in cmd

    def test_command_with_diff(self):
        """n7 dkc pybl --diff"""
        with patch("n7.commands.docker.format.docker_black_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.format.docker_black_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(docker_black_command, ["--diff"])

                assert result.exit_code == 0
                cmd = mock_run.call_args[0][0]
                assert "--diff" in cmd

    def test_command_with_line_length(self):
        """n7 dkc pybl --line-length 100"""
        with patch("n7.commands.docker.format.docker_black_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.format.docker_black_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(docker_black_command, ["--line-length", "100"])

                assert result.exit_code == 0
                cmd = mock_run.call_args[0][0]
                assert "--line-length" in cmd
                assert "100" in cmd

    def test_command_with_target_version(self):
        """n7 dkc pybl --target-version py313"""
        with patch("n7.commands.docker.format.docker_black_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.format.docker_black_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(docker_black_command, ["--target-version", "py313"])

                assert result.exit_code == 0
                cmd = mock_run.call_args[0][0]
                assert "--target-version" in cmd
                assert "py313" in cmd

    def test_command_with_verbose(self):
        """n7 dkc pybl -v"""
        with patch("n7.commands.docker.format.docker_black_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.format.docker_black_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(docker_black_command, ["-v"])

                assert result.exit_code == 0
                cmd = mock_run.call_args[0][0]
                assert "--verbose" in cmd

    def test_command_with_custom_service(self):
        """n7 dkc pybl --service backend"""
        with patch("n7.commands.docker.format.docker_black_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.format.docker_black_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(docker_black_command, ["--service", "backend"])

                assert result.exit_code == 0
                cmd = mock_run.call_args[0][0]
                assert "backend" in cmd

    def test_command_combined_options(self):
        """n7 dkc pybl src/ --check --diff -v"""
        with patch("n7.commands.docker.format.docker_black_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.format.docker_black_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(
                    docker_black_command,
                    [
                        "--check",
                        "--diff",
                        "-v",
                        "src/",
                    ],
                )

                assert result.exit_code == 0
                cmd = mock_run.call_args[0][0]
                assert "--check" in cmd
                assert "--diff" in cmd
                assert "--verbose" in cmd
                assert cmd[-1] == "src/"

    def test_command_with_formatting_options(self):
        """n7 dkc pybl with formatting options"""
        with patch("n7.commands.docker.format.docker_black_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.format.docker_black_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(
                    docker_black_command,
                    [
                        "--line-length",
                        "100",
                        "--target-version",
                        "py313",
                        "--skip-string-normalization",
                    ],
                )

                assert result.exit_code == 0
                cmd = mock_run.call_args[0][0]
                assert "--line-length" in cmd
                assert "100" in cmd
                assert "--target-version" in cmd
                assert "py313" in cmd
                assert "--skip-string-normalization" in cmd
