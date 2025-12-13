from unittest.mock import patch

from typer.testing import CliRunner

from n7.commands.docker.format.docker_ruff_command import docker_ruff_command

runner = CliRunner()


class TestDockerRuffCommand:
    """Tests pour la commande docker ruff"""

    def test_command_without_options(self):
        """n7 dkc pyrf -> ruff check simple dans container"""
        with patch("n7.commands.docker.format.docker_ruff_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.format.docker_ruff_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(docker_ruff_command, [])

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
                    "ruff",
                    "check",
                )

    def test_command_with_path(self):
        """n7 dkc pyrf src/"""
        with patch("n7.commands.docker.format.docker_ruff_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.format.docker_ruff_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(docker_ruff_command, ["src/"])

                assert result.exit_code == 0
                cmd = mock_run.call_args[0][0]
                assert cmd[-1] == "src/"

    def test_command_with_fix(self):
        """n7 dkc pyrf --fix"""
        with patch("n7.commands.docker.format.docker_ruff_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.format.docker_ruff_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(docker_ruff_command, ["--fix"])

                assert result.exit_code == 0
                cmd = mock_run.call_args[0][0]
                assert "--fix" in cmd

    def test_command_with_diff(self):
        """n7 dkc pyrf --diff"""
        with patch("n7.commands.docker.format.docker_ruff_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.format.docker_ruff_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(docker_ruff_command, ["--diff"])

                assert result.exit_code == 0
                cmd = mock_run.call_args[0][0]
                assert "--diff" in cmd

    def test_command_with_select(self):
        """n7 dkc pyrf --select E,F"""
        with patch("n7.commands.docker.format.docker_ruff_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.format.docker_ruff_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(docker_ruff_command, ["--select", "E,F"])

                assert result.exit_code == 0
                cmd = mock_run.call_args[0][0]
                assert "--select" in cmd
                assert "E,F" in cmd

    def test_command_with_ignore(self):
        """n7 dkc pyrf --ignore E501"""
        with patch("n7.commands.docker.format.docker_ruff_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.format.docker_ruff_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(docker_ruff_command, ["--ignore", "E501"])

                assert result.exit_code == 0
                cmd = mock_run.call_args[0][0]
                assert "--ignore" in cmd
                assert "E501" in cmd

    def test_command_with_verbose(self):
        """n7 dkc pyrf -v"""
        with patch("n7.commands.docker.format.docker_ruff_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.format.docker_ruff_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(docker_ruff_command, ["-v"])

                assert result.exit_code == 0
                cmd = mock_run.call_args[0][0]
                assert "--verbose" in cmd

    def test_command_with_custom_service(self):
        """n7 dkc pyrf --service backend"""
        with patch("n7.commands.docker.format.docker_ruff_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.format.docker_ruff_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(docker_ruff_command, ["--service", "backend"])

                assert result.exit_code == 0
                cmd = mock_run.call_args[0][0]
                assert "backend" in cmd

    def test_command_combined_options(self):
        """n7 dkc pyrf src/ --fix --diff -v"""
        with patch("n7.commands.docker.format.docker_ruff_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.format.docker_ruff_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(
                    docker_ruff_command,
                    [
                        "--fix",
                        "--diff",
                        "-v",
                        "src/",
                    ],
                )

                assert result.exit_code == 0
                cmd = mock_run.call_args[0][0]
                assert "--fix" in cmd
                assert "--diff" in cmd
                assert "--verbose" in cmd
                assert cmd[-1] == "src/"

    def test_command_with_rules_options(self):
        """n7 dkc pyrf with rules options"""
        with patch("n7.commands.docker.format.docker_ruff_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.format.docker_ruff_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(
                    docker_ruff_command,
                    [
                        "--select",
                        "E,F",
                        "--ignore",
                        "E501",
                        "--extend-select",
                        "B",
                    ],
                )

                assert result.exit_code == 0
                cmd = mock_run.call_args[0][0]
                assert "--select" in cmd
                assert "E,F" in cmd
                assert "--ignore" in cmd
                assert "E501" in cmd
                assert "--extend-select" in cmd
                assert "B" in cmd
