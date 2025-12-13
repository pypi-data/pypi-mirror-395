import logging
from typing import override

from ai_parade._toolkit.constants import TRACE_LVL, VENV_DIR
from ai_parade._toolkit.logging import subprocess_run_log_async
from ai_parade.toolkit import ModelMetadata

from ._PackageManagerInstaller import PackageManagerInstaller
from .ModelInstaller import ModelInstaller

logger = logging.getLogger(__name__)


class CondaInstaller(ModelInstaller):
	"""Installs dependencies with conda and pip

	The installation process is as follows:
	- download model (model weights)
	- download repository (git clone)
	- if conda is available:
		- create venv with conda, set up proper python version
		- install conda dependencies from ai-parade.install.conda_dependencies in pyproject.toml
	- if conda is not available:
		- create venv
	- install pip dependencies:
		- install dependencies from ai-parade.install.pip_dependencies in pyproject.toml
		- install dependencies from requirements.txt
		- install self, this will invoke build scripts like setup.py, pyproject.toml, etc.
	"""

	def __init__(
		self,
		model_metadata: ModelMetadata,
		package_installer: PackageManagerInstaller,
	):
		"""Interacts with a model

		Args:
				 model_metadata: metadata
				 model: Fully initialized model, including weights Default None.
		"""

		self.model_metadata = model_metadata
		self.conda = "conda"

		assert model_metadata.repository_path is not None
		self.repo_path = model_metadata.repository_path
		self.venv_path = model_metadata.repository_path / VENV_DIR

		package_installer.package_manager.prepend_commands(
			[self.conda, "run", "--prefix", str(self.venv_path)]
		)
		self.package_installer = package_installer

		assert model_metadata.install is not None
		self.install_parameters = model_metadata.install

		assert model_metadata.install.conda_dependencies is not None
		self.conda_dependencies = model_metadata.install.conda_dependencies

	async def is_conda_dependencies_installed(self) -> bool:
		"""Checks if conda dependencies are installed

		Returns:
			 True if conda dependencies are installed
		"""

		logger.log(TRACE_LVL, "Checking if conda dependencies are installed")

		retCode, stdout, _ = await subprocess_run_log_async(
			[self.conda, "install", "--dry-run", "--prefix", self.venv_path],
			check=False,
			logger=logger,
		)
		is_installed = stdout.find("All requested packages already installed.") != -1
		return retCode == 0 and is_installed

	@override
	async def is_installed(self) -> bool:
		"""Checks if model and dependencies are installed

		Returns:
			 True if everything is installed
		"""

		return (
			self.package_installer.is_installed()
			and await self.is_conda_dependencies_installed()
		)

	def is_venv_created(self) -> bool:
		"""Checks if venv could be found

		Returns:
			 True if venv is found
		"""

		logger.log(TRACE_LVL, "Checking if venv is created")
		return (self.venv_path / "conda-meta").is_dir()

	async def _create_conda_venv(self):
		"""Creates conda environment"""
		if self.is_venv_created():
			logger.debug("Conda environment already there. Skipping")
			return

		if (self.repo_path / "environment.yml").exists():
			logger.debug("Creating conda environment from environment.yml")
			await subprocess_run_log_async(
				[
					self.conda,
					"create",
					"--prefix",
					self.venv_path,
					"--file",
					"environment.yml",
					"--yes",
					"--quiet",
				],
				logger=logger,
			)
		else:
			logger.debug("Creating conda venv")
			await subprocess_run_log_async(
				[
					self.conda,
					"create",
					"--prefix",
					self.venv_path,
					"pip",
					"python=" + self.install_parameters.python,
					"--yes",
					"--quiet",
				],
				logger=logger,
			)

	async def _install_conda_dependencies(self):
		"""Installs conda dependencies from ai-parade.install.conda_dependencies"""
		if await self.is_conda_dependencies_installed():
			logger.debug("Conda dependencies already installed. Skipping")
			return

		logger.debug("Installing conda dependencies")
		await subprocess_run_log_async(
			[
				self.conda,
				"install",
				"--prefix",
				self.venv_path,
				"--yes",
				"--quiet",
			]
			+ list(self.conda_dependencies),
			logger=logger,
		)

	@override
	async def install(self, override: bool = False):
		"""Installs model see `CondaPipInstaller`

		Args:
			 override: If True, will override all existing files. Defaults to False.
		"""
		logger.info(f"Installing model `{self.model_metadata.name}`: ")

		logger.info("Going to install model dependencies")
		# todo: nuke the dependencies on override == True
		await self._create_conda_venv()
		await self._install_conda_dependencies()
		await self.package_installer._install_pip_dependencies()

		logger.info("Installation done.")
