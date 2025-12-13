from pathlib import Path
from typing import override

from .FileDataset import FileDataset


class COCO(FileDataset):
	def __init__(
		self,
		data_dir: Path,
		annotations_path: Path,
	):
		self._data_dir = data_dir
		self._annotations_path = annotations_path

	@override
	def walk(self):
		"""Walk the dataset directory tree.

		Returns:
			 iterator of tuples of (path to the annotation file and path to the data file)
		"""
		raise NotImplementedError()
