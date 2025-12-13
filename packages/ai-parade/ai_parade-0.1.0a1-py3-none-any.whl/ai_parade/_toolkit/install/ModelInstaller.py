from abc import ABC, abstractmethod
from typing import Any, override


class ModelInstaller(ABC):
	"""Interface of model installer"""

	def __init__(self, *args: Any) -> None:
		pass

	async def is_installed(self) -> bool:
		"""Checks if model and dependencies are installed

		Returns:
			True if everything is installed
		"""
		return False

	@abstractmethod
	async def install(self, override: bool = False) -> None:
		"""Installs model and all its dependencies

		Args:
			 override: if True, will override all existing files. Defaults to False.
		"""
		pass


class NOPInstaller(ModelInstaller):
	"""Does nothing"""

	@override
	async def install(self, override: bool = False) -> None:
		pass

	@override
	async def is_installed(self) -> bool:
		return True
