from enum import StrEnum


class ModelTasks(StrEnum):
	HPE = "pose"
	HPE3D = "3d_pose"
	ObjectTracking = "tracking"
	PersonIdentification = "identification"
	FaceKeypoints = "face"
	DepthEstimation = "depth"
	ObjectDetection = "detection"
	Classification = "classification"
