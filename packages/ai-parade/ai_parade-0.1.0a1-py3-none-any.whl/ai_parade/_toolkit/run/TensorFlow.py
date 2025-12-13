import logging
from typing import TYPE_CHECKING, Any, override

if TYPE_CHECKING:
	import tensorflow as tf  # type: ignore

from .ModelRunnerBase import (
	Dataset,
	ModelOutput,
	ModelRunnerBase,
	TReturn,
)

logger = logging.getLogger(__name__)


class TensorFlowRunner(ModelRunnerBase["TensorFlowRunner", "tf.Graph"]):
	@override
	def __enter__(self):
		logger.debug(f"Loading TensorFlow model from {self.weights}")
		raise NotImplementedError
		return self

	@override
	def __exit__(self, *err: Any):
		self._model = None

	@override
	def inference(self, dataset: Dataset) -> list[ModelOutput]:
		logger.info("Running inference on model")
		raise NotImplementedError

		# return self._postprocess(outputs, infos, self.model_metadata)
