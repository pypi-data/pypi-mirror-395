from unittest.mock import patch

from typer.testing import CliRunner

from n7.commands.docker.container.connect_postgres_command import connect_postgres_command

runner = CliRunner()


class TestConnectPostgresCommand:
    """Test pour la commande qui permet de se connecter a la base de donnees PostgreSQL"""

    def test_connect_postgres_command_default(self):
        """Test connexion par defaut au service 'db'"""
        with patch(
            "n7.commands.docker.container.connect_postgres_command.subprocess.run"
        ) as mock_run:
            with patch(
                "n7.commands.docker.container.connect_postgres_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": None,
                }

                result = runner.invoke(connect_postgres_command, [])

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
                    "db",
                    "psql",
                )

    def test_connect_postgres_command_with_service(self):
        """Test connexion avec un service specifique"""
        with patch(
            "n7.commands.docker.container.connect_postgres_command.subprocess.run"
        ) as mock_run:
            with patch(
                "n7.commands.docker.container.connect_postgres_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": None,
                }

                result = runner.invoke(connect_postgres_command, ["--service", "postgres"])

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
                    "postgres",
                    "psql",
                )

    def test_connect_postgres_command_with_user(self):
        """Test connexion avec un utilisateur specifique"""
        with patch(
            "n7.commands.docker.container.connect_postgres_command.subprocess.run"
        ) as mock_run:
            with patch(
                "n7.commands.docker.container.connect_postgres_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": None,
                }

                result = runner.invoke(connect_postgres_command, ["--user", "admin"])

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
                    "db",
                    "psql",
                    "-U",
                    "admin",
                )

    def test_connect_postgres_command_with_database(self):
        """Test connexion avec une base de donnees specifique"""
        with patch(
            "n7.commands.docker.container.connect_postgres_command.subprocess.run"
        ) as mock_run:
            with patch(
                "n7.commands.docker.container.connect_postgres_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": None,
                }

                result = runner.invoke(connect_postgres_command, ["--database", "myapp"])

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
                    "db",
                    "psql",
                    "-d",
                    "myapp",
                )

    def test_connect_postgres_command_with_all_options(self):
        """Test connexion avec toutes les options"""
        with patch(
            "n7.commands.docker.container.connect_postgres_command.subprocess.run"
        ) as mock_run:
            with patch(
                "n7.commands.docker.container.connect_postgres_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": None,
                }

                result = runner.invoke(
                    connect_postgres_command,
                    ["--service", "postgres", "--user", "admin", "--database", "myapp"],
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
                    "postgres",
                    "psql",
                    "-U",
                    "admin",
                    "-d",
                    "myapp",
                )

    def test_connect_postgres_command_with_short_options(self):
        """Test connexion avec les options courtes"""
        with patch(
            "n7.commands.docker.container.connect_postgres_command.subprocess.run"
        ) as mock_run:
            with patch(
                "n7.commands.docker.container.connect_postgres_command.DockerFileResolver"
            ) as mock_resolver:
                mock_resolver.return_value.resolve.return_value = {
                    "env_file": ".env",
                    "compose_file": "docker-compose.yml",
                    "default_service": None,
                }

                result = runner.invoke(
                    connect_postgres_command, ["-s", "postgres", "-u", "admin", "-d", "myapp"]
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
                    "postgres",
                    "psql",
                    "-U",
                    "admin",
                    "-d",
                    "myapp",
                )
