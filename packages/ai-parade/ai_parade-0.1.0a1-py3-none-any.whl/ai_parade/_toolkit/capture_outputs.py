import io
import logging
import sys
import traceback
import warnings
from enum import Enum
from pathlib import Path
from types import TracebackType
from typing import Any, override


class CaptureOutputs:
	"""Capture the outputs of a process, including stdout, stderr, and logs.

	What is captured:
	- stdout
	- stderr
	- logs
	- warnings
	- errors/exceptions

	Once exited, the class contains the captured outputs in its public attributes.
	"""

	def __init__(
		self,
		save_dir: Path | None = None,
		single_output: bool = True,
		catch_errors: bool = True,
		**kwargs: Any,
	):
		"""
		Args:
			save_dir: Directory to save the captured outputs.
			single_output: If `True` all outputs will be saved to the logs field / file.
			catch_errors: If `True` all exceptions will be caught and saved to `error` field.
		"""
		# path attributes
		self.save_dir = save_dir
		"""Directory to save the captured outputs."""

		# setup attributes
		self._catch_errors = catch_errors
		self._single_output = single_output

		# Public attributes for inspecting the outputs
		self.error = ""
		"""Error messages of error that cause the CaptureOutputs to exit."""
		self.stdout = ""
		"""Captured stdout. Empty if `mixed_stdout_logger` is set to `True`."""
		self.stderr = ""
		"""Captured stderr. Empty if `mixed_stdout_stderr` is set to `True`."""
		self.logs = ""
		"""Captured logs"""
		self.warnings = []
		"""Captured warning messages."""
		self._warnings = []

		# logging, stdout, and stderr streams
		self._log_stream = io.StringIO()
		self._stdout_stream = self._log_stream if single_output else io.StringIO()
		self._stderr_stream = self._log_stream if single_output else io.StringIO()

		# capture handlers
		self._handlers_original = {}
		self._handler = None
		self._warnings_catcher = None

		self._is_entered = False

	def __enter__(self):
		self._is_entered = True

		# capture logs
		# - set up new log handler
		self._handler = logging.StreamHandler(self._log_stream)
		self._handler.setFormatter(
			logging.Formatter("[%(levelname)-9s%(asctime)s][%(name)s] %(message)s")
		)
		self._handler.addFilter(lambda record: len(record.msg) != 0)
		self._handler.setLevel(0)

		# - save original handlers and replace them
		self._handlers_original: dict[str | None, list[logging.Handler]] = {
			None: logging.root.handlers
		}
		logging.root.handlers = [self._handler]
		for key, value in logging.root.manager.loggerDict.items():
			if isinstance(value, logging.Logger):
				self._handlers_original[key] = value.handlers
				value.handlers = [] if value.propagate else [self._handler]

		# capture stdout and stderr
		# note we can't use the sys.__stderr__ and sys.__stdout__
		# because it breaks notebooks i.e. the notebooks redirects the streams
		self._original_stdout = sys.stdout
		self._original_stderr = sys.stderr
		sys.stdout = self._stdout_stream
		sys.stderr = self._stderr_stream

		# capture warnings
		if self._single_output:
			self._logging_captures_warnings = logging._warnings_showwarning is not None  # type: ignore
			logging.captureWarnings(True)
		else:
			self._warnings_catcher = warnings.catch_warnings(record=True)
			self._warnings = self._warnings_catcher.__enter__()

		return self

	def __exit__(
		self,
		error_type: type[BaseException] | None,
		error: BaseException | None,
		tb: TracebackType | None,
	):
		self._is_entered = False

		# save to fields and file
		self._save_to_fields(error_type, error, tb)
		if self.save_dir is not None:
			self.save(reset=False)

		# restore stdout and stderr
		sys.stderr = self._original_stderr
		sys.stdout = self._original_stdout

		# restore warnings
		if self._single_output:
			logging.captureWarnings(self._logging_captures_warnings)
		else:
			assert self._warnings_catcher is not None
			self._warnings_catcher.__exit__(error_type, error, tb)

		# restore logging
		assert self._handler is not None
		logging.root.handlers = self._handlers_original.pop(None)
		for key, value in self._handlers_original.items():
			assert key is not None
			logger = logging.root.manager.loggerDict[key]
			assert isinstance(logger, logging.Logger)
			logger.handlers = value

		# close streams
		self._log_stream.close()
		self._stdout_stream.close()
		self._stderr_stream.close()

		return self._catch_errors

	def _save_to_fields(
		self,
		error_type: type[BaseException] | None = None,
		error: BaseException | None = None,
		tb: TracebackType | None = None,
	):
		"""Save the captured outputs to the public fields."""
		self.logs += self._log_stream.getvalue()
		self._log_stream = io.StringIO()

		if not self._single_output:
			self.stdout += self._stdout_stream.getvalue()
			self._stdout_stream = io.StringIO()

			self.stderr += self._stderr_stream.getvalue()
			self._stderr_stream = io.StringIO()

			if error_type is not None:
				self.error = "".join(traceback.format_exception(error_type, error, tb))
		else:
			if error_type is not None:
				self.logs += "".join(traceback.format_exception(error_type, error, tb))

		self.warnings += self._warnings

	def reset(self):
		"""Reset the captured outputs."""
		self.error = ""
		self.stdout = ""
		self.stderr = ""
		self.logs = ""
		self.warnings = []

	def update(self, other: "CaptureOutputs"):
		"""Update the captured outputs with another instance."""
		self.error += other.error
		self.stdout += other.stdout
		self.stderr += other.stderr
		self.logs += other.logs
		self.warnings += other.warnings

	def __setstate__(self, state: dict):
		self.__init__(**state)
		self.__dict__.update(state)
		return self

	@override
	def __getstate__(self):
		return {
			key: self.__dict__[key]
			for key in [
				# data:
				"error",
				"stdout",
				"stderr",
				"logs",
				"warnings",
				# state:
				"temp_dir",
				# setup:
				"_with_temp_dir",
				"_single_output",
				"_catch_errors",
			]
		}

	@property
	def summary(self):
		state = LogSummary.State.OK if self.error == "" else LogSummary.State.Error
		return LogSummary(
			state,
			error=[self.error],
			warnings=self._warnings,
			log_dir=[self.save_dir] if self.save_dir is not None else [],
		)

	def save(self, save_dir: Path | None = None, reset: bool = False):
		"""
		Save the captured outputs to the specified directory.

		Args:
			save_dir: Directory to save the captured outputs. Falls back to `self.save_dir` if not provided.
			reset: If `True`, reset the captured outputs after saving.
		"""
		save_dir = save_dir or self.save_dir
		if save_dir is None:
			raise ValueError("save_dir is not set")

		if self._is_entered:
			self._save_to_fields()
			if reset:
				self.reset()

		save_dir.mkdir(parents=True, exist_ok=True)
		for key in ["error", "warnings", "logs", "stdout", "stderr"]:
			assert hasattr(self, key)
			value = getattr(self, key)
			if value is not None and len(value) != 0:
				with open(save_dir / f"{key}.txt", "a") as file:
					if isinstance(value, list):
						value = "\n".join([str(x) for x in value])
					file.write(str(value))


class LogSummary:
	class State(Enum):
		OK = 0
		Error = 1

	def __init__(
		self,
		state: State,
		*,
		error: list[str],
		warnings: list[warnings.WarningMessage],
		log_dir: list[Path],
	):
		self.state = state
		self.error = error
		self.warnings = warnings
		self.log_dir = log_dir

	def merge(self, other: "LogSummary"):
		return LogSummary(
			self.State(max(self.state.value, other.state.value)),
			error=self.error + other.error,
			warnings=self.warnings + other.warnings,
			log_dir=self.log_dir + other.log_dir,
		)
