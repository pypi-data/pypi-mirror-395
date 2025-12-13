from enum import StrEnum


class HardwareAcceleration(StrEnum):
	"""Enumeration for hardware acceleration options."""

	CPU = "CPU"
	GPU = "GPU"
	XNNPACK = "XNNPACK"
	NNAPI = "NNAPI"
	QNN = "QNN"
	VULKAN = "Vulkan"
	OPENGLES = "OpenGLES"
	Mediatek = "Mediatek"
	CoreML = "CoreML"
	Metal = "Metal"
