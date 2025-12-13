import logging
import re
from abc import ABC, abstractmethod
from pathlib import Path
from typing import override

from ai_parade._toolkit.constants import TRACE_LVL, VENV_DIR
from ai_parade._toolkit.metadata.models.final import InstallOptions

from .ModelInstaller import ModelInstaller
from .utilities import convert_lock_to_requirements, is_pinned_requirements_txt

logger = logging.getLogger(__name__)


class PackageManager(ABC):
	"""Abstract base class for package installers (uv, pip, etc.)"""

	@abstractmethod
	def prepend_commands(self, prefix: list[str]):
		"""Prepends all commands with the given prefix"""
		pass

	@abstractmethod
	async def freeze_command(self) -> str:
		"""Returns installed packages in the current environment

		Returns:
			str: installed packages in pip freeze format
		"""
		pass

	@abstractmethod
	async def _create_venv_command(self, python_version: str):
		"""Creates a virtual environment

		Args:
			python_version: Python version to use for the virtual environment
		"""
		pass

	@abstractmethod
	async def _install_dependencies_command(self, dependencies: list[str]):
		"""Installs a list of dependencies"""
		pass

	@abstractmethod
	async def _install_requirements_txt_command(self):
		"""Installs dependencies from requirements.txt"""
		pass

	@abstractmethod
	async def _install_self_command(self):
		"""
		Use `--no-build-isolation` if possible.
		This option in pip does two things:
		- the outside environment is not isolated from the build.
		- the build dependencies are not installed.

		There is an common issue when the package needs to build itself
		with the same version of a dependency as is then using in runtime.
		(i.e. prebuilt torch operations vs torch runtime)
		see: https://github.com/astral-sh/uv/issues/2252#issuecomment-2710054979

		So to make everything hopefully work with the `--no-build-isolation`
		- we are working in a venv (per project)
		- we installed build dependencies from pyproject.toml in the venv prior to calling this
		"""
		pass


