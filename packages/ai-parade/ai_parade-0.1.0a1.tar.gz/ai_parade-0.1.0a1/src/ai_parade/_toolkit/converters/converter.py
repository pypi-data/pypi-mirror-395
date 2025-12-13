from abc import ABC, abstractmethod
from pathlib import Path
from typing import Callable, NamedTuple, final, override

from ai_parade._toolkit.data.datasets.Dataset import Dataset
from ai_parade._toolkit.enums import (
	HardwareAcceleration,
	ModelFormat,
	QuantizedModelFormat,
)
from ai_parade._toolkit.get_weights import get_weights_name
from ai_parade._toolkit.run.ModelRunner import ModelRunner

Conversion = tuple[QuantizedModelFormat, QuantizedModelFormat]
"""
A conversion is a tuple of (input_format, output_format)
"""


class ConverterOptions(NamedTuple):
	"""
	Options for a converter.
	"""

	calibration_data: Dataset | None = None
	"""
	Dataset to use for quantization calibration, unused if no quantization
	"""
	hw_acceleration: HardwareAcceleration | None = None
	"""
	Hardware acceleration to use for quantization, unused if format does not distinguish it
	"""


class Converter(ABC):
	"""
	Converts a model from one format to another (including quantization).

	"""

	def __init__(self) -> None:
		self._output_weights = get_weights_name(self.conversion[1])

	@property
	@abstractmethod
	def conversion(self) -> Conversion:
		"""
		Available conversions in form of (input_format, output_format)
		"""
		pass

	@abstractmethod
	def create(self, options: ConverterOptions) -> Callable[[ModelRunner], Path]:
		"""
		Creates a converter callable.

		The callable takes a ModelRunner as input and does not return anything.
		The converted model is stored in ModelRunner.output_directory as a `model.suffix` file(s).

		Implementation notes:
		- make sure to run super().create(options) first to set self._output_weights
		- make sure to use the ModelRunner.output_directory / "model.suffix" to store the converted model.

		Args:
			 calibration_data: dataset to use for quantization calibration, unused if no quantization

		Returns:
			 Callable that takes a ModelRunner as input and converts the model with it.
			 It returns the path to the converted model inside the runner's output directory
		"""
		self._output_weights = get_weights_name(
			self.conversion[1], options.hw_acceleration
		)


class FormatConverter(Converter):
	"""
	Subclass of Converter that converts model formats without quantization.
	"""

	@property
	@final
	@override
	def conversion(self) -> Conversion:
		formats = self.format_conversion
		return (
			QuantizedModelFormat(formats[0]),
			QuantizedModelFormat(formats[1]),
		)

	@property
	@abstractmethod
	def format_conversion(self) -> tuple[ModelFormat, ModelFormat]:
		pass
