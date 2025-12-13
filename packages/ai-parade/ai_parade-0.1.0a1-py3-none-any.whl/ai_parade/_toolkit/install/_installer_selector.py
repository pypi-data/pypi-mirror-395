from ai_parade._toolkit.metadata.custom import Customizations
from ai_parade._toolkit.metadata.models.final import InstallerGetter

from ._PackageManagerInstaller import PackageManagerInstaller
from .ModelInstaller import NOPInstaller


def choose_installer(
	install_options: bool = False,
	customizations: Customizations | None = None,
	has_conda: bool = False,
) -> InstallerGetter:
	"""Choose appropriate installer based on parameters

	Args:
		install_options: True if tools.ai-parade.install is present. Defaults to False.
		customizations: Customizations. Defaults to None.
		has_conda: True if tools.ai-parade.c.install.conda_dependencies is present. Defaults to False.

	Returns:
		Selected installer in form of InstallerGetter
	"""

	if customizations is not None and len(customizations.installers) > 0:
		installer = next(iter(customizations.installers.values()))
		return installer
	else:
		if not install_options:
			return NOPInstaller
		else:
			if has_conda:
				from ._CondaInstaller import CondaInstaller
				from ._Uv import UV

				def conda_installer(metadata):
					assert metadata.repository_path is not None
					return CondaInstaller(
						metadata,
						PackageManagerInstaller(
							metadata.repository_path,
							metadata.install,
							UV(metadata.repository_path),
						),
					)

				return conda_installer
			else:
				from ._Uv import UV

				def uv_installer(metadata):
					assert metadata.repository_path is not None
					return PackageManagerInstaller(
						metadata.repository_path,
						metadata.install,
						UV(metadata.repository_path),
					)

				return uv_installer
