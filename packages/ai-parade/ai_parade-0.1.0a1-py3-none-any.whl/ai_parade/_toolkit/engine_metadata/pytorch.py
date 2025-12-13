from ..enums import (
	HardwareAcceleration,
	InferenceEngine,
	ModelFormat,
	Platform,
	Quantization,
)
from ._common import ModelAttributes

engine = InferenceEngine.PyTorch
capabilities = {
	Platform.Windows: {
		Quantization.none: {
			HardwareAcceleration.CPU,
		},
	}
}

format = ModelFormat.PyTorch
format_distinguishes = [ModelAttributes.Quantization]
