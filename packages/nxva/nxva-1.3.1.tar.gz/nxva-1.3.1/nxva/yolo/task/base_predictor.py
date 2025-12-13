import re
from typing import List, Dict, Union, Any, Tuple

import numpy as np

from ..utils import np_ops
# from ..utils.torch_utils import build_nms
from ..nn.autobackend import AutoBackend


class BasePredictor:
    """
    This class provides the foundation for all YOLO task predictors including
    detection, segmentation, pose estimation, and classification. It handles
    common functionality such as model loading, preprocessing, inference, and
    postprocessing pipeline.
    """

    DEFAULT_CONFIG = {
        'device': 'cpu',
        'conf': 0.25,
        'iou': 0.45,
        'classes': None,
        'class_names': None,
        'agnostic': False,
        'fp16': False,
        'replace': {},
        'nc': 0,
        'kpt_shape': (17, 3),
    }

    def __init__(self, config: dict):
        """Initialize the BasePredictor class."""
        # Step 1: merge defaults
        for k, v in self.DEFAULT_CONFIG.items():
            config.setdefault(k, v)

        # Step 2: validate required fields
        required_keys = ['version', 'weights', 'task', 'size']
        missing = [k for k in required_keys if config.get(k) in [None, '']]
        if missing:
            raise ValueError(f"Missing required config keys: {missing}")

        # Step 3: assign core params
        self.model_path = config['weights']
        self.task = config['task']
        self.device = config['device']
        self.version = config['version']
        self.input_shape = config['size']
        self.preprocess_transpose = not config['weights'].endswith('.hef')

        # thresholds & others
        self.conf = config['conf']
        self.iou = config['iou']
        self.classes = config['classes']
        self.class_names = config['class_names']
        self.agnostic = config['agnostic']
        self.kpt_shape = config.get('kpt_shape', None)
        self.model_name = config.get('model_name', None)
        self.nc = config.get('nc', 80)

        # Step 4: load model
        self.model = AutoBackend(self.model_path, self.device, config)

        # Step 5: init classes
        if self.class_names is None:
            if hasattr(self.model, 'names') and self.model.names is not None:
                # Get from model
                self.class_names = self.model.names
                self.nc = len(self.class_names) if self.nc == 0 else self.nc
            elif self.nc > 0:
                # Auto-generate names if only nc is known
                self.class_names = {i: f'class_{i}' for i in range(self.nc)}
            else:
                raise ValueError(
                    "Failed to initialize: both `nc` and `class_names` are None, "
                    "and model does not have `names` attribute."
                )
        # Step 6: check version
        if not re.match(r'^yolo(v?\d+|11)$', self.version):
            raise ValueError(f"Invalid YOLO version: {self.version}")

        # Step 7: pose task
        if self.task == 'pose':
            self.nc = self.nc or len(getattr(self.model, 'names', [])) or 1
            if self.kpt_shape is None:
                self.kpt_shape = getattr(self.model, 'kpt_shape', (17, 3))

        # Step 8: input shape normalization
        if isinstance(self.input_shape, int):
            self.input_shape = (self.input_shape, self.input_shape)
        elif isinstance(self.input_shape, (list, tuple)):
            self.input_shape = tuple(self.input_shape)
        else:
            raise TypeError(f"Unsupported type for input_shape: {type(self.input_shape).__name__}")

        # Step 9: sync back to config
        config.update({
            'class_names': self.class_names,
            'nc': self.nc,
            'kpt_shape': self.kpt_shape
        })
        self.config = config

    def __call__(self, imgs: List[np.ndarray]) -> List[Union[Dict[str, Any], np.ndarray]]:
        """
        Perform complete inference pipeline on input images.
        
        This method orchestrates the full inference process: preprocessing,
        model inference, and postprocessing.
        
        Args:
            imgs: Input images (a list of numpy array)
            
        Returns:
            Processed detection results
        """
        # Execute the complete inference pipeline
        pre_imgs, orig_imgs = self.preprocess(imgs)
        preds = self.infer(pre_imgs)
        dets = self.postprocess(preds, orig_imgs)
        return dets

    def preprocess(self, imgs: List[np.ndarray]) -> Tuple[np.ndarray, List[np.ndarray]]:
        """
        Prepare input images for model inference.
        
        This method performs the necessary preprocessing steps including:
        - Resizing images to the target size using letterbox
        - Converting BGR to RGB color space
        - Transposing dimensions from BHWC to BCHW format
        - Normalizing pixel values to [0, 1] range
        
        Args:
            im (List[np.ndarray]): List of input images, each of shape (H, W, 3)

        Returns:
            tuple: (preprocessed_images, original_images)
                - preprocessed_images: numpy.ndarray of shape (N, 3, H, W)
                - original_images: List of original input images
        """
            
        # Apply letterbox transformation to resize images while maintaining aspect ratio
        pre_imgs = np.stack([np_ops.letterbox(img=x, new_shape=self.input_shape) for x in imgs])
    
        # Convert BGR to RGB color space
        if pre_imgs.shape[-1] == 3:
            pre_imgs = pre_imgs[..., ::-1]  # BGR to RGB
            
        # Transpose from BHWC to BCHW format for PyTorch models
        if self.preprocess_transpose:
            pre_imgs = pre_imgs.transpose((0, 3, 1, 2))  # BHWC to BCHW, (n, 3, h, w)
        
        # Ensure memory layout is contiguous and convert to float32
        pre_imgs = np.ascontiguousarray(pre_imgs, dtype=np.float32)
    
        # Normalize pixel values from [0, 255] to [0, 1]
        pre_imgs /= 255.0
        return pre_imgs, imgs

    def infer(self, imgs: np.ndarray) -> Union[np.ndarray, List[np.ndarray], Tuple]:
        """
        Perform model inference on preprocessed images.
        
        Args:
            imgs: Preprocessed input images
            
        Returns:
            Model predictions (format depends on task type)
        """
        return self.model(imgs)

    def postprocess(self, preds: np.ndarray, orig_imgs: List[np.ndarray]):
        """
        Post-process model predictions to generate final results.
        
        This method should be implemented by subclasses to handle task-specific
        postprocessing such as NMS, coordinate transformations, and result formatting.
        
        Args:
            preds: Raw model predictions
            img: Preprocessed images
            orig_imgs: Original input images
            
        Returns:
            Processed results in task-specific format
            
        Raises:
            NotImplementedError: This method must be implemented by subclasses
        """
        raise NotImplementedError("Subclasses must implement this method")