import os
import importlib
from typing import Dict, List, Optional, Union, Tuple, Any
from dataclasses import dataclass

import numpy as np

from .utils.loader import load_config

@dataclass(frozen=True)
class YOLOOptions:
    weights: str = './weights/yolo11s.pt'
    version: str = 'yolo11'
    task: str = 'detect'
    size: int = 320
    device: str = 'cpu'
    model_heads: Optional[List[int]] = None
    conf: float = 0.45
    iou: float = 0.5
    nc: int = 80
    agnostic: bool = False
    classes: Optional[List[int]] = None
    class_names: Optional[Dict[int, str]] = None
    fp16: bool = False
    kpt_shape: Optional[List[int]] = None
    

class YOLO:
    """    
    This class provides a unified interface for different YOLO tasks including
    detection, segmentation, pose estimation, and classification. It dynamically
    loads the appropriate predictor based on the task specified in the configuration.
    """
    
    _REGISTER = {
        "detect"  : ("nxva.yolo.task.detect"   ,  "DetectionPredictor"     ),
        "segment" : ("nxva.yolo.task.segment"  ,  "SegmentationPredictor"  ),
        "pose"    : ("nxva.yolo.task.pose"     ,  "PosePredictor"          ),
        "classify": ("nxva.yolo.task.classify" ,  "ClassificationPredictor"),
    }

    def __init__(self, config: Union[str, YOLOOptions]):
        """
        Initialize the YOLO model with the given configuration.
        
        Args:
            config (Union[str, YOLOOptions]): Configuration object or YAML file path containing model parameters
        """

        # Load and validate configuration
        # Load config from a YAML file or a YOLOOptions object
        if isinstance(config, str) and config.endswith(('yaml', 'yml')):
            self.config = load_config(config)
        elif isinstance(config, YOLOOptions):
            self.config = {k: v for k, v in config.__dict__.items() if not k.startswith("__")}
        else:
            raise ValueError("Config must be a YAML file or object.")

        self.task = self.config.get('task', 'detect')
        # Extract module and class names for the specified task
        
        module_name, class_name = self._REGISTER[self.task]

        # Dynamically import the module and get the predictor class
        module = importlib.import_module(module_name)
        predictor_class = getattr(module, class_name)
        
        # Initialize the predictor with the configuration
        self._predictor = predictor_class(self.config)

    def __call__(self, imgs: List[np.ndarray]) -> List[Union[Dict[str, Any], np.ndarray]]:
        """
        Perform inference on input images.
        
        Args:
            imgs: List of input images as numpy arrays
            
        Returns:
            List of prediction results, format depends on task type
        """
        return self._predictor(imgs)

    @property
    def backend(self) -> Any:
        """
        Access the underlying model backend.
        
        Returns:
            The model backend instance
        """
        return self._predictor.model


