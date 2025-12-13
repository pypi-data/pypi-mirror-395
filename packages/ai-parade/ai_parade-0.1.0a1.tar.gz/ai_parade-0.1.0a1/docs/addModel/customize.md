
# Customizations

## Metadata generation

```python
def include(config: BasicConfig) -> list[ModelMetadataApi]:
	return [ModelMetadataApi(...)]
```

The [ModelMetadataApi](../reference/customize.md#ai_parade.custom_definitions.ModelMetadataApi) derives from the object hoding  properties in `[tool.ai-parade]` (so everything in the `pyproject.toml` could be defined with it). There are two extra properties to specify installer ([get_installer](../reference/customize.md#ai_parade.custom_definitions.ModelMetadataApi.get_installer)) and runner ([get_runner](../reference/customize.md#ai_parade.custom_definitions.ModelMetadataApi.get_runner)).

## Installation

To customize installation process define install function.

```python
class Installer(ModelInstaller):
	def __init__(self, model_metadata: ModelMetadata) -> None:
		pass
	
	@override
	def install(self, overwrite: bool = False, update: bool = False) -> None:
		# install everything

	# You should likely also is_installed method although it is not required.
	# Here is default implementation:
	async def is_installed(self) -> bool:
		return False
```

## Running

To customize running of the model create class which inherits directly or indirectly from [`ModelRunner`](../reference/customize.md#ai_parade.custom_definitions.ModelRunner).

>[!TIP]
Using more specific runner than `ModelRunner` is recommended.
> see [`PyTorchRunner`](../reference/customize.md#ai_parade.custom_definitions.PyTorchRunner)

The name of the class is significant because you can specify multiple runners and choose one at per model basis. See the [`runner_name`](../reference/pyproject.md#ai_parade._toolkit.metadata.models.pyproject.ModelMetadataPyproject.runner_name) property in the model metadata.

Here is example of adding additional inputs in Pytorch models:

```python
from typing import Any, override, TYPE_CHECKING
import ai_parade.custom_definitions as aip

if TYPE_CHECKING:
	import torch


class Pytorch(aip.PyTorchRunner):
	"""
	In `PyTorchRunner` simplest thing is to override the `_inference_call` method where the model is prepared.
	"""

	@override
	def _inference_call(self, tensor: "torch.Tensor") -> "torch.Tensor":
		assert self.model is not None
		output = self.model(tensor, **special_parameters)
		
		# compute results from output
		result = output

		return result
```
