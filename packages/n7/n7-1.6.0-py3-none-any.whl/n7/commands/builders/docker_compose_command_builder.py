class DockerComposeCommandBuilder:
    def __init__(self, env_file: str, compose_file: str):
        self.env_file = env_file
        self.compose_file = compose_file

    def _base(self) -> tuple[str, ...]:
        """Commande de base docker compose"""
        return (
            "docker",
            "compose",
            "--env-file",
            self.env_file,
            "-f",
            self.compose_file,
        )

    def build_exec(
        self,
        service: str,
        cmd: tuple[str, ...],
        disable_tty: bool = True,
    ) -> tuple[str, ...]:
        """Construit docker compose exec"""
        base = self._base()
        if disable_tty:
            return *base, "exec", "-T", service, *cmd
        return *base, "exec", service, *cmd

    def build_up(self, detach: bool = True, build: bool = False) -> tuple[str, ...]:
        """Construit docker compose up"""
        base = self._base()
        if detach and build:
            return *base, "up", "--build", "-d"
        if detach:
            return *base, "up", "-d"
        if build:
            return *base, "up", "--build"
        return *base, "up"

    def build_down(self, volumes: bool = False) -> tuple[str, ...]:
        """Construit docker compose down"""
        base = self._base()
        if volumes:
            return *base, "down", "-v"
        return *base, "down"

    def build_logs(self, service: str, follow: bool = False) -> tuple[str, ...]:
        """Construit docker compose logs"""
        base = self._base()
        if follow:
            return *base, "logs", "-f", service
        return *base, "logs", service
