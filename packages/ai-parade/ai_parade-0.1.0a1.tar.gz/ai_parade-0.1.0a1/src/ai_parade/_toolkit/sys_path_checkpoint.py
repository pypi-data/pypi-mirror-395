import sys
from pathlib import Path

from ai_parade._toolkit.constants import get_site_packages_path


class SysPathCheckpoint:
	def __init__(self, temp_repository: Path | None = None):
		self.temp_repository_path = temp_repository
		self._sys_path = []

	def __enter__(self):
		self._sys_path = sys.path.copy()
		if self.temp_repository_path is not None:
			try:
				site_packages = get_site_packages_path(self.temp_repository_path)
				if site_packages.exists():
					sys.path.insert(0, str(site_packages))
			except StopIteration:
				pass
			# this give precedence to repository over the site packages
			sys.path.insert(0, str(self.temp_repository_path))
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		sys.path = self._sys_path
