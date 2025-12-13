from ai_parade._toolkit.enums import ModelFormat, Quantization, QuantizedModelFormat

from .ai_edge_torch import capabilities as ai_edge_torch_capabilities
from .converter import Converter
from .executorch import capabilities as executorch_capabilities
from .nobuco import NobucoConverter
from .onnx import ONNX_Quantization
from .onnx2tf import ONNX2TensorFlowConverter
from .onnx_tf import ONNX_TensorFlowConverter
from .pnnx import capabilities as pnnx_capabilities
from .pytorch import PyTorch_onnx_export

_priority_list: list[Converter] = (
	[
		# top priority first
		# to quantized, to edge formats:
		ONNX_Quantization(Quantization.int8),
		ONNX_Quantization(Quantization.float16),
		PyTorch_onnx_export(),
	]
	+ executorch_capabilities
	+ pnnx_capabilities
	+ ai_edge_torch_capabilities
	# 3rd party:
	+ [
		NobucoConverter(),
		ONNX2TensorFlowConverter(),
	]
	# not maintained:
	+ [
		ONNX_TensorFlowConverter(),
	]
)

# adjacency list, keyed by the source node/format
_converter_from: dict[QuantizedModelFormat, list[Converter]] = {
	QuantizedModelFormat(source_format, source_quantization): []
	for source_format in ModelFormat
	for source_quantization in Quantization
}
for converter in _priority_list:
	source_format, target_format = converter.conversion
	assert source_format is not None and target_format is not None
	_converter_from[source_format].append(converter)


def get_converter(
	source_format: QuantizedModelFormat, target_format: QuantizedModelFormat
) -> list[list[Converter]]:
	"""
	Gets the list of converters that can convert from `source_format` to `target_format`.
	Returns a list of conversion chains.
	A conversion chain is a list of conversions from `source_format` via intermediate formats to `target_format`.
	The chains are sorted from the most reasonable one (most likely to work and be correct), others are there as fallback.

	Args:
		source_format (QuantizedModelFormat): the source format
		target_format (QuantizedModelFormat): the target format

	Returns:
		list[list[Converter]]: the list of conversion chains
	"""
	open_conversion_chains: list[tuple[QuantizedModelFormat, list[Converter]]] = [
		(source_format, [])
	]

	conversion_chains: list[list[Converter]] = []

	# BFS:
	while len(open_conversion_chains) > 0:
		chain_target_format, this_chain = open_conversion_chains.pop()
		for converter in _converter_from[chain_target_format]:
			new_chain_target_format = converter.conversion[1]

			# we found the target
			if new_chain_target_format == target_format:
				conversion_chains.append(this_chain + [converter])
				break

			# we are in a loop
			if new_chain_target_format in this_chain:
				break

			open_conversion_chains.append(
				(new_chain_target_format, this_chain + [converter])
			)

	return conversion_chains
