import functools
from pathlib import Path
from typing import Callable, Literal, override

from ai_parade._toolkit.enums import ModelFormat, Quantization, QuantizedModelFormat
from ai_parade._toolkit.run import ModelRunner
from ai_parade._toolkit.run.ONNX import ONNXRunner

from .converter import Converter, ConverterOptions


class ONNX_Quantization(Converter):
	"""
	Built-in ONNX post training quantization
	"""

	def __init__(
		self,
		quantization_type: Literal[Quantization.float16] | Literal[Quantization.int8],
	):
		self.quantization_type = quantization_type

	@property
	@override
	def conversion(self):
		return (
			QuantizedModelFormat(ModelFormat.ONNX),
			QuantizedModelFormat(ModelFormat.ONNX, self.quantization_type),
		)

	@override
	def create(self, options: ConverterOptions) -> Callable[[ModelRunner], Path]:
		super().create(options)
		match self.quantization_type:
			case Quantization.float16:
				return self.convert_to_f16
			case Quantization.int8:
				assert options.calibration_data is not None
				return functools.partial(self.convert_to_i8, options=options)
			case _:
				raise RuntimeError("Unknown quantization type")

	def convert_to_f16(self, runner: ModelRunner):
		"""
		https://onnxruntime.ai/docs/performance/model-optimizations/float16.html
		"""
		assert isinstance(runner, ONNXRunner)
		import onnx  # type: ignore
		from onnxconverter_common import float16  # type: ignore

		# ?todo: https://onnxruntime.ai/docs/performance/transformers-optimization.html

		model = onnx.load(runner.weights)
		model_fp16 = float16.convert_float_to_float16(model, keep_io_types=True)
		onnx.save(model_fp16, runner.output_directory / self._output_weights)

		return self._output_weights

	def convert_to_i8(self, runner: ModelRunner, options: ConverterOptions):
		"""
		https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html
		"""
		assert isinstance(runner, ONNXRunner)

		from onnxruntime.quantization import (  # type: ignore
			CalibrationDataReader,
			quant_pre_process,
			quantize_static,
		)

		class DataReader(CalibrationDataReader):
			def __init__(self, runner: ModelRunner):
				assert options.calibration_data is not None
				self.iterator = iter(
					map(lambda x: {"input": x[0]}, options.calibration_data)
				)

				# Use inference session to get input shape.
				# session = runner.model
				# (_, _, height, width) = session.get_inputs()[0].shape

				# self.input_name = session.get_inputs()[0].name

			def get_next(self):
				return next(self.iterator, None)

		# ?todo: https://onnxruntime.ai/docs/performance/transformers-optimization.html

		preprocessed_model = runner.output_directory / "preprocessed_model.onnx"
		quant_pre_process(runner.weights, preprocessed_model)
		quantize_static(
			preprocessed_model,
			runner.output_directory / self._output_weights,
			calibration_data_reader=DataReader(runner),
		)

		return self._output_weights
