import shutil
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Literal, override

from ai_parade._toolkit.converters._pytorch_base import PyTorchConvertBase
from ai_parade._toolkit.enums import ModelFormat, Quantization, QuantizedModelFormat
from ai_parade._toolkit.run import ModelRunner
from ai_parade._toolkit.run.ONNX import ONNXRunner

from .converter import Converter, ConverterOptions

if TYPE_CHECKING:
	import torch  # type: ignore


def _create_ncnn_model_dir(output_directory: Path, directory_name: Path):
	model_path = output_directory / directory_name
	model_path.mkdir(exist_ok=True)
	(output_directory / "model.ncnn.bin").rename(model_path / "model.bin")
	(output_directory / "model.ncnn.param").rename(model_path / "model.param")


class PNNXPytorchConverter(Converter):
	"""
	https://github.com/Tencent/ncnn/tree/master/tools/pnnx/python
	https://github.com/pnnx/pnnx
	"""

	def __init__(
		self, quantization: Literal[Quantization.none] | Literal[Quantization.float16]
	):
		self.quantization = quantization

	@property
	@override
	def conversion(self):
		return (
			QuantizedModelFormat(ModelFormat.PyTorch),
			QuantizedModelFormat(ModelFormat.NCNN, self.quantization),
		)

	@override
	def create(self, options: ConverterOptions):
		super().create(options)
		return self.PNNXConverter(self.conversion, options)

	class PNNXConverter(PyTorchConvertBase):
		@override
		def _export_call(
			self,
			model: "torch.nn.Module",
			sample_inputs: tuple["torch.Tensor"],
			output_directory: Path,
			**kvargs: Any,
		):
			import pnnx  # type: ignore

			_ = pnnx.export(
				model,
				f"{output_directory}/model.pt",
				sample_inputs,
				fp16=self.conversion[1].quantization == Quantization.float16,
			)
			_create_ncnn_model_dir(output_directory, self.output_weights)


class PNNXConverter(Converter):
	def __init__(self, conversion: tuple[QuantizedModelFormat, QuantizedModelFormat]):
		self._conversion = conversion

	@property
	@override
	def conversion(self):
		return self._conversion

	@override
	def create(self, options: ConverterOptions) -> Callable[[ModelRunner], Path]:
		super().create(options)
		return self.convert

	def convert(self, runner: ModelRunner):
		assert isinstance(runner, ONNXRunner)
		import pnnx  # type: ignore
		import torch  # type: ignore

		shutil.copy(runner.weights, runner.output_directory / "model.onnx")
		# I guess it does not have an option to set output directory (for everything)
		_ = pnnx.convert(
			str(runner.output_directory / "model.onnx"),
			torch.rand(runner.model_metadata.image_input.shape),
			fp16=self.conversion[1].quantization != Quantization.float32,
		)
		_create_ncnn_model_dir(runner.output_directory, self._output_weights)

		return self._output_weights


capabilities: list[Converter] = [
	PNNXPytorchConverter(Quantization.none),
	PNNXPytorchConverter(Quantization.float16),
	PNNXConverter(
		(
			QuantizedModelFormat(ModelFormat.ONNX),
			QuantizedModelFormat(ModelFormat.NCNN),
		)
	),
	PNNXConverter(
		(
			QuantizedModelFormat(ModelFormat.ONNX),
			QuantizedModelFormat(ModelFormat.NCNN, Quantization.float16),
		)
	),
	# following two may not work properly
	PNNXConverter(
		(
			QuantizedModelFormat(ModelFormat.ONNX, Quantization.int8),
			QuantizedModelFormat(ModelFormat.NCNN, Quantization.int8),
		)
	),
	PNNXConverter(
		(
			QuantizedModelFormat(ModelFormat.ONNX, Quantization.float16),
			QuantizedModelFormat(ModelFormat.NCNN, Quantization.float16),
		)
	),
]
