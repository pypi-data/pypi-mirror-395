# Adding a new model

The steps could be summarized as:

1. Prepare the repository: fork,clone, create venv
2. [Install `ai-parade`](#installation)
3. [configure it](#configure)
	- [With multiple models (multiple sizes, variants etc.)](#multiple-models-multiple-sizes-variants-etc)
	- [Customizations](#customizations)
4. [Pin dependencies](#pin-dependencies)
5. [Test it](#test-it)
6. [Profit](#profit)

## Installation

PIP packages Installation:

```sh
pip install ai-parade
```

UV installation:

```sh
uv add --dev ai-parade
```

## Configure

The simplest configuration method is via  `[tool.ai-parade]` key in `pyproject.toml`.
There you add properties that define where to find your model and how to use it, along with the model name and other metadata.

The basic example looks like:

```toml
[tool.ai-parade]
name = "FooBarModel"
format = "PyTorch"
task = "Classification"
pytorch = {model_import = "foo_bar.model", model_init_fx = "model"}
[tool.ai-parade.image_input]
	batchSize = 1
	height = 256
	width = 256
	channelOrder = "BGRA"
	dataOrder = "NCHW"
	dataType = "UINT8"
```

For the full list of available properties see [this](../reference/pyproject.md)

### Multiple models (multiple sizes, variants etc.)

If your repository contains multiple models you can define them with `variants` list which overrides any property defined under the `[tool.ai-parade]` (including nested properties as long as they are not in `variants`).
For example:

```toml
[tool.ai-parade]
format = "PyTorch"
task = "Classification"
pytorch = {model_import = "foo_bar.model", model_init_fx = "model"}
[tool.ai-parade.image_input]
	batchSize = 1
	height = 256
	width = 256
	channelOrder = "BGRA"
	dataOrder = "NCHW"
	dataType = "UINT8"
[[tool.ai-parade.variants]]
name = "Foo small"
size = 1
pytorch = {model_init_fx = "model_small"}
[[tool.ai-parade.variants]]
name = "Foo base"
size = 2
```

Will register 2 sizes of models.
> [!TIP]
> The required properties can be skipped under the `[tool.ai-parade]` if all `variants` define them.

### Customizations

If you want even more options for customization, i.e. adding large number of models and doing so programmatically, add `ai-parade.py` in the project root (alongside the `pyproject.toml`). There you import `ai_parade.custom_definitions`

**Then you can customize**:

- the *model definition* process via `include` function
	- a function with signature `() -> list[ModelMetadataApi]`. The return value is a list of models definitions. The `ModelMetadataApi` has extended set of properties from `pyproject.toml`.
- *running* of the model classes derived from `ModelRunner`. see also `runner_name` property.
- *installation process* via class derived from `ModelInstaller`

See more info in [Customize guide](customize.md) and [reference](../reference/customize.md)

## Pin dependencies

To generate **pinned** `requirements.txt` use any of:

- your package manager
- `ai-parade check --pin-installed` to use all installed dependencies
- `ai-parade check --pin-defined` to use dependencies from lock files

## Test it

```sh
ai-parade check FooBarModel
```

See documentation for the [`ai-parade check`](../reference/CLI.md#ai-parade-check)

If there are problems you will need to solve them. [Debug](debug.md) is guide to help you with setting up debugging.

## [Profit](../use/index.md)
