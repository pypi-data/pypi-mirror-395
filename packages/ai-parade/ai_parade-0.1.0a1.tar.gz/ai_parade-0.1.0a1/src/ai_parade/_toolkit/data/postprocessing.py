from .datasets.Dataset import DatasetInfo
from .output import ModelOutput


def postprocess(result: ModelOutput, info: DatasetInfo):
	return bbox_rescale_back(result, info)


def bbox_rescale_back(result: ModelOutput, info: DatasetInfo):
	if "objects" not in result or len(result["objects"]) == 0:
		return result
	assert len(info.source_data_shape) == 3
	assert len(info.data_shape) == 3

	# OpenCV, PyTorch, TF uses (height, width) formats
	source_height, source_width = info.source_data_shape[:2]
	height, width = (
		info.data_shape[:2] if info.data_shape[2] == 3 else info.data_shape[1:3]
	)

	rescale = min(height / source_height, width / source_width)
	x_padding = (width - source_width * rescale) // 2
	y_padding = (height - source_height * rescale) // 2

	for object in result["objects"]:
		if (
			"bbox_xmin" not in object
			or "bbox_xmax" not in object
			or "bbox_ymin" not in object
			or "bbox_ymax" not in object
		):
			continue
		object["bbox_xmin"] = int((object["bbox_xmin"] - x_padding) / rescale)
		object["bbox_xmax"] = int((object["bbox_xmax"] - x_padding) / rescale)
		object["bbox_ymin"] = int((object["bbox_ymin"] - y_padding) / rescale)
		object["bbox_ymax"] = int((object["bbox_ymax"] - y_padding) / rescale)

	return result
