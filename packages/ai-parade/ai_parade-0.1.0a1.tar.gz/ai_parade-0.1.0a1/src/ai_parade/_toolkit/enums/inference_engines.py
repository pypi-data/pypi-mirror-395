from enum import StrEnum


class InferenceEngine(StrEnum):
	TensorFlow = "TensorFlow"
	PyTorch = "PyTorch"
	ExecuTorch = "ExecuTorch"
	LiteRT = "LiteRT"
	ncnn = "ncnn"
	ONNXRuntime = "ONNXRuntime"
	# New DL-lib: update here
