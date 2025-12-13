from dataclasses import dataclass
from typing import List

# backward compatibility <=3.11: typing import TypedDict
from typing_extensions import TypedDict


@dataclass(frozen=True)
class Output:
	"""
	Represents the output specification of the model.
	"""

	shape: List[int]
	"""Shape of the output data."""


class ObjectsObject(TypedDict, total=False):
	# coco_class: int
	bbox_xmin: float
	bbox_xmax: float
	bbox_ymin: float
	bbox_ymax: float
	ILSVRC2015_class: str
	confidence: float
	ImageNet_1k_class: int
	class_label: str


class ModelOutput(TypedDict, total=False):
	"""
	Represents the output of the model.

	Currently only vision models are supported.
	"""

	objects: list[ObjectsObject]
