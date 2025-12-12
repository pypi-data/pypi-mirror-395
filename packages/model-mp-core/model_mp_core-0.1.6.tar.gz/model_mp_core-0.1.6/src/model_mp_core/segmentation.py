import cv2
import numpy as np
import yaml
from .base import BaseInference

class SegmentInference(BaseInference):

    def __init__(self, onnx_model_path, onnx_yaml_path, confidence_thres=0.1, iou_thres=0.45, imgsz=None):
        """
        Initialize the segmentation inference engine.
        
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
        self.num_masks = 32  # YOLOv8-seg model has 32 mask prototypes
        self.size = (imgsz, imgsz) if isinstance(imgsz, int) else imgsz
        
        # Check model compatibility based on YAML configuration
        self._check_model_compatibility_from_yaml(onnx_yaml_path)

    def _check_model_compatibility_from_yaml(self, yaml_path):
        """
        Check model compatibility based on model_name field in YAML configuration.
        
        Reads the YAML configuration file to determine the model type. Only YOLOv8n
        models are supported. Program will terminate if unsupported models are detected.
        
        Args:
            yaml_path (str): Path to the YAML configuration file
            
        Raises:
            ValueError: If the model type is not YOLOv8n or if YAML cannot be read
        """
        try:
            with open(yaml_path, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)
            
            model_name = config.get('base_model', '').lower()
            # Check if it's YOLOv11 or YOLOv8, if not, exit
            if 'yolo11' not in model_name and 'yolov8' not in model_name:
                raise ValueError("Only YOLOv8 and YOLO11 models are supported. Please check the model path or format.")

                
        except FileNotFoundError:
            raise ValueError(f"YAML configuration file not found: {yaml_path}")
            
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML format: {e}")
            
        except Exception as e:
            if isinstance(e, ValueError):
                raise
            raise ValueError(f"Error reading YAML configuration: {e}")

    def inference(self, img):
        """
        Perform complete image segmentation inference on an input image.
        
        Executes the full segmentation pipeline:
        1. Load model if not already loaded
        2. Preprocess input image with padding preservation
        3. Run model inference to get detections and mask prototypes
        4. Postprocess results to generate final segmentation masks
        
        Args:
            img (numpy.ndarray): Input image in BGR format
            
        Returns:
            dict: Segmentation results with bounding boxes, masks, and metadata
            
        Note:
            Contains commented debugging code for analysis of model outputs.
            The debugging section saves detection data to CSV for inspection.
        """
        # Ensure model is loaded before inference
        self._load_model()
        
        # Preprocess image and store transformation parameters
        input_data, (self.scale, self.top, self.left), (orig_h, orig_w) = \
            self.preprocess(img, self.size)
            
        # Perform inference using ONNX Runtime
        raw_outputs = self.session.run(None, {self.input_name: input_data})
        
        # Postprocess raw outputs to generate final segmentation results
        results = self.postprocess(raw_outputs, (orig_h, orig_w))
        return results


    def preprocess(self, img: np.ndarray, new_shape: tuple[int, int]) -> np.ndarray:
        """
        Preprocess input image for segmentation model inference.
        
        Performs aspect-ratio preserving resize with padding to maintain
        original image proportions while fitting the model's input requirements.
        
        Processing steps:
        1. Calculate optimal scaling factor preserving aspect ratio
        2. Resize image using calculated scale
        3. Add gray padding (value 114) to reach target dimensions
        4. Convert BGR to RGB and normalize to [0, 1]
        5. Transpose from HWC to CHW format
        6. Add batch dimension
        
        Args:
            img (np.ndarray): Input image in BGR format with shape (H, W, C)
            new_shape (tuple[int, int]): Target shape for resizing as (height, width)
            
        Returns:
            tuple: Contains three elements:
                - input_data (np.ndarray): Preprocessed image tensor (1, 3, H, W)
                - transform_params (tuple): Scaling and padding info (scale, top, left)
                - original_shape (tuple): Original image dimensions (orig_h, orig_w)
                
        Note:
            The padding values (top, left) and scale factor are stored for
            coordinate transformation during postprocessing.
        """
        # Get original image dimensions
        orig_h, orig_w = img.shape[:2]
        
        # Use default image size if not specified
        if new_shape is None:
            new_shape = self.imgsz
        target_h, target_w = new_shape

        # Calculate optimal scaling factor preserving aspect ratio
        scale = min(target_h / orig_h, target_w / orig_w)
        new_w, new_h = int(orig_w * scale), int(orig_h * scale)
        
        # Resize image with calculated dimensions
        resized_img = cv2.resize(img, (new_w, new_h))

        # Create padded image with gray background (114 is standard YOLO padding value)
        padded_img = np.full((target_h, target_w, 3), 114, dtype=np.uint8)
        
        # Calculate padding offsets to center the resized image
        top = (target_h - new_h) // 2
        left = (target_w - new_w) // 2
        
        # Place resized image in center of padded canvas
        padded_img[top:top + new_h, left:left + new_w] = resized_img

        # Convert BGR to RGB and normalize pixel values to [0, 1]
        img_rgb = cv2.cvtColor(padded_img, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
        
        # Transpose from HWC to CHW format (channels first)
        img_chw = np.transpose(img_rgb, (2, 0, 1))
        
        # Add batch dimension for model input
        input_data = np.expand_dims(img_chw, axis=0)

        return input_data, (scale, top, left), (orig_h, orig_w)

    def postprocess(self, raw_outputs, orig_shape):
        """
        Postprocess YOLOv8-seg model outputs to generate segmentation results.
        
        Processes the raw detection and mask prototype outputs by:
        1. Parsing detection results and mask coefficients
        2. Filtering detections by confidence threshold
        3. Applying Non-Maximum Suppression (NMS)
        4. Generating segmentation masks from prototypes
        5. Transforming coordinates back to original image space
        
        Args:
            raw_outputs (list): Raw model output tensors containing:
                - raw_outputs[0]: Detection results (1, num_dets, 4+1+num_classes+num_masks)
                - raw_outputs[1]: Mask prototypes (1, num_masks, mask_h, mask_w)
            orig_shape (tuple): Original image dimensions (height, width)
            
        Returns:
            dict: Structured segmentation results containing:
                - model (str): Model type identifier ("segmentation")
                - result (list): List of segmentation results, each containing:
                    - bbox (list): Bounding box coordinates [x1, y1, x2, y2]
                    - class_id (int): Detected object class ID
                    - class_name (str): Human-readable class name
                    - score (float): Detection confidence score [0, 1]
                    - mask (np.ndarray): Segmentation mask (H, W) with values [0, 1]
                    - result_id (int): Detection index in final results
                    - area (int): Pixel area of the mask (calculated as the sum of mask pixels)
                    - mask_coords (list): List of [x, y] coordinates defining the mask contour
        """
        # Parse model outputs
        detections = np.squeeze(raw_outputs[0]).T  # Shape: (num_dets, 4+1+num_classes+num_masks)
        mask_prototypes = np.squeeze(raw_outputs[1], axis=0)  # Shape: (num_masks, mask_h, mask_w)
        # test_mask = detections.shape[1] - 4 - self.num_classes
        # Debug information for understanding output structure
        # print(f"test_mask: {test_mask}")  # (N, 4+1+nc+nm)
        # print(f"Sample detection row: {detections[0, :10]}")  # First 10 values
        # print(f"Number of classes: {self.num_classes}")
        
        # Initialize lists for filtered results
        boxes, scores, class_ids, mask_coeffs = [], [], [], []

        # Process each detection
        for row in detections:
            # Extract bounding box coordinates (center format)
            cx, cy, w, h = row[:4]
            
            # Extract class probabilities (skip objectness score at index 4)
            class_probs = row[4:4 + self.num_classes]

            if class_probs.size == 0:
                return {"model": "segmentation", "result": []}  
            
            # Find class with highest probability
            cls_id = np.argmax(class_probs)
            score = class_probs[cls_id]
            
            # Filter by confidence threshold
            if score > self.confidence_thres:
                boxes.append([cx, cy, w, h])
                scores.append(float(score))
                class_ids.append(int(cls_id))
                # Extract mask coefficients (last 32 values for YOLOv8-seg)
                mask_coeffs.append(row[4 + self.num_classes:])

        # Return empty result if no detections pass threshold
        if not boxes:
            return {"model": "segmentation", "result": []}

        # Prepare data for Non-Maximum Suppression (NMS)
        cx, cy, w, h = np.array(boxes).T
        x = cx - w / 2  # Convert center format to corner format
        y = cy - h / 2
        boxes_for_nms = np.column_stack((x, y, w, h))
        
        # Apply NMS to remove duplicate detections
        indices = cv2.dnn.NMSBoxes(boxes_for_nms.tolist(), scores,
                                   self.confidence_thres, self.iou_thres)
        
        if len(indices) == 0:
            return {"model": "segmentation", "result": []}

        # Extract final results after NMS
        final_boxes, final_scores, final_class_ids, final_coeffs = [], [], [], []
        for i in indices:
            final_boxes.append(boxes[i])
            final_scores.append(scores[i])
            final_class_ids.append(class_ids[i])
            final_coeffs.append(mask_coeffs[i])

        # Generate segmentation masks from prototypes and coefficients
        mask_coeffs_array = np.array(final_coeffs)
        proto_h, proto_w = mask_prototypes.shape[1:]

        # Reshape prototypes for matrix multiplication
        prototypes_reshaped = mask_prototypes.reshape(self.num_masks, -1)

        # Combine mask coefficients with prototypes
        masks = np.matmul(mask_coeffs_array, prototypes_reshaped)  # Shape: (num_selected, H*W)
        masks = masks.reshape(-1, proto_h, proto_w)
        
        # Apply sigmoid activation to get probability masks
        masks_sigmoid = 1 / (1 + np.exp(-masks))

        # Transform masks and coordinates back to original image space
        final_masks = []
        orig_h, orig_w = orig_shape
        
        for i in range(len(final_boxes)):
            mask = masks_sigmoid[i]

            # Remove padding from mask coordinates
            crop_top = self.top * proto_h // self.imgsz[0]
            crop_left = self.left * proto_w // self.imgsz[1]
            crop_h = mask.shape[0] - 2 * crop_top
            crop_w = mask.shape[1] - 2 * crop_left
            
            # Crop mask to remove padding
            mask_cropped = mask[crop_top:crop_top + crop_h,
                              crop_left:crop_left + crop_w]
            
            # Resize mask to original image dimensions
            mask_resized = cv2.resize(mask_cropped, (orig_w, orig_h),
                                     interpolation=cv2.INTER_LINEAR)
            
            # Store final mask (continuous values for better visualization)
            # mask_bin = (mask_resized > 0.5).astype(np.uint8)  # Binary mask option
            final_masks.append(mask_resized)

            # Transform bounding box coordinates back to original image space
            cx, cy, w, h = final_boxes[i]
            final_boxes[i] = [
                int((cx - w / 2 - self.left) / self.scale),
                int((cy - h / 2 - self.top) / self.scale),
                int((cx + w / 2 - self.left) / self.scale),
                int((cy + h / 2 - self.top) / self.scale)
            ]

        # Format final results
        results = []
        for i in range(len(final_boxes)):
            # Calculate mask area and contours
            mask = final_masks[i]
            mask_bin = (mask > 0.5).astype(np.uint8)
            area = int(np.sum(mask_bin))
            
            # Get mask coordinates (contours)
            contours, _ = cv2.findContours(mask_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            mask_coords = []
            if contours:
                # Take the largest contour
                c = max(contours, key=cv2.contourArea)
                mask_coords = c.reshape(-1, 2).tolist()

            results.append({
                "bbox": final_boxes[i],
                "score": float(np.round(final_scores[i], 4)),
                "class_id": final_class_ids[i],
                "class_name": self.class_names[final_class_ids[i]],
                "mask": mask,
                "result_id": i,
                "area": area,
                "mask_coords": mask_coords
            })
            
        # Sort results by confidence score in descending order
        results.sort(key=lambda x: x["score"], reverse=True)

        return {"model": "segmentation", "result": results}