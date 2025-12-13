import logging
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Literal

from ai_parade._toolkit.logging import subprocess_run_log

logger = logging.getLogger(__name__)


class ONNXSimplify:
	def __init__(
		self,
		simplifier: Literal["onnxslim"] | Literal["onnxsim"] = "onnxslim",
	):
		self.simplifier = simplifier

	def simplify(
		self,
		onnx_path: Path,
	):
		with NamedTemporaryFile() as tmp_file:
			logger.info(f"Running {self.simplifier} on ONNX model")

			returncode, _, _ = subprocess_run_log(
				[
					self.simplifier,
					onnx_path,
					tmp_file.name,
				],
				logger=logger,
			)
			if returncode == 0:
				shutil.move(
					onnx_path, onnx_path.with_stem(onnx_path.stem + "_unsimplified")
				)
				shutil.copy(tmp_file.name, onnx_path)

			return returncode == 0
