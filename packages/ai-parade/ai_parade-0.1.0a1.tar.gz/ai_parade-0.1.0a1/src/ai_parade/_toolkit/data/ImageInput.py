from dataclasses import dataclass
from enum import StrEnum
from typing import List, Optional


@dataclass(frozen=True)
class ImageInput:
	"""
	Represents the input specification for a CV model.
	"""

	batchSize: int
	"""Number of images in a single batch."""

	height: int
	"""Height of the input image."""

	width: int
	"""Width of the input image."""

	channelOrder: "ImageInput.ChannelOrder"
	"""Order of color channels in the image."""

	dataOrder: "ImageInput.DataOrder"
	"""Order of data dimensions."""

	dataType: "ImageInput.DataType"
	"""Data type of the image pixels."""

	means: Optional[List[float]] = None
	"""Mean values for normalization, per channel."""

	stds: Optional[List[float]] = None
	"""Standard deviation values for normalization, per channel."""

	@property
	def channels(self) -> int:
		"""
		Number of channels in the image.
		"""
		return (
			4
			if self.channelOrder
			in {ImageInput.ChannelOrder.RGBA, ImageInput.ChannelOrder.BGRA}
			else 3
		)

	@property
	def shape(self) -> List[int]:
		"""
		Shape of the input image, including batch size
		"""
		return (
			[self.batchSize, self.channels, self.height, self.width]
			if self.dataOrder == ImageInput.DataOrder.NCHW
			else [self.batchSize, self.height, self.width, self.channels]
		)

	class DataOrder(StrEnum):
		"""Enumeration for data order formats."""

		NHWC = "NHWC"
		NCHW = "NCHW"

	class DataType(StrEnum):
		"""Enumeration for data types."""

		UINT8 = "UINT8"
		FLOAT32 = "FLOAT32"

	class ChannelOrder(StrEnum):
		"""Enumeration for channel order types."""

		RGB = "RGB"
		BGR = "BGR"
		RGBA = "RGBA"
		BGRA = "BGRA"
