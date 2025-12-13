from ..enums import (
	HardwareAcceleration,
	InferenceEngine,
	ModelFormat,
	Platform,
	Quantization,
)
from ._common import ModelAttributes

engine = InferenceEngine.TensorFlow
capabilities = {
	Platform.Windows: {
		Quantization.none: {
			HardwareAcceleration.CPU,
		},
	}
}

format = ModelFormat.SavedModel
format_distinguishes = [ModelAttributes.Quantization]
