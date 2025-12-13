from n7.commands.resolver import DockerFileResolver


class TestDockerFileResolver:
    """Tests pour DockerFileResolver"""

    def test_find_compose_file_at_root(self, tmp_path):
        """Trouve docker-compose.yml à la racine"""
        (tmp_path / "docker-compose.yml").touch()

        resolver = DockerFileResolver(base_path=tmp_path)
        result = resolver.find_compose_file()

        assert result == "docker-compose.yml"

    def test_find_compose_file_yaml_extension(self, tmp_path):
        """Trouve docker-compose.yaml à la racine"""
        (tmp_path / "docker-compose.yaml").touch()

        resolver = DockerFileResolver(base_path=tmp_path)
        result = resolver.find_compose_file()

        assert result == "docker-compose.yaml"

    def test_find_compose_file_short_name(self, tmp_path):
        """Trouve compose.yml à la racine"""
        (tmp_path / "compose.yml").touch()

        resolver = DockerFileResolver(base_path=tmp_path)
        result = resolver.find_compose_file()

        assert result == "compose.yml"

    def test_find_compose_file_with_env(self, tmp_path):
        """Trouve docker-compose.dev.yml"""
        (tmp_path / "docker-compose.dev.yml").touch()

        resolver = DockerFileResolver(base_path=tmp_path)
        result = resolver.find_compose_file()

        assert result == "docker-compose.dev.yml"

    def test_find_compose_file_in_docker_folder(self, tmp_path):
        """Trouve compose.yml dans docker/"""
        (tmp_path / "docker").mkdir()
        (tmp_path / "docker" / "compose.yml").touch()

        resolver = DockerFileResolver(base_path=tmp_path)
        result = resolver.find_compose_file()

        assert result == "docker/compose.yml"

    def test_find_compose_file_priority_root_over_folder(self, tmp_path):
        """Priorité racine sur docker/"""
        (tmp_path / "docker-compose.yml").touch()
        (tmp_path / "docker").mkdir()
        (tmp_path / "docker" / "compose.yml").touch()

        resolver = DockerFileResolver(base_path=tmp_path)
        result = resolver.find_compose_file()

        assert result == "docker-compose.yml"

    def test_find_compose_file_returns_none_when_not_found(self, tmp_path):
        """Retourne None si aucun fichier trouvé"""
        resolver = DockerFileResolver(base_path=tmp_path)
        result = resolver.find_compose_file()

        assert result is None

    def test_find_env_file_at_root(self, tmp_path):
        """Trouve .env à la racine"""
        (tmp_path / ".env").touch()

        resolver = DockerFileResolver(base_path=tmp_path)
        result = resolver.find_env_file()

        assert result == ".env"

    def test_find_env_file_with_suffix(self, tmp_path):
        """Trouve .env.local"""
        (tmp_path / ".env.local").touch()

        resolver = DockerFileResolver(base_path=tmp_path)
        result = resolver.find_env_file()

        assert result == ".env.local"

    def test_find_env_file_with_suffix_api(self, tmp_path):
        """Trouve .env.local"""
        (tmp_path / ".env.api").touch()

        resolver = DockerFileResolver(base_path=tmp_path)
        result = resolver.find_env_file()

        assert result == ".env.api"

    def test_find_env_file_in_api_folder(self, tmp_path):
        """Trouve .env dans api/"""
        (tmp_path / "api").mkdir()
        (tmp_path / "api" / ".env").touch()

        resolver = DockerFileResolver(base_path=tmp_path)
        result = resolver.find_env_file()

        assert result == "api/.env"

    def test_find_env_file_priority_root_over_folder(self, tmp_path):
        """Priorité racine sur dossiers"""
        (tmp_path / ".env").touch()
        (tmp_path / "api").mkdir()
        (tmp_path / "api" / ".env").touch()

        resolver = DockerFileResolver(base_path=tmp_path)
        result = resolver.find_env_file()

        assert result == ".env"

    def test_find_env_file_returns_none_when_not_found(self, tmp_path):
        """Retourne None si aucun fichier trouvé"""
        resolver = DockerFileResolver(base_path=tmp_path)
        result = resolver.find_env_file()

        assert result is None

    def test_resolve_uses_config_override(self, tmp_path):
        """Utilise les valeurs de n7.yaml si présent"""
        config_content = """
        docker:
          path_env_file: .env.prod
          path_compose_file: docker-compose.prod.yml
        """
        (tmp_path / "n7.yaml").write_text(config_content)
        (tmp_path / ".env").touch()
        (tmp_path / "docker-compose.yml").touch()

        resolver = DockerFileResolver(base_path=tmp_path)
        result = resolver.resolve()

        assert result["env_file"] == ".env.prod"
        assert result["compose_file"] == "docker-compose.prod.yml"

    def test_resolve_uses_auto_detection(self, tmp_path):
        """Utilise la détection auto si pas de n7.yaml"""
        (tmp_path / ".env.local").touch()
        (tmp_path / "docker-compose.dev.yml").touch()

        resolver = DockerFileResolver(base_path=tmp_path)
        result = resolver.resolve()

        assert result["env_file"] == ".env.local"
        assert result["compose_file"] == "docker-compose.dev.yml"

    def test_resolve_returns_default_service(self, tmp_path):
        """Retourne le default_service de la config"""
        config_content = """
        docker:
          default_service: worker
        """
        (tmp_path / "n7.yaml").write_text(config_content)

        resolver = DockerFileResolver(base_path=tmp_path)
        result = resolver.resolve()

        assert result["default_service"] == "worker"

    def test_resolve_default_service_none_when_not_set(self, tmp_path):
        """default_service est None si pas défini"""
        resolver = DockerFileResolver(base_path=tmp_path)
        result = resolver.resolve()

        assert result["default_service"] is None
