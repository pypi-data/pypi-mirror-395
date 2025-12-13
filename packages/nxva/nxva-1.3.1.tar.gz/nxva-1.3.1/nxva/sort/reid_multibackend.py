import cv2
import numpy as np


class BaseInference:
    """Base class for inference backends"""
    
    def __init__(self, weights, model_name, device, fp16=False):
        self.weights = weights 
        self.model_name = model_name
        self.device = device
        self.fp16 = fp16
        
    def load_model(self):
        """Load model - to be implemented by subclasses"""
        raise NotImplementedError
        
    def __call__(self, im_batch):
        """Run inference - to be implemented by subclasses"""
        raise NotImplementedError


class PyTorchInference(BaseInference):
    """PyTorch inference backend for pt and pth models"""
    
    def __init__(self, weights, model_name, device, fp16=False):
        super().__init__(weights, model_name, device, fp16)
        self.model = None
        
    def load_model(self):
        """Load PyTorch model"""
        import torch
        from .models import build_model
        from .reid_model_factory import load_pretrained_weights
        
        self.model = build_model(
            self.model_name,
            num_classes=1,
            pretrained=not(self.weights),
            use_gpu=self.device
        )
        load_pretrained_weights(self.model, self.weights)
        
        device_obj = torch.device(self.device) if isinstance(self.device, str) else self.device
        self.model.to(device_obj).eval()
        self.model.half() if self.fp16 else self.model.float()
        
    def __call__(self, im_batch):
        """Run PyTorch inference"""
        import torch
        
        # Convert numpy to torch tensor
        device_obj = torch.device(self.device) if isinstance(self.device, str) else self.device
        im_batch_tensor = torch.from_numpy(im_batch).to(device_obj)
        
        if self.fp16 and im_batch_tensor.dtype != torch.float16:
            im_batch_tensor = im_batch_tensor.half()
        
        with torch.no_grad():
            features = self.model(im_batch_tensor)
        
        # Convert torch tensor to numpy
        if isinstance(features, torch.Tensor):
            features = features.cpu().numpy()
        elif isinstance(features, (list, tuple)):
            features = [f.cpu().numpy() if isinstance(f, torch.Tensor) else f for f in features]
            features = features[0] if len(features) == 1 else features
            
        return features


class ONNXInference(BaseInference):
    """ONNX Runtime inference backend"""
    
    def __init__(self, weights, model_name, device, fp16=False):
        super().__init__(weights, model_name, device, fp16)
        self.session = None
        self.input_name = None
        self.output_name = None
        
    def load_model(self):
        """Load ONNX model"""
        import onnxruntime as ort
        
        # Determine providers based on device
        if isinstance(self.device, str):
            use_cuda = (self.device == 'cuda')
        elif hasattr(self.device, 'type'):
            use_cuda = (self.device.type == 'cuda')
        else:
            use_cuda = False
            
        providers = ['CUDAExecutionProvider'] if use_cuda else ['CPUExecutionProvider']
        
        self.session = ort.InferenceSession(self.weights, providers=providers)
        self.input_name = self.session.get_inputs()[0].name
        self.output_name = self.session.get_outputs()[0].name
        print(f'Successfully loaded ONNX model from {self.weights}')
        
    def __call__(self, im_batch):
        """Run ONNX inference"""
        features = self.session.run([self.output_name], {self.input_name: im_batch})[0]
        return features


class EngineInference(BaseInference):
    """TensorRT engine inference backend"""
    
    def __init__(self, weights, model_name, device, fp16=False):
        super().__init__(weights, model_name, device, fp16)
        self.model = None
        
    def load_model(self):
        """Load TensorRT engine model"""
        from ..nxtrt import TRTInference
        
        if "ir" in self.model_name:
            input_shape = [(1, 3, 112, 112)]
        elif "osnet" in self.model_name:
            input_shape = [(1, 3, 256, 128)]
        else:
            raise ValueError(f"Unknown model name for engine: {self.model_name}")
            
        self.model = TRTInference(self.weights, input_shape=input_shape)
        print(f'Successfully loaded engine model from {self.weights}')
        
    def __call__(self, im_batch):
        """Run TensorRT engine inference"""
        features = self.model([im_batch])
        if isinstance(features, (list, tuple)):
            return features[0] if len(features) == 1 else features
        return features

class HailoInference(BaseInference):
    """Hailo inference backend for hef models"""
    
    def __init__(self, weights, model_name, device, fp16=False):
        super().__init__(weights, model_name, device, fp16)
        self.model = None
        
    def load_model(self):
        """Load Hailo model"""
        from ..nxhailo import HefInference
        
        self.model = HefInference(self.weights)
        print(f'Successfully loaded Hailo model from {self.weights}')
        
    def __call__(self, im_batch):
        """Run Hailo inference"""
        # HefInference.__call__ expects numpy array input
        # Input format should be (N, H, W, C) for batch inference (NHWC format)
        # or (H, W, C) for single image
        
        # Ensure input is numpy array
        if not isinstance(im_batch, np.ndarray):
            im_batch = np.array(im_batch)
        
        # Call Hailo inference (HefInference.__call__ handles batch processing)
        results = self.model(im_batch)
        m = self.model.models_pool[self.model.active_model_id]
        return [results[info.name] for info in m["output_infos"]]
    
    def close(self):
        """Close Hailo model"""
        self.model.close()


