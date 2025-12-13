from pathlib import Path

from ai_parade._toolkit.engine_metadata import ModelAttributes, format_distinguishes
from ai_parade._toolkit.enums import (
	HardwareAcceleration,
	QuantizedModelFormat,
	format_suffixes,
)


def get_weights_name(
	format: QuantizedModelFormat, hw_acceleration: HardwareAcceleration | None = None
) -> Path:
	"""
	Get path to model weights, this path may not exist

	Example:
	>>> get_weights_name(QuantizedModelFormat(ModelFormat.ONNX, Quantization.none))
	'onnx.all.all.onnx'

	>>> get_weights_name(QuantizedModelFormat(ModelFormat.ExecutorTorch, Quantization.int8, HardwareAcceleration.XNNPACK))
	'executorch.int8.xnnpack.pte'
	"""
	hw_acceleration = hw_acceleration or HardwareAcceleration.CPU
	name = ".".join(
		[
			format.format.value,
			(
				format.quantization.value
				if ModelAttributes.Quantization in format_distinguishes[format.format]
				else "all"
			),
			(
				hw_acceleration.value
				if ModelAttributes.HWAcceleration in format_distinguishes[format.format]
				else "all"
			),
		]
	)
	return Path(name + format_suffixes[format.format])
