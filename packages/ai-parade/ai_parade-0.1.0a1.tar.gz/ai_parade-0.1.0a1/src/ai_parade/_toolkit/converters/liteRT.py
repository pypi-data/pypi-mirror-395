import functools
from pathlib import Path
from typing import Callable, Literal, override

from ai_parade._toolkit.enums import ModelFormat, Quantization, QuantizedModelFormat
from ai_parade._toolkit.run import ModelRunner
from ai_parade._toolkit.run.TensorFlow import TensorFlowRunner

from .converter import Converter, ConverterOptions


class LiteRT_Converter(Converter):
	"""
	Built-in TensorFlow to LiteRT converter, including post training quantization

	PTQ:
	https://docs.pytorch.org/ao/stable/tutorials_source/pt2e_quant_ptq.html
	"""

	def __init__(
		self,
		quantization_type: Literal[Quantization.float16]
		| Literal[Quantization.int8]
		| Literal[Quantization.float32],
	):
		self.quantization_type = quantization_type

	@property
	@override
	def conversion(self):
		return (
			QuantizedModelFormat(ModelFormat.SavedModel),
			QuantizedModelFormat(ModelFormat.SavedModel, self.quantization_type),
		)

	@override
	def create(self, options: ConverterOptions) -> Callable[[ModelRunner], Path]:
		super().create(options)
		assert self.quantization_type not in [Quantization.int8] or options is not None
		return functools.partial(self.convert, options=options)

	def convert(self, runner: ModelRunner, options: ConverterOptions):
		assert isinstance(runner, TensorFlowRunner)
		import tensorflow as tf  # type: ignore

		converter = tf.lite.TFLiteConverter.from_saved_model(runner.model)
		match self.quantization_type:
			case Quantization.float32:
				pass
			case Quantization.int8:
				assert options.calibration_data is not None
				# with fallback to other datatypes
				converter.optimizations = [tf.lite.Optimize.DEFAULT]
				converter.representative_dataset = options.calibration_data
			case Quantization.float16:
				converter.optimizations = [tf.lite.Optimize.DEFAULT]
				converter.target_spec.supported_types = [tf.float16]
		tflite_quant_model = converter.convert()

		with open(runner.output_directory / self._output_weights, "wb") as f:
			f.write(tflite_quant_model)

		return self._output_weights
