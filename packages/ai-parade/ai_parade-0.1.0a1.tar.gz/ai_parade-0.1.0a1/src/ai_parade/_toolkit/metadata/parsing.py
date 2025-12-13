import logging
import platform
from pathlib import Path
from typing import Any, cast

import tomllib
from pydantic import ValidationError

from ai_parade._toolkit.constants import TRACE_LVL
from ai_parade._toolkit.install._installer_selector import choose_installer
from ai_parade._toolkit.run.RemoteRunner import RemoteRunner
from ai_parade._toolkit.run.runner_selector import _choose_local_runner

from ..enums import formats_preferred_inference_engine
from .custom import Customizations, get_customizations
from .models.api import ModelMetadataApi
from .models.final import (
	InstallOptions,
	ModelMetadata,
)
from .models.pyproject import ModelMetadataPyproject

logger = logging.getLogger(__name__)

ModelMetadataApi.model_rebuild()


def _deep_dict_merge(base: dict, variant: dict):
	"""Recursively merges two dictionaries, overwriting the base with the variant"""

	def merge_recursion(base: Any, variant: Any):
		if isinstance(base, dict) and isinstance(variant, dict):
			for key in variant.keys():
				if key not in base or not merge_recursion(base[key], variant[key]):
					base[key] = variant[key]
			return True
		elif (
			isinstance(base, list)
			and isinstance(variant, list)
			and len(base) == len(variant)
		):
			for key, _ in enumerate(base):
				if not merge_recursion(base[key], variant[key]):
					base[key] = variant[key]
				return True
		else:
			return False

	base = base.copy()
	merge_recursion(base, variant)
	return base


_VARIANTS_KEY = "variants"


def _parse_variants(raw: dict):
	"""Parses the variants from the raw metadata

	Resolves overriding of the base (non-variant) properties, assign unique names to the variants
	"""
	parsed: list[ModelMetadataPyproject] = []
	common = raw.copy()
	del common[_VARIANTS_KEY]

	logger.info(f"Found metadata with {len(raw['variants'])} variants")
	for i, variant in enumerate(raw["variants"]):
		parsed_variant = _deep_dict_merge(common, variant)
		definition = ModelMetadataPyproject.model_validate(parsed_variant)
		logger.debug(f"Found variant `{definition.name}`")
		logger.log(TRACE_LVL, f"--> {definition}")
		parsed.append(definition)
	return parsed


class MetadataNotFoundError(Exception):
	"""
	Exception raised when no model metadata has been found
	"""

	pass


def _raw_to_definitions(
	raw: dict, group_name: str, has_customizations: bool
) -> list[ModelMetadataPyproject]:
	"""Parses the raw metadata from the pyproject.toml file into ModelMetadataDefinitions"""
	parsed = []
	if "tool" not in raw or "ai-parade" not in raw["tool"]:
		if not has_customizations:
			raise MetadataNotFoundError(group_name)
	else:
		raw_metadata = raw["tool"]["ai-parade"]

		try:
			if _VARIANTS_KEY in raw_metadata:
				parsed = _parse_variants(raw_metadata)
			else:
				parsed = [ModelMetadataPyproject.model_validate(raw_metadata)]
		except ValidationError as e:
			e.add_note(group_name)
			raise e
	return parsed


def _definitions_to_api(
	definitions: list[ModelMetadataPyproject],
) -> list[ModelMetadataApi]:
	"""Converts ModelMetadataApi to ModelMetadataDefinitions"""
	return [
		ModelMetadataApi(
			**definition.model_dump(),
		)
		for definition in definitions
	]


def _customization_to_api(customizations: Customizations) -> list[ModelMetadataApi]:
	"""Loads ModelMetadataApi from Customizations"""
	customization_metadata = []
	if customizations.include is None:
		return []
	else:
		logger.info("Loading metadata from Customizations")
		for api in customizations.include():
			assert isinstance(api, ModelMetadataApi)
			customization_metadata.append(api)
			logger.debug(f"Customizations added model: {api.name}")
			logger.log(TRACE_LVL, f"--> {api}")
		return customization_metadata


