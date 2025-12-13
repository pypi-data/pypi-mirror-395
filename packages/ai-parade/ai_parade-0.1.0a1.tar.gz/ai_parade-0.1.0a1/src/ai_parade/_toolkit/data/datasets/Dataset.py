import itertools
import logging
import random
from abc import ABC, abstractmethod
from copy import copy as copy_object
from functools import partial
from typing import (
	Any,
	Callable,
	Generic,
	Iterable,
	Iterator,
	NamedTuple,
	Sequence,
	TypeVar,
	override,
)

import numpy as np

from ai_parade._toolkit.constants import TRACE_LVL

from ..ImageInput import ImageInput
from ..output import ModelOutput
from ..preprocessing import preprocess_fx

logger = logging.getLogger(__name__)


class DatasetInfo(NamedTuple):
	source_data_shape: Sequence[int]
	data_shape: Sequence[int]
	data_source: str


Output_batched = tuple[np.ndarray, Sequence[ModelOutput], Sequence[DatasetInfo]]
Output_unbatched = tuple[np.ndarray, ModelOutput, DatasetInfo]


TWalkOutput = TypeVar("TWalkOutput")


class Dataset(ABC, Iterable[Output_batched], Generic[TWalkOutput]):
	"""Abstract class for datasets

	This class implements common functionality for datasets, such as
	- preprocessing, map
	- skip, take
	- shuffle
	- adding metadata of its source

	Remarks:
		The dataset must be picklable. This mean we can't store generators or lambdas :-(
		As a workaround we can put them in functions and create them when needed

	"""

	def __init__(self):
		self._iterable_transformations: list[
			Callable[[Iterable[Output_unbatched]], Iterable[Output_unbatched]]
		] = []
		self._preload_transformations: list[
			Callable[[Iterable[Any]], Iterable[Any]]
		] = []

		self._batch_size: int = 1
		self._skip_last_batch = False

	@abstractmethod
	def walk(self) -> Iterable[TWalkOutput]:
		"""Walk through the dataset and yield data

		This should be cheap and stable operation.
		The data loading should be done in the parse_data method.

		Returns:
			Iterable of data
		"""
		pass

	@abstractmethod
	def parse_data(
		self, iterable: Iterable[TWalkOutput], should_load: bool
	) -> Iterable[Output_unbatched]:
		"""Parse the data from the iterable and yield data, annotations and info

		Args:
			iterable: Iterable with format of walk method
			should_load: Whether to load the data, or load just annotations

		Returns:
			Ready to use data
		"""
		pass

	@override
	def __iter__(
		self,
	) -> Iterator[Output_batched]:
		return self._iter_implementation(batching=True)  # type: ignore

	def no_batch_iterator(
		self,
	) -> Iterator[Output_unbatched]:
		"""Return an iterator without batching

		Returns:
			Iterator of unbatched data
		"""
		return self._iter_implementation(batching=False)  # type: ignore

	def no_load_iterator(
		self,
	) -> Iterator[Output_unbatched]:
		"""Return an iterator of only annotations

		Returns:
			Iterator of unbatched annotations without data
		"""
		return self._iter_implementation(batching=False, should_load=False)  # type: ignore

	def _iter_implementation(
		self, batching: bool, should_load: bool = True
	) -> Iterator[Output_batched | Output_unbatched]:
		logger.debug("Created iterator")
		logger.log(
			TRACE_LVL,
			"Iterator with transformations: \n"
			f"{self._preload_transformations}\n"
			f"{self._iterable_transformations}\n",
		)

		iterable = self.walk()

		# run data independent transformations i.e. take, skip
		for transform in self._preload_transformations:
			iterable = transform(iterable)

		# load the data
		iterable = self.parse_data(iterable, should_load)  # type: ignore

		# run data dependent transformations
		for transform in self._iterable_transformations:
			iterable = transform(iterable)

		iterable = self._set_final_info(iterable)

		if batching:
			iterable = self._batched(iterable)

		for x in iterable:
			yield x

	def _set_final_info(
		self, iterable: Iterable[Output_unbatched]
	) -> Iterable[Output_unbatched]:
		for data, annotations, info in iterable:
			info = info._replace(data_shape=data.shape)
			yield data, annotations, info

	def _batched(
		self, iterable: Iterable[Output_unbatched]
	) -> Iterable[Output_batched]:
		assert self._batch_size is not None
		# save current values in the iterator
		batch_size = self._batch_size
		skip_last_batch = self._skip_last_batch

		batch_data = []
		batch_annotations = []
		batch_info = []
		for data, annotations, info in iterable:
			batch_data.append(data)
			batch_annotations.append(annotations)
			batch_info.append(info)
			if len(batch_data) == batch_size:
				yield np.array(batch_data), batch_annotations, batch_info
				batch_data = []
				batch_annotations = []
				batch_info = []

		if len(batch_data) != 0 and not skip_last_batch:
			yield np.array(batch_data), batch_annotations, batch_info

	def show(self, n: int | None = None) -> Output_batched | list[Output_batched]:
		"""Show the first n elements of the dataset"

		Args:
			n: number of elements to show. If None, show only the first element
		Returns:
			First n elements of the dataset or the first element if n is None
		"""
		stop = n or 1
		result = list(itertools.islice(self, stop))
		return result[0] if n is None else result

	def take(self, n: int):
		"""Take the first n elements of the dataset

		Args:
			n: number of elements to take
		Returns:
			Dataset with the first n elements
		"""
		copy = copy_object(self)
		copy._preload_transformations = self._preload_transformations.copy()
		copy._preload_transformations.append(partial(self._islice, start=0, stop=n))
		return copy

	@staticmethod
	def _shuffle(
		iterable: Iterable[Output_unbatched], seed: int | None
	) -> Iterable[Output_unbatched]:
		if seed is not None:
			random.seed(seed)
		shuffled = list(iterable)
		random.shuffle(shuffled)
		return shuffled

	def shuffle(self, seed: int | None = None):
		"""Shuffle the dataset

		Args:
			seed: seed for the random number generator
		Returns:
			Shuffled dataset
		"""
		copy = copy_object(self)
		copy._iterable_transformations = self._iterable_transformations.copy()
		copy._iterable_transformations.append(partial(self._shuffle, seed=seed))
		return copy

	@staticmethod
	def _map(
		iterable: Iterable[Output_unbatched], fx: Callable[[np.ndarray], np.ndarray]
	):
		for data, annotations, info in iterable:
			yield fx(data), annotations, info

	def map(self, fx: Callable[[np.ndarray], np.ndarray]):
		"""Transform the data with a function

		Args:
			fx: function to transform each element of the dataset
		Returns:
			Transformed dataset
		"""
		copy = copy_object(self)
		copy._iterable_transformations = self._iterable_transformations.copy()
		copy._iterable_transformations.append(partial(self._map, fx=fx))
		return copy

	def preprocess(self, image_input: ImageInput):
		"""Convert data to the format of the model

		Args:
			image_input: image input to convert the data to
		Returns:
			Transformed dataset
		"""

		return self.map(preprocess_fx(image_input)).set(
			batch_size=image_input.batchSize
		)

	@staticmethod
	def _islice(iterable: Iterable, start: int | None, stop: int | None):
		return itertools.islice(iterable, start, stop)

	def skip(self, n: int):
		"""Skip the first n elements of the dataset

		Args:
			n: number of elements to skip
		Returns:
			Dataset with the first n elements skipped
		"""
		copy = copy_object(self)
		copy._preload_transformations = self._preload_transformations.copy()
		copy._preload_transformations.append(partial(self._islice, start=n, stop=None))
		return copy

	@property
	def batch_size(self):
		return self._batch_size

	@property
	def skip_last_batch(self):
		return self._skip_last_batch

	def set(
		self, *, batch_size: int | None = None, skip_last_batch: bool | None = None
	) -> "Dataset":
		"""Set dataset properties

		Args:
			batch_size: size of the batch
			skip_last_batch: skip the last batch if it is smaller than the batch size
		Returns:
			Dataset with the batch size and skip_last_batch set
		"""
		copy = copy_object(self)
		copy._batch_size = batch_size or self._batch_size
		copy._skip_last_batch = skip_last_batch or self._skip_last_batch
		return copy
