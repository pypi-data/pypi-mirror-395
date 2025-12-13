from enum import Enum, StrEnum
from typing import NamedTuple

from .inference_engines import InferenceEngine


class ModelFormat(StrEnum):
	PyTorch = "pytorch"
	ExecutorTorch = "executorch"
	SavedModel = "savedmodel"
	LiteRT = "tflite"
	ONNX = "onnx"
	SNPE = "snpe"
	NCNN = "ncnn"
	MNN = "mnn"
	bolt = "bolt"
	MACE = "mace"
	PaddleLite = "paddlelite"
	# New DL-lib: update here


class Quantization(Enum):
	none = "float32"
	float32 = "float32"
	float16 = "float16"
	int8 = "int8"
	int4 = "int4"


class QuantizedModelFormat(NamedTuple):
	"""
	Represents a quantized or non-quantized model format.
	"""

	format: ModelFormat
	quantization: Quantization = Quantization.none


formats_preferred_inference_engine: dict[ModelFormat, InferenceEngine] = {
	ModelFormat.LiteRT: InferenceEngine.LiteRT,
	ModelFormat.NCNN: InferenceEngine.ncnn,
	ModelFormat.ONNX: InferenceEngine.ONNXRuntime,
	ModelFormat.PyTorch: InferenceEngine.PyTorch,
	ModelFormat.SavedModel: InferenceEngine.TensorFlow,
}

format_suffixes: dict[ModelFormat, str] = {
	ModelFormat.SavedModel: ".savedmodel",
	ModelFormat.PyTorch: ".pth",
	ModelFormat.SavedModel: ".pb",
	ModelFormat.LiteRT: ".tflite",
	ModelFormat.ONNX: ".onnx",
	# this should be directory with ncnn.param and ncnn.bin
	ModelFormat.NCNN: ".ncnn",
	ModelFormat.ExecutorTorch: ".pte",
	# New DL-lib: update here
}