class PackageManagerInstaller(ModelInstaller):
	"""Installs dependencies using a package manager

	The installation process is as follows:
	- create venv
	- install pip dependencies:
		- install dependencies from ai-parade.install.pip_dependencies in pyproject.toml
		- install dependencies from requirements.txt
		- install self, this will invoke build scripts like setup.py, pyproject.toml, etc.
	"""

	def __init__(
		self,
		repo_path: Path,
		install_options: InstallOptions,
		package_manager: PackageManager,
	):
		"""Interacts with a model

		Args:
			repo_path: Path to the repository
			package_manager: The package manager to use (uv, pip, etc.)
			install_options: Optional installation options. If None, will create a new one with default values.
		"""
		self.repo_path = repo_path
		self.package_manager = package_manager
		self.venv_path = repo_path / VENV_DIR
		self.install_parameters = install_options

	def is_venv_created(self) -> bool:
		"""Checks if venv could be found

		Returns:
			True if venv is found
		"""
		logger.debug("Checking if venv is created")
		has_venv = (self.venv_path / "bin" / "activate").is_file()
		logger.log(TRACE_LVL, f"venv is {'found' if has_venv else 'not found'}")
		return has_venv

	async def ensure_requirements_txt(self):
		requirements_txt = self.repo_path / "requirements.txt"
		if not requirements_txt.is_file():
			result = await convert_lock_to_requirements(requirements_txt.parent)
			if result is None:
				raise FileNotFoundError(
					"requirements.txt could not be found or created."
				)
			else:
				with open(Path(requirements_txt.name), "w") as f:
					f.write(result)
				return True
		return True

	async def is_pip_dependencies_installed(self) -> tuple[bool, bool, bool, bool]:
		"""Checks if pip dependencies are installed

		Returns tuple of bools where each one represents one check:
		- dependencies from requirements.txt
		- self
		- dependencies from ai-parade.install.pip_dependencies in pyproject.toml
		- dependencies from build-system.requires in pyproject.toml

		Returns:
			tuple of bools where each one represents one check

			`(bool, bool, bool, bool)`: (requirements.txt, self, pip_dependencies, build_system_dependencies)
		"""
		logger.debug("Checking if pip dependencies are installed")
		freezed = await self.package_manager.freeze_command()

		requirements_txt = self.repo_path / "requirements.txt"

		installed_requirements = False
		if await self.ensure_requirements_txt() and requirements_txt.is_file():
			with requirements_txt.open() as f:
				installed_requirements = True
				for dependency in f.read().splitlines():
					dependency = dependency.strip()
					if dependency.startswith("#"):
						continue
					dependency = dependency.split("#")[0]
					if dependency not in freezed:
						installed_requirements = False
						logger.debug(f"Dependency {dependency} not installed")
		logger.log(TRACE_LVL, f"installed_requirements: {installed_requirements}")

		installed_self = freezed.find("@ file://") != -1
		logger.log(TRACE_LVL, f"installed_self: {installed_self}")

		def is_in_freeze(dependencies: list[str] | tuple[str, ...]) -> bool:
			return all(
				[
					re.split("@|<|<=|!=|==|>=|>|~=|===", dependency)[0].strip()
					in freezed
					for dependency in dependencies
				]
			)

		if self.install_parameters.pip_dependencies is None:
			installed_list = True
		else:
			installed_list = is_in_freeze(self.install_parameters.pip_dependencies)
		logger.log(TRACE_LVL, f"installed_list: {installed_list}")

		installed_build_dependencies = is_in_freeze(
			self.install_parameters.build_system_dependencies
		)
		logger.log(
			TRACE_LVL, f"installed_build_dependencies: {installed_build_dependencies}"
		)

		return (
			installed_requirements,
			installed_self,
			installed_list,
			installed_build_dependencies,
		)

	@override
	async def is_installed(self) -> bool:
		return (
			self.repo_path.exists()
			and self.is_venv_created()
			and all(await self.is_pip_dependencies_installed())
		)

	async def _create_venv(self):
		"""Creates python venv"""
		if self.is_venv_created():
			logger.debug("Virtual environment already there. Skipping")
			return

		await self.package_manager._create_venv_command(self.install_parameters.python)

	async def _install_pip_dependencies(self):
		"""Installs pip dependencies

		These include:
		- dependencies from ai-parade.install.pip_dependencies in pyproject.toml
		- dependencies from requirements.txt
		- build dependencies from pyproject.toml (`build-system.requires`)
		- self
		"""
		(
			installed_requirements,
			installed_self,
			installed_list,
			installed_build_dependencies,
		) = await self.is_pip_dependencies_installed()

		if self.install_parameters.pip_dependencies is not None:
			if installed_list:
				logger.debug("Custom pip dependencies already installed. Skipping")
			else:
				logger.debug("Installing pip dependencies")
				await self.package_manager._install_dependencies_command(
					list(self.install_parameters.pip_dependencies)
				)

		if installed_requirements:
			logger.debug(
				"Pip dependencies from requirements.txt already installed. Skipping"
			)
		else:
			if not (self.repo_path / "requirements.txt").exists():
				raise FileNotFoundError("No requirements.txt found in the repository")
			if not is_pinned_requirements_txt(self.repo_path / "requirements.txt"):
				raise ValueError("requirements.txt is not pinned")

			logger.debug("Installing pip dependencies from requirements.txt")
			await self.package_manager._install_requirements_txt_command()

		if len(self.install_parameters.build_system_dependencies) != 0:
			if installed_build_dependencies:
				logger.debug("Build dependencies already installed. Skipping")
			else:
				logger.debug("Installing build dependencies")
				await self.package_manager._install_dependencies_command(
					self.install_parameters.build_system_dependencies
				)

		if installed_self:
			logger.debug("The project is already installed. Skipping")
		else:
			if (self.repo_path / "setup.py").exists() or (
				self.repo_path / "pyproject.toml"
			).exists():
				logger.debug("Running pip install on self")
				await self.package_manager._install_self_command()

	@override
	async def install(self, override: bool = False):
		"""Installs model

		Args:
			override: If True, will override all existing files. Defaults to False.
		"""
		logger.info("Installing model")

		if override:
			# todo: nuke the dependencies on override == True
			raise NotImplementedError
		logger.debug("Creating virtual environment.")
		await self._create_venv()

		logger.debug("Installing pip dependencies.")
		await self._install_pip_dependencies()
		logger.info("Installation done.")
