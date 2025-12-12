import cv2
import numpy as np
from .base import BaseInference

class ObjectDetectionInference(BaseInference):

    
    def __init__(self, onnx_model_path, onnx_yaml_path, confidence_thres=0.25, iou_thres=0.45, imgsz=None):
        """
        Initialize the object detection inference engine.
        
        Args:
            onnx_model_path (str): Path to the ONNX model file
            onnx_yaml_path (str): Path to the YAML configuration file
            confidence_thres (float): Minimum confidence threshold for detections [0, 1]
            iou_thres (float): IoU threshold for NMS [0, 1]
            imgsz (tuple, optional): Input image size. Defaults to (320, 320)
        """
        super().__init__(onnx_model_path, onnx_yaml_path, imgsz)
        self.confidence_thres = confidence_thres
        self.iou_thres = iou_thres

    def preprocess(self, img):
        """
        Preprocess input image for object detection model inference.
        
        Performs standard YOLO preprocessing:
        1. Resize image to model input size
        2. Convert BGR to RGB color space
        3. Normalize pixel values to [0, 1] range
        4. Convert from HWC to CHW format
        5. Add batch dimension
        
        Args:
            img (numpy.ndarray): Input image in BGR format with shape (H, W, C)
            
        Returns:
            numpy.ndarray: Preprocessed image tensor with shape (1, C, H, W)
        """
        # Resize image to model's expected input size
        img = cv2.resize(img, self.imgsz)
        
        # Convert color space from BGR to RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Normalize pixel values to [0, 1] range
        img = img.astype(np.float32) / 255.0
        
        # Transpose from HWC to CHW format (channels first)
        img = np.transpose(img, (2, 0, 1))  # HWC -> CHW
        
        # Add batch dimension for model input
        img = np.expand_dims(img, axis=0)
        
        return img

    def postprocess(self, img_hw, raw_output):
        """
        Postprocess raw model outputs to extract object detections.
        
        Handles different YOLO model output formats:
        - YOLOv8: Transposed output with separate confidence scores
        - YOLOv10: Direct detection format with 6 values per detection
        
        Processing steps:
        1. Parse model output based on architecture
        2. Filter detections by confidence threshold
        3. Transform coordinates to original image space
        4. Apply Non-Maximum Suppression (NMS)
        5. Format results for downstream usage
        
        Args:
            img_hw (tuple): Original image dimensions (height, width)
            raw_output (list): Raw model output tensors
            
        Returns:
            dict: Structured detection results containing:
                - model (str): Model type identifier ("object_detection")
                - result (list): List of detections, each containing:
                    - bbox (list): Bounding box coordinates [x1, y1, x2, y2]
                    - class_id (int): Detected object class ID
                    - class_name (str): Human-readable class name
                    - score (float): Detection confidence score [0, 1]
                    - result_id (int): Detection index in final results
                    
        Raises:
            ValueError: If model architecture is unsupported or output format is unexpected
        """
        results = []
        img_h, img_w = img_hw

        if self.model_name.startswith("yolov8n"):
            # YOLOv8 output format: (1, 4+num_classes, num_detections)
            # Transpose to get (num_detections, 4+num_classes)
            outputs = np.transpose(np.squeeze(raw_output[0]))
            
            # Extract confidence scores for all classes
            confidences = outputs[:, 4:]
            
            # Get class with highest confidence for each detection
            class_ids = np.argmax(confidences, axis=1)
            scores = np.max(confidences, axis=1)
            
            # Filter detections by confidence threshold
            mask = scores >= self.confidence_thres
            boxes = outputs[mask, :4]  # cx, cy, w, h format
            scores = scores[mask]
            class_ids = class_ids[mask]

            # Calculate scaling factors for coordinate transformation
            x_factor = img_w / self.imgsz[0]
            y_factor = img_h / self.imgsz[1]

            # Convert from center format (cx, cy, w, h) to corner format (x1, y1, x2, y2)
            cx, cy, w, h = boxes[:, 0], boxes[:, 1], boxes[:, 2], boxes[:, 3]
            x1 = np.clip((cx - w / 2) * x_factor, 0, img_w)
            y1 = np.clip((cy - h / 2) * y_factor, 0, img_h)
            x2 = np.clip((cx + w / 2) * x_factor, 0, img_w)
            y2 = np.clip((cy + h / 2) * y_factor, 0, img_h)

            # Convert to (x, y, width, height) format for NMS
            boxes_xywh = np.stack([x1, y1, x2 - x1, y2 - y1], axis=1).astype(np.int32)
            scores_list = scores.tolist()
            class_ids_list = class_ids.tolist()

        elif self.model_name.startswith("yolov10n"):
            # YOLOv10 output format: Direct detections with 6 values per detection
            # Format: [x1, y1, x2, y2, confidence, class_id]
            
            # Handle different output formats (list/tuple vs single array)
            arr = None
            if isinstance(raw_output, (list, tuple)):
                # Search for tensor with correct shape (N, 6)
                for item in raw_output:
                    item = np.asarray(item)
                    if item.ndim >= 2 and item.shape[-1] == 6:
                        arr = item
                        break
                if arr is None:
                    raise ValueError(
                        f"Unexpected YOLO output shape: {[np.asarray(x).shape for x in raw_output]}"
                    )
            else:
                arr = np.asarray(raw_output)

            # Remove batch dimension if present
            arr = np.squeeze(arr, axis=0) if arr.ndim == 3 else arr
            
            # Validate output shape
            if arr.ndim != 2 or arr.shape[1] != 6:
                raise ValueError(f"Unexpected YOLOv10 output shape: {arr.shape}")

            detections = arr.astype(np.float32)
            
            # Filter by confidence threshold
            mask = detections[:, 4] >= self.confidence_thres
            detections = detections[mask]
            
            if detections.size == 0:
                return {
                    "model": "object_detection",
                    "result": []
                }

            # Clip coordinates to image boundaries
            x1 = np.clip(detections[:, 0], 0, img_w)
            y1 = np.clip(detections[:, 1], 0, img_h)
            x2 = np.clip(detections[:, 2], 0, img_w)
            y2 = np.clip(detections[:, 3], 0, img_h)

            # Convert to (x, y, width, height) format for NMS
            boxes_xywh = np.stack([x1, y1, x2 - x1, y2 - y1], axis=1).astype(np.int32)
            scores_list = detections[:, 4].tolist()
            class_ids_list = detections[:, 5].astype(np.int32).tolist()

        else:
            raise ValueError(f"Unsupported model architecture: {self.model_name}")

        # Apply Non-Maximum Suppression to remove duplicate detections
        indices = cv2.dnn.NMSBoxes(
            boxes_xywh.tolist(), scores_list, self.confidence_thres, self.iou_thres
        )
        
        if len(indices) == 0:
            return {
                "model": "object_detection",
                "result": []
            }

        # Process surviving detections after NMS
        indices = np.array(indices).reshape(-1)
        for det_idx, i in enumerate(indices):
            x, y, w, h = boxes_xywh[i]
            bbox_xyxy = [int(x), int(y), int(x + w), int(y + h)]
            cls_id = int(class_ids_list[i])
            
            # Validate class ID exists in mapping
            if cls_id not in self.class_names:
                raise ValueError(f"Unknown class_id={cls_id}")
                
            results.append({
                "bbox": bbox_xyxy,
                "class_id": cls_id,
                "class_name": self.class_names[cls_id],
                "score": float(np.round(scores_list[i], 4)),
                "result_id": det_idx,
            })
            
        # Sort results by confidence score in descending order
        results.sort(key=lambda x: x["score"], reverse=True)
        
        return {
            "model": "object_detection",
            "result": results
        }

    def inference(self, image):
        """
        Perform complete object detection inference on an input image.
        
        Executes the full detection pipeline:
        1. Validate model compatibility
        2. Load model if not already loaded
        3. Preprocess input image
        4. Run model inference
        5. Postprocess results
        
        Args:
            image (numpy.ndarray): Input image in BGR format
            
        Returns:
            dict: Detection results with bounding boxes, classes, and confidence scores
            
        Raises:
            ValueError: If model is not a supported YOLO architecture
            
        Note:
            Prints original image dimensions for debugging purposes.
        """
        # Validate model architecture compatibility
        if not any(k in str(getattr(self, "model_name", "")).lower()
                  for k in ("yolov8", "yolov10", "yolov11")):
            raise ValueError(
                f"Unsupported model architecture. Expected: yolov8/yolov10/yolov11, "
                f"Found: {getattr(self, 'model_name', None)}")

        # Ensure model is loaded before inference
        self._load_model()
        
        # Preprocess image for model input
        x = self.preprocess(image)
        
        # Perform inference using ONNX Runtime
        raw_outputs = self.session.run(None, {self.input_name: x})
        
        # Debug: Print original image dimensions
        print(f"[Detection] Original image shape: {image.shape[:2]}")
        
        # Postprocess and return structured detection results
        results = self.postprocess(image.shape[:2], raw_outputs)
        return results
