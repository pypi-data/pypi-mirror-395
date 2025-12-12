import numpy as np
from .base import BaseInference
import cv2

class ImageClassificationInference(BaseInference):

    def preprocess(self, img):
        """
        Preprocess input image for classification model inference.
        
        Performs the following transformations:
        1. Resize image to model input size
        2. Convert BGR to RGB color space
        3. Normalize pixel values to [0, 1] range
        4. Convert from HWC to CHW format
        5. Add batch dimension
        
        Args:
            img (numpy.ndarray): Input image in BGR format with shape (H, W, C)
            
        Returns:
            numpy.ndarray: Preprocessed image tensor with shape (1, C, H, W)
                          ready for model inference
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
        img = np.expand_dims(img, axis=0)  # Shape: (1, C, H, W)
        
        return img

    def postprocess(self, raw_output):
        """
        Convert raw model output to structured classification results.
        
        Processes the raw logits from the model by:
        1. Applying softmax to convert logits to probabilities
        2. Creating result entries for each class
        3. Sorting results by confidence score
        4. Adding result IDs for tracking
        
        Args:
            raw_output (numpy.ndarray): Raw model output logits with shape (N, num_classes)
            
        Returns:
            dict: Structured classification results containing:
                - model (str): Model type identifier ("image_classification")
                - result (list): List of classification results, each containing:
                    - class_id (int): Numerical class identifier
                    - class_name (str): Human-readable class name
                    - score (float): Confidence probability [0, 1]
                    - result_id (int): Ranked position in results
                    
        Example:
            {
                'model': "image_classification",
                'result': [
                    {'class_id': 0, 'class_name': 'people', 'score': 0.8451, 'result_id': 0},
                    {'class_id': 1, 'class_name': 'car', 'score': 0.1549, 'result_id': 1}
                ]
            }
        """
        results = []
        
        # Extract probabilities from first batch item
        probs = raw_output[0]
        
        # # Apply softmax to convert logits to probabilities
        # probs = np.exp(probs) / np.sum(np.exp(probs))

        # Create result entry for each class
        for class_id, prob in enumerate(probs):
            # Skip classes not defined in class mapping
            if class_id not in self.class_names:
                continue
                
            # Get class name from mapping, fallback to ID string
            class_name = self.class_names.get(class_id, str(class_id))
            
            results.append({
                "class_id": class_id,
                "class_name": class_name,
                "score":  float(np.round(float(prob), 4)),
            })

        # Sort results by confidence score in descending order
        results.sort(key=lambda x: x["score"], reverse=True)

        # Add ranking information to each result
        for idx, result in enumerate(results):
            result["result_id"] = idx
            
        return {
            "model": "image_classification",
            "result": results
        }

    def inference(self, image):
        """
        Perform complete image classification inference.
        
        Executes the full inference pipeline:
        1. Load model if not already loaded
        2. Preprocess input image
        3. Run model inference
        4. Postprocess results
        
        Args:
            image (numpy.ndarray): Input image in BGR format
            
        Returns:
            dict: Classification results with confidence scores and rankings
            
        Note:
            This method prints the raw output shape for debugging purposes.
        """
        # Ensure model is loaded before inference
        self._load_model()
        
        # Preprocess image for model input
        x = self.preprocess(image)
        
        # Perform inference using ONNX Runtime
        raw = self.session.run(None, {self.input_name: x})[0]
        
        # Debug: Print raw output shape
        print(f"[Classification] Raw output shape: {raw.shape}")
        
        # Postprocess and return structured results
        return self.postprocess(raw)
