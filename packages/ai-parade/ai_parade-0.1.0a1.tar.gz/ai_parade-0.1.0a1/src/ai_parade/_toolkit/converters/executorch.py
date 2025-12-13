from pathlib import Path
from typing import TYPE_CHECKING, Any, override

from ai_parade._toolkit.converters._pytorch_base import PyTorchConvertBase
from ai_parade._toolkit.enums import (
	HardwareAcceleration,
	ModelFormat,
	Quantization,
	QuantizedModelFormat,
)

from .converter import Converter, ConverterOptions

if TYPE_CHECKING:
	import torch  # type: ignore


class Executorch(Converter):
	"""
	https://docs.pytorch.org/executorch/main/using-executorch-export.html
	"""

	def __init__(self, quantization: Quantization):
		self._quantization = quantization

	@property
	@override
	def conversion(self):
		return (
			QuantizedModelFormat(ModelFormat.PyTorch),
			QuantizedModelFormat(ModelFormat.ExecutorTorch, self._quantization),
		)

	@override
	def create(self, options: ConverterOptions):
		super().create(options)
		return self.ExecutorchConverter(self.conversion, options)

	class ExecutorchConverter(PyTorchConvertBase):
		@override
		def _export_call(
			self,
			model: "torch.nn.Module",
			sample_inputs: tuple["torch.Tensor"],
			output_directory: Path,
			**kvargs: Any,
		):
			import torch  # type: ignore
			from executorch.exir import to_edge_transform_and_lower  # type: ignore
			from torchao.quantization.pt2e.quantize_pt2e import (  # type: ignore
				convert_pt2e,
				prepare_pt2e,
			)

			model.eval()
			# ?TODO: add support for dynamic shapes,
			# problem is the executorch doesn't support unbound dims (i.e. [1, inf])
			# and for some reason it complains with sample output batch dim set to 1 that
			# "You marked batch_dim as dynamic but your code specialized it to be a constant (1)"
			dynamic_shapes = ()  # ({0: torch.export.Dim("batch_dim", min=1, max=8)},)
			match self.options.hw_acceleration:
				case HardwareAcceleration.XNNPACK:
					partitioner, quantizer = self.xnnpack_setup()
				case HardwareAcceleration.VULKAN:
					partitioner, quantizer = self.vulkan_setup()
				case _:
					raise NotImplementedError(
						f"{self.options.hw_acceleration} is not supported"
					)
			match self.conversion[1].quantization:
				case Quantization.none:
					pass
				case Quantization.float16:
					# !todo: is this correct?
					model = model.half()
				case Quantization.int8:
					assert self.options.calibration_data is not None

					training_ep = torch.export.export(
						model, sample_inputs, dynamic_shapes=dynamic_shapes
					).module()
					prepared_model = prepare_pt2e(training_ep, quantizer)

					# calibration
					for cal_sample, _, _ in self.options.calibration_data:
						prepared_model(torch.from_numpy(cal_sample))

					model = convert_pt2e(prepared_model)

			executorch_program = to_edge_transform_and_lower(
				torch.export.export(
					model,
					sample_inputs
					if self.conversion[1].quantization != Quantization.float16
					else (sample_inputs[0].half(),),
					dynamic_shapes=dynamic_shapes,
				),
				partitioner=[partitioner],
			).to_executorch()

			with open(output_directory / self.output_weights, "wb") as file:
				file.write(executorch_program.buffer)

		def vulkan_setup(self):
			from executorch.backends.vulkan.partitioner.vulkan_partitioner import (  # type: ignore
				VulkanPartitioner,
			)
			from executorch.backends.vulkan.quantizer.vulkan_quantizer import (  # type: ignore
				VulkanQuantizer,
				get_symmetric_quantization_config,
			)

			qparams = get_symmetric_quantization_config(is_dynamic=False, weight_bits=8)
			quantizer = VulkanQuantizer()
			quantizer.set_global(qparams)

			return VulkanPartitioner(), quantizer

		def xnnpack_setup(self):
			from executorch.backends.xnnpack.partition.xnnpack_partitioner import (  # type: ignore
				XnnpackPartitioner,
			)
			from executorch.backends.xnnpack.quantizer.xnnpack_quantizer import (  # type: ignore
				XNNPACKQuantizer,
				get_symmetric_quantization_config,
			)

			qparams = get_symmetric_quantization_config(is_per_channel=True)
			quantizer = XNNPACKQuantizer()
			quantizer.set_global(qparams)

			return XnnpackPartitioner(), quantizer


capabilities = [
	Executorch(Quantization.none),
	Executorch(Quantization.float16),
	Executorch(Quantization.int8),
]
