import asyncio
import logging
import re
import subprocess
from asyncio.subprocess import Process
from pathlib import Path

from ai_parade._toolkit.constants import TRACE_LVL

_Args = list[str] | list[str | Path] | list[Path]


def _log_command(logger: logging.Logger, args: _Args, **kwargs):
	logger.debug(f"Running command: `{' '.join([str(x) for x in args])}`")
	if kwargs:
		logger.debug(f"\twith kwargs: {kwargs}")


# From https://stackoverflow.com/a/14693789/5739006
_ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")


def better_decode(b: bytes) -> str:
	text = b.decode()
	return _ansi_escape.sub("", text)


def _log_results(
	logger: logging.Logger,
	args: _Args,
	returncode: int,
	stdout: bytes,
	stderr: bytes,
	check: bool,
):
	msg = f"Command: `{' '.join([str(x) for x in args])}` exited with return code {returncode} and output:"
	if stdout is not None:  # type: ignore because it is simply not true
		msg += "\n" + better_decode(stdout)
	if stderr is not None:  # type: ignore because it is simply not true
		msg += "\n" + better_decode(stderr)

	logger.log(logging.ERROR if returncode != 0 else TRACE_LVL, msg)

	if check and returncode != 0:
		raise subprocess.CalledProcessError(returncode, args, stdout, stderr)


def log_subprocess_result(
	result: subprocess.CompletedProcess[bytes],
	*,
	logger: logging.Logger,
	check: bool = True,
):
	_log_results(
		logger, result.args, result.returncode, result.stdout, result.stderr, check
	)
	return result.returncode, better_decode(result.stdout), better_decode(result.stderr)


async def log_subprocess_result_async(
	process: Process,
	args: _Args = [],
	*,
	logger: logging.Logger,
	check: bool = True,
	stdin: bytes | None = None,
):
	stdout, stderr = await process.communicate(input=stdin)
	assert process.returncode is not None
	_log_results(
		logger,
		args,
		process.returncode,
		stdout,
		stderr,
		check,
	)
	return process.returncode, better_decode(stdout), better_decode(stderr)


async def subprocess_run_log_async(
	args: _Args,
	*,
	logger: logging.Logger,
	check: bool = True,
	stdin: str | None = None,
	**kwargs,
):
	_log_command(logger, args, **kwargs)

	process = await asyncio.create_subprocess_exec(
		str(args[0]),
		*map(str, args[1:]),
		stdout=asyncio.subprocess.PIPE,
		stderr=asyncio.subprocess.PIPE,
		stdin=asyncio.subprocess.PIPE if stdin is not None else None,
		**kwargs,
	)
	return await log_subprocess_result_async(
		process,
		args,
		logger=logger,
		check=check,
		stdin=stdin.encode() if stdin is not None else None,
	)


def subprocess_run_log(
	args: _Args, *, logger: logging.Logger, check: bool = True, **kwargs
):
	_log_command(logger, args, **kwargs)
	result = subprocess.run(
		args,
		stdout=asyncio.subprocess.PIPE,
		stderr=asyncio.subprocess.PIPE,
		**kwargs,
	)
	return log_subprocess_result(result, logger=logger, check=check)


def get_ai_parade_logger() -> logging.Logger:
	"""Get the logger for ai_parade"""
	return logging.getLogger("ai_parade._toolkit")
