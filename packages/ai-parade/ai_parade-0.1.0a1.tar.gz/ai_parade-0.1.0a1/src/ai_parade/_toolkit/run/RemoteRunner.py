import asyncio
import logging
import os
import signal
import subprocess
from enum import Enum
from pathlib import Path
from typing import Any, Callable, TypeVar, override

from rich.traceback import Traceback

from ai_parade._cli.ai_parade_puppet.communication import (
	ConnectionClosed,
	receive_async,
	send_async,
)
from ai_parade._toolkit.constants import TRACE_LVL, VENV_DIR
from ai_parade._toolkit.data.datasets.Dataset import Dataset, ModelOutput
from ai_parade._toolkit.enums import InferenceEngine
from ai_parade._toolkit.metadata.models.final import ModelMetadata, RunnerGetter

from .ModelRunner import LoadedModelRunner, ModelRunner, TReturn

logger = logging.getLogger(__name__)

ReturnType = TypeVar("ReturnType")


class MessageKind(Enum):
	"""Message kinds for the remote runner."""

	OK = "OK"
	"""Success message."""

	ERROR = "ERROR"
	"""Error message."""


class RemoteRunner(
	ModelRunner["RemoteRunner", None], LoadedModelRunner["RemoteRunner", None]
):
	"""Runs the model as separate process."""

	MAX_MEM = 6_500_000_000

	def __init__(
		self,
		model_metadata: ModelMetadata,
		inference_engine: InferenceEngine,
		weights: Path,
		local_runner: RunnerGetter,
	):
		"""Initialize the remote runner, and **NOT** yet start the process

		Args:
			model_metadata: metadata
			model_format: Format of the model.
			weights: Path to the model weights
			local_runner: runner used in the target or instead of the remote runner in case we are running runners locally

		To start the process, use `with remote_runner_instance:`
		or call directly`RemoteRunner.__enter__()`
		"""
		super().__init__(model_metadata, weights)
		assert model_metadata.repository_path is not None

		self.local_runner = local_runner
		self.venv_path = model_metadata.repository_path / VENV_DIR
		self.inference_engine = inference_engine

		self._writer = None
		self._loop = None
		self._isConnected = None
		"""Future that resolves when the remote runner is connected or None if not connected"""

		self._debugging = False
		try:
			import debugpy  # type: ignore

			self._debugging = debugpy.is_client_connected()

		except ImportError:
			pass

	async def __aenter__(self):
		self._server = await asyncio.start_server(
			self._handle_client,
			host="localhost",
			port=0,  # choose a random available port
		)
		port = self._server.sockets[0].getsockname()[1]

		self._server_task = asyncio.create_task(self._server.serve_forever())
		self._start_puppet(port)

		self._isConnected = asyncio.Future()

		logger.debug(f"Waiting for the remote runner to connect on port {port}...")
		await asyncio.wait_for(
			self._isConnected, timeout=300 if self._debugging else 60
		)
		logger.debug("Remote runner connected")

		# copy current value to the remote - triggers send
		await self.set_output_directory_async(self.output_directory)

		try:
			await self._send_command(self.__enter__.__name__)
		except Exception as e:
			await self.__aexit__(e)
			raise

		return self

	async def __aexit__(self, *err: Any):
		logger.debug("Exiting remote runner")

		self._isConnected = None

		assert self._writer is not None
		# we must close the writer before the server
		self._writer.close()
		self._writer = None
		# self._server.close()
		self._server_task.cancel()
		await self._server.wait_closed()

		self._process.kill()

	@override
	def __enter__(self):
		self._loop = asyncio.new_event_loop()
		self._loop.run_until_complete(self.__aenter__())
		return self

	@override
	def __exit__(self, *err: Any):
		assert self._loop is not None
		self._loop.run_until_complete(self.__aexit__(*err))
		self._loop.close()
		self._loop = None

	@override
	def set_output_directory(self, value: Path | None):
		assert self._loop is not None
		return self._loop.run_until_complete(self.set_output_directory_async(value))

	async def set_output_directory_async(self, value: Path | None):
		# run the base method to set the local value
		super().set_output_directory(value)

		await self._send_command(self.set_output_directory.__name__, value)

	def ensure_entered(self):
		if self._isConnected is None or not self._isConnected.done():
			raise RuntimeError("Runner used without `with` statement")

	@override
	def inference(self, dataset: Dataset) -> list[ModelOutput]:
		assert self._loop is not None
		return self._loop.run_until_complete(self.inference_async(dataset))

	async def inference_async(self, dataset: Dataset) -> list[ModelOutput]:
		self.ensure_entered()
		return await self._send_command(self.inference.__name__, dataset)

	@override
	def run(self, what: Callable[["RemoteRunner"], TReturn], *args) -> TReturn:
		assert self._loop is not None
		return self._loop.run_until_complete(self.run_async(what, *args))

	async def run_async(
		self, what: Callable[["RemoteRunner"], TReturn], *args
	) -> TReturn:
		self.ensure_entered()
		return await self._send_command(self.run.__name__, what, *args)

	@property
	@override
	def model(self):
		raise RuntimeError("Trying to get the model from a remote runner")

	def _start_puppet(self, port: int):
		environment = os.environ.copy()
		environment.pop("MPLBACKEND", None)  # Do not share the matplotlib backend
		environment["PATH"] = (
			str(self.venv_path / "bin") + os.pathsep + environment["PATH"]
		)

		logger.info("Starting remote runner process")
		self._process = subprocess.Popen(
			[
				str(self.venv_path / "bin" / "ai-parade-puppet"),
				"--weights",
				str(self.weights),
				"--repository-path",
				str(self._model_metadata.repository_path),
				"--model-name",
				self._model_metadata.name,
				"--engine",
				self.inference_engine.value,
				"--port",
				str(port),
				"--max-mem",
				str(RemoteRunner.MAX_MEM),
			]
			+ (["--debugger-port", str(5678)] if self._debugging else []),
			env=environment,
		)

	async def _send_command(self, attribute: str, *params: Any):
		assert self._writer is not None
		logger.debug("Sending command: " + attribute)
		logger.log(TRACE_LVL, f"Command {attribute}({params})")

		self._response_future = asyncio.Future()
		data = (attribute, params)

		try:
			if self._debugging:
				await asyncio.wait_for(send_async(self._writer, data), timeout=60)
				result = await self._response_future
			else:
				await asyncio.wait_for(send_async(self._writer, data), timeout=10)
				result = await asyncio.wait_for(self._response_future, timeout=15 * 60)
		except ConnectionClosed as e:
			logger.debug("Connection closed trying to get more info:")
			return_code = self._process.poll()
			if return_code is not None and -return_code in [
				signal.SIGKILL,
				signal.SIGTERM,
			]:  # negative return code == signal number on posix
				logger.info(
					f"Remote runner process has been killed (return code {return_code}), we assume it's because of OOM."
				)
				raise MemoryError(e)
			logger.info(
				f"Remote runner process has died with return code {return_code}"
			)
			raise e
		finally:
			self._response_future = None

		logger.debug(f"Command {attribute} done.")
		return result

	async def _handle_client(
		self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
	):
		assert self._isConnected is not None and not self._isConnected.done()
		self._isConnected.set_result(True)
		assert self._writer is None
		self._writer = writer

		while True:
			try:
				response = await receive_async(reader)
				self._parse_response(response)

			except Exception as e:
				if self._isConnected is None:
					break
				logger.error(f"Receive results in exception: {e}")
				if self._response_future is not None:
					self._response_future.set_exception(e)
				break

	def _parse_response(self, received: tuple[MessageKind, Any]):
		kind, output = received

		logger.log(
			TRACE_LVL, f"Received data of kind: {kind.value} with output: {output}"
		)
		if self._response_future is None:
			return

		match kind:
			case MessageKind.OK:
				self._response_future.set_result(output)
			case MessageKind.ERROR:
				inner_error = output[0]
				# inner_error.add_note(output[1])
				if "memory" in str(inner_error).lower():
					logger.info("Got error containing keyword 'memory', assume OOM")
					e = MemoryError(inner_error)
				else:
					e = RemoteError(
						output[1],
						"Error in the remote process. \n" + str(inner_error),
					)
				e.__cause__ = inner_error
				self._response_future.set_exception(e)


class RemoteError(Exception):
	"""
	Exception raised when the remote runner returns an error.
	"""

	def __init__(self, rich_traceback: Traceback, *args: object) -> None:
		self.rich_traceback = rich_traceback
		super().__init__(*args)

	def __str__(self) -> str:
		return "Remote error:\n" + repr(self.rich_traceback)
