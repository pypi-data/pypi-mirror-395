import importlib
import importlib.util
import logging
import sys
from contextlib import contextmanager
from pathlib import Path
from types import ModuleType
from typing import TYPE_CHECKING, Any, Callable, final, override
from xmlrpc.client import boolean

from ai_parade._toolkit.metadata.models.pyproject import InlineCode
from ai_parade._toolkit.sys_path_checkpoint import SysPathCheckpoint

from .ModelRunnerBase import (
	Dataset,
	ModelMetadata,
	ModelRunnerBase,
	structural_map,
)

if TYPE_CHECKING:
	import torch  # type: ignore

logger = logging.getLogger(__name__)


class PyTorchRunner(ModelRunnerBase["PyTorchRunner", "torch.nn.Module"]):
	def __init__(self, model_metadata: ModelMetadata, weights: Path):
		"""Interacts with a model

		There are these methods for overriding:
		- `inference_call`: the call to the model
		- `postprocess`: the postprocessing of the output
		- `load_weights`: the loading of the weights
		- `get_yacs_config`: the loading of the yacs config

		Args:
			model_metadata: metadata
			weights: Path to the model weights
		"""

		super().__init__(model_metadata, weights)
		if model_metadata.pytorch is None:
			raise RuntimeError("No way of constructing model, no `pytorch` key")
		self.run_parameters = model_metadata.pytorch
		self._model = None

	@final
	@property
	@override
	def model(self):
		assert self._model is not None
		return self._model

	@final
	def _to_cpu_numpy(self, x: Any, to_cpu: bool = True, to_numpy: bool = True):
		import torch  # type: ignore

		if isinstance(x, torch.Tensor):
			x = x.detach()
			if to_cpu:
				x = x.to("cpu")
			if to_numpy:
				x = x.numpy()
			return x
		elif isinstance(x, dict):
			return {k: self._to_cpu_numpy(v) for k, v in x.items()}
		elif isinstance(x, list) or isinstance(x, tuple):
			return [self._to_cpu_numpy(v) for v in x]
		else:
			raise TypeError(f"Unsupported type: {type(x)}")

	def _inference_call(self, tensor: "torch.Tensor") -> "torch.Tensor":
		assert self.model is not None
		return self.model(tensor)

	@final
	@override
	def inference(self, dataset: Dataset):
		logger.info("Running inference on model")
		import torch  # type: ignore

		# self.model.to("cuda")
		self.model.eval()
		outputs = []
		infos = []
		for x, _, data_info in dataset:
			tensor = torch.from_numpy(x)  # .to("cuda")
			with torch.no_grad():
				raw_output = self._inference_call(tensor)
			outputs.append(self._to_cpu_numpy(raw_output))
			infos.append(data_info)

		return self._postprocess(outputs, infos, self.model_metadata)

	@override
	def get_model_size(self) -> int | None:
		downloaded_size = super().get_model_size()
		if downloaded_size is not None:
			return downloaded_size
		with self.not_downloaded():
			param_size = 0
			for param in self.model.parameters():
				param_size += param.nelement() * param.element_size()

			buffer_size = 0
			for buffer in self.model.buffers():
				buffer_size += buffer.nelement() * buffer.element_size()

			return param_size + buffer_size

	@contextmanager
	def not_downloaded(self):
		try:
			yield self.__parametrized_enter(should_load_weights=False)
		finally:
			# ?todo: where to get exception parameters?
			self.__exit__()

	@final
	@override
	def __enter__(self):
		"""
		Initialize the model. Load the weights.
		"""
		return self.__parametrized_enter(should_load_weights=True)

	def __parametrized_enter(self, should_load_weights: boolean):
		logger.debug(f"Loading PyTorch model with weights at {self.weights}")
		assert self.model_metadata.repository_path is not None

		self.sys_path_checkpoint = SysPathCheckpoint(
			self.model_metadata.repository_path
		)
		self.sys_path_checkpoint.__enter__()

		args: list[Any] = []
		if self.run_parameters.yacs_configs is not None:
			args.append(self._get_yacs_config(self.run_parameters.yacs_configs))

		if self.run_parameters.model_init_expression is not None:
			logger.debug(
				f"Running `model_init_expression: {self.run_parameters.model_init_expression}`"
			)
			code = self.run_parameters.model_init_expression
			# has to return the model, without weight initialization
			self._model = self.__load_weights(
				lambda module: eval(code), should_load_weights
			)
		elif self.run_parameters.model_init_fx is not None:
			logger.debug(
				f"Running `model_init_fx: {self.run_parameters.model_init_fx}`"
			)
			model_init_fx = self.run_parameters.model_init_fx
			self._model = self.__load_weights(
				lambda module: getattr(
					module or sys.modules[__name__],
					model_init_fx,
				)(*args),
				should_load_weights,
			)

		else:
			assert False, "It should fail the validation during parsing"

		return self

	@final
	@override
	def __exit__(self, *err: Any):
		self._model = None
		assert self.model_metadata.repository_path is not None
		self.sys_path_checkpoint.__exit__(*err)

	def __load_weights(
		self,
		init_fx: Callable[[ModuleType | None], "torch.nn.Module"],
		should_load_weights: boolean,
	) -> "torch.nn.Module":
		import torch  # type: ignore

		logger.debug("Loading the model weights")
		if self.run_parameters.model_import is not None:
			logger.debug(
				f"Importing `model_import: {self.run_parameters.model_import}`"
			)
			try:
				model_module = importlib.import_module(self.run_parameters.model_import)
			except ModuleNotFoundError as e:
				if self.run_parameters.model_import in str(e):
					logger.warning(
						f"Can't import as module\n  defined as metadata.model_import = {self.run_parameters.model_import}"
					)
					logger.info(f"Failed with error: {str(e)}")
					# todo: this will probably never fix anything, because there should be implicit namespace packages

					assert self.model_metadata.repository_path is not None
					import_components = self.run_parameters.model_import.split(".")
					spec = importlib.util.spec_from_file_location(
						import_components[-1],
						Path(
							self.model_metadata.repository_path,
							*import_components[:-1],
							import_components[-1] + ".py",
						),
					)
					if spec is not None:
						logger.debug(
							"Importing it as a file, the error could be caused by missing `__init__.py`"
						)
						model_module = importlib.util.module_from_spec(spec)
						spec.loader.exec_module(model_module)  # type: ignore
					else:
						raise e
				else:
					raise e

		else:
			model_module = None

		model = init_fx(model_module)
		if not should_load_weights:
			return model
		if not self.weights.exists():
			raise FileNotFoundError(
				f"Model weights not found: {self.weights.resolve()}"
			)
		loaded_data = torch.load(
			self.weights,
			weights_only=True,
			map_location="cpu",
		)
		state_dict = structural_map(
			loaded_data,
			self.run_parameters.load_mapping
			if self.run_parameters.load_mapping is not None
			else "state_dict",
		)["state_dict"]

		model.load_state_dict(state_dict)
		return model

	def _get_yacs_config(self, yacs_configs: tuple[str | InlineCode, ...]) -> Any:
		logger.debug("Loading the yacs configs")
		# todo: where is it checked?
		assert self.model_metadata.repository_path is not None

		base_config = yacs_configs[0]
		if not isinstance(base_config, str):
			raise RuntimeError()

		cfg = importlib.import_module(base_config).cfg  # todo: or not?
		for config_file in yacs_configs[1:]:
			if isinstance(config_file, str):
				cfg.merge_from_file(self.model_metadata.repository_path / config_file)
			else:
				exec(config_file["code"])
		return cfg
