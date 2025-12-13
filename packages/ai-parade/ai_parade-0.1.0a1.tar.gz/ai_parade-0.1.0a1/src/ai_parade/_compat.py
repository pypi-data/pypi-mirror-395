import sys

# Backport `override` decorator for Python < 3.12
import typing

if not hasattr(typing, "override"):

	def override(method: typing.Any):
		return method

	typing.override = override

# Backport `StrEnum` for Python < 3.11
import enum

if not hasattr(enum, "StrEnum"):
	from backports.strenum import StrEnum

	enum.StrEnum = StrEnum

# Backport `tomllib` for Python < 3.11
try:
	import tomllib
except ImportError:
	import tomli as tomllib

	# Register the module globally
	sys.modules["tomllib"] = tomllib
