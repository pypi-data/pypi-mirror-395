from pathlib import Path

from typer.testing import CliRunner

from ai_parade._cli.ai_parade.main import app

from ._common import setup_cwd_any

runner = CliRunner()


class TestCheck:
	def test_no_requirements(self, tmp_path, monkeypatch):
		setup_cwd_any(
			tmp_path,
			monkeypatch,
			repo_path=Path("fixtures/FooBarModel"),
			skip=["requirements.txt"],
		)
		result = runner.invoke(app, "check")
		assert result.exit_code == 8

	def test_no_requirements_pin(self, tmp_path, monkeypatch):
		setup_cwd_any(
			tmp_path,
			monkeypatch,
			repo_path=Path("fixtures/FooBarModel"),
			skip=["requirements.txt"],
		)
		assert not Path("requirements.txt").exists()

		result = runner.invoke(app, "check --pin-installed")

		assert Path("requirements.txt").exists()
		assert result.exit_code == 0

	def test_no_venv(self, tmp_path, monkeypatch):
		setup_cwd_any(
			tmp_path,
			monkeypatch,
			repo_path=Path("fixtures/FooBarModel"),
			skip=[".venv"],
		)

		result = runner.invoke(app, "check")

		assert result.exit_code == 8

	def test_ok(self, tmp_path, monkeypatch):
		setup_cwd_any(
			tmp_path,
			monkeypatch,
			repo_path=Path("fixtures/FooBarModel"),
		)

		result = runner.invoke(app, "check")
		print(result.output)

		assert result.exit_code == 0

	def test_with_inference(self, tmp_path, monkeypatch):
		setup_cwd_any(
			tmp_path,
			monkeypatch,
			repo_path=Path("fixtures/FooBarModel"),
		)

		result = runner.invoke(app, "check FooBarModel weights.pth")
		print(result.output)

		assert result.exit_code == 0

	def test_with_inference_missing_weights(self, tmp_path, monkeypatch):
		setup_cwd_any(
			tmp_path,
			monkeypatch,
			repo_path=Path("fixtures/FooBarModel"),
			skip=["weights.pth"],
		)

		result = runner.invoke(app, "check FooBarModel weights.pth")
		print(result.output)

		assert result.exit_code != 0
