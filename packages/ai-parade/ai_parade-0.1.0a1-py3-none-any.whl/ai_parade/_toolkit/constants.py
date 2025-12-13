import logging
from pathlib import Path

TRACE_LVL = 5
logging.addLevelName(TRACE_LVL, "TRACE")

VENV_DIR = ".venv"
CUSTOM_RUNNER_FILE_NAME = "ai-parade.py"


def get_site_packages_path(repository_path: Path) -> Path:
	return (repository_path / VENV_DIR / "lib").glob(
		"python*"
	).__next__() / "site-packages"
