from pathlib import Path

from typer.testing import CliRunner

from ai_parade._cli.ai_parade.main import app

from ._common import setup_cwd_any

runner = CliRunner()


def test_python_3_10_separate_env(tmp_path, monkeypatch):
	setup_cwd_any(
		tmp_path,
		monkeypatch,
		repo_path=Path("fixtures/EnvCheckerModel"),
	)
	result = runner.invoke(app, "inference EnvCheckerModel weights.pth --separate-env")
	assert result.exit_code == 0


def test_python_3_10_no_separate_env(tmp_path, monkeypatch):
	setup_cwd_any(
		tmp_path,
		monkeypatch,
		repo_path=Path("fixtures/EnvCheckerModel"),
	)
	result = runner.invoke(app, "inference EnvCheckerModel weights.pth")
	assert result.exit_code != 0
