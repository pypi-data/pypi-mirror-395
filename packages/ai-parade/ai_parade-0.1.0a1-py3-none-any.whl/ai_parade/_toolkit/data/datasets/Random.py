from typing import Iterable, override

import numpy as np

from .Dataset import Dataset, DatasetInfo, ImageInput, Output_unbatched


class Random(Dataset[None]):
	"""Dataset with random data of the ImageInput specifications"""

	def __init__(self, image_input: ImageInput, seed: int | None = None):
		super().__init__()
		self._image_input = image_input
		self._batch_size = image_input.batchSize
		self._seed = seed

	@override
	def walk(self) -> Iterable[None]:
		while True:
			yield None

	@override
	def parse_data(
		self, iterable: Iterable[None], should_load: bool
	) -> Iterable[Output_unbatched]:
		rng = np.random.RandomState(self._seed)
		shape = self._image_input.shape[1:]
		for _ in iterable:
			match self._image_input.dataType:
				case ImageInput.DataType.FLOAT32:
					data = rng.rand(*shape).astype(np.float32)
				case ImageInput.DataType.UINT8:
					data = rng.randint(
						0,
						255,
						size=shape,
						dtype=np.uint8,
					)
			yield (
				data,
				{},
				DatasetInfo(
					source_data_shape=shape,
					data_source="Random",
					data_shape=shape,
				),
			)

	@override
	def preprocess(self, image_input: ImageInput):
		return Random(image_input)
