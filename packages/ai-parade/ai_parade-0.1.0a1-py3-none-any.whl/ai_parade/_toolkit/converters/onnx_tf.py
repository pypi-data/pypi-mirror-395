from typing import override

from ai_parade._toolkit.enums import ModelFormat
from ai_parade._toolkit.run.ModelRunner import ModelRunner
from ai_parade._toolkit.run.ONNX import ONNXRunner

from .converter import ConverterOptions, FormatConverter


class ONNX_TensorFlowConverter(FormatConverter):
	"""
	https://github.com/onnx/onnx-tensorflow/tree/main
	"""

	@property
	@override
	def format_conversion(self):
		return (ModelFormat.ONNX, ModelFormat.SavedModel)

	@override
	def create(self, options: ConverterOptions):
		super().create(options)
		return self.convert

	def convert(self, runner: ModelRunner):
		assert isinstance(runner, ONNXRunner)
		from onnx_tf.backend import prepare  # type: ignore

		tf_rep = prepare(runner.model)  # prepare tf representation
		dist_path = runner.output_directory / self._output_weights
		tf_rep.export_graph(dist_path)  # export the model

		return self._output_weights
