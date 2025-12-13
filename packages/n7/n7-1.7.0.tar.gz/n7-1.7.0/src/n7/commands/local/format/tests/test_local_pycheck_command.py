from unittest.mock import patch

from typer.testing import CliRunner

from n7.commands.local.format.local_pycheck_command import local_pycheck_command

runner = CliRunner()


class TestLocalPycheckCommand:
    """Tests pour la commande pycheck local"""

    def test_command_without_options(self):
        """command n7 pycheck -> pytest, black --check, ruff check, mypy"""
        with patch("n7.commands.local.format.local_pycheck_command.subprocess.run") as mock_run:
            result = runner.invoke(local_pycheck_command, [])

            assert result.exit_code == 0
            assert mock_run.call_count == 4

            # Vérifier les commandes appelées
            calls = mock_run.call_args_list
            pytest_cmd = calls[0][0][0]
            black_cmd = calls[1][0][0]
            ruff_cmd = calls[2][0][0]
            mypy_cmd = calls[3][0][0]

            assert pytest_cmd == ("pytest",)
            assert black_cmd == ("black", "--check", ".")
            assert ruff_cmd == ("ruff", "check", ".")
            assert mypy_cmd == ("mypy", ".")

    def test_command_with_path(self):
        """command n7 pycheck src/"""
        with patch("n7.commands.local.format.local_pycheck_command.subprocess.run") as mock_run:
            result = runner.invoke(local_pycheck_command, ["src/"])

            assert result.exit_code == 0
            assert mock_run.call_count == 4

            calls = mock_run.call_args_list
            pytest_cmd = calls[0][0][0]
            black_cmd = calls[1][0][0]
            ruff_cmd = calls[2][0][0]
            mypy_cmd = calls[3][0][0]

            assert pytest_cmd == ("pytest", "src/")
            assert black_cmd == ("black", "--check", "src/")
            assert ruff_cmd == ("ruff", "check", "src/")
            assert mypy_cmd == ("mypy", "src/")

    def test_command_with_fix(self):
        """command n7 pycheck --fix -> pytest, black (format), ruff check --fix, mypy"""
        with patch("n7.commands.local.format.local_pycheck_command.subprocess.run") as mock_run:
            result = runner.invoke(local_pycheck_command, ["--fix"])

            assert result.exit_code == 0
            assert mock_run.call_count == 4

            calls = mock_run.call_args_list
            pytest_cmd = calls[0][0][0]
            black_cmd = calls[1][0][0]
            ruff_cmd = calls[2][0][0]
            mypy_cmd = calls[3][0][0]

            # Pytest reste inchangé
            assert pytest_cmd == ("pytest",)
            # Black sans --check (mode format)
            assert black_cmd == ("black", ".")
            # Ruff avec --fix
            assert ruff_cmd == ("ruff", "check", "--fix", ".")
            # Mypy reste inchangé
            assert mypy_cmd == ("mypy", ".")

    def test_command_with_fix_and_path(self):
        """command n7 pycheck --fix src/"""
        with patch("n7.commands.local.format.local_pycheck_command.subprocess.run") as mock_run:
            result = runner.invoke(local_pycheck_command, ["--fix", "src/"])

            assert result.exit_code == 0
            assert mock_run.call_count == 4

            calls = mock_run.call_args_list
            pytest_cmd = calls[0][0][0]
            black_cmd = calls[1][0][0]
            ruff_cmd = calls[2][0][0]
            mypy_cmd = calls[3][0][0]

            assert pytest_cmd == ("pytest", "src/")
            assert black_cmd == ("black", "src/")
            assert ruff_cmd == ("ruff", "check", "--fix", "src/")
            assert mypy_cmd == ("mypy", "src/")

    def test_commands_executed_sequentially(self):
        """Vérifie que les commandes sont exécutées dans l'ordre: pytest, black, ruff, mypy"""
        with patch("n7.commands.local.format.local_pycheck_command.subprocess.run") as mock_run:
            runner.invoke(local_pycheck_command, [])

            calls = mock_run.call_args_list
            assert len(calls) == 4
            assert calls[0][0][0][0] == "pytest"
            assert calls[1][0][0][0] == "black"
            assert calls[2][0][0][0] == "ruff"
            assert calls[3][0][0][0] == "mypy"

    def test_command_with_verbose(self):
        """command n7 pycheck -v -> pytest -v"""
        with patch("n7.commands.local.format.local_pycheck_command.subprocess.run") as mock_run:
            result = runner.invoke(local_pycheck_command, ["-v"])

            assert result.exit_code == 0
            calls = mock_run.call_args_list
            pytest_cmd = calls[0][0][0]
            assert pytest_cmd == ("pytest", "-v")

    def test_command_with_stop_first(self):
        """command n7 pycheck -x -> pytest -x"""
        with patch("n7.commands.local.format.local_pycheck_command.subprocess.run") as mock_run:
            result = runner.invoke(local_pycheck_command, ["-x"])

            assert result.exit_code == 0
            calls = mock_run.call_args_list
            pytest_cmd = calls[0][0][0]
            assert pytest_cmd == ("pytest", "-x")

    def test_command_with_filter_tests(self):
        """command n7 pycheck -k test_name -> pytest -k test_name"""
        with patch("n7.commands.local.format.local_pycheck_command.subprocess.run") as mock_run:
            result = runner.invoke(local_pycheck_command, ["-k", "test_name"])

            assert result.exit_code == 0
            calls = mock_run.call_args_list
            pytest_cmd = calls[0][0][0]
            assert pytest_cmd == ("pytest", "-k", "test_name")

    def test_command_with_all_pytest_options(self):
        """command n7 pycheck -v -x -k test_name src/"""
        with patch("n7.commands.local.format.local_pycheck_command.subprocess.run") as mock_run:
            result = runner.invoke(local_pycheck_command, ["-v", "-x", "-k", "test_name", "src/"])

            assert result.exit_code == 0
            calls = mock_run.call_args_list
            pytest_cmd = calls[0][0][0]
            assert "-v" in pytest_cmd
            assert "-x" in pytest_cmd
            assert "-k" in pytest_cmd
            assert "test_name" in pytest_cmd
            assert pytest_cmd[-1] == "src/"
