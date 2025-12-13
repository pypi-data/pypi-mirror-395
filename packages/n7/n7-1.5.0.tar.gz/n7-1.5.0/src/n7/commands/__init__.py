"""Commandes du CLI N7"""

from n7.commands.docker.container.connect_shell_command import connect_shell_command
from n7.commands.docker.container.down_command import down_command
from n7.commands.docker.container.logs_command import logs_command
from n7.commands.docker.container.py_manage_command import py_manage_command
from n7.commands.docker.container.up_command import up_command
from n7.commands.docker.format.docker_black_command import docker_black_command
from n7.commands.docker.format.docker_mypy_command import docker_mypy_command
from n7.commands.docker.format.docker_pycheck_command import docker_pycheck_command
from n7.commands.docker.format.docker_pyqa_command import docker_pyqa_command
from n7.commands.docker.format.docker_ruff_command import docker_ruff_command
from n7.commands.docker.format.docker_uv_command import docker_uv_command
from n7.commands.docker.test.docker_pytest_command import docker_pytest_command
from n7.commands.local.format.local_black_command import local_black_command
from n7.commands.local.format.local_mypy_command import local_mypy_command
from n7.commands.local.format.local_pycheck_command import local_pycheck_command
from n7.commands.local.format.local_pyqa_command import local_pyqa_command
from n7.commands.local.format.local_ruff_command import local_ruff_command
from n7.commands.local.format.local_uv_command import local_uv_command
from n7.commands.local.test.local_pytest_command import local_pytest_command

__all__ = [
    "local_pytest_command",
    "local_black_command",
    "local_ruff_command",
    "local_mypy_command",
    "local_pyqa_command",
    "local_pycheck_command",
    "local_uv_command",
    "docker_pytest_command",
    "docker_black_command",
    "docker_ruff_command",
    "docker_mypy_command",
    "docker_pyqa_command",
    "docker_pycheck_command",
    "docker_uv_command",
    "up_command",
    "down_command",
    "logs_command",
    "connect_shell_command",
    "py_manage_command",
]
