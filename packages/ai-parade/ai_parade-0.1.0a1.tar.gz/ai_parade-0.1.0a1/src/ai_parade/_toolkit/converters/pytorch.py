from pathlib import Path
from typing import TYPE_CHECKING, Any, override

from ai_parade._toolkit.run.ONNX import ONNXRunner

if TYPE_CHECKING:
	import torch  # type: ignore

from ai_parade._toolkit.enums import ModelFormat

from ._onnx_simplify import ONNXSimplify
from ._pytorch_base import PyTorchConvertBase
from .converter import ConverterOptions, FormatConverter


class PyTorch_onnx_export(FormatConverter):
	"""
	Built-in converter from PyTorch to ONNX.
	"""

	@property
	@override
	def format_conversion(self):
		return (ModelFormat.PyTorch, ModelFormat.ONNX)

	@override
	def create(self, options: ConverterOptions):
		super().create(options)
		return self.PyTorchConverter(self.conversion, options)

	class PyTorchConverter(PyTorchConvertBase):
		@override
		def _export_call(
			self,
			model: "torch.nn.Module",
			sample_inputs: tuple["torch.Tensor"],
			output_directory: Path,
			**kvargs: Any,
		):
			import torch  # type: ignore
			from onnxscript import opset18 as op  # type: ignore

			def sym_not(x: Any):
				return op.Not(x)

			# This notation is kind of cryptic but:
			# - tuple define model input argument (could be dict instead to act as kwargs)
			# - key in the dictionary is the index of its dimensions
			# - value is the dimension
			dynamic_shapes = ({0: torch.export.Dim("batch_dim", min=1)},)

			dist_path = output_directory / self.output_weights
			onnx_model = torch.onnx.export(
				model,
				sample_inputs,
				external_data=False,  # ?todo: at least for now this large models are useless for us
				dynamo=True,
				report=True,
				artifacts_dir=output_directory,
				verify=True,
				dynamic_shapes=dynamic_shapes,
				input_names=[ONNXRunner.INPUT_NAME],
				# todo after https://github.com/pytorch/pytorch/issues/136572 : remove
				custom_translation_table={torch.sym_not: sym_not},
			)
			onnx_model.save(dist_path)

			if not ONNXSimplify().simplify(dist_path):
				raise RuntimeError("Failed to simplify ONNX model")
