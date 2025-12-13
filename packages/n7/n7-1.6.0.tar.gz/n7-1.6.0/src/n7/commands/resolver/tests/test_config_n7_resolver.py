from n7.commands.resolver import ConfigN7Resolver


class TestConfigResolver:
    """Tests pour ConfigResolver"""

    def setup_method(self):
        self.resolver = ConfigN7Resolver()

    def test_default_config_file_name(self):
        """Le fichier config par défaut est n7.yaml"""
        assert self.resolver.config_file == "n7.yaml"

    def test_load_returns_none_when_file_not_exists(self):
        """Retourne None si n7.yaml n'existe pas"""
        result = self.resolver.load()
        assert result is None

    def test_load_returns_config_when_file_exists(self, tmp_path):
        """Retourne la config si n7.yaml existe"""

        config_content = """
        docker:
          path_env_file: .env.local
          path_compose_file: docker-compose.dev.yml
          default_service: api
        """
        config_file = tmp_path / "n7.yaml"
        config_file.write_text(config_content)

        resolver = ConfigN7Resolver(base_path=tmp_path)
        result = resolver.load()

        assert result == {
            "docker": {
                "path_env_file": ".env.local",
                "path_compose_file": "docker-compose.dev.yml",
                "default_service": "api",
            }
        }

    def test_get_docker_config_returns_docker_section(self, tmp_path):
        """Retourne la section docker"""

        config_content = """
        docker:
          path_env_file: .env.prod
          path_compose_file: docker-compose.prod.yml
          default_service: worker
        """
        config_file = tmp_path / "n7.yaml"
        config_file.write_text(config_content)

        resolver = ConfigN7Resolver(base_path=tmp_path)
        result = resolver.get_docker_config()

        assert result == {
            "path_env_file": ".env.prod",
            "path_compose_file": "docker-compose.prod.yml",
            "default_service": "worker",
        }

    def test_get_docker_config_returns_none_when_no_file(self):
        """Retourne None si pas de fichier"""
        result = self.resolver.get_docker_config()
        assert result is None

    def test_get_docker_config_returns_none_when_no_docker_section(self, tmp_path):
        """Retourne None si pas de section docker"""

        config_content = """
        other:
          key: value
        """
        config_file = tmp_path / "n7.yaml"
        config_file.write_text(config_content)

        resolver = ConfigN7Resolver(base_path=tmp_path)
        result = resolver.get_docker_config()

        assert result is None

    def test_get_path_env_file(self, tmp_path):
        """Récupère path_env_file"""

        config_content = """
        docker:
          path_env_file: .env.local
        """
        config_file = tmp_path / "n7.yaml"
        config_file.write_text(config_content)

        resolver = ConfigN7Resolver(base_path=tmp_path)
        result = resolver.get_path_env_file()

        assert result == ".env.local"

    def test_get_path_env_file_returns_none_when_not_set(self, tmp_path):
        """Retourne None si path_env_file pas défini"""

        config_content = """
        docker:
          default_service: api
        """
        config_file = tmp_path / "n7.yaml"
        config_file.write_text(config_content)

        resolver = ConfigN7Resolver(base_path=tmp_path)
        result = resolver.get_path_env_file()

        assert result is None

    def test_get_path_compose_file(self, tmp_path):
        """Récupère path_compose_file"""

        config_content = """ 
        docker:
          path_compose_file: docker-compose.dev.yml
        """
        config_file = tmp_path / "n7.yaml"
        config_file.write_text(config_content)

        resolver = ConfigN7Resolver(base_path=tmp_path)
        result = resolver.get_path_compose_file()

        assert result == "docker-compose.dev.yml"

    def test_get_default_service(self, tmp_path):
        """Récupère default_service"""

        config_content = """
        docker:
          default_service: worker
        """
        config_file = tmp_path / "n7.yaml"
        config_file.write_text(config_content)

        resolver = ConfigN7Resolver(base_path=tmp_path)
        result = resolver.get_default_service()

        assert result == "worker"