def _api_to_final(
	api: ModelMetadataApi,
	repo_path: Path | None,
	customizations: Customizations,
	build_dependencies: list[str],
	python_version: str,
) -> ModelMetadata:
	"""
	Converts ModelMetadataApi object to ModelMetadata by:
	- setting default values on unset properties
	- setting generated properties
	"""
	get_runner = api.get_runner  # store it for lambda closure
	engine = formats_preferred_inference_engine[api.format]
	if get_runner is not None:
		api.get_runner = lambda model_metadata, weights: RemoteRunner(
			model_metadata, engine, weights, get_runner
		)
	else:
		api.get_runner = lambda model_metadata, weights: RemoteRunner(
			model_metadata,
			engine,
			weights,
			_choose_local_runner(engine, customizations, api.runner_name),
		)

	api.get_installer = api.get_installer or choose_installer(
		api.install is not None,
		customizations,
		False if api.install is None else api.install.conda_dependencies is not None,
	)
	parsed_definition_dict = api.model_dump()

	if api.install is not None:
		parsed_definition_dict["install"] = InstallOptions(
			**api.install.model_dump(),
			build_system_dependencies=build_dependencies,
			python=python_version,
		).model_dump()  # ?todo: why it does not work without it???

	return ModelMetadata(
		**parsed_definition_dict,
		repository_path=repo_path,
	)


def parse_metadata(
	raw: dict | None,
	*,
	repo_path: Path | None,
	customizations: Customizations,
	# family_name: str | None,
	python_version: str | None = None,
) -> list[ModelMetadata]:
	"""
	Parses the raw metadata dict into ModelMetadata.

	Args:
		raw: raw metadata dict
		repo_path: path to the repository
		customizations: Customizations

	Returns:
		list[ModelMetadata]: list of ModelMetadata
	"""
	raw = raw or {}
	debug_name = repo_path.stem if repo_path else "unknown"
	python_version = python_version or platform.python_version()

	metadataDefinitions = _raw_to_definitions(
		raw, debug_name, customizations.include is not None
	)
	metadataApis = _definitions_to_api(metadataDefinitions)
	metadataApis.extend(_customization_to_api(customizations))

	# Set generated field's defaults
	parsed_list: list[ModelMetadata] = []
	for api in metadataApis:
		build_dependencies = []
		if (
			api.install is not None
			and "build-system" in raw
			and "requires" in raw["build-system"]
		):
			build_dependencies = cast(list[str], raw["build-system"]["requires"])
		else:
			# if no build-system is defined, add setuptools
			build_dependencies.append("setuptools")
		final_metadata = _api_to_final(
			api, repo_path, customizations, build_dependencies, python_version
		)

		parsed_list.append(final_metadata)
	return parsed_list


async def get_local_metadata(
	repo_path: Path,
) -> list[ModelMetadata]:
	"""
	Get metadata from the pyproject.toml file in the repository

	Args:
		repo_path: Path to the repository

	Returns:
		list[ModelMetadata]: List of found ModelMetadata
	"""
	logger.info(f"Getting metadata from `{repo_path}`")
	pyproject = repo_path / "pyproject.toml"

	if pyproject.exists():
		logger.info(f"Parsing {pyproject}")
		with pyproject.open("rb") as file:
			raw = tomllib.load(file)
	else:
		logger.info(f"pyproject.toml not found in {repo_path}, will use customizations")
		raw = {}

	python_version = raw.get("required-python", platform.python_version())
	install_options = InstallOptions(
		pip_dependencies=tuple(raw.get("dependency-groups", {}).get("ai-parade", [])),
		python=python_version,
		build_system_dependencies=list(
			raw.get("build-system", {}).get("requires", ["setuptools"])
		),
	)
	customizations = await get_customizations(repo_path, install_options)

	return parse_metadata(
		raw,
		repo_path=repo_path,
		customizations=customizations,
		python_version=python_version,
	)
