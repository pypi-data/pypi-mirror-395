from typing import Optional

from pydantic import ConfigDict, DirectoryPath

from .api import (
	InstallerGetter,
	InstallOptionsApi,
	ModelMetadataApi,
	PyTorchOptionsApi,
	RunnerGetter,
)


class ModelMetadata(ModelMetadataApi):
	"""
	Model metadata -- everything needed to install and run the model and more
	"""

	model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

	repository_path: Optional[DirectoryPath] = None
	"""
	Path to the repository, or None if the model is not locally available
	"""

	pytorch: Optional["PyTorchOptions"] = None  # type: ignore
	install: Optional["InstallOptions"] = None  # type: ignore

	get_installer: InstallerGetter  # type: ignore -> make it required
	"""
	Uninitialized type of the installer
	"""

	get_runner: RunnerGetter  # type: ignore -> make it required
	"""
	Uninitialized type of the runner
	"""


class InstallOptions(InstallOptionsApi):
	"""
	Installation options
	"""

	model_config = ConfigDict(frozen=True)
	build_system_dependencies: list[str]
	"""
	Build system dependencies from pyproject (build-system.requires)
	"""
	python: str
	"""
	The environment is initialized with python of this version.
	
	"""


class PyTorchOptions(PyTorchOptionsApi):
	"""
	PyTorch options
	"""

	model_config = ConfigDict(frozen=True, protected_namespaces=())
	pass
