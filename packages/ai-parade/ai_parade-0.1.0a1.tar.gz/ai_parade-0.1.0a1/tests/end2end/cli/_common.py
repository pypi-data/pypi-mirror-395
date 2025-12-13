import hashlib
from pathlib import Path


def setup_cwd_any(tmp_path: Path, monkeypatch, repo_path: Path, skip: list[str] = []):
	skip = skip + ["build"]
	for item in (Path(__file__).parent.parent / repo_path).iterdir():
		if item.name in skip:
			continue
		(tmp_path / item.name).symlink_to(item.resolve())

	monkeypatch.chdir(tmp_path)
	monkeypatch.setenv("VIRTUAL_ENV", str(tmp_path / ".venv"))


def compare_models(expected: Path, actual: Path) -> None:
	"""Assert that files/directories at expected and actual paths are identical."""
	expected_hash = _hash_path(expected)
	actual_hash = _hash_path(actual)
	assert expected_hash == actual_hash, f"Artifact mismatch for {expected} vs {actual}"


def _hash_path(path: Path) -> str:
	path = path.resolve()
	if path.is_file():
		with open(path, "rb") as f:
			return hashlib.file_digest(f, "sha256").hexdigest()

	if path.is_dir():
		digest = hashlib.sha256()
		for child in sorted(path.iterdir()):
			assert child.is_file(), f"Nested directories are not supported: {child}"
			digest.update(child.name.encode())
			with open(child, "rb") as f:
				digest.update(hashlib.file_digest(f, "sha256").digest())

		return digest.hexdigest()

	raise FileNotFoundError(path)
