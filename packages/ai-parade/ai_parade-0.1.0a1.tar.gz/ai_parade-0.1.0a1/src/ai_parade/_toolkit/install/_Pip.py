import logging
from pathlib import Path
from typing import override

from ai_parade._toolkit.logging import subprocess_run_log_async

from ._PackageManagerInstaller import PackageManager

logger = logging.getLogger(__name__)


class Pip(PackageManager):
	def __init__(self, repo_path: Path):
		self.repo_path = repo_path
		self.venv_path = repo_path / "venv"

		self._pip_in_venv = [self.venv_path / "bin" / "pip"]

	@override
	def prepend_commands(self, prefix: list[str]):
		self._pip_in_venv = prefix + self._pip_in_venv

	@override
	async def freeze_command(self):
		retCode, stdout, stderr = await subprocess_run_log_async(
			self._pip_in_venv + ["freeze"],
			logger=logger,
		)
		return stdout

	@override
	async def _create_venv_command(self, python_version: str):
		await subprocess_run_log_async(
			[
				"python" + python_version,
				"-m",
				"venv",
				self.venv_path,
			],
			logger=logger,
		)

	@override
	async def _install_dependencies_command(self, dependencies: list[str]):
		await subprocess_run_log_async(
			self._pip_in_venv
			+ [
				"install",
				"--progress-bar",
				"off",
			]
			+ dependencies,
			logger=logger,
		)

	@override
	async def _install_requirements_txt_command(self):
		await subprocess_run_log_async(
			self._pip_in_venv + ["install", "--progress-bar", "off"],
			logger=logger,
		)

	@override
	async def _install_self_command(self):
		await subprocess_run_log_async(
			self._pip_in_venv
			+ [
				"install",
				"--progress-bar",
				"off",
				"--no-build-isolation",
				self.repo_path,
			],
			logger=logger,
		)