def create_inference(weights, model_name, model_type, device, fp16=False):
    """Factory function to create inference instance based on model type
    
    Args:
        weights: Path to model weights
        model_name: Name of the model
        model_type: Type of model ('pt', 'pth', 'onnx', 'engine', 'hef')
        device: Device to run inference on
        fp16: Whether to use fp16 precision
        
    Returns:
        BaseInference: Inference instance for the specified backend
    """
    if model_type in ['pt', 'pth']:
        return PyTorchInference(weights, model_name, device, fp16)
    elif model_type == 'onnx':
        return ONNXInference(weights, model_name, device, fp16)
    elif model_type == 'engine':
        return EngineInference(weights, model_name, device, fp16)
    elif model_type == 'hef':
        return HailoInference(weights, model_name, device, fp16)
    else:
        raise ValueError(f"Unsupported model type: {model_type}")


class Inference:
    """Inference class wrapper that uses factory pattern"""
    
    def __init__(self, weights, model_name, model_type, device, fp16=False):
        self.inference_instance = create_inference(weights, model_name, model_type, device, fp16)
        
    def load_model(self):
        """Load model using the inference instance
        
        Returns:
            BaseInference: The loaded inference instance
        """
        self.inference_instance.load_model()
        
    def __call__(self, im_batch):
        """Run inference using the inference instance"""
        return self.inference_instance(im_batch)

    


class ReIDDetectMultiBackend:
    """ReID models MultiBackend class for python inference on various backends"""
    
    def __init__(self, weights='osnet_x0_25_msmt17.pt', device='cpu', fp16=False, pretrained=True):
        self.weights = weights
        self.model_name = (weights.split('/')[-1]).split('.')[0]
        self.model_type = (weights.split('/')[-1]).split('.')[-1]
        self.device = device
        self.fp16 = fp16
        self.pretrained = pretrained
        
        # Initialize flags
        self.pt = (self.model_type == 'pt')
        self.pth = (self.model_type == 'pth')
        self.onnx = (self.model_type == 'onnx')
        self.engine = (self.model_type == 'engine')
        self.hef = (self.model_type == 'hef')
        
        # Inference instance will be created in load_model
        self.inference = None
        self.load_model()

        # Determine resize target and normalization params based on model type
        if 'osnet' in self.model_name:
            self.target_size = (128, 256)
            self.mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
            self.std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
        elif 'ir' in self.model_name:
            self.target_size = (112, 112)
            self.mean = np.array([0.5, 0.5, 0.5], dtype=np.float32)
            self.std = np.array([0.5, 0.5, 0.5], dtype=np.float32)
        else:
            raise ValueError(f"Unknown model name: {self.model_name}")
        
    def load_model(self):
        """Load model using Inference class"""
        self.inference = Inference(
            weights=self.weights,
            model_name=self.model_name,
            model_type=self.model_type,
            device=self.device,
            fp16=self.fp16
        )
        self.inference.load_model()
        
    def _preprocess(self, imgs):
        if isinstance(imgs, np.ndarray) and len(imgs.shape) == 3:
            imgs = np.expand_dims(imgs, axis=0)

        resized_imgs = []
        for img in imgs:
            resized_img = cv2.resize(img, self.target_size, interpolation=cv2.INTER_AREA)
            resized_imgs.append(resized_img)
        # Stack resized images into 4D batch (N, H, W, C)
        batch = np.stack(resized_imgs, axis=0)
        
        # Batch operations on numpy array
        # BGR to RGB conversion (reverse last channel)
        if batch.shape[3] == 3:
            batch = batch[..., ::-1]
        
        # Convert to float32 and normalize
        batch = batch.astype(np.float32) / 255.0
        batch = (batch - self.mean) / self.std
        
        # Convert HWC to CHW format based on backend type
        # HEF models use NHWC format, others use NCHW format
        if not self.hef:
            # Convert (N, H, W, C) -> (N, C, H, W) for pt/pth/onnx/engine
            batch = np.transpose(batch, (0, 3, 1, 2))
        # HEF keeps (N, H, W, C) format
        
        # Convert to fp16 if needed
        if self.fp16:
            batch = batch.astype(np.float16)
            
        return batch
    
    def __call__(self, im_batch):
        """Forward pass - returns numpy array"""
        if self.inference is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        # Preprocess batch (numpy only)
        im_batch = self._preprocess(im_batch)
        
        # Run inference
        features = self.inference(im_batch)
        
        # Ensure output is numpy array
        if isinstance(features, (list, tuple)):
            if len(features) == 1:
                features = features[0]
            else:
                features = np.array(features)
        elif not isinstance(features, np.ndarray):
            features = np.array(features)
            
        return features

    @property
    def backend(self):
        """
        Access the underlying model backend.
        
        Returns:
            The model backend instance
        """
        return self.inference.inference_instance.model
    
    def warmup(self):
        """Warmup the model"""
        if self.inference is None:
            return
        
        # Check if device is CPU
        is_cpu = False
        if isinstance(self.device, str):
            is_cpu = (self.device == 'cpu')
        elif hasattr(self.device, 'type'):
            is_cpu = (self.device.type == 'cpu')
        else:
            is_cpu = True  # Default to CPU if unknown
            
        if is_cpu:
            return
        
        # Determine shape based on model type and backend
        shape_map = {
            "ir": ((1, 3, 112, 112), (112, 112, 3)),
            "osnet": ((1, 3, 256, 128), (256, 128, 3)),
        }
        
        shape = None
        for key, (engine_shape, default_shape) in shape_map.items():
            if key in self.model_name:
                # Use engine_shape for engine/hef, default_shape for others
                shape = engine_shape if (self.engine or self.hef) else default_shape
                break
        
        if shape is None:
            raise ValueError(f"Unknown model name: {self.model_name}")
        
        # Create dummy input and run warmup
        dummy_input = np.empty(shape, dtype=np.uint8)
        self.__call__(dummy_input)
        print('Warm Up Successfully')
