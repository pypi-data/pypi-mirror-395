from pathlib import Path

import pytest
from typer.testing import CliRunner

from ai_parade._cli.ai_parade.main import app

from ._common import compare_models, setup_cwd_any

runner = CliRunner()


class TestConvertCompare:
	repo_path = Path("fixtures/FooBarModel")

	@pytest.fixture(autouse=True)
	def copy_repo(self, tmp_path, monkeypatch):
		setup_cwd_any(
			tmp_path,
			monkeypatch,
			repo_path=self.repo_path,
			skip=["models"],
		)

	@pytest.mark.parametrize(
		["args", "file_name"],
		[
			pytest.param(*p, id=p[1])
			for p in [
				# LiteRT
				(
					"convert FooBarModel weights.pth tflite --artifacts build --separate-env",
					"tflite.float32.all.tflite",
				),
				(
					"convert FooBarModel weights.pth tflite --quantization float16 --separate-env",
					"tflite.float16.all.tflite",
				),
				(
					"convert FooBarModel weights.pth tflite --quantization int8 --calibration-dataset Random --separate-env",
					"tflite.int8.all.tflite",
				),
				# ncnn
				(
					"convert FooBarModel weights.pth ncnn --separate-env",
					"ncnn.float32.all.ncnn",
				),
				(
					"convert FooBarModel weights.pth ncnn --quantization float16 --separate-env",
					"ncnn.float16.all.ncnn",
				),
				(
					"convert FooBarModel weights.pth ncnn --quantization int8 --calibration-dataset Random --separate-env",
					"ncnn.int8.all.ncnn",
				),
				# Executorch
				(
					"convert FooBarModel weights.pth Executorch --hw-acceleration XNNPACK --separate-env",
					"executorch.float32.XNNPACK.pte",
				),
				(
					"convert FooBarModel weights.pth Executorch --quantization float16 --hw-acceleration XNNPACK --separate-env",
					"executorch.float16.XNNPACK.pte",
				),
				(
					"convert FooBarModel weights.pth Executorch --quantization int8 --calibration-dataset Random --hw-acceleration XNNPACK --separate-env",
					"executorch.int8.XNNPACK.pte",
				),
				(
					"convert FooBarModel weights.pth Executorch --hw-acceleration Vulkan --separate-env",
					"executorch.float32.Vulkan.pte",
				),
				(
					"convert FooBarModel weights.pth Executorch --quantization float16 --hw-acceleration Vulkan --separate-env",
					"executorch.float16.Vulkan.pte",
				),
				(
					"convert FooBarModel weights.pth Executorch --quantization int8 --calibration-dataset Random --hw-acceleration Vulkan --separate-env",
					"executorch.int8.Vulkan.pte",
				),
				# ONNX
				(
					"convert FooBarModel weights.pth ONNX --separate-env",
					"onnx.float32.all.onnx",
				),
				(
					"convert FooBarModel weights.pth ONNX --quantization float16 --separate-env",
					"onnx.float16.all.onnx",
				),
				(
					"convert FooBarModel weights.pth ONNX --quantization int8 --calibration-dataset Random --separate-env",
					"onnx.int8.all.onnx",
				),
			]
		],
	)
	def test_conversion(self, args, file_name):
		result = runner.invoke(app, args)

		assert result.exit_code == 0

		expected_path = (
			Path(__file__).parent.parent / self.repo_path / "models" / file_name
		)
		actual_path = Path(file_name)

		compare_models(expected_path, actual_path)
