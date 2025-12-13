from abc import ABC
from pathlib import Path
from typing import (
	Iterable,
	cast,
	override,
)

import cv2 as cv
import numpy as np

from ai_parade._toolkit.structural_mapping import ObjectMapping

from ..output import ModelOutput
from .Dataset import Dataset, DatasetInfo, Output_unbatched


class FileDataset(Dataset[tuple[Path, dict]], ABC):
	"""Dataset from files.
	Loads and parses image data.
	The source of the data is provided from derived classes by implementing walk().
	"""

	def __init__(
		self,
		annotation_mapping: ObjectMapping,
	) -> None:
		super().__init__()
		self._annotation_mapping = annotation_mapping

	@override
	def parse_data(
		self, iterable: Iterable[tuple[Path, dict]], should_load: bool
	) -> Iterable[Output_unbatched]:
		for data, annotation in iterable:
			if should_load:
				image = cv.imread(str(data))
			else:
				image = np.array([])
			annotation = self._annotation_mapping(annotation)

			if __debug__:
				import pydantic

				annotation = pydantic.TypeAdapter(ModelOutput).validate_python(
					annotation
				)
			else:
				annotation = cast(ModelOutput, annotation)

			info = DatasetInfo(
				source_data_shape=image.shape,
				data_source=str(data),
				data_shape=image.shape,
			)
			yield image, annotation, info
