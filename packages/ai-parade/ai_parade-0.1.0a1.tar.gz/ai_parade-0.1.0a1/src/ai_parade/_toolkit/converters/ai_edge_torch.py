from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal, override

if TYPE_CHECKING:
	import torch  # type: ignore

from ai_parade._toolkit.enums import (
	ModelFormat,
	Quantization,
	QuantizedModelFormat,
)

from ._pytorch_base import PyTorchConvertBase
from .converter import Converter, ConverterOptions


class AIEdgeConverterEntry(Converter):
	"""
	https://github.com/google-ai-edge/ai-edge-torch
	and
	https://github.com/google-ai-edge/ai-edge-torch/blob/main/docs/pytorch_converter/README.md#quantization
	"""

	def __init__(
		self,
		quantization_type: Literal[Quantization.none]
		| Literal[Quantization.float16]
		| Literal[Quantization.int8],
	):
		self.quantization_type = quantization_type

	@property
	@override
	def conversion(self):
		return (
			QuantizedModelFormat(ModelFormat.PyTorch),
			QuantizedModelFormat(ModelFormat.LiteRT, self.quantization_type),
		)

	@override
	def create(self, options: ConverterOptions):
		super().create(options)
		return self.AIEdgeConverter(self.conversion, options)

	class AIEdgeConverter(PyTorchConvertBase):
		@override
		def _export_call(
			self,
			model: "torch.nn.Module",
			sample_inputs: tuple["torch.Tensor"],
			output_directory: Path,
			**kvargs: Any,
		):
			import ai_edge_torch  # type: ignore
			import tensorflow as tf  # type: ignore

			converter_flags = {}
			match self.conversion[1].quantization:
				case Quantization.float32:
					pass
				case Quantization.int8:
					assert self.options.calibration_data is not None
					# with fallback to other datatypes
					converter_flags["optimizations"] = [tf.lite.Optimize.DEFAULT]
					converter_flags["representative_dataset"] = list(
						map(lambda x: [x[0]], self.options.calibration_data)
					).__iter__
				case Quantization.float16:
					converter_flags["optimizations"] = [tf.lite.Optimize.DEFAULT]
					converter_flags["target_spec.supported_types"] = [tf.float16]

			edge_model = ai_edge_torch.convert(
				model, sample_inputs, _ai_edge_converter_flags=converter_flags
			)

			edge_model.export(output_directory / self.output_weights)


capabilities: list[Converter] = [
	AIEdgeConverterEntry(Quantization.none),
	AIEdgeConverterEntry(Quantization.int8),
	AIEdgeConverterEntry(Quantization.float16),
]
