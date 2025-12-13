"""
AutoBackend Class - Automatic Backend Model Loader

This class provides a unified interface to automatically load YOLO models in different formats.
It supports multiple model formats (PyTorch, ONNX, TensorRT Engine, TorchScript, Hailo HEF) and task types
(detection, segmentation, pose estimation, classification).

Main Features:
- Automatically selects appropriate backend handler based on model file extension
- Supports multiple YOLO task types
- Provides unified model loading and inference interface
- Automatically handles model loading for different devices (CPU/GPU)
"""


import os
from pathlib import Path
import numpy as np

import logging
LOGGER = logging.getLogger(__name__)


class AutoBackend:
    _REGISTER = {}
    def __init__(self, model_path: str, device: str, config: dict):
        """
        Initialize the automatic backend loader
        
        Args:
            model_path (str): Path to the model file
            device (str): Computing device (e.g., 'cpu', 'cuda:0')
            config (dict): Configuration dictionary, must contain 'task' and 'version' keys
        
        Raises:
            ValueError: Raised when task type is not supported or model format is not supported
        """
        self.model_path = model_path
        self.config = config
        self.device = device
        self.model = self.load_model()  # Load the model during initialization

    def __init_subclass__(cls, *, exts: str, **kwargs):
        super().__init_subclass__(**kwargs)
        for ext in exts:
            cls._REGISTER[ext.lower()] = cls

    def __new__(cls, model_path, *args):
        if cls is AutoBackend:
            suffix = Path(model_path).suffix.lower()
            real_cls = cls._REGISTER[suffix]
            return super().__new__(real_cls)
        return super().__new__(cls)

    def __call__(self, imgs):
        """
        Execute model inference
        
        This is an abstract method that subclasses must implement to perform actual inference.
        
        Args:
            imgs: Input images, format determined by specific implementation
            
        Returns:
            Inference results, format determined by specific implementation
            
        Raises:
            NotImplementedError: Raised when subclass does not implement this method
        """
        raise NotImplementedError("Subclasses should overwrite this method to run the detection!")
        
    def load_model(self):
        """
        Load the model
        
        This is an abstract method that subclasses must implement to load models of corresponding format.
        
        Returns:
            Loaded model object
            
        Raises:
            NotImplementedError: Raised when subclass does not implement this method
        """
        raise NotImplementedError("Subclasses should overwrite this method to load the model!")
        
        
class EngineHandler(AutoBackend, exts=['.engine']):
    def __init__(self, model_path, device, config: dict):
        super().__init__(model_path, device, config)
        
    def __call__(self, imgs):
        return self.model([imgs])

    def load_model(self):
        from nxva.nxtrt import TRTInference        
        self.input_shape = self.config['size']
        return TRTInference(self.config['weights'],  [(1, 3, self.input_shape[0], self.input_shape[1])])

    
class TorchHandler(AutoBackend, exts=['.pt', '.pth']):
    _torch_module = None
    def __init__(self, model_path, device, config: dict):
        super().__init__(model_path, device, config)      

    def __call__(self, imgs):
        imgs = TorchHandler._torch_module.from_numpy(imgs)
        with TorchHandler._torch_module.no_grad():
            pred = self.model(imgs.to(self.device))
        return self.to_numpy_recursive(pred)

    def load_model(self):   
        if TorchHandler._torch_module is None:
            import torch
            TorchHandler._torch_module = torch

        from ..utils.torch_utils import attempt_load
        if self.device.split(':')[0] == 'cuda' and not TorchHandler._torch_module.cuda.is_available():
            LOGGER.warning("CUDA is not available, using CPU")
            self.device = 'cpu'

        replace = self.replace_module(self.config)
        model = attempt_load(self.config['weights'], device=self.device, replace=replace, task=self.config['task'], version=self.config['version'])
        model = model.half().eval() if self.config['fp16'] else model.float().eval()
        return model

    def replace_module(self, config: dict):
        # just for .pt
        version = config['version'].lower()
        task = config['task']
        if version == 'yolov5':
            if task == 'pose':
                config['replace'] = {'Detect': 'PoseV5', 'Model': 'PoseModel', 'Upsample': 'torch1_10_Upsample'}
            elif task == 'detect':
                config['replace'] = {'Detect': 'DetectV5', 'Model': 'DetectionModel', 'Upsample': 'torch1_10_Upsample'}
            elif task == 'segment':
                config['replace'] = {'Segment': 'SegmentV5', 'Detect': 'DetectV5'}
            elif task == 'classify':
                config['replace'] = {'Classify': 'ClassifyV5'}
        elif version in ['yolov5u', 'yolov8', 'yolo11']: 
            if task == 'pose':
                config['replace'] = {'Pose': 'PoseV11', 'Detect': 'DetectV11'}
            elif task == 'detect':
                config['replace'] = {'Detect': 'DetectV11'}
            elif task == 'segment':
                config['replace'] = {'Segment': 'SegmentV11', 'Detect': 'DetectV11'}
            elif task == 'classify':
                config['replace'] = {'Classify': 'ClassifyV11'}
        else:
            raise ValueError(f"Unsupported version: {version}. Supported versions: yolov5, yolov5u, yolov8, yolo11")
        return config['replace']

    def to_numpy_recursive(self, obj):
        """
        Recursively convert all torch.Tensor in obj to numpy.ndarray.
        Convert tuple to list, and keep the original structure for other types.

        Args:
            obj: Any nested structure containing tensors, tuples, lists, dicts, etc.

        Returns:
            The same structure with all tensors converted to numpy arrays,
            and all tuples converted to lists.
        """
        # If it's a torch.Tensor, convert to numpy
        if isinstance(obj, TorchHandler._torch_module.Tensor):
            return obj.cpu().numpy()
        # If it's a tuple, convert to list and recursively process each element
        elif isinstance(obj, tuple):
            return [self.to_numpy_recursive(item) for item in obj]
        # If it's a list, recursively process each element
        elif isinstance(obj, list):
            return [self.to_numpy_recursive(item) for item in obj]
        # If it's a dict, recursively process each value
        else:
            return obj


