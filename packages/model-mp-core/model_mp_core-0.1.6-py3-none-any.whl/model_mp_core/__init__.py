from .detection import ObjectDetectionInference
from .segmentation import SegmentInference
from .classification import ImageClassificationInference
from .tinyml import TinyMLInference

# These aliases provide backward compatibility and simplified naming
DetectionModel = ObjectDetectionInference
SegmentationModel = SegmentInference
ClassificationModel = ImageClassificationInference
TinyMLModel = TinyMLInference

# Export all available model classes for external usage
__all__ = [
    "DetectionModel", 
    "SegmentationModel",
    "ClassificationModel",
    "TinyMLModel"
]
