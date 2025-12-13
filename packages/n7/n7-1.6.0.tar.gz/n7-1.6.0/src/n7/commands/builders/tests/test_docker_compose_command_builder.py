from n7.commands.builders import DockerComposeCommandBuilder


class TestDockerComposeCommandBuilder:
    def setup_method(self):
        self.builder = DockerComposeCommandBuilder(
            env_file=".env",
            compose_file="docker-compose.yml",
        )

    def test_instance(self):
        """test docker compose instance"""
        assert self.builder is not None

    def test_build_exec_simple(self):
        """command docker compose exec service cmd"""
        result = self.builder.build_exec(
            service="api",
            cmd=("bash",),
        )
        assert result == (
            "docker",
            "compose",
            "--env-file",
            ".env",
            "-f",
            "docker-compose.yml",
            "exec",
            "-T",
            "api",
            "bash",
        )

    def test_build_exec_with_command_options(self):
        """command docker compose exec with options"""
        result = self.builder.build_exec(
            service="api",
            cmd=("pytest", "-v", "-n", "auto"),
        )
        assert result == (
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
            "-v",
            "-n",
            "auto",
        )

    def test_build_exec_with_tty(self):
        """command docker compose exec without TTY"""
        result = self.builder.build_exec(
            service="api",
            cmd=("pytest",),
            disable_tty=False,
        )
        assert result == (
            "docker",
            "compose",
            "--env-file",
            ".env",
            "-f",
            "docker-compose.yml",
            "exec",
            "api",
            "pytest",
        )

    def test_build_up(self):
        """command docker compose up -d"""
        result = self.builder.build_up()
        assert result == (
            "docker",
            "compose",
            "--env-file",
            ".env",
            "-f",
            "docker-compose.yml",
            "up",
            "-d",
        )

    def test_build_up_without_detach(self):
        """command docker compose up sans -d"""
        result = self.builder.build_up(detach=False)
        assert result == (
            "docker",
            "compose",
            "--env-file",
            ".env",
            "-f",
            "docker-compose.yml",
            "up",
        )

    def test_build_down(self):
        """command docker compose down"""
        result = self.builder.build_down()
        assert result == (
            "docker",
            "compose",
            "--env-file",
            ".env",
            "-f",
            "docker-compose.yml",
            "down",
        )

    def test_build_down_with_volumes(self):
        """command docker compose down -v"""
        result = self.builder.build_down(volumes=True)
        assert result == (
            "docker",
            "compose",
            "--env-file",
            ".env",
            "-f",
            "docker-compose.yml",
            "down",
            "-v",
        )

    def test_build_logs(self):
        """command docker compose logs service"""
        result = self.builder.build_logs(service="api")
        assert result == (
            "docker",
            "compose",
            "--env-file",
            ".env",
            "-f",
            "docker-compose.yml",
            "logs",
            "api",
        )

    def test_build_logs_with_follow(self):
        """command docker compose logs -f service"""
        result = self.builder.build_logs(service="api", follow=True)
        assert result == (
            "docker",
            "compose",
            "--env-file",
            ".env",
            "-f",
            "docker-compose.yml",
            "logs",
            "-f",
            "api",
        )

    def test_custom_files(self):
        """Builder avec fichiers custom"""
        builder = DockerComposeCommandBuilder(
            env_file=".env.prod",
            compose_file="docker-compose.prod.yml",
        )
        result = builder.build_up()
        assert result == (
            "docker",
            "compose",
            "--env-file",
            ".env.prod",
            "-f",
            "docker-compose.prod.yml",
            "up",
            "-d",
        )
