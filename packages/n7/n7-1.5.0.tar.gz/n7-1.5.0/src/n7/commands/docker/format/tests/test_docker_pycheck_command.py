from unittest.mock import patch

from typer.testing import CliRunner

from n7.commands.docker.format.docker_pycheck_command import docker_pycheck_command

runner = CliRunner()


class TestDockerPycheckCommand:
    """Tests pour la commande docker pycheck"""

    def test_command_without_options(self):
        """n7 dkc pycheck -> pytest, black --check, ruff check, mypy dans container"""
        with patch("n7.commands.docker.format.docker_pycheck_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.format.docker_pycheck_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(docker_pycheck_command, [])

                assert result.exit_code == 0
                assert mock_run.call_count == 4

                # Vérifier les commandes appelées
                calls = mock_run.call_args_list

                # Pytest command
                pytest_cmd = calls[0][0][0]
                assert pytest_cmd[0:6] == (
                    "docker",
                    "compose",
                    "--env-file",
                    ".env",
                    "-f",
                    "docker-compose.yml",
                )
                assert "api" in pytest_cmd
                assert "pytest" in pytest_cmd

                # Black command
                black_cmd = calls[1][0][0]
                assert "black" in black_cmd
                assert "--check" in black_cmd

                # Ruff command
                ruff_cmd = calls[2][0][0]
                assert "ruff" in ruff_cmd
                assert "check" in ruff_cmd

                # Mypy command
                mypy_cmd = calls[3][0][0]
                assert "mypy" in mypy_cmd

    def test_command_with_path(self):
        """n7 dkc pycheck src/"""
        with patch("n7.commands.docker.format.docker_pycheck_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.format.docker_pycheck_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(docker_pycheck_command, ["src/"])

                assert result.exit_code == 0
                assert mock_run.call_count == 4

                calls = mock_run.call_args_list
                pytest_cmd = calls[0][0][0]
                black_cmd = calls[1][0][0]
                ruff_cmd = calls[2][0][0]
                mypy_cmd = calls[3][0][0]

                assert pytest_cmd[-1] == "src/"
                assert black_cmd[-1] == "src/"
                assert ruff_cmd[-1] == "src/"
                assert mypy_cmd[-1] == "src/"

    def test_command_with_fix(self):
        """n7 dkc pycheck --fix -> pytest, black (format), ruff check --fix, mypy"""
        with patch("n7.commands.docker.format.docker_pycheck_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.format.docker_pycheck_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(docker_pycheck_command, ["--fix"])

                assert result.exit_code == 0
                assert mock_run.call_count == 4

                calls = mock_run.call_args_list
                pytest_cmd = calls[0][0][0]
                black_cmd = calls[1][0][0]
                ruff_cmd = calls[2][0][0]
                mypy_cmd = calls[3][0][0]

                # Pytest reste inchangé
                assert "pytest" in pytest_cmd

                # Black sans --check (mode format)
                assert "black" in black_cmd
                assert "--check" not in black_cmd

                # Ruff avec --fix
                assert "ruff" in ruff_cmd
                assert "--fix" in ruff_cmd

                # Mypy reste inchangé
                assert "mypy" in mypy_cmd

    def test_command_with_fix_and_path(self):
        """n7 dkc pycheck --fix src/"""
        with patch("n7.commands.docker.format.docker_pycheck_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.format.docker_pycheck_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(docker_pycheck_command, ["--fix", "src/"])

                assert result.exit_code == 0
                assert mock_run.call_count == 4

                calls = mock_run.call_args_list
                pytest_cmd = calls[0][0][0]
                black_cmd = calls[1][0][0]
                ruff_cmd = calls[2][0][0]
                mypy_cmd = calls[3][0][0]

                assert "src/" in pytest_cmd
                assert "src/" in black_cmd
                assert "--check" not in black_cmd
                assert "src/" in ruff_cmd
                assert "--fix" in ruff_cmd
                assert "src/" in mypy_cmd

    def test_command_with_custom_service(self):
        """n7 dkc pycheck --service backend"""
        with patch("n7.commands.docker.format.docker_pycheck_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.format.docker_pycheck_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(docker_pycheck_command, ["--service", "backend"])

                assert result.exit_code == 0
                assert mock_run.call_count == 4

                calls = mock_run.call_args_list
                pytest_cmd = calls[0][0][0]
                black_cmd = calls[1][0][0]
                ruff_cmd = calls[2][0][0]
                mypy_cmd = calls[3][0][0]

                assert "backend" in pytest_cmd
                assert "backend" in black_cmd
                assert "backend" in ruff_cmd
                assert "backend" in mypy_cmd

    def test_commands_executed_sequentially(self):
        """Vérifie que les commandes sont exécutées dans l'ordre: pytest, black, ruff, mypy"""
        with patch("n7.commands.docker.format.docker_pycheck_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.format.docker_pycheck_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                runner.invoke(docker_pycheck_command, [])

                calls = mock_run.call_args_list
                assert len(calls) == 4

                # Vérifier l'ordre d'exécution via les commandes
                assert "pytest" in calls[0][0][0]
                assert "black" in calls[1][0][0]
                assert "ruff" in calls[2][0][0]
                assert "mypy" in calls[3][0][0]

    def test_command_with_verbose(self):
        """n7 dkc pycheck -v -> pytest -v"""
        with patch("n7.commands.docker.format.docker_pycheck_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.format.docker_pycheck_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(docker_pycheck_command, ["-v"])

                assert result.exit_code == 0
                calls = mock_run.call_args_list
                pytest_cmd = calls[0][0][0]
                assert "-v" in pytest_cmd

    def test_command_with_stop_first(self):
        """n7 dkc pycheck -x -> pytest -x"""
        with patch("n7.commands.docker.format.docker_pycheck_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.format.docker_pycheck_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(docker_pycheck_command, ["-x"])

                assert result.exit_code == 0
                calls = mock_run.call_args_list
                pytest_cmd = calls[0][0][0]
                assert "-x" in pytest_cmd

    def test_command_with_filter_tests(self):
        """n7 dkc pycheck -k test_name -> pytest -k test_name"""
        with patch("n7.commands.docker.format.docker_pycheck_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.format.docker_pycheck_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(docker_pycheck_command, ["-k", "test_name"])

                assert result.exit_code == 0
                calls = mock_run.call_args_list
                pytest_cmd = calls[0][0][0]
                assert "-k" in pytest_cmd
                assert "test_name" in pytest_cmd

    def test_command_with_all_pytest_options(self):
        """n7 dkc pycheck -v -x -k test_name src/"""
        with patch("n7.commands.docker.format.docker_pycheck_command.subprocess.run") as mock_run:
            with patch(
                "n7.commands.docker.format.docker_pycheck_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": "api",
                }

                result = runner.invoke(
                    docker_pycheck_command, ["-v", "-x", "-k", "test_name", "src/"]
                )

                assert result.exit_code == 0
                calls = mock_run.call_args_list
                pytest_cmd = calls[0][0][0]
                assert "-v" in pytest_cmd
                assert "-x" in pytest_cmd
                assert "-k" in pytest_cmd
                assert "test_name" in pytest_cmd
                assert "src/" in pytest_cmd
