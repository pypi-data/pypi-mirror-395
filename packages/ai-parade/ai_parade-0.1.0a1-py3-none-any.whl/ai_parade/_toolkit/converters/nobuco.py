from pathlib import Path
from typing import TYPE_CHECKING, Any, override

if TYPE_CHECKING:
	import torch  # type: ignore

from ai_parade._toolkit.enums import ModelFormat

from ._pytorch_base import PyTorchConvertBase
from .converter import ConverterOptions, FormatConverter


class NobucoConverter(FormatConverter):
	"""
	https://github.com/AlexanderLutsenko/nobuco
	"""

	@property
	@override
	def format_conversion(self):
		return (ModelFormat.PyTorch, ModelFormat.SavedModel)

	@override
	def create(self, options: ConverterOptions):
		super().create(options)
		return self.NobucoConverter(self.conversion, options)

	class NobucoConverter(PyTorchConvertBase):
		@override
		def _export_call(
			self,
			model: "torch.nn.Module",
			sample_inputs: tuple["torch.Tensor"],
			output_directory: Path,
			**kvargs: Any,
		):
			import nobuco  # type: ignore
			from nobuco import ChannelOrder, ChannelOrderingStrategy  # type: ignore
			from nobuco.layers.weight import WeightLayer  # type: ignore

			keras_model = nobuco.pytorch_to_keras(
				model,
				args=sample_inputs,
				kwargs=None,
				inputs_channel_order=ChannelOrder.TENSORFLOW,
				outputs_channel_order=ChannelOrder.TENSORFLOW,
			)
			dist_path = output_directory / self.output_weights
			keras_model.save(dist_path, save_format="tf")