class YOLOToolBox(YOLO):
    """    
    This class extends the base YOLO class with additional utility methods
    for model evaluation, export, and performance testing.
    """
    def __init__(self, config: Union[str, YOLOOptions]):
        super().__init__(config)

    def __call__(self, imgs: List[np.ndarray], img_paths: List[str]) -> List[Any]:
        """
        Perform inference and construct results using the Results object.
        
        This method overrides the parent's __call__ method to provide
        additional result processing and formatting.
        
        Args:
            imgs: List of input images as numpy arrays
            img_paths: List of image file paths
            
        Returns:
            List of Results objects containing processed predictions
        """
        return self.__construct_results(self._predictor(imgs), imgs, img_paths)
    
    def export(
        self,
        model: Optional[Any] = None,
        shape: Tuple[int, int, int, int] = (1, 3, 224, 224),
        dynamic: bool = False,
        dynamic_batch: int = 16,
        precision: str = 'fp16',
        output_path: str = 'model.onnx',
        task: str = 'torch2engine'
    ) -> None:
        """
        Export the model to different formats (ONNX, TensorRT engine, etc.).
        
        Args:
            model: Model to export (defaults to the predictor's model)
            shape: Input shape for the model (batch_size, channels, height, width)
            onnx_path: If task is onnx2engine, please input onnx path 
            dynamic: Whether to use dynamic batch size
            precision: Precision type for export (fp16, fp32, etc.)
            output_path: Path where the exported model will be saved
            task: Export task type (torch2engine, torch2onnx, onnx2engine)
            model_wrapper: Optional wrapper function to modify the model before export
        """
        if self.config['weights'].split('.')[-1] == 'pt':
            import torch
            yolo_task = self.config['task']
            if model is None:
                model = self._predictor.model.model
                model.to(torch.device(self.config['device']))

            if yolo_task == 'segment':
                def custom_forward(self, x):
                    outputs = self.model(x)
                    return outputs[0], outputs[1][-1]
            else:
                def custom_forward(self, x):
                    outputs = self.model(x)
                    return outputs[0]

            from nxva.yolo.utils.torch_utils import ExportWrapper        
            ExportWrapper.forward = custom_forward

            model = ExportWrapper(model)       

        # if self.config['weights'].split('.')[-1] != 'pt':
        #     raise ValueError("Only pt weights are supported for export")
        if self.config['weights'].split('.')[-1] == 'onnx':
            onnx_path = self.config['weights']
            
        from nxva.nxtrt.convert import Convert        
        # Validate input shape format
        assert len(shape) == 4, "The input shape must be (1, C, H, W)"
        
        # Perform the specified export task
        if task == 'torch2engine':
            Convert.torch_to_engine(model, shape, onnx_output_path=output_path, dynamic=dynamic, dynamic_batch=dynamic_batch, type=precision)
        elif task == 'torch2onnx':
            Convert.torch_to_onnx(model, shape, onnx_output_path=output_path, dynamic=dynamic)
        elif task == 'onnx2engine':
            Convert.onnx_to_engine(onnx_path, shape, dynamic=dynamic, dynamic_batch=dynamic_batch, type=precision)
        # elif task == 'onnx2jit':
        #     Convert.torch_to_jit(self.model, (1, 3, 224, 224), onnx_output_path=output_path, dynamic=False, type='fp16')
        else:
            raise ValueError(f"Unsupported task: {task}. Supported tasks: torch2engine, torch2onnx, onnx2engine")

    def speed(self, val_txt_path: str, batch_size: int = 1) -> None:
        """
        Perform speed testing on the model using validation data.
        
        This method measures the inference time for preprocessing, inference,
        and postprocessing stages separately.
        
        Args:
            val_txt_path: Path to validation data text file
            batch_size: Batch size for testing
            
        Returns:
            None (prints speed test results)
        """
        from nxva.toolbox.val import SpeedCalculator, Profile, DatasetLoader
        
        # Initialize speed calculator
        self.speed = SpeedCalculator()            
        
        # Create data loader for validation
        val_loader = DatasetLoader(val_txt_path, task=self._predictor.task, num_kpts=self._predictor.kpt_shape, batch_size=batch_size)

        #warmup
        for val_img, gt_label in val_loader:
            pre_imgs, imgs = self._predictor.preprocess(val_img)
            pred = self._predictor.infer(pre_imgs)
            dets = self._predictor.postprocess(pred, imgs)

        # Iterate through validation data and measure performance
        for val_img, gt_label in val_loader:
            
            # Create profilers for different stages
            profilers = (
                Profile(device=self._predictor.model.device),  # Preprocessing
                Profile(device=self._predictor.model.device),  # Inference
                Profile(device=self._predictor.model.device),  # Postprocessing
            )
            
            # Measure preprocessing time
            with profilers[0]:
                pre_imgs, imgs = self._predictor.preprocess(val_img)
                
            # Measure inference time
            with profilers[1]:
                pred = self._predictor.infer(pre_imgs)
                
            # Measure postprocessing time
            with profilers[2]:
                dets = self._predictor.postprocess(pred, imgs)
                
            # Update speed calculator with measurements
            self.speed.update(len(val_img), profilers)
            
        # Print speed test results
        print(self.speed.compute())
    
    def plot_results(self, results: List[Any], task: str) -> None:
        """
        Plot and save detection results.
        
        Args:
            results: List of Results objects
            task: Task name for output directory
            
        Returns:
            None
        """
        for i, result in enumerate(results):
            # create folder
            os.makedirs(f'./{task}_results', exist_ok=True)

            # save label as txt
            os.makedirs(f'./{task}_results/labels', exist_ok=True)
            result.save_txt(f'./{task}_results/labels/{task}_{i}.txt')

            # save image 
            os.makedirs(f'./{task}_results/images', exist_ok=True)
            img = result.plot(save=True, filename=f'./{task}_results/images/{task}_{i}.jpeg')

    def __construct_results(
        self,
        preds: List[Union[Dict[str, Any], np.ndarray]],
        orig_imgs: List[np.ndarray],
        img_paths: List[str]
    ) -> List[Any]:
        """
        Construct Results objects to encapsulate prediction results.
        
        This method uses the ultralytics Results object to standardize prediction
        results, enabling consistent visualization and processing across different
        YOLO tasks.
        
        Args:
            preds: List of prediction results from the model
            orig_imgs: List of original images in numpy array format
            img_paths: List of image file paths
            
        Returns:
            List of Results objects containing processed predictions
        """
        import torch
        from nxva.toolbox.result import Results
        
        results = []
        
        class_names = self.config['class_names']

        # Process predictions for each image based on task type
        for pred, orig_img, img_path in zip(preds, orig_imgs, img_paths):
            if self.task == 'detect':
                # Handle detection task - concatenate predictions if multiple detections
                if pred.shape[0] == 0:
                    pred = np.zeros((1, 6))
                pred = torch.from_numpy(pred)
                results.append(Results(orig_img=orig_img, path=img_path, names=class_names, boxes=pred[:, :6]))            
                
            elif self.task == 'pose':
                # Handle pose estimation task - separate boxes and keypoints
                boxes, kpts = pred['boxes'], pred['keypoints']
                r = Results(orig_img=orig_img, path=img_path, names=class_names, boxes=boxes)            
                r.update(keypoints=kpts)
                results.append(r)

            elif self.task == 'segment':
                # Handle segmentation task - filter predictions with valid masks
                box, masks = pred['boxes'], pred['mask']
                keep = masks.sum((-2, -1)) > 0  # only keep predictions with masks
                box, masks = box[keep], masks[keep]
                results.append(Results(orig_img=orig_img, path=img_path, names=class_names, boxes=box, masks=masks))

            elif self.task == 'classify':
                # Handle classification task - use probabilities
                results.append(Results(orig_img=orig_img, path=img_path, names=class_names, probs=pred[0]))  
        return results