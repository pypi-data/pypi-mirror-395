import asyncio
import logging
import sys
from pathlib import Path
from pprint import pprint
from typing import Annotated, cast

import rich
import rich.traceback
import typer

import ai_parade._compat  # noqa: F401
from ai_parade._toolkit.constants import TRACE_LVL
from ai_parade._toolkit.converters.converter import ConverterOptions
from ai_parade._toolkit.get_weights import get_weights_name
from ai_parade._toolkit.install.utilities import check_missing_dependencies
from ai_parade._toolkit.verify import compute_statistics
from ai_parade.datasets import ImageNet_VID, Random
from ai_parade.toolkit import (
	Dataset,
	HardwareAcceleration,
	ModelFormat,
	ModelMetadata,
	Quantization,
	QuantizedModelFormat,
	RemoteError,
	format_suffixes,
	formats_preferred_inference_engine,
	get_converter,
	get_local_metadata,
	get_runner,
)
from ai_parade.toolkit import (
	get_ai_parade_logger as get_toolkit_logger,
)

logger = logging.getLogger(__name__)

app = typer.Typer()

RepositoryPathType = Annotated[
	Path, typer.Option("--repository", help="Path to repository with pyproject.toml")
]
WeightsPathTypeHelp = "Path to the model file (including weights), or directory if given format stores the model in directory or in multiple files (splits model and weights)"
WeightsPathType = Annotated[Path, typer.Argument(help=WeightsPathTypeHelp)]

VerboseType = Annotated[
	list[bool],
	typer.Option(
		"--verbose",
		"-v",
		help="Enable verbose logging, repeat for more verbosity (current max: `-vvvv`)",
	),
]
ModelNameTypeHelp = (
	"Name of model (as in the [tool.ai-parade.name] property in pyproject.toml file)"
)
ModelNameType = Annotated[str, typer.Argument(help=ModelNameTypeHelp)]

NEED_CALIBRATION = [Quantization.int4, Quantization.int8]


def _set_verbosity(verbose: VerboseType):
	toolkit_logger = get_toolkit_logger()
	this_logger = logging.getLogger("ai_parade._cli.ai_parade")
	verbosity_level = verbose.count(True)

	if verbosity_level < 2:
		logging.basicConfig(
			format="[%(levelname)-9s%(asctime)s] %(message)s",
			datefmt="%H:%M:%S",
		)
	else:
		logging.basicConfig(
			format="[%(levelname)-9s%(asctime)s] %(filename)s#%(lineno)d - %(message)s",
			datefmt="%H:%M:%S",
		)
	match verbosity_level:
		case 0:
			this_logger.setLevel(logging.INFO)
		case 1:
			toolkit_logger.setLevel(logging.INFO)
			this_logger.setLevel(logging.DEBUG)
		case 2:
			toolkit_logger.setLevel(logging.DEBUG)
			this_logger.setLevel(TRACE_LVL)
		case 3:
			toolkit_logger.setLevel(TRACE_LVL)
			this_logger.setLevel(TRACE_LVL)
		case _:
			logging.getLogger().setLevel(TRACE_LVL)
	return verbosity_level


def handle_remote_error(e: RemoteError, verbosity_level: int):
	rich.print(e.rich_traceback)
	if verbosity_level >= 3:
		rich.print(rich.traceback.Traceback.from_exception(*sys.exc_info()))  # type: ignore
	raise typer.Exit(code=1)


def _get_dataset(
	dataset_name: str, dataset_path: Path | None, metadata: ModelMetadata
) -> Dataset:
	match dataset_name:
		case "ImageNet_VID":
			if dataset_path is None:
				raise ValueError("Dataset path is required for ImageNet_VID dataset")
			dataset = ImageNet_VID(dataset_path).preprocess(metadata.image_input)
		case "Random":
			dataset = Random(metadata.image_input, seed=442)
		case _:
			raise NotImplementedError(f"Dataset {dataset_name} not implemented")
	return dataset


@app.command()
def ls(
	repository: RepositoryPathType = Path("."),
	verbose: VerboseType = [],
):
	"""
	List all available models in the repository.
	"""
	_set_verbosity(verbose)
	metadata_list = asyncio.run(get_local_metadata(repository))
	print(
		"Models metadata parsed:\n\t" + "\n\t".join(m.name for m in metadata_list),
		flush=True,
	)


