# commands/resolver/docker_file_resolver.py

from pathlib import Path

from n7.commands.resolver.config_n7_resolver import ConfigN7Resolver

# Extensions
EXTENSIONS = ("yaml", "yml")

# Environnements
ENVS = (
    "",
    "dev",
    "development",
    "prod",
    "production",
    "staging",
    "preprod",
    "test",
    "local",
    "api",
)

# Préfixes dossiers pour compose
COMPOSE_FOLDERS = (
    "",
    "docker/",
)

# Préfixes dossiers pour .env
ENV_FOLDERS = (
    "",
    "api/",
    "app/",
    "front/",
    "back/",
    "server/",
    "frontend/",
    "backend/",
)


def _generate_compose_files() -> tuple[str, ...]:
    """Génère la liste des fichiers compose à chercher"""
    files = []
    for folder in COMPOSE_FOLDERS:
        for ext in EXTENSIONS:
            for env in ENVS:
                suffix = f".{env}" if env else ""
                files.append(f"{folder}docker-compose{suffix}.{ext}")
                files.append(f"{folder}compose{suffix}.{ext}")
    return tuple(files)


def _generate_env_files() -> tuple[str, ...]:
    """Génère la liste des fichiers env à chercher"""
    files = []
    for folder in ENV_FOLDERS:
        for env in ENVS:
            suffix = f".{env}" if env else ""
            files.append(f"{folder}.env{suffix}")
    return tuple(files)


COMPOSE_FILES = _generate_compose_files()
ENV_FILES = _generate_env_files()


class DockerFileResolver:
    """Résout les fichiers docker (.env et compose)"""

    def __init__(self, base_path: Path | None = None):
        self.base_path = base_path or Path.cwd()
        self.config_resolver = ConfigN7Resolver(base_path=self.base_path)

    def find_compose_file(self) -> str | None:
        """Trouve le premier fichier compose existant"""
        for file in COMPOSE_FILES:
            if (self.base_path / file).exists():
                return file
        return None

    def find_env_file(self) -> str | None:
        """Trouve le premier fichier env existant"""
        for file in ENV_FILES:
            if (self.base_path / file).exists():
                return file
        return None

    def resolve(self) -> dict:
        """Résout les fichiers docker avec priorité config > auto"""
        config_env = self.config_resolver.get_path_env_file()
        config_compose = self.config_resolver.get_path_compose_file()
        default_service = self.config_resolver.get_default_service()

        return {
            "env_file": config_env or self.find_env_file(),
            "compose_file": config_compose or self.find_compose_file(),
            "default_service": default_service,
        }
