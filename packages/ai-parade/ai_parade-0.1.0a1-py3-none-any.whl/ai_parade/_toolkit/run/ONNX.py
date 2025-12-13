import logging
from pathlib import Path
from typing import TYPE_CHECKING, Any, override

if TYPE_CHECKING:
	import onnxruntime as ort  # type: ignore

from .ModelRunnerBase import (
	Dataset,
	ModelMetadata,
	ModelOutput,
	ModelRunnerBase,
)

logger = logging.getLogger(__name__)


class ONNXRunner(ModelRunnerBase["ONNXRunner", "ort.InferenceSession|None"]):
	INPUT_NAME = "input"

	def __init__(self, model_metadata: ModelMetadata, weights: Path) -> None:
		super().__init__(model_metadata, weights)
		self.is_entered = False
		self._model = None

	@override
	def __enter__(self):
		try:
			import onnxruntime as ort  # type: ignore

			logger.debug(f"Loading ONNX model from {self.weights}")

			self._model = ort.InferenceSession(self.weights)
		except ImportError:
			logger.warning("ONNX runtime not installed, cannot run inference")
			import onnx  # type: ignore
		self.is_entered = True
		return self

	@override
	def __exit__(self, *err: Any):
		self._model = None

	@override
	def inference(self, dataset: Dataset) -> list[ModelOutput]:
		if self.model is None:
			raise RuntimeError("ONNX runtime not installed, cannot run inference")

		logger.info("Running inference on model")

		outputs = []
		infos = []
		for data, _, data_info in dataset:
			outputs.append(self.model.run(None, {self.INPUT_NAME: data})[0])
			infos.append(data_info)

		return self._postprocess(outputs, infos, self.model_metadata)

	@property
	@override
	def model(self):
		return self._model
