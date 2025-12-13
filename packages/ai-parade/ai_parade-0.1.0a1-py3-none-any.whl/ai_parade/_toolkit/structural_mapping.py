import functools
import logging
from typing import Any, Callable, Mapping, cast

import numpy as np

logger = logging.getLogger(__name__)

# ?todo: Recursive definition not working with pydantic
MappingDefinition0 = str | list[str] | dict[str, str]
MappingDefinition1 = str | list[MappingDefinition0] | dict[str, MappingDefinition0]
MappingDefinition = str | list[MappingDefinition1] | dict[str, MappingDefinition1]
# MappingDefinition = str | list["MappingDefinition"] | dict[str, "MappingDefinition"]


class StructuralMappingError(Exception):
	pass


def structural_map(
	raw_output: Any,
	mapping: MappingDefinition | None,
	additionalMappings: Mapping[
		str,
		MappingDefinition,
	]
	| None = None,
	skip_missing: bool = False,
) -> dict[str, Any]:
	if additionalMappings is None:
		additionalMappings = {}
	if mapping is None:
		return cast(dict[str, Any], raw_output)

	output: dict[str, Any] = {}

	def _recursive_map(raw_output: Any, mapping: MappingDefinition):
		try:
			if isinstance(mapping, str):
				if not mapping == "":
					output[mapping] = raw_output
			elif isinstance(mapping, list) or isinstance(mapping, tuple):
				for raw_item, item in zip(raw_output, mapping):
					_recursive_map(raw_item, item)
			else:
				try:
					if isinstance(raw_output, dict):
						for key in mapping.keys():
							_recursive_map(raw_output[key], mapping[key])
					else:
						for key in mapping.keys():
							_recursive_map(getattr(raw_output, key), mapping[key])
				except KeyError as e:
					key = e.args[0]
					if e.args[0] in additionalMappings:
						_recursive_map([], key)
					else:
						raise e
		except (
			TypeError,  # wrong indexing
			IndexError,  # list indexing
			KeyError,  # dict indexing
			AttributeError,  # object attribute indexing
		) as e:
			if skip_missing:
				logger.debug(f"Skipping missing index `{e.args[0]}`")
			else:
				raise StructuralMappingError(e, raw_output, mapping, output)

	_recursive_map(raw_output, mapping)

	for property, mapping in additionalMappings.items():
		if property not in output:
			output[property] = []
		if not (
			isinstance(output[property], list)
			or isinstance(output[property], tuple)
			or isinstance(output[property], np.ndarray)
		):
			output[property] = [output[property]]

		output[property] = [structural_map(item, mapping) for item in output[property]]

	return output


ObjectMapping = Callable[[Any], dict[str, Any]]


def structural_map_fx(
	mapping: MappingDefinition | None,
	additionalMappings: Mapping[str, MappingDefinition] = {},
	skip_missing: bool = False,
) -> ObjectMapping:
	return functools.partial(
		structural_map,
		mapping=mapping,
		additionalMappings=additionalMappings,
		skip_missing=skip_missing,
	)