@app.command()
def check(
	model_name: Annotated[
		str | None,
		typer.Argument(help=ModelNameTypeHelp, show_default="All available models"),
	] = None,
	weights_path: Annotated[
		Path | None,
		typer.Argument(help=WeightsPathTypeHelp),
	] = None,
	skip_dependencies: Annotated[
		bool,
		typer.Option(help="If set to True, don't check dependencies."),
	] = False,
	# reinstall_dependencies: Annotated[
	# bool,
	# typer.Option(
	# help="If set to True, create a new environment and install dependencies for each model."
	# ),
	# ] = False,
	pin_installed: Annotated[
		bool,
		typer.Option(
			help=(
				"Set to True to pin dependencies to specific version into `requirements.txt`. "
				"Uses currently installed dependencies... its pip freeze equivalent"
			)
		),
	] = False,
	pin_defined: Annotated[
		bool,
		typer.Option(
			help=(
				"Set to True to pin dependencies to specific version into `requirements.txt`. "
				"If the repository contains a lock file they will be converted to requirements.txt"
				"Supported dependency sources: "
				"requirements.in, setup.cfg, setup.py, pyproject.toml, requirements.txt; "
				"Supported lock files: "
				"pipFile.lock, poetry.lock"
			)
		),
	] = False,
	repository: RepositoryPathType = Path("."),
	verbose: VerboseType = [],
):
	"""
	Check if model repository is correctly set up.

	It runs the following steps:

	1. Check if installed dependencies are pinned.
		- Skip with `--skip-dependencies`

	2. Parse metadata and select model (`MODEL_NAME`)

	3. Run inference on random data.
		- Only run if model name and weights are provided (`MODEL_NAME` and `WEIGHTS_PATH`)
	"""
	_set_verbosity(verbose)
	has_missing_dependencies = False
	if not skip_dependencies:
		has_missing_dependencies = asyncio.run(
			check_missing_dependencies(
				Path.cwd(), pin_installed=pin_installed, pin_defined=pin_defined
			)
		)
		logger.info("Dependencies checked!")

	metadata_list = asyncio.run(get_local_metadata(repository))
	logger.info("Model metadata successfully parsed")

	if model_name is not None:
		assert weights_path is not None
		metadata = next(
			x for x in metadata_list if x.name == model_name if model_name is not None
		)
		logger.info(f"Selected model: {metadata.name}")

		# if reinstall_dependencies:
		# with TemporaryDirectory() as venv:
		# raise NotImplementedError
		# runner.inference(Random(metadata.image_input))
		# else:
		with metadata.get_runner(metadata, weights_path) as runner:
			runner.inference(Random(metadata.image_input).take(2))

	exit_code = 0
	if has_missing_dependencies:
		exit_code |= 8
	raise typer.Exit(code=exit_code)


def convert_impl(
	source_format: QuantizedModelFormat,
	target_format: QuantizedModelFormat,
	metadata: ModelMetadata,
	weights_path: Path,
	hw_acceleration: HardwareAcceleration,
	calibration_dataset: Dataset | None,
	verify_dataset: Dataset | None,
	override: bool,
	output: Path,
	artifacts: Path,
	use_remote: bool,
):
	converter_chains = get_converter(source_format, target_format)

	if not converter_chains or len(converter_chains) == 0:
		raise RuntimeError(
			f"Failed to find converter from {source_format} to {target_format}"
		)
	base_results = None
	if verify_dataset is not None:
		with get_runner(
			formats_preferred_inference_engine[source_format.format],
			metadata,
			weights_path,
			use_remote=use_remote,
		) as runner:
			runner.set_output_directory(artifacts)
			base_results = runner.inference(verify_dataset)

	for converter_chain in converter_chains:
		current_source_weights_path = weights_path
		try:
			for converter in converter_chain:
				current_source_format, current_target_format = converter.conversion
				current_hw_acceleration = (
					hw_acceleration if target_format == current_target_format else None
				)
				current_target_weights_path = output / get_weights_name(
					current_target_format, current_hw_acceleration
				)
				if override or not current_target_weights_path.exists():
					with get_runner(
						formats_preferred_inference_engine[
							converter.conversion[0].format
						],
						metadata,
						current_source_weights_path,
						use_remote=use_remote,
					) as runner:
						runner.set_output_directory(artifacts)
						converted_weights = runner.run(
							converter.create(
								ConverterOptions(
									calibration_data=calibration_dataset,
									hw_acceleration=hw_acceleration,
								)
							)
						)
					(artifacts / converted_weights).rename(current_target_weights_path)
				# update weights in next iteration
				current_source_weights_path = current_target_weights_path
			break
		except Exception as e:
			logger.error(e.__cause__)
			raise e

	if verify_dataset is not None:
		with get_runner(
			formats_preferred_inference_engine[target_format.format],
			metadata,
			output / get_weights_name(target_format, hw_acceleration),
			use_remote=use_remote,
		) as runner:
			runner.set_output_directory(artifacts)
			converted_results = runner.inference(verify_dataset)

		return compute_statistics(cast(list, base_results), converted_results)


OutputType = Annotated[
	Path,
	typer.Option(help="Output directory for converted weights."),
]

SeparateEnvironmentType = Annotated[
	bool,
	typer.Option(
		"--separate-environment",
		"--separate-env",
		"--separate-venv",
		help="Separates environment (python interpreter and venv) from the local one. Setting this will complicate debugging.",
		show_default="False - local environment",
	),
]


