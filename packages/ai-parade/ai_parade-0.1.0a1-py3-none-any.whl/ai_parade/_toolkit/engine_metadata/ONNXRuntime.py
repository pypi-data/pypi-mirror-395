from ..enums import (
	HardwareAcceleration,
	InferenceEngine,
	ModelFormat,
	Platform,
	Quantization,
)
from ._common import ModelAttributes

engine = InferenceEngine.ONNXRuntime
capabilities = {
	Platform.Android: {
		Quantization.none: {
			HardwareAcceleration.CPU,
			HardwareAcceleration.XNNPACK,
			HardwareAcceleration.NNAPI,
			#HardwareAcceleration.QNN,
		},
		Quantization.int8: {
			HardwareAcceleration.CPU,
			HardwareAcceleration.XNNPACK,
			HardwareAcceleration.NNAPI,
			#HardwareAcceleration.QNN,
		},
		Quantization.float16: {
			HardwareAcceleration.CPU,
			HardwareAcceleration.XNNPACK,
			HardwareAcceleration.NNAPI,
			#HardwareAcceleration.QNN,
		},
	},
	Platform.IOS: {
		Quantization.none: {
			HardwareAcceleration.CPU,
			HardwareAcceleration.XNNPACK,
			HardwareAcceleration.CoreML,
		},
		Quantization.int8: {
			HardwareAcceleration.CPU,
			HardwareAcceleration.XNNPACK,
			HardwareAcceleration.CoreML,
		},
		Quantization.float16: {
			HardwareAcceleration.CPU,
			HardwareAcceleration.XNNPACK,
			HardwareAcceleration.CoreML,
		},
	},
}

format = ModelFormat.ONNX
format_distinguishes = [ModelAttributes.Quantization]
