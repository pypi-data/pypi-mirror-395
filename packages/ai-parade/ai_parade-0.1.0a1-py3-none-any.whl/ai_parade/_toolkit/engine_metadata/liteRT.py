from ..enums import (
	HardwareAcceleration,
	InferenceEngine,
	ModelFormat,
	Platform,
	Quantization,
)
from ._common import ModelAttributes

engine = InferenceEngine.LiteRT
capabilities = {
	Platform.Android: {
		Quantization.none: {
			HardwareAcceleration.CPU,
			HardwareAcceleration.XNNPACK,
			HardwareAcceleration.NNAPI,
			HardwareAcceleration.OPENGLES,
		},
		Quantization.int8: {
			HardwareAcceleration.CPU,
			HardwareAcceleration.XNNPACK,
			HardwareAcceleration.NNAPI,
			HardwareAcceleration.OPENGLES,
		},
		Quantization.float16: {
			HardwareAcceleration.CPU,
			HardwareAcceleration.XNNPACK,
			HardwareAcceleration.NNAPI,
			HardwareAcceleration.OPENGLES,
		},
	},
	Platform.IOS: {
		Quantization.none: {
			HardwareAcceleration.CPU,
			HardwareAcceleration.XNNPACK,
			HardwareAcceleration.OPENGLES,
		},
		Quantization.int8: {
			HardwareAcceleration.CPU,
			HardwareAcceleration.XNNPACK,
			HardwareAcceleration.OPENGLES,
		},
		Quantization.float16: {
			HardwareAcceleration.CPU,
			HardwareAcceleration.XNNPACK,
			HardwareAcceleration.OPENGLES,
		},
	},
}

format = ModelFormat.LiteRT
format_distinguishes = [ModelAttributes.Quantization]
