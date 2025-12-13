from pathlib import Path

from ai_parade._toolkit.structural_mapping import structural_map_fx

from ._PascalVOC import PascalVOC


def ImageNet_VID(path: Path = Path("datasets/ILSVRC2015_VID")):
	if (path / "ILSVRC2015_VID").exists():
		path = path / "ILSVRC2015_VID"
	return PascalVOC(
		path,
		structural_map_fx(
			mapping={"annotation": {"object": "objects"}},
			additionalMappings={
				"objects": (
					{
						"name": "ILSVRC2015_class",
						"bndbox": {
							"xmin": "bbox_xmin",
							"xmax": "bbox_xmax",
							"ymin": "bbox_ymin",
							"ymax": "bbox_ymax",
						},
					}
				)
			},
			skip_missing=True,
		),
	)
