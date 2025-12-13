import numpy as np
import pytest

from ai_parade._toolkit.data import preprocessing


@pytest.mark.parametrize(
	"source_shape, target_shape",
	[
		((10, 10, 3), (10, 10)),
		((11, 11, 3), (10, 10)),
		((9, 9, 3), (10, 10)),
	],
)
def test_resize_resize_valid_shapes(
	source_shape: tuple[int, int, int], target_shape: tuple[int, int]
):
	source_image = np.zeros(source_shape, dtype=np.uint8)

	resized = preprocessing.resize(source_image, target_shape)

	assert resized.shape[:2] == target_shape


@pytest.mark.parametrize(
	"source_shape, target_shape",
	[
		((10, 10, 3), (10, 10)),
		((11, 11, 3), (10, 10)),
		((9, 9, 3), (10, 10)),
	],
)
def test_resize_resize_valid_shapes_with_padding_doing_nothing(
	source_shape: tuple[int, int, int], target_shape: tuple[int, int]
):
	source_image = np.zeros(source_shape, dtype=np.uint8)

	resized = preprocessing.resize(source_image, target_shape, padding=(1, 1, 1))

	assert resized.shape[:2] == target_shape
	assert resized.sum() == 0


@pytest.mark.parametrize(
	"source_shape, target_shape, padding_sum",
	[
		((10, 8, 3), (10, 10), 10 * 2 * 3),
		((11, 8, 3), (10, 10), 10 * 3 * 3),
		((9, 8, 3), (10, 10), 10 * 2 * 3),
	],
)
def test_resize_resize_valid_shapes_with_padding(
	source_shape: tuple[int, int, int], target_shape: tuple[int, int], padding_sum: int
):
	source_image = np.zeros(source_shape, dtype=np.uint8)

	resized = preprocessing.resize(source_image, target_shape, padding=(1, 1, 1))

	assert resized.shape[:2] == target_shape
	assert resized.sum() == padding_sum


def test_resize_resize_not_uniform_padding():
	source_image = np.zeros((10, 1, 3), dtype=np.uint8)

	resized = preprocessing.resize(source_image, (10, 10), padding=(1, 2, 3))

	assert resized.shape[:2] == (10, 10)
	assert resized.sum() == 10 * 9 * (1 + 2 + 3)
