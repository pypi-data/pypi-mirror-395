import argparse
import asyncio
import inspect
import logging
import resource
import socket
import sys
from pathlib import Path

from rich.traceback import Traceback

import ai_parade._compat  # noqa: F401
from ai_parade._toolkit.run.RemoteRunner import MessageKind
from ai_parade._toolkit.run.runner_selector import get_runner
from ai_parade.toolkit import (
	CaptureOutputs,
	InferenceEngine,
	ModelMetadata,
	get_local_metadata,
)

from .communication import ConnectionClosed, receive, send

logger = logging.getLogger(__name__)

# log everything! (then save it)
logging.root.setLevel(0)


def prepare_args(
	args: argparse.Namespace,
) -> tuple[InferenceEngine, ModelMetadata, Path]:
	metadata_list = asyncio.run(get_local_metadata(args.repository_path))
	metadata = list(filter(lambda m: m.name == args.model_name, metadata_list))[0]
	engine = InferenceEngine(args.engine)

	return engine, metadata, Path(args.weights)


def define_params():
	parser = argparse.ArgumentParser(
		description="CLI tool for inference and data conversion"
	)
	parser.add_argument(
		"-e",
		"--engine",
		type=str,
		required=True,
		help="Desired inference engine of the model",
	)
	parser.add_argument(
		"-w", "--weights", type=str, required=True, help="Path to the model weights"
	)
	parser.add_argument(
		"-n",
		"--model-name",
		type=str,
		required=True,
		help="Name of model (as in the name in its metadata file)",
	)
	parser.add_argument(
		"-r",
		"--repository-path",
		type=Path,
		required=True,
		help="Name of the model repository",
	)

	parser.add_argument(
		"-p", "--port", type=int, required=True, help="Communication port"
	)

	parser.add_argument(
		"--max-memory",
		type=int,
		default=2**30,
		help="Maximum amount of memory to use in bytes",
	)

	parser.add_argument(
		"--debugger-port",
		type=int,
		help="Enable debug with debugger port",
	)
	parser.add_argument(
		"--debugger-host",
		type=str,
		help="Set debugger host (default: localhost)",
		default="localhost",
	)

	args = parser.parse_args()
	is_debugging = False
	if args.debugger_port is not None:
		is_debugging = True
		try:
			import debugpy  # type: ignore

			print(f"Is debugging? {debugpy.is_client_connected()}")

			debugpy.listen((args.debugger_host, args.debugger_port))
			print(f"Waiting for debugger to connect at port {args.debugger_port}...")
			debugpy.wait_for_client()
			print("Debugger connected.")
		except ImportError:
			print(
				"Debugpy is not installed. Please install it to enable debugging of RemoteRunner."
			)
	engine, metadata, weights = prepare_args(args)

	resource.setrlimit(resource.RLIMIT_DATA, (args.max_memory, args.max_memory))

	run_as_puppet(args, engine, metadata, weights, is_debugging)


def main():
	define_params()


if __name__ == "__main__":
	main()


def run_as_puppet(
	args: argparse.Namespace,
	engine: InferenceEngine,
	metadata: ModelMetadata,
	weights: Path,
	is_debugging: bool,
):
	"""
	Delegates the command from the main process to the runner.

	Args:
		args: Parsed CLI arguments.
		engine: Desired engine of the model.
		metadata: Metadata of the model to run.
		weights: Path to the model weights
	"""

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
		connection.connect(("localhost", args.port))
		runner = get_runner(engine, metadata, weights, use_remote=False)

		while True:
			try:
				return_value = None

				data = receive(connection)
				attribute, params = data

				if not hasattr(runner, attribute):
					raise RuntimeError(f"Unknown attribute `{attribute}`")
				maybe_method = getattr(runner, attribute)
				if inspect.ismethod(maybe_method):
					with CaptureOutputs(
						save_dir=runner.output_directory, catch_errors=False
					):
						return_value = maybe_method(*params)

					if attribute == "__enter__":
						runner = return_value
						# __enter__ outputs the loaded runner, which is not picklable
						# so just don't send it, after all the remote runner should do is to return itself
						return_value = None
				else:
					if params:
						assert len(params) == 1
						return_value = setattr(runner, attribute, params[0])
					else:
						return_value = getattr(runner, attribute)

				send(connection, (MessageKind.OK, return_value))
			except ConnectionClosed as e:
				if is_debugging:
					print("[Puppet] Connection closed:")
					print(e)
				logger.debug(f"Connection closed: {e}")
			except Exception as e:
				if is_debugging:
					print("[Puppet] Error:")
					print(e)
				rich_traceback = Traceback.from_exception(*sys.exc_info())

				# Custom errors can't be unpickled, so we don't send them
				if e.__class__.__module__ == "builtins":
					error_message = (e, rich_traceback)
				else:
					error_message = (RuntimeError(*e.args), rich_traceback)

				send(connection, (MessageKind.ERROR, error_message))
