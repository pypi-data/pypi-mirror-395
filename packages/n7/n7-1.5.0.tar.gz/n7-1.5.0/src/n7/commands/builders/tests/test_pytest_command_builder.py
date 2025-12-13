from n7.commands.builders import PytestCommandBuilder


class TestPytestCommandBuilder:
    def setup_method(self):
        self.builder = PytestCommandBuilder()

    def test_instance_builder(self):
        """test instance builder"""
        assert self.builder is not None
        assert self.builder.base_cmd == "pytest"

    def test_build_command_without_all(self):
        """command pytest only"""
        res = self.builder.build()
        assert res == ("pytest",)

    def test_build_command_with_path(self):
        """command pytest with path"""
        res = self.builder.build(path="my/path")
        assert res == ("pytest", "my/path")

    def test_build_with_verbose(self):
        """command pytest -v"""
        result = self.builder.build(verbose=True)
        assert result == ("pytest", "-v")

    def test_build_with_stop_first(self):
        """command pytest -x"""
        result = self.builder.build(stop_first=True)
        assert result == ("pytest", "-x")

    def test_build_with_filter_tests(self):
        """command pytest -k test_name"""
        result = self.builder.build(filter_tests="test_name")
        assert result == ("pytest", "-k", "test_name")

    def test_build_with_workers(self):
        """command pytest -n auto"""
        result = self.builder.build(workers="auto")
        assert result == ("pytest", "-n", "auto")

    def test_build_with_workers_number(self):
        """command pytest -n 4"""
        result = self.builder.build(workers="4")
        assert result == ("pytest", "-n", "4")

    def test_build_with_cov(self):
        """command pytest --cov=app"""
        result = self.builder.build(cov="users")
        assert result == ("pytest", "--cov=users")

    def test_build_with_cov_report(self):
        """command pytest --cov-report=html"""
        result = self.builder.build(cov_report="html")
        assert result == ("pytest", "--cov-report=html")

    def test_build_with_last_failed(self):
        """command pytest --lf"""
        result = self.builder.build(last_failed=True)
        assert result == ("pytest", "--lf")

    def test_build_with_failed_first(self):
        """command pytest --ff"""
        result = self.builder.build(failed_first=True)
        assert result == ("pytest", "--ff")

    def test_build_with_create_db(self):
        """command pytest --create-db"""
        result = self.builder.build(create_db=True)
        assert result == ("pytest", "--create-db")

    def test_build_with_migrations(self):
        """command pytest --migrations"""
        result = self.builder.build(migrations=True)
        assert result == ("pytest", "--migrations")

    def test_build_with_multiple_options(self):
        """command pytest with many options"""
        result = self.builder.build(
            path="users/tests/",
            verbose=True,
            workers="auto",
        )
        assert result == ("pytest", "-v", "-n", "auto", "users/tests/")

    def test_build_with_coverage_full(self):
        """command pytest coverage completed"""
        result = self.builder.build(
            cov="users",
            cov_report="html",
            verbose=True,
        )
        assert result == ("pytest", "-v", "--cov=users", "--cov-report=html")

    def test_path_always_last(self):
        """This path always last"""
        result = self.builder.build(
            path="tests/",
            verbose=True,
            cov="app",
            workers="auto",
        )
        assert result[-1] == "tests/"
