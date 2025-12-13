from pathlib import Path

import pytest
from typer.testing import CliRunner

from ai_parade._cli.ai_parade.main import app

from ._common import setup_cwd_any

runner = CliRunner()


class TestInference:
	repo_path = Path("fixtures/FooBarModel")

	@pytest.fixture(autouse=True)
	def copy_repo(self, tmp_path, monkeypatch):
		setup_cwd_any(
			tmp_path,
			monkeypatch,
			repo_path=self.repo_path,
			skip=[],
		)

	@pytest.mark.parametrize(
		[
			"args",
		],
		[
			pytest.param(*p, id=p[0].removeprefix("inference FooBarModel "))
			for p in [
				("inference FooBarModel weights.pth --separate-env",),
				("inference FooBarModel models/onnx.float32.all.onnx --separate-env",),
				("inference FooBarModel models/onnx.float16.all.onnx --separate-env",),
				("inference FooBarModel models/onnx.int8.all.onnx --separate-env",),
			]
		],
	)
	def test_inference(self, args):
		result = runner.invoke(app, [*args.split(" ")])

		assert result.exit_code == 0
