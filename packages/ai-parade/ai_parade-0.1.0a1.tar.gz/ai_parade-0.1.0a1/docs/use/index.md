# Using AI-parade toolkit

## Installation

PIP packages Installation:

```sh
pip install ai-parade
```

UV installation:

```sh
uv add --dev ai-parade
```

However this can't do much alone. You will need to install extras to be able to run and convert the model.
We have split it into the extra because downloading everything is quite huge.

| For inference | To convert | Note |
|---|---|---|
| `inference`| `convert` | All supported engines |
| `inference-onnx` | `convert-onnx` ||
| `inference-tf` | `convert-tf` ||
| `inference-pytorch` | `convert-pytorch` ||
| `inference-ncnn` | `convert-ncnn` ||

So for example you will install `pip install ai-parade[convert]` or `uv add --dev ai-parade[convert]`

## Usage

```sh
ai-parade inference FooBarModel path/to/weights

ai-parade convert FooBarModel path/to/weights onnx
```

See [`ai-parade convert`](../reference/CLI.md#ai-parade-convert)
and [`ai-parade inference`](../reference/CLI.md#ai-parade-inference) reference.
