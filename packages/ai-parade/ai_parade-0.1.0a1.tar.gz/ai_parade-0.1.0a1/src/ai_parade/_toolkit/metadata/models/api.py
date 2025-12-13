from pathlib import Path
from typing import TYPE_CHECKING, Callable

from ai_parade._toolkit.install.ModelInstaller import ModelInstaller
from ai_parade._toolkit.run.ModelRunner import ModelRunner

from .pyproject import (
	InstallOptionsPyproject,
	ModelMetadataPyproject,
	PyTorchOptionsPyproject,
)

if TYPE_CHECKING:
	# its circular import, but we need it only for types and we could split the models
	from .final import ModelMetadata

InstallerGetter = Callable[["ModelMetadata"], ModelInstaller]
RunnerGetter = Callable[["ModelMetadata", Path], ModelRunner]


class ModelMetadataApi(ModelMetadataPyproject):
	"""
	Api definition of model metadata (registration).
	"""

	get_installer: InstallerGetter | None = None
	"""
	Uninitialized type of the installer
	None (default) will use default `CondaPipInstaller`
	"""

	get_runner: RunnerGetter | None = None
	"""
	Uninitialized type of the runner

	The getter function which returns ModelRunner instance from ModelMetadata and weights path.

	None (default) will use default runner for given format
	"""

	size: float  # type: ignore redefinition with un-optional type


InstallOptionsApi = InstallOptionsPyproject
"""
Api definition of install options 
"""
PyTorchOptionsApi = PyTorchOptionsPyproject
"""
Api definition of pytorch options 
"""
