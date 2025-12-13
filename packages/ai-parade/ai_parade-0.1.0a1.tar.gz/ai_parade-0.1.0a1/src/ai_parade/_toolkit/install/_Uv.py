import logging
import os
from pathlib import Path
from typing import override

from ai_parade._toolkit.logging import subprocess_run_log_async

from ._PackageManagerInstaller import PackageManager

logger = logging.getLogger(__name__)


class UV(PackageManager):
	def __init__(self, repo_path: Path):
		self.repo_path = repo_path.expanduser().resolve()

		self._uv_in_repo = [
			Path(os.getcwd()) / ".venv" / "bin" / "uv",
		]
		self._common_options = [
			"--no-progress",
			"--directory",
			self.repo_path,
		]
		self._env = {
			**os.environ.copy(),
			"VIRTUAL_ENV": str(self.repo_path / ".venv"),
			"UV_GIT_LFS": "1",  # enable git lfs
		}

	@override
	def prepend_commands(self, prefix: list[str]):
		self._uv_in_repo = prefix + self._uv_in_repo

	@override
	async def freeze_command(self):
		retCode, stdout, stderr = await subprocess_run_log_async(
			self._uv_in_repo + ["pip", "freeze"] + self._common_options,
			env=self._env,
			logger=logger,
		)
		return stdout

	@override
	async def _create_venv_command(self, python_version: str):
		await subprocess_run_log_async(
			self._uv_in_repo
			+ [
				"venv",
				"--python",
				python_version,
			]
			+ self._common_options,
			env=self._env,
			logger=logger,
		)

	@override
	async def _install_dependencies_command(self, dependencies: list[str]):
		await subprocess_run_log_async(
			self._uv_in_repo
			+ [
				"pip",
				"install",
			]
			+ self._common_options
			+ dependencies,
			env=self._env,
			logger=logger,
		)

	@override
	async def _install_requirements_txt_command(self):
		await subprocess_run_log_async(
			self._uv_in_repo
			+ [
				"pip",
				"install",
				"-r",
				self.repo_path / "requirements.txt",
			]
			+ self._common_options,
			env=self._env,
			logger=logger,
		)

	@override
	async def _install_self_command(self):
		await subprocess_run_log_async(
			self._uv_in_repo
			+ [
				"pip",
				"install",
				"--no-build-isolation",
				self.repo_path,
			]
			+ self._common_options,
			env=self._env,
			logger=logger,
		)
