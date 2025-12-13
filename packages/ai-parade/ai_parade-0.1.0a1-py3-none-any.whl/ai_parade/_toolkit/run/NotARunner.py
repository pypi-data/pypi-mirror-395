import logging
from pathlib import Path
from typing import Any, override

from .ModelRunnerBase import (
	Dataset,
	ModelMetadata,
	ModelOutput,
	ModelRunnerBase,
)

logger = logging.getLogger(__name__)


class NotARunner(ModelRunnerBase["NotARunner", "None"]):
	def __init__(self, model_metadata: ModelMetadata, weights: Path) -> None:
		super().__init__(model_metadata, weights)

	@override
	def __enter__(self):
		return self

	@override
	def __exit__(self, *err: Any):
		self._model = None

	@override
	def inference(self, dataset: Dataset) -> list[ModelOutput]:
		raise NotImplementedError(
			"Not a runner, this model cannot be used for inference on this device"
		)
