from ..enums import (
	HardwareAcceleration,
	InferenceEngine,
	ModelFormat,
	Platform,
	Quantization,
)
from ._common import ModelAttributes

engine = InferenceEngine.ExecuTorch
capabilities = {
	Platform.Android: {
		Quantization.none: {
			HardwareAcceleration.XNNPACK,
			HardwareAcceleration.VULKAN,
		},
		Quantization.int8: {
			HardwareAcceleration.XNNPACK,
			HardwareAcceleration.VULKAN,
		},
		Quantization.float16: {
			HardwareAcceleration.XNNPACK,
			HardwareAcceleration.VULKAN,
		},
	},
	Platform.IOS: {
		Quantization.none: {
			HardwareAcceleration.XNNPACK,
			# HardwareAcceleration.Metal
			# HardwareAcceleration.CoreML
		},
		Quantization.int8: {
			HardwareAcceleration.XNNPACK,
			# HardwareAcceleration.Metal
			# HardwareAcceleration.CoreML
		},
		Quantization.float16: {
			HardwareAcceleration.XNNPACK,
			# HardwareAcceleration.Metal
			# HardwareAcceleration.CoreML
		},
	},
}

format = ModelFormat.ExecutorTorch
format_distinguishes = [ModelAttributes.Quantization, ModelAttributes.HWAcceleration]
