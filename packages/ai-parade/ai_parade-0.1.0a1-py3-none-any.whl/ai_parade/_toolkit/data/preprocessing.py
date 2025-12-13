from functools import partial
from math import ceil, floor

import cv2 as cv
import numpy as np

from .ImageInput import ImageInput


def resize(
	input: np.ndarray,
	target_size: tuple[int, int],
	padding: None | tuple[float, float, float] = None,
) -> np.ndarray:
	assert len(input.shape) == 3
	assert input.shape[2] == 3
	if padding is not None:
		# mind that x = height, y = width
		x_rescale = target_size[0] / input.shape[0]
		y_rescale = target_size[1] / input.shape[1]
		rescale = min(x_rescale, y_rescale)
		input = cv.resize(
			input, (int(input.shape[1] * rescale), int(input.shape[0] * rescale))
		)
		x_padding = (target_size[0] - input.shape[0]) / 2
		y_padding = (target_size[1] - input.shape[1]) / 2
		input = cv.copyMakeBorder(
			input,
			floor(x_padding),
			ceil(x_padding),
			floor(y_padding),
			ceil(y_padding),
			cv.BORDER_CONSTANT,
			value=padding,
		)
		return input
	else:
		return cv.resize(input, target_size)


def preprocess(mat: np.ndarray, image_input: ImageInput) -> np.ndarray:
	assert len(mat.shape) == 3
	assert mat.shape[2] == 3
	# RGB -> imageInput.channelOrder
	match image_input.channelOrder:
		case ImageInput.ChannelOrder.RGB:
			pass
		case ImageInput.ChannelOrder.RGBA:
			mat = cv.cvtColor(mat, cv.COLOR_RGBA2RGB)
		case ImageInput.ChannelOrder.BGR:
			mat = cv.cvtColor(mat, cv.COLOR_BGR2RGB)
		case ImageInput.ChannelOrder.BGRA:
			mat = cv.cvtColor(mat, cv.COLOR_BGRA2RGB)

	# Resize
	mat_resized = resize(mat, (image_input.width, image_input.height))

	# Convert UINT8 to data type imageInput.dataType
	match image_input.dataType:
		case ImageInput.DataType.FLOAT32:
			mat = mat_resized.astype(np.float32)
		case ImageInput.DataType.UINT8:
			pass

	# Normalize if available
	if image_input.means is not None:
		assert image_input.channels == 3
		mean = np.array(image_input.means, dtype=np.float32)
		mat = cv.subtract(mat, mean)

	if image_input.stds is not None:
		assert image_input.channels == 3
		std = np.array(image_input.stds, dtype=np.float32)
		mat = cv.divide(mat, std)

	# Transpose to the imageInput.dataOrder
	if image_input.dataOrder == ImageInput.DataOrder.NCHW:
		mat = np.transpose(mat, (2, 0, 1))

	return mat


def preprocess_fx(image_input: ImageInput):
	return partial(preprocess, image_input=image_input)
