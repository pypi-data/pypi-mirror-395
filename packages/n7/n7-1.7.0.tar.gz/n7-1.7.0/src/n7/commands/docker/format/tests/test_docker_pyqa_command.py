from unittest.mock import patch

from typer.testing import CliRunner

from n7.commands.docker.format.docker_pyqa_command import docker_pyqa_command

runner = CliRunner()


class TestDockerPyqaCommand:
    """Tests pour la commande docker pyqa"""

    def test_command_without_options(self):
        """n7 dkc pyqa -> black --check, ruff check, mypy dans container"""
        with patch("n7.commands.docker.format.docker_pyqa_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.format.docker_pyqa_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(docker_pyqa_command, [])

                assert result.exit_code == 0
                assert mock_run.call_count == 3

                # Vérifier les commandes appelées
                calls = mock_run.call_args_list

                # Black command
                black_cmd = calls[0][0][0]
                assert black_cmd[0:6] == (
                    "docker",
                    "compose",
                    "--env-file",
                    ".env",
                    "-f",
                    "docker-compose.yml",
                )
                assert "api" in black_cmd
                assert "black" in black_cmd
                assert "--check" in black_cmd

                # Ruff command
                ruff_cmd = calls[1][0][0]
                assert "ruff" in ruff_cmd
                assert "check" in ruff_cmd

                # Mypy command
                mypy_cmd = calls[2][0][0]
                assert "mypy" in mypy_cmd

    def test_command_with_path(self):
        """n7 dkc pyqa src/"""
        with patch("n7.commands.docker.format.docker_pyqa_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.format.docker_pyqa_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(docker_pyqa_command, ["src/"])

                assert result.exit_code == 0
                assert mock_run.call_count == 3

                calls = mock_run.call_args_list
                black_cmd = calls[0][0][0]
                ruff_cmd = calls[1][0][0]
                mypy_cmd = calls[2][0][0]

                assert black_cmd[-1] == "src/"
                assert ruff_cmd[-1] == "src/"
                assert mypy_cmd[-1] == "src/"

    def test_command_with_fix(self):
        """n7 dkc pyqa --fix -> black (format), ruff check --fix, mypy"""
        with patch("n7.commands.docker.format.docker_pyqa_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.format.docker_pyqa_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(docker_pyqa_command, ["--fix"])

                assert result.exit_code == 0
                assert mock_run.call_count == 3

                calls = mock_run.call_args_list
                black_cmd = calls[0][0][0]
                ruff_cmd = calls[1][0][0]
                mypy_cmd = calls[2][0][0]

                # Black sans --check (mode format)
                assert "black" in black_cmd
                assert "--check" not in black_cmd

                # Ruff avec --fix
                assert "ruff" in ruff_cmd
                assert "--fix" in ruff_cmd

                # Mypy reste inchangé
                assert "mypy" in mypy_cmd

    def test_command_with_fix_and_path(self):
        """n7 dkc pyqa --fix src/"""
        with patch("n7.commands.docker.format.docker_pyqa_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.format.docker_pyqa_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(docker_pyqa_command, ["--fix", "src/"])

                assert result.exit_code == 0
                assert mock_run.call_count == 3

                calls = mock_run.call_args_list
                black_cmd = calls[0][0][0]
                ruff_cmd = calls[1][0][0]
                mypy_cmd = calls[2][0][0]

                assert "src/" in black_cmd
                assert "--check" not in black_cmd
                assert "src/" in ruff_cmd
                assert "--fix" in ruff_cmd
                assert "src/" in mypy_cmd

    def test_command_with_custom_service(self):
        """n7 dkc pyqa --service backend"""
        with patch("n7.commands.docker.format.docker_pyqa_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.format.docker_pyqa_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(docker_pyqa_command, ["--service", "backend"])

                assert result.exit_code == 0
                assert mock_run.call_count == 3

                calls = mock_run.call_args_list
                black_cmd = calls[0][0][0]
                ruff_cmd = calls[1][0][0]
                mypy_cmd = calls[2][0][0]

                assert "backend" in black_cmd
                assert "backend" in ruff_cmd
                assert "backend" in mypy_cmd

    def test_commands_executed_sequentially(self):
        """Vérifie que les commandes sont exécutées dans l'ordre: black, ruff, mypy"""
        with patch("n7.commands.docker.format.docker_pyqa_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.format.docker_pyqa_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                runner.invoke(docker_pyqa_command, [])

                calls = mock_run.call_args_list
                assert len(calls) == 3

                # Vérifier l'ordre d'exécution via les commandes
                assert "black" in calls[0][0][0]
                assert "ruff" in calls[1][0][0]
                assert "mypy" in calls[2][0][0]
