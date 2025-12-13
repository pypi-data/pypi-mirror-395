import logging
import traceback
from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING, Any

from ai_parade._toolkit.converters.converter import Conversion, ConverterOptions
from ai_parade._toolkit.get_weights import get_weights_name
from ai_parade._toolkit.run.ModelRunner import ModelRunner
from ai_parade._toolkit.run.PyTorch import PyTorchRunner

if TYPE_CHECKING:
	import torch  # type: ignore

logger = logging.getLogger(__name__)


class PyTorchConvertBase(ABC):
	def __init__(self, conversion: Conversion, options: ConverterOptions):
		self.conversion = conversion
		self.options = options

	@abstractmethod
	def _export_call(
		self,
		model: "torch.nn.Module",
		sample_inputs: tuple["torch.Tensor"],
		output_directory: Path,
		**kvargs: Any,
	) -> None:
		pass

	def __call__(self, runner: ModelRunner):
		import torch  # type: ignore

		assert isinstance(runner, PyTorchRunner)

		sample_inputs = torch.rand(runner.model_metadata.image_input.shape)
		runner.model.eval()

		def run(sample_inputs: "torch.Tensor"):
			# run the model to trigger potential lazy initialization
			runner.model(sample_inputs)

			self._export_call(runner.model, (sample_inputs,), runner.output_directory)
			return self.output_weights

		try:
			runner.model.to("cpu")
			return run(sample_inputs.to("cpu"))
		except Exception as e:
			msg = str(e)
			if "cpu" in msg or "gpu" in msg or "device" in msg:
				logger.warning("Conversion on CPU model failed, trying cuda instead.")
				logger.info(f"Failed with error: '{msg}'")
				logger.debug(traceback.format_exc())
				runner.model.to("cuda")
				return run(sample_inputs.to("cuda"))
			else:
				raise e

	@property
	def output_weights(self) -> Path:
		return get_weights_name(self.conversion[1], self.options.hw_acceleration)
