import yaml
import onnxruntime as ort
import gc

class BaseInference:
    def __init__(self, onnx_model_path, onnx_yaml_path, imgsz=None):
        """
        Initialize the base inference class.
        
        Args:
            onnx_model_path (str): Path to the ONNX model file
            onnx_yaml_path (str): Path to the YAML configuration file
            imgsz (tuple, optional): Input image size. Defaults to None.
        """
        self.onnx_model_path = onnx_model_path
        self.onnx_yaml_path = onnx_yaml_path
        self.session = None
        self.input_name = None
        self.model_name = None
        self.class_names = {}
        self.model_outputs = None
        self.output_names = []
        self.num_classes = 0

        # 1️⃣ Set default image size - can be overridden by YAML config
        self.imgsz = (320, 320)

        # 2️⃣ Load configuration from YAML file
        self._load_yaml_config()

        # 3️⃣ Override with user-provided parameters if specified
        if imgsz is not None:
            self.imgsz = tuple(imgsz)

    def _load_yaml_config(self):
        """
        Load model configuration from YAML file.
        
        Parses the YAML configuration file to extract:
        - Model name
        - Class names mapping
        - Input image size
        
        Raises:
            FileNotFoundError: If YAML file doesn't exist
            yaml.YAMLError: If YAML file is malformed
        """
        with open(self.onnx_yaml_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        # Extract model name if present
        if "base_model" in data:
            self.model_name = data["base_model"]

        # Parse class names mapping and count classes
        if "labels" in data:
            self.class_names = {
                int(k) if str(k).isdigit() else str(k): v
                for k, v in data["labels"].items()
            }
            self.num_classes = len(self.class_names)

        # Set input image size from config if specified
        if "input_shape" in data:
            self.imgsz = tuple(data["input_shape"])

    def _load_model(self):
        """
        Load the ONNX model into memory using ONNX Runtime.
        
        Creates an inference session and extracts model metadata including:
        - Input tensor name
        - Output tensor information
        - Output tensor names
        
        This method is called lazily when inference is first performed.
        """
        if self.session is None:
            # Create ONNX Runtime inference session
            self.session = ort.InferenceSession(self.onnx_model_path)
            
            # Extract input tensor name (assuming single input)
            self.input_name = self.session.get_inputs()[0].name
            
            # Extract output tensor information
            self.model_outputs = self.session.get_outputs()
            self.output_names = [output.name for output in self.model_outputs]
            
            print(f"[model-mp-core] Model loaded successfully: {self.onnx_model_path}")

    def unload(self):
        """
        Unload the model from memory and perform garbage collection.
        
        This method helps free up memory by:
        - Deleting the inference session
        - Forcing garbage collection
        - Resetting session to None
        
        Should be called when the model is no longer needed.
        """
        if self.session is not None:
            del self.session
            self.session = None
            gc.collect()
            print("[model-mp-core] Model unloaded and memory freed")
