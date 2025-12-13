from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Generic, ParamSpec, TypeVar

from ai_parade._toolkit.data.datasets.Dataset import Dataset

if TYPE_CHECKING:
	from ai_parade._toolkit.metadata.models.final import ModelMetadata
from ai_parade._toolkit.data.output import ModelOutput

TChild = TypeVar("TChild", bound="LoadedModelRunner")
TReturn = TypeVar("TReturn")
TModel = TypeVar("TModel")
P = ParamSpec("P")


# backward compatibility <=3.11: generic class notation
class ModelRunner(Generic[TChild, TModel], ABC):
	"""
	Runs model inference or anything on loaded model. It is a wrapper of execution engines.

	Implementation notes:
	- **IMPORTANT**: Do not import the engine on module level, the module should be importable even if the engine is not installed.
		e.g. do not do `import torch` at the top of the module
	"""

	def __init__(
		self, model_metadata: "ModelMetadata", weights: Path, *args: Any
	) -> None:
		self._output_dir: Path = Path.cwd()
		self._model_metadata = model_metadata
		self.weights = weights

	@property
	def output_directory(self) -> Path:
		"""Used for logs, artifacts, etc."""
		return self._output_dir

	@property
	def model_metadata(self) -> "ModelMetadata":
		return self._model_metadata

	def get_model_size(self) -> int | None:
		"""
		Get the size of the model in bytes

		Returns:
			Size of the model in bytes or None if the size could not be determined (model not yet downloaded)
		"""
		if not self.weights.exists():
			return None
		return self.weights.resolve().stat().st_size

	def set_output_directory(self, value: Path | None):
		"""Set output directory for the runner. Used for logs, artifacts, etc."""
		self._output_dir = value or Path.cwd()

	@abstractmethod
	def __enter__(self) -> "LoadedModelRunner[TChild, TModel]":
		pass

	@abstractmethod
	def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any):
		pass


class LoadedModelRunner(Generic[TChild, TModel], ABC):
	"""
	Runs model inference or anything on loaded model
	"""

	def __init__(self, runner: ModelRunner) -> None:
		self._runner = runner

	@property
	def output_directory(self) -> Path:
		"""Used for logs, artifacts, etc."""
		return self._runner._output_dir

	@property
	def model_metadata(self) -> "ModelMetadata":
		return self._runner._model_metadata

	def get_model_size(self) -> int | None:
		"""
		Get the size of the model in bytes

		Returns:
			Size of the model in bytes
		"""
		size = self._runner.get_model_size()
		assert size is not None
		return size

	def set_output_directory(self, value: Path | None):
		"""Set output directory for the runner. Used for logs, artifacts, etc."""
		# it is not property setter because I am lazy to implement them in the puppet
		self._runner.set_output_directory(value)

	@abstractmethod
	def inference(self, dataset: Dataset) -> list[ModelOutput]:
		"""Run inference on model

		Args:
			dataset: data to use to the inference

		Returns:
			output of the model
		"""
		pass

	@abstractmethod
	def run(self, what: Callable[[TChild], TReturn]) -> TReturn:
		"""Run something in the scope of the runner

		For example the remote runner is given converter to convert the model

		Args:
			what: callable to run, it is given the model from the runner

		Returns:
			result of the callable
		"""
		pass

	@property
	@abstractmethod
	def model(self) -> TModel:
		"""Get internal representation of the model (i.e. PyTorch model)

		Used by the converters
		"""
		pass
