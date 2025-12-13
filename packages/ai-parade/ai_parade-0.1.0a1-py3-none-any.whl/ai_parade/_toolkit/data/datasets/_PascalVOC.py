import os
from pathlib import Path
from typing import override

import xmltodict

from .FileDataset import FileDataset, ObjectMapping


class PascalVOC(FileDataset):
	def __init__(
		self,
		dataset_path: Path,
		annotation_mapping: ObjectMapping,
		annotations_dir: str = "Annotations",
		data_dir: str = "Data",
	):
		super().__init__(annotation_mapping)
		self._dataset_path = dataset_path
		self._data_path = dataset_path / data_dir
		self._annotations_path = dataset_path / annotations_dir

		if not self._data_path.exists():
			raise ValueError(f"Data directory {self._data_path} does not exist")
		if not self._annotations_path.exists():
			raise ValueError(f"Annotations directory {self._annotations_path} does not exist")

	@override
	def walk(self):
		"""Walk the dataset directory tree.

		Returns:
			 iterator of tuples of (path to the annotation file and path to the data file)
		"""
		""" Example paths:
		- Data/VID/test/ILSVRC2015_test_00000000/000000.JPEG
		- Data/VID/train/ILSVRC2015_VID_train_0000/ILSVRC2015_train_00000000/000000.JPEG
		- Annotations/VID/train/ILSVRC2015_VID_train_0000/ILSVRC2015_train_00000000/000000.xml
		"""
		# backward compatibility <=3.11: path.walk not available
		path, _, files = os.walk(self._data_path, topdown=False).__next__()
		image_suffix = (Path(path) / files[0]).suffix

		for path, dirs, files in os.walk(self._annotations_path):
			# this makes the walking of the directories in sorted order
			# https://stackoverflow.com/a/18282602/5739006
			dirs.sort()
			for file in sorted(files):
				annotation_path = Path(path) / file
				with open(annotation_path) as fd:
					annotation = xmltodict.parse(fd.read())
				data_path = annotation_path.relative_to(self._annotations_path)
				data_path = data_path.with_suffix(image_suffix)
				yield self._data_path / data_path, annotation
