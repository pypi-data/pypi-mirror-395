from unittest.mock import patch

from typer.testing import CliRunner

from n7.commands.local.format.local_pyqa_command import local_pyqa_command

runner = CliRunner()


class TestLocalPyqaCommand:
    """Tests pour la commande pyqa local"""

    def test_command_without_options(self):
        """command n7 pyqa -> black --check, ruff check, mypy"""
        with patch("n7.commands.local.format.local_pyqa_command.subprocess.run") as mock_run:
            result = runner.invoke(local_pyqa_command, [])

            assert result.exit_code == 0
            assert mock_run.call_count == 3

            # Vérifier les commandes appelées
            calls = mock_run.call_args_list
            black_cmd = calls[0][0][0]
            ruff_cmd = calls[1][0][0]
            mypy_cmd = calls[2][0][0]

            assert black_cmd == ("black", "--check", ".")
            assert ruff_cmd == ("ruff", "check", ".")
            assert mypy_cmd == ("mypy", ".")

    def test_command_with_path(self):
        """command n7 pyqa src/"""
        with patch("n7.commands.local.format.local_pyqa_command.subprocess.run") as mock_run:
            result = runner.invoke(local_pyqa_command, ["src/"])

            assert result.exit_code == 0
            assert mock_run.call_count == 3

            calls = mock_run.call_args_list
            black_cmd = calls[0][0][0]
            ruff_cmd = calls[1][0][0]
            mypy_cmd = calls[2][0][0]

            assert black_cmd == ("black", "--check", "src/")
            assert ruff_cmd == ("ruff", "check", "src/")
            assert mypy_cmd == ("mypy", "src/")

    def test_command_with_fix(self):
        """command n7 pyqa --fix -> black (format), ruff check --fix, mypy"""
        with patch("n7.commands.local.format.local_pyqa_command.subprocess.run") as mock_run:
            result = runner.invoke(local_pyqa_command, ["--fix"])

            assert result.exit_code == 0
            assert mock_run.call_count == 3

            calls = mock_run.call_args_list
            black_cmd = calls[0][0][0]
            ruff_cmd = calls[1][0][0]
            mypy_cmd = calls[2][0][0]

            # Black sans --check (mode format)
            assert black_cmd == ("black", ".")
            # Ruff avec --fix
            assert ruff_cmd == ("ruff", "check", "--fix", ".")
            # Mypy reste inchangé
            assert mypy_cmd == ("mypy", ".")

    def test_command_with_fix_and_path(self):
        """command n7 pyqa --fix src/"""
        with patch("n7.commands.local.format.local_pyqa_command.subprocess.run") as mock_run:
            result = runner.invoke(local_pyqa_command, ["--fix", "src/"])

            assert result.exit_code == 0
            assert mock_run.call_count == 3

            calls = mock_run.call_args_list
            black_cmd = calls[0][0][0]
            ruff_cmd = calls[1][0][0]
            mypy_cmd = calls[2][0][0]

            assert black_cmd == ("black", "src/")
            assert ruff_cmd == ("ruff", "check", "--fix", "src/")
            assert mypy_cmd == ("mypy", "src/")

    def test_commands_executed_sequentially(self):
        """Vérifie que les commandes sont exécutées dans l'ordre: black, ruff, mypy"""
        with patch("n7.commands.local.format.local_pyqa_command.subprocess.run") as mock_run:
            runner.invoke(local_pyqa_command, [])

            calls = mock_run.call_args_list
            assert len(calls) == 3
            assert calls[0][0][0][0] == "black"
            assert calls[1][0][0][0] == "ruff"
            assert calls[2][0][0][0] == "mypy"
