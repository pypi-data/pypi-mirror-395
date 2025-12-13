from pathlib import Path

from ai_parade._toolkit.enums import InferenceEngine
from ai_parade._toolkit.metadata.custom import Customizations
from ai_parade._toolkit.metadata.models.final import ModelMetadata, RunnerGetter

from .ModelRunner import ModelRunner
from .NotARunner import NotARunner
from .RemoteRunner import RemoteRunner


def get_runner(
	engine: InferenceEngine,
	model_metadata: ModelMetadata,
	weights: Path,
	use_remote: bool = True,
	customizations: Customizations | None = None,
	runner_name: str | None = None,
) -> ModelRunner:
	"""Returns appropriate runner for the model based on the parameters

	Args:
		engine: Desired inference engine
		model_metadata: metadata
		weights: Model weights
		use_remote: If False, don't use remote runner. Defaults to True.
		customizations: Customizations. Defaults to None.
		runner_name: Name of the runner in the customizations. Defaults to None, required if customizations is not None

	Returns:
		Initialized ModelRunner
	"""
	if model_metadata.format == engine:
		runner = model_metadata.get_runner(model_metadata, weights)
		if not use_remote and isinstance(runner, RemoteRunner):
			return runner.local_runner(model_metadata, weights)
		return runner
	else:
		local_getter = _choose_local_runner(engine, customizations, runner_name)
		if not use_remote:
			return local_getter(model_metadata, weights)

		return RemoteRunner(model_metadata, engine, weights, local_getter)


def _choose_local_runner(
	engine: InferenceEngine,
	customizations: Customizations | None = None,
	runner_name: str | None = None,
) -> RunnerGetter:
	"""Chooses default runner or runner from customizations

	Args:
		model_format: Desired model format
		customizations: Customizations. Defaults to None.
		runner_name: Name of the runner in the customizations. Defaults to None, required if customizations is not None

	Returns:
		ModelRunner in form of RunnerGetter
	"""
	if customizations is not None and runner_name is not None:
		return customizations.runners[runner_name]

	else:
		match engine:
			case InferenceEngine.PyTorch:
				from .PyTorch import PyTorchRunner

				return PyTorchRunner
			case InferenceEngine.ONNXRuntime:
				from .ONNX import ONNXRunner

				return ONNXRunner
			case InferenceEngine.TensorFlow:
				from .TensorFlow import TensorFlowRunner

				return TensorFlowRunner
			case InferenceEngine.ExecuTorch:
				return NotARunner
			case InferenceEngine.LiteRT:
				return NotARunner
			case InferenceEngine.ncnn:
				return NotARunner
			case _:
				raise RuntimeError(f"Unknown model format `{engine}`")
			# New DL-lib: register runner - ModelRunner derived class
