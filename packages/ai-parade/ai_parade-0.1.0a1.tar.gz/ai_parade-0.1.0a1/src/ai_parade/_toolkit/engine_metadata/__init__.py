import importlib
import pathlib
import pkgutil

from ..enums.formats import ModelFormat, Quantization
from ..enums.hw_acceleration import HardwareAcceleration
from ..enums.inference_engines import InferenceEngine
from ..enums.platform import Platform
from ._common import ModelAttributes

# Discover all modules and subpackages under this package
__all__ = []
submodules = [
	importlib.import_module(f"{__name__}.{module_info.name}")
	for module_info in pkgutil.iter_modules([str(pathlib.Path(__file__).parent)])
	if module_info.name != "_common"
]

capabilities: dict[
	InferenceEngine,
	dict[Platform, dict[Quantization, set[HardwareAcceleration]]],
] = {module.engine: module.capabilities for module in submodules}
"""
Capabilities of each inference engine on each platform for each quantization and hardware acceleration.
"""

format_distinguishes: dict[ModelFormat, list[ModelAttributes]] = {
	module.format: module.format_distinguishes for module in submodules
}
"""
A dictionary mapping model formats to lists of attributes that the format distinguishes.
"""

format: dict[InferenceEngine, ModelFormat] = {
	module.engine: module.format for module in submodules
}
"""
A dictionary mapping inference engines to model formats.
"""

__all__ = ["capabilities", "format_distinguishes", "format", "ModelAttributes"]