class OnnxHandler(AutoBackend, exts=['.onnx']):
    def __init__(self, model_path, device, config: dict):
        super().__init__(model_path, device, config)
        self.version = self.config['version']
        self.task = self.config['task']

    def __call__(self, imgs):
        pred = self.model.run(None, {self.model.get_inputs()[0].name: imgs})
        return pred

    def load_model(self):
        import onnxruntime as ort
        if self.device.split(':')[0] == 'cuda':
            if ort.get_available_providers() == ['CPUExecutionProvider']:
                LOGGER.warning("CUDA is not available, using CPU")
                providers = ["CPUExecutionProvider"]
                return ort.InferenceSession(self.config['weights'], providers=providers)
            else:
                device_id = self.device.split(':')[1]
                if device_id is None:
                    device_id = 0
                providers = [("CUDAExecutionProvider", {"device_id": device_id})]
                return ort.InferenceSession(self.config['weights'], providers=providers)
        elif self.device == 'cpu':
            providers = ["CPUExecutionProvider"]
            return ort.InferenceSession(self.config['weights'], providers=providers)
        else:
            raise ValueError(f"Unsupported provider: {self.device}")

        
class JitHandler(AutoBackend, exts=['.jit']):
    _torch_module = None
    def __init__(self, model_path, device, config: dict):
        super().__init__(model_path, device, config)

    def __call__(self, imgs):
        with JitHandler._torch_module.no_grad():
            pred = self.model(imgs)[0]
        return pred

    def load_model(self):
        if JitHandler._torch_module is None:
            import torch
            JitHandler._torch_module = torch
        if self.device.split(':')[0] == 'cuda' and not JitHandler._torch_module.cuda.is_available():
            LOGGER.warning("CUDA is not available, using CPU")
            self.device = 'cpu'

        model = JitHandler._torch_module.jit.load(self.config['weights'], map_location=self.device)
        model = model.half().eval() if self.fp16 else model.float().eval()
        return model


class NefHandler(AutoBackend, exts=['.nef']):
    dev_dict = {} #port_id : dev
    def __init__(self, model_path, device, config:dict):
        super().__init__(model_path, device, config)
        from nxva.nxkp import decode_yolo_head

        self.input_shape = self.config['size']
        self.version = self.config['version']
        self.task = self.config['task'] 
        self.model_id = self.config['model_id']
        self.decode_yolo_head = decode_yolo_head

    def __call__(self, imgs):
        results = []
        for img in imgs:
            results.append(self.decode_yolo_head(self.model.infer(img, model_id=self.model_id), img_size=(self.input_shape[0], self.input_shape[1]), version=self.version, task=self.task))
        return np.concatenate(results, axis=0)
    
    def load_model(self):
        from nxva.nxkp import KneronDevice, InferenceSession, scan_devices
        #parse device
        usb_port_id = self.config.get('usb_port_id', None)
        device_config = self.device.split(':')
        _, platform, *rest = device_config
        device_id = int(rest[0]) if rest else None

        if usb_port_id is not None:
            pass
        elif device_id is not None:
            platform_id = int('100' if platform == '520' else platform, 16)
            scan_results = [d.usb_port_id for d in scan_devices() if d.product_id == platform_id]

            if device_id >= len(scan_results):
                raise ValueError(f"device id not found in device: {device_id}")
            
            usb_port_id = scan_results[device_id]
        else:
            raise ValueError(f"usb port id or device id not found")
            
        if usb_port_id in self.dev_dict:
            dev = self.dev_dict[usb_port_id]
        else:
            dev = KneronDevice(platform=platform)
            dev.usb_port_id = usb_port_id
            dev.connect()
            self.dev_dict[usb_port_id] = dev

        session = InferenceSession(
            device=dev,
            nef_path=self.config['weights'],
            version = self.config['version'],
            task = self.config['task'],
            max_inflight = 1
        )
        return session
        

class HefHandler(AutoBackend, exts=['.hef']):
    def __init__(self, model_path, device, config:dict):
        super().__init__(model_path, device, config)
        from nxva.nxhailo import HailoFeatPostFactory, HailoFeatPreFactory
        from .modules.decode_head import DecodeHead

        self.version = self.config['version']
        self.task = self.config['task']
        self.size = self.config['size']
        self.decode_head = DecodeHead(version=self.version, task=self.task, nc=self.config['nc'], kpt_shape=self.config['kpt_shape'])
        self.preprocess_feat = HailoFeatPreFactory.create(version=self.version, task=self.task)
        self.postprocess_feat = HailoFeatPostFactory.create(version=self.version, task=self.task)
        self.m = self.model.models_pool[self.model_id]

    def __call__(self, imgs):
        input_data = self.preprocess_feat({self.m["input_info"][0]: imgs})
        results = self.model(input_data)
        return [self.decode_head(self.postprocess_feat(results, self.m))]

    def load_model(self):
        from nxva.nxhailo import HefInference

        model = HefInference(self.config['weights'])
        self.model_id = model.model_id
        return model

    def close(self):
        self.model.close()