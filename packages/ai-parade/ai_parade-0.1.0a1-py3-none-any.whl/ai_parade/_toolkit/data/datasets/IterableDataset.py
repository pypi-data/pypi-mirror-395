from typing import (
	Callable,
	Iterable,
	override,
)

import numpy as np

from ..output import ModelOutput
from .Dataset import Dataset, DatasetInfo, Output_unbatched


class IteratorDataset(Dataset[Output_unbatched]):
	"""Dataset wrapper for an iterable"""

	def __init__(
		self, iterable: Callable[[], Iterable[tuple[np.ndarray, ModelOutput]]]
	):
		super().__init__()
		self._source_iterable = iterable

	@override
	def walk(self) -> Iterable[Output_unbatched]:
		for i, (data, annotations) in enumerate(self._source_iterable()):
			info = DatasetInfo(
				source_data_shape=data.shape,
				data_source=f"{type(self).__name__}[{i}]",
				data_shape=data.shape,
			)
			yield data, annotations, info

	@override
	def parse_data(
		self, iterable: Iterable[Output_unbatched]
	) -> Iterable[Output_unbatched]:
		return iterable