@app.command()
def convert(
	model_name: ModelNameType,
	weights_path: WeightsPathType,
	model_format: Annotated[
		ModelFormat, typer.Argument(case_sensitive=False, help="Target model format")
	],
	quantization: Annotated[
		Quantization,
		typer.Option(
			"--quantization",
			"--quantize",
			case_sensitive=False,
			help="Quantization of the target model",
		),
	] = Quantization.none,
	hw_acceleration: Annotated[
		HardwareAcceleration,
		typer.Option(
			case_sensitive=False,
			help="Hardware acceleration of the target model. It is used only by Executorch",
		),
	] = HardwareAcceleration.CPU,
	override: Annotated[
		bool,
		typer.Option(
			help="Overwrite already converted weights if they exist (including intermediate ones)."
		),
	] = False,
	artifacts: Annotated[
		Path,
		typer.Option(
			help="Directory for conversion artifacts (logs, dumps) are stored."
		),
	] = Path("build"),
	# calibration for quantization
	calibration_dataset: Annotated[
		str | None,
		typer.Option(
			"--calibration-dataset",
			help="Dataset name used to calibrate INT4/INT8 conversions. Required for INT4/INT8 conversions.",
		),
	] = None,
	calibration_dataset_path: Annotated[
		Path | None,
		typer.Option(
			"--calibration-dataset-path",
			help="Path with assets for the calibration dataset (when required).",
		),
	] = None,
	# verification
	verify: Annotated[
		bool,
		typer.Option(
			help="Run inference before/after conversion and compare.",
		),
	] = False,
	verify_dataset: Annotated[
		str | None,
		typer.Option(
			"--verify-dataset",
			help="Dataset name used for verification. Automatically sets `--verify` to True.",
			show_default="None; Random if `--verify` is set",
		),
	] = None,
	verify_dataset_path: Annotated[
		Path | None,
		typer.Option(
			"--verify-dataset-path",
			help="Path with assets for the verification dataset.",
		),
	] = None,
	# common
	use_remote: SeparateEnvironmentType = False,
	repository_path: RepositoryPathType = Path("."),
	output: OutputType = Path("."),
	verbose: VerboseType = [],
):
	"""
	Convert an existing model to a different format. Target format can be quantized.
	"""
	assert quantization not in NEED_CALIBRATION or calibration_dataset is not None
	verbosity_level = _set_verbosity(verbose)

	artifacts.mkdir(parents=True, exist_ok=True)
	output.mkdir(parents=True, exist_ok=True)

	metadata_list = asyncio.run(get_local_metadata(repository_path))
	metadata = next(x for x in metadata_list if x.name == model_name)

	if calibration_dataset is not None:
		parsed_calibration_dataset = (
			_get_dataset(
				calibration_dataset,
				calibration_dataset_path,
				metadata,
			)
			.shuffle(42)
			.take(1000)
		)
	else:
		parsed_calibration_dataset = None

	if verify or verify_dataset is not None:
		parsed_verify_dataset = (
			_get_dataset(
				verify_dataset or "Random",
				verify_dataset_path,
				metadata,
			)
			.shuffle(42)
			.take(1000)
		)
	else:
		parsed_verify_dataset = None

	try:
		results = convert_impl(
			QuantizedModelFormat(metadata.format),
			QuantizedModelFormat(model_format, quantization),
			metadata,
			weights_path,
			hw_acceleration=hw_acceleration,
			calibration_dataset=parsed_calibration_dataset,
			verify_dataset=parsed_verify_dataset,
			override=override,
			output=output,
			artifacts=artifacts,
			use_remote=use_remote,
		)
		if results is not None:
			print(results)
	except RemoteError as e:
		handle_remote_error(e, verbosity_level)


@app.command()
def inference(
	model_name: ModelNameType,
	weights_path: WeightsPathType,
	dataset_name: Annotated[
		str,
		typer.Argument(help="Dataset used for inference."),
	] = "Random",
	dataset_path: Annotated[
		Path | None,
		typer.Option(
			help="Optional path to the dataset assets (required for non-random datasets)."
		),
	] = None,
	take: Annotated[
		int,
		typer.Option(
			help="Number of samples to run through the model during inference.",
		),
	] = 10,
	# common
	use_remote: SeparateEnvironmentType = False,
	repository_path: RepositoryPathType = Path("."),
	output: OutputType = Path("."),
	verbose: VerboseType = [],
):
	"""
	Run inference on a model using a selected dataset and print results.
	"""
	verbosity_level = _set_verbosity(verbose)

	metadata_list = asyncio.run(get_local_metadata(repository_path))
	metadata = next(x for x in metadata_list if x.name == model_name)
	dataset = _get_dataset(dataset_name, dataset_path, metadata).take(take)
	model_format = next(
		(
			format
			for format, suffix in format_suffixes.items()
			if suffix == weights_path.suffix
		),
		metadata.format,
	)
	engine = formats_preferred_inference_engine[model_format]
	try:
		with get_runner(
			engine, metadata, weights_path, use_remote=use_remote
		) as runner:
			runner.set_output_directory(output)
			results = runner.inference(dataset)

		pprint(results)
	except RemoteError as e:
		handle_remote_error(e, verbosity_level)


if __name__ == "__main__":
	app()
