from typing import Annotated, Any, Mapping, Optional

from pydantic import (
	BaseModel,
	ConfigDict,
	StringConstraints,
	field_validator,
	model_validator,
)

# backward compatibility <=3.11: typeddict from here
from typing_extensions import TypedDict

from ai_parade._toolkit.data.ImageInput import ImageInput
from ai_parade._toolkit.enums import ModelFormat
from ai_parade._toolkit.structural_mapping import MappingDefinition

from ..enums import ModelTasks


class InlineCode(TypedDict):
	code: str


NAME_REGEX = "^[-+ _.a-zA-Z0-9]*$"


class ModelMetadataPyproject(BaseModel):
	"""
	pyproject.toml [tool.ai-parade] options for model registration.
	"""

	model_config = ConfigDict(validate_assignment=False, extra="forbid")

	# Basic information about the model #
	#####################################

	name: Annotated[str, StringConstraints(pattern=NAME_REGEX, min_length=1)]
	"""
	Name of the model

	There are some restrictions:
	- it must be unique in the repository
	"""

	family: str | None = None
	"""
	Used to group models.
	"""

	size: float | None = None
	"""
	Size of the model

	Only the ordering is important, not the actual size. 
	"""

	format: ModelFormat
	"""
	Format of the model, e.g. `PyTorch`
	"""

	task: ModelTasks | tuple[ModelTasks, ...]
	"""
	Task or list of tasks which the model solves.
	"""

	task_properties: Mapping[str, object] = {}
	"""
	Additional task properties/specification
	"""

	# Attribution and sources #
	###########################

	citation: Optional[str | tuple[str, ...]] = None
	"""
	Citation(s) in bib format.
	"""

	citation_link: Optional[str | tuple[str, ...]] = None
	"""
	Link(s) for the cited paper(s)
	"""

	download_link: Optional[str] | dict[str, str] = None
	"""
	URL to download weights. Supported services:

		- direct download
		- Google drive

	If the model is trained on multiple datasets this can be a dictionary where the key is the dataset name and the value is the URL to download the weights.
	"""

	license: Optional[str] = None

	# Running the model #
	#####################
	install: "InstallOptionsPyproject | None" = None
	"""
	Defines install options.
	"""

	image_input: ImageInput
	"""
	Remarks:
	- resize is with padding, keeping the aspect ratio
	- batch size is not much used
	- before any normalization the input is always [0, 255] for each channel, even with floating point types
	"""

	output_mapping: Optional[MappingDefinition] = None
	"""
	Maps output of the model to a dict with `ModelOutput` [see here](data/output.py). The value is recursively string, list or dict. The structure should match the structure of the model output and the leaf nodes values should match the `ModelOutputKeys` values. For example:

	```toml
	output_mapping = {bbox=["xmin", "xmax", "ymin", "ymax"]}
	```

	`None`, the default, does no matching - your output format is compatible with the `ModelOutput`. Empty strings are skipped.
	"""

	output_mapping_values: Optional[dict[str, MappingDefinition]] = None
	"""
	todo: docs
	"""

	runner_name: Optional[str] = None
	"""
	Name of the custom runner class. This class have to be defined in a python file (`.py`) with the same name and path as the metadata file (i.e. the toml file documented here). This class have to inherit from the `model.ModelRunner` abstract class. Usually it will inherit from other classes like `PyTorchRunner`.

	Setting it `None` - the default value - the python file (if present) will be searched for class with the same name as the model format if found it will be used otherwise the default runner for given format is used.
	"""

	# Additional information #
	##########################
	dataset: Optional[str] | list[str] = None
	"""
	Dataset used to train the model
	"""

	backbone: Optional[str] = None
	"""
	todo:
	Just information about backbone
	"""

	architecture: Optional[str] = None
	"""
	todo:
	Just information about architecture
	"""

	tags: Optional[tuple[str, ...]] = ()
	"""
	Tags
	"""

	# DL-Lib specific options #
	###########################

	pytorch: Optional["PyTorchOptionsPyproject"] = None
	"""
	pytorch specific settings
	"""
	# New DL-lib: update here

	@model_validator(mode="after")
	def _dl_lib_specific_options(self):
		assert self.runner_name is None or getattr(self, self.format.value), (
			f"Model format `{self.format.value}`, no such key is present. "
			"Metadata has to define options specific to the model format."
		)
		return self

	@field_validator("format", "task", mode="before")
	@classmethod
	def _normalize(cls, v: Any):
		if isinstance(v, str):
			return v.lower().strip()
		else:
			return v

	@model_validator(mode="after")
	def _set_install_default(self):
		if self.format == ModelFormat.PyTorch and self.install is None:
			self.install = InstallOptionsPyproject()
		return self


