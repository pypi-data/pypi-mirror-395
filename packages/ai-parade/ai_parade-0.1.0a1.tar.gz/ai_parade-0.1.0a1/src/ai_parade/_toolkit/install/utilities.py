import logging
import re
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import cast

from ai_parade._toolkit.constants import TRACE_LVL
from ai_parade._toolkit.logging import subprocess_run_log_async

logger = logging.getLogger(__name__)


async def check_missing_dependencies(
	root_path: Path, pin_defined: bool, pin_installed: bool
) -> bool:
	"""Checks if there are missing dependencies

	Args:
		root_path: Path to project
		pin_requirements: True if dependencies should be pinned into requirements.txt

	Returns:
		True if there are missing dependencies
	"""
	locked_dependencies = await convert_lock_to_requirements(root_path)
	if locked_dependencies is None:
		logger.warning(
			"Could not resolve lock file/pinned dependencies, trying to generate them from project files."
		)

	requirements_file = root_path / "requirements.txt"
	if pin_installed:
		_, locked_dependencies, _ = await subprocess_run_log_async(
			["uv", "pip", "freeze"], logger=logger
		)
		requirements_file.write_text(locked_dependencies)
	elif pin_defined:
		locked_dependencies = await pin_dependencies(root_path, requirements_file)
	elif locked_dependencies is None:
		with NamedTemporaryFile() as temp_file:
			locked_dependencies = await pin_dependencies(
				root_path, Path(temp_file.name)
			)

	locked_dependencies = locked_dependencies.split("\n")

	logger.debug("Will freeze current dependencies")
	_, actual_dependencies, _ = await subprocess_run_log_async(
		["uv", "pip", "freeze"], logger=logger
	)
	actual_dependencies = actual_dependencies.split("\n")

	difference = set(actual_dependencies) - set(locked_dependencies)
	for dep in difference:
		found_in_lock = next(
			(
				x
				for x in locked_dependencies
				if dep.split("==")[0] in x and not x.strip().startswith("#")
			),
			None,
		)
		logger.warning(
			f"Installed dependency missmatch: found {dep}; need {found_in_lock}"
		)

	return len(difference) > 0


def is_pinned_requirements_txt(requirements_file: Path) -> bool:
	"""Check if given requirements.txt contains only pinned dependencies"""
	with requirements_file.open() as f:
		lines = f.read().splitlines()
		for line in lines:
			line = re.sub(r"#.*$", "", line)  # remove comments
			if line.strip() == "":
				continue
			# the @ denotes git or other VCS dependencies
			# ?todo:  they are not necessarily pinned with this simple check
			if "==" not in line and "@" not in line:
				return False
	return True


async def convert_lock_to_requirements(root_path: Path):
	"""Converts a lock file into a requirements.txt

	Supports:
	- pipenv - Pipfile.lock
	- poetry - poetry.lock
	- requirements.txt

	Uses micropipenv

	Args:
		root_path: Path to project where lock file is

	Returns:
		Contents of the requirements file or its equivalent as a string
	"""
	# See this issue: https://github.com/pytorch/pytorch/issues/140914
	# to why we are importing here and patching sys.modules
	import sys

	import micropipenv
	import typing_extensions

	sys.modules["pip._vendor.typing_extensions"] = typing_extensions

	NO_DEV = True
	ONLY_DIRECT = True

	resolveAs = [  # The order defines priority
		("Pipfile.lock", "pipenv"),
		("poetry.lock", "poetry"),
		("requirements.txt", "requirements.txt"),
	]

	method = None
	for file, resolve_method in resolveAs:
		path = root_path / file
		if path.exists():
			method = resolve_method
			break

	sections = None
	if method == "pipenv":
		sections = micropipenv.get_requirements_sections(
			only_direct=ONLY_DIRECT, no_dev=NO_DEV
		)
	elif method == "poetry":
		sections = micropipenv._poetry2pipfile_lock(  # type: ignore
			only_direct=ONLY_DIRECT, no_dev=NO_DEV
		)
	elif method == "requirements.txt":
		is_pinned_requirements_txt(root_path / "requirements.txt")
		with open(root_path / "requirements.txt", "r") as f:
			return f.read()

	if sections is not None:
		result = cast(
			str,
			micropipenv.requirements_str(
				sections,
				# no_hashes=no_hashes,
				# no_indexes=no_indexes,
				# no_versions=no_versions,
				only_direct=ONLY_DIRECT,
				no_dev=NO_DEV,
				no_comments=True,
			),
		)
		return result
	return None


async def pin_dependencies(
	root_path: Path, requirements_file: Path, pinned_requirements: str | None = None
) -> str:
	"""Pins dependencies

	Args:
		root_path: Path to project
		requirements_file: Path to requirements.txt where dependencies should be pinned to

	Raises:
		FileNotFoundError: when no dependency file could be found

	Returns:
		Pinned dependencies
	"""
	logger.debug(f"Pinning dependencies to `{requirements_file}`")
	resolveAs = [  # The order defines priority
		"requirements.in",
		"pyproject.toml",
		"requirements.txt",
		"setup.py",
		"setup.cfg",
	]

	found_dependency_files: list[Path] = []
	for file in resolveAs:
		path = root_path / file
		if path.exists():
			found_dependency_files.append(path)

	logger.log(TRACE_LVL, "Trying to pin dependencies")
	returnCode, _, stderr = await subprocess_run_log_async(
		[
			"uv",
			"pip",
			"compile",
			"--no-build-isolation",
			"--output-file",
			requirements_file,
		]
		+ (found_dependency_files if pinned_requirements is None else ["-"]),
		check=False,
		logger=logger,
		stdin=None if pinned_requirements is None else pinned_requirements,
	)
	if returnCode != 0:
		raise FileNotFoundError(
			f"Could not resolve dependencies, tried: {', '.join([str(x) for x in found_dependency_files])}",
			stderr,
		)
	logger.debug("Successfully pinned dependencies")
	with open(requirements_file, "r") as f:
		result = f.read()

		return result
