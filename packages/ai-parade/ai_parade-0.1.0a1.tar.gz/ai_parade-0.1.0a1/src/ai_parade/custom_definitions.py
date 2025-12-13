import ai_parade._compat  # noqa: F401
import ai_parade._toolkit.engine_metadata as engine_metadata

from ._toolkit.data.ImageInput import ImageInput
from ._toolkit.data.output import ModelOutput
from ._toolkit.enums import (
	InferenceEngine,
	ModelFormat,
)
from ._toolkit.install._PackageManagerInstaller import PackageManagerInstaller
from ._toolkit.install._Uv import UV
from ._toolkit.install.ModelInstaller import ModelInstaller
from ._toolkit.metadata.enums import ModelTasks
from ._toolkit.metadata.models.final import (
	InstallOptionsApi,
	ModelMetadata,
	ModelMetadataApi,
	PyTorchOptionsApi,
)
from ._toolkit.metadata.size import parse_model_size
from ._toolkit.run.ModelRunner import ModelRunner
from ._toolkit.run.PyTorch import PyTorchRunner

__all__ = [
	# Installers
	"ModelInstaller",
	"PackageManagerInstaller",
	"UV",
	# Runners
	"ModelRunner",
	"PyTorchRunner",
	# Models
	"ModelOutput",
	"ModelTasks",
	"ModelFormat",
	"InferenceEngine",
	"ImageInput",
	"ModelMetadata",
	"ModelMetadataApi",
	"InstallOptionsApi",
	"PyTorchOptionsApi",
	# Utils
	"parse_model_size",
	"engine_metadata",
]