class InstallOptionsPyproject(BaseModel):
	"""
	Options for automatic installation.

	The order of installation is as follows (assuming no steps are skipped):

	- virtual environment initialization
	        - optionally with conda's `environment.yml`
	- installing `install.conda_dependencies` via conda
	- installing `install.pip_dependencies` via pip
	- installing `requirements.txt` or other files via pip
	        - dependencies from `requirements.txt` (pinned and unpinned)
	        - poetry dependencies from `poetry.lock` and `pyproject.toml`
	        - Pipenv dependencies from `Pipfile.lock`

	        The install procedure uses `micropipenv`.
	- install itself via pip
	"""

	model_config = ConfigDict(extra="forbid")

	pip_dependencies: Optional[tuple[str, ...]] = None
	"""
	Additional pip dependencies (other than defined in `requirements.txt`).
	See the `InstallOptions` docs for installation order and precedence
	"""

	conda_dependencies: Optional[tuple[str, ...]] = None
	"""
	Additional conda dependencies (other than `environment.yml`). 
	See the `InstallOptions` docs for installation order and precedence
	"""


class PyTorchOptionsPyproject(BaseModel):
	"""
	Options specific to PyTorch, mainly how to run the model.
	"""

	model_config = ConfigDict(protected_namespaces=(), extra="forbid")

	model_import: Optional[str] = None
	"""
	Name of a module to import. Used with:
	- `model_init_expression`
	- `model_init_fx`
	"""

	model_init_expression: Optional[str] = None
	"""
	Define an expression to run which returns model object (`torch.nn.Module`).
	Returned model should be without initialized weights. The weights will be initialized automatically later.
	Could use these variables:

	- `args: list[cfg]` list of parameters - there is the loaded configuration, if available
	- `module: ModuleType` imported module as defined in `pytorch.model_import`	
	"""

	model_init_fx: Optional[str] = None
	"""
	Name of a method (callable) that will be called to instantiate the model.
	It is given the config (if available) as a positional parameter.
	Returned model should be without initialized weights. The weights will be initialized automatically later.

	Setting `pytorch.model_init_fx = my_function` is equivalent to specifying `pytorch.model_init_expression = "module.my_function(*args)"`.
	"""

	yacs_configs: Optional[tuple[str | InlineCode, ...]] = None
	"""
	List of config files or dict with single key `code`.
	The first entry must be the base configuration python file.
	The other entries are added in the same order as defined. The code has accessible the `cfg` object with the configuration.

	For example:

	```toml
	pytorch.yacs_configs= [
		"base_config.py",
		{code = "cfg = patch_config(cfg)"}
	]
	```
	"""

	load_mapping: Optional[MappingDefinition] = None
	"""
	Maps loaded weights to something.
	It has similar semantic as in `output_mapping`. I.E. match the structure of the data in the file and put string `state_dict` on the position of the `state_dict` data.
	"""

	@model_validator(mode="after")
	def _field_set_validation(self):
		assert any(
			[hasattr(self, key) for key in ["model_init_fx", "model_init_expression"]]
		), (
			"No way of constructing model, none of these keys have been defined:"
			"\n\t- `pytorch.model_init_fx`"
			"\n\t- `pytorch.model_init_expression`"
		)
		return self
