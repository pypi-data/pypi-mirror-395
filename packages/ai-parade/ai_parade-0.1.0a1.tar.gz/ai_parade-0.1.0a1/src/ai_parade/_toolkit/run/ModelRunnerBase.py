import logging
from typing import Any, Callable, Generic, Sequence, override

from ai_parade._toolkit.data.datasets.Dataset import Dataset as Dataset
from ai_parade._toolkit.data.datasets.Dataset import DatasetInfo
from ai_parade._toolkit.data.output import ModelOutput
from ai_parade._toolkit.data.postprocessing import postprocess
from ai_parade._toolkit.metadata.models.final import ModelMetadata
from ai_parade._toolkit.run.ModelRunner import (  # type: ignore
	LoadedModelRunner,
	ModelRunner,
	TChild,
	TModel,
	TReturn,
)
from ai_parade._toolkit.structural_mapping import structural_map

logger = logging.getLogger(__name__)


# backward compatibility <=3.11: generic class notation
class ModelRunnerBase(
	Generic[TChild, TModel],
	ModelRunner[TChild, TModel],
	LoadedModelRunner[TChild, TModel],
):
	def _postprocess(
		self,
		outputs: list[Any],
		infos: list[Sequence[DatasetInfo]],
		model_metadata: ModelMetadata,
	):
		results: list[ModelOutput] = []
		for output_batch, info_batch in zip(outputs, infos):
			for output, model_info in zip(output_batch, info_batch):
				mapped = self._output_mapping(output, model_metadata)
				results.append(postprocess(mapped, model_info))

		return results

	@staticmethod
	def _output_mapping(output: Any, model_metadata: ModelMetadata) -> ModelOutput:
		# ?todo: use pydantic to check types? ... only in debug mode
		return structural_map(
			output,
			model_metadata.output_mapping,
			model_metadata.output_mapping_values,
		)

	@override
	def run(self, what: Callable[[TChild], TReturn]) -> TReturn:
		logger.debug("Running %s", what)
		return what(self)  # type: ignore
