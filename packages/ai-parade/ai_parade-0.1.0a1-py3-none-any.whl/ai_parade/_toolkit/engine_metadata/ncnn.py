from ..enums import (
	HardwareAcceleration,
	InferenceEngine,
	ModelFormat,
	Platform,
	Quantization,
)
from ._common import ModelAttributes

engine = InferenceEngine.ncnn
capabilities = {
	Platform.Android: {
		Quantization.none: {
			HardwareAcceleration.CPU,
			HardwareAcceleration.VULKAN,
		},
		Quantization.int8: {
			HardwareAcceleration.CPU,
			HardwareAcceleration.VULKAN,
		},
		Quantization.float16: {
			HardwareAcceleration.CPU,
			HardwareAcceleration.VULKAN,
		},
	},
	Platform.IOS: {
		Quantization.none: {
			HardwareAcceleration.CPU,
			HardwareAcceleration.VULKAN,
		},
		Quantization.int8: {
			HardwareAcceleration.CPU,
			HardwareAcceleration.VULKAN,
		},
		Quantization.float16: {
			HardwareAcceleration.CPU,
			HardwareAcceleration.VULKAN,
		},
	},
}

format = ModelFormat.NCNN
format_distinguishes = [ModelAttributes.Quantization]
