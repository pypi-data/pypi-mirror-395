from pathlib import Path
from typing import Any

import yaml


class ConfigN7Resolver:
    def __init__(self, base_path: Path | None = None):
        self.base_path = base_path or Path.cwd()
        self.config_file = "n7.yaml"

    def load(self) -> dict[Any, Any] | None:
        """Charge le fichier n7.yaml"""
        config_path = self.base_path / self.config_file

        if not config_path.exists():
            return None

        with open(config_path) as f:
            result: Any = yaml.safe_load(f)
            return result if isinstance(result, dict) else None

    def get_docker_config(self) -> dict[Any, Any] | None:
        """Retourne la section docker de la config"""
        config = self.load()

        if config is None:
            return None

        result = config.get("docker")
        return result if isinstance(result, dict) else None

    def get_path_env_file(self) -> str | None:
        """Retourne path_env_file de la config docker"""
        docker_config = self.get_docker_config()

        if docker_config is None:
            return None

        return docker_config.get("path_env_file")

    def get_path_compose_file(self) -> str | None:
        """Retourne path_compose_file de la config docker"""
        docker_config = self.get_docker_config()

        if docker_config is None:
            return None

        return docker_config.get("path_compose_file")

    def get_default_service(self) -> str | None:
        """Retourne default_service de la config docker"""
        docker_config = self.get_docker_config()

        if docker_config is None:
            return None

        return docker_config.get("default_service")
