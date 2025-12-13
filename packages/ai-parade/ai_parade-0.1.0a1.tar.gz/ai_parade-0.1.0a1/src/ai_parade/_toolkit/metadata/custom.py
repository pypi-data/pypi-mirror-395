import logging
from inspect import isclass
from pathlib import Path
from typing import Callable

from ai_parade._toolkit.constants import CUSTOM_RUNNER_FILE_NAME, TRACE_LVL
from ai_parade._toolkit.install._PackageManagerInstaller import PackageManagerInstaller
from ai_parade._toolkit.install._Uv import UV
from ai_parade._toolkit.install.ModelInstaller import ModelInstaller
from ai_parade._toolkit.metadata.models.api import (
	InstallerGetter,
	ModelMetadataApi,
	RunnerGetter,
)
from ai_parade._toolkit.metadata.models.final import InstallOptions
from ai_parade._toolkit.run.ModelRunner import ModelRunner
from ai_parade._toolkit.sys_path_checkpoint import SysPathCheckpoint

logger = logging.getLogger(__name__)


class Customizations:
	"""
	Customizations object

	`ai-parade.py` file specification:
	- include: () -> list[ModelMetadataApi]
		Function to define metadata instead of using `pyproject.toml`.
	- installers: (ModelMetadata) -> ModelInstaller
		Model installer class.
		Name of the class could be used to select the installer from within the model metadata.
		The parameters are passed to the constructor.
	- runners: (ModelMetadata) -> ModelRunner
		Model runner class.
		Name of the class could be used to select the runner from within the model metadata.
		The parameters are passed to the constructor.
	"""

	include: Callable[[], list[ModelMetadataApi]] | None = None
	installers: dict[str, InstallerGetter] = {}
	runners: dict[str, RunnerGetter] = {}


async def get_customizations(
	repo_path: Path,
	install_options: InstallOptions,
):
	"""Get customizations from the repository, **installs the model dependencies**.

	The customizations are defined in the `ai-parade.py` file in the repository.

	Args:
		repo_path: Path to the repository

	Returns:
		Customizations: Customizations object with the customizations
	"""
	# todo: this loads everything (modules) into the memory, which is bad
	# best would be to run everything in a separate process via puppet, and implement sw for that
	customizations = Customizations()
	customizations_file = repo_path / CUSTOM_RUNNER_FILE_NAME
	if customizations_file.exists():
		import importlib.util
		import sys

		logger.info(f"Customization file found: {customizations_file}")

		installer = PackageManagerInstaller(repo_path, install_options, UV(repo_path))
		if not await installer.is_installed():
			logger.info(
				"Will install model dependencies, to be able to run customizations"
			)
			await installer.install()

		logger.debug("Importing customizations (ai-parade.py)")

		with SysPathCheckpoint(repo_path):
			# patch path so it includes customizations and its dependencies
			sys.path.insert(0, str(repo_path / ".venv/lib/python3.10/site-packages"))
			sys.path.insert(0, str(repo_path))

			spec = importlib.util.spec_from_file_location(
				"ai_parade_customizations", customizations_file
			)
			custom_runner_module = importlib.util.module_from_spec(spec)  # type: ignore
			spec.loader.exec_module(custom_runner_module)  # type: ignore

		logger.debug("Inspecting customizations (ai-parade.py):")

		# includes
		customizations.include = getattr(custom_runner_module, "include", None)
		if customizations.include is not None:
			assert callable(customizations.include)
			logger.debug("Found include function")

		for x in dir(custom_runner_module):
			member = getattr(custom_runner_module, x)
			if (
				not hasattr(member, "__module__")
				or not member.__module__ == custom_runner_module.__name__
			):
				logger.log(TRACE_LVL, f"Skipping {x}")
				continue

			# runners
			if isclass(member) and issubclass(member, ModelRunner):
				customizations.runners[x] = member
				logger.debug(f"Found runner `{x}`")

			# installers
			if isclass(member) and issubclass(member, ModelInstaller):
				customizations.installers[x] = member
				logger.debug(f"Found installer `{x}`")
	return customizations
