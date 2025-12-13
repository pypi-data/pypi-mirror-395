#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Custom PyTorch Model Serialization/Deserialization Tool

This module provides a custom model loading function that can work with custom pickle modules,
used for loading YOLOv5 and YOLOv11 models, and supports module path mapping.

Main Features:
- Support for custom pickle modules
- Automatic module path mapping handling
- Compatible with YOLOv5 and YOLOv11
- Provides detailed debug information

Usage Example:
    from serialization import custom_load, create_custom_pickle_module
    
    pickle_module = create_custom_pickle_module({"DetectV5": "Detect"})
    model = custom_load('model.pt', pickle_module=pickle_module)

if you want to add block, head, etc., following the steps below:
    1. add block, head, code etc. into the nn.modules, nn.models correspoding file
    2. add the new module to the __init__.py file
"""

import io, os, glob, yaml, importlib, pickle, re
from pathlib import Path
from typing import Union


import cv2, torch, numpy as np

class CustomModelLoader:
    """
    Custom PyTorch model loader for YOLO models with module path mapping support.
    
    This class handles loading of PyTorch checkpoint files (.pt) for YOLO models,
    with special handling for different YOLO versions (v5, v8, v11) and tasks
    (detection, segmentation, pose estimation, classification).
    
    The loader supports automatic module path remapping to handle compatibility
    issues between different YOLO implementations and PyTorch versions.
    
    Attributes:
        path (str): Path to the model checkpoint file
        map_location (str or torch.device): Device to map tensors to (e.g., 'cpu', 'cuda:0')
        loaded_storages (dict): Cache of loaded tensor storages to avoid duplicate loading
        pickle_load_args (dict): Arguments for pickle loading (encoding settings)
        torch_verson (str): PyTorch version in major.minor format (e.g., '1.10', '1.13')
        replace (dict): Module name mapping dictionary for class name replacement
        restore_location (callable): Function to restore tensor storage location
    """
    def __init__(self, path, model_version='yolov5', task='detect', map_location='cpu'):
        """
        Initialize the custom model loader.
        
        Args:
            path (str): Path to the PyTorch checkpoint file (.pt)
            model_version (str): YOLO model version. Options: 'yolov5', 'yolov5u', 'yolov8', 'yolo11'
            task (str): Task type. Options: 'detect', 'segment', 'pose', 'classify'
            map_location (str or torch.device): Device to load tensors to. Default: 'cpu'
        """
        self.path = path
        self.map_location = map_location
        self.loaded_storages = {}  # Cache for loaded tensor storages
        self.pickle_load_args = {'encoding': 'utf-8'}  # Pickle loading arguments

        # Automatically get torch major.minor version, e.g., '1.10', '1.13'
        self.torch_verson = self._get_torch_version()

        # Replace module mapping - maps original class names to new class names
        self.replace = self._replace_module(model_version, task)

        # Get restore_location corresponding to map_location
        # This function handles device mapping for tensor storages
        self.restore_location = self._get_restore_location(map_location, self.torch_verson)

    # ---------------- private helpers ------------------
    def _replace_module(self, version, task):
        """
        Generate module name replacement mapping based on YOLO version and task.
        
        This mapping is used to remap class names from the original checkpoint
        to the corresponding classes in the nxva.yolo module structure.
        
        Args:
            version (str): YOLO model version ('yolov5', 'yolov5u', 'yolov8', 'yolo11')
            task (str): Task type ('detect', 'segment', 'pose', 'classify')
            
        Returns:
            dict: Mapping from original class names to new class names
                Format: {original_name: new_name}
                
        Raises:
            ValueError: If version or task is not supported
        """
        if version == 'yolov5':
            if task == 'pose':
                replace = {'Detect': 'PoseV5', 'Model': 'PoseModel', 'Upsample': 'torch1_10_Upsample'}
            elif task == 'detect':
                replace = {'Detect': 'DetectV5', 'Model': 'DetectionModel', 'Upsample': 'torch1_10_Upsample'}
            elif task == 'segment':
                replace = {'Segment': 'SegmentV5', 'Detect': 'DetectV5'}
            elif task == 'classify':
                replace = {'Classify': 'ClassifyV5'}
            else:
                raise ValueError(f"Unsupported task: {task}")
        elif version in ['yolov5u', 'yolov8', 'yolo11']:
            if task == 'pose':
                replace = {'Pose': 'PoseV11', 'Detect': 'DetectV11'}
            elif task == 'detect':
                replace = {'Detect': 'DetectV11'}
            elif task == 'segment':
                replace = {'Segment': 'SegmentV11', 'Detect': 'DetectV11'}
            elif task == 'classify':
                replace = {'Classify': 'ClassifyV11'}
            else:
                raise ValueError(f"Unsupported task: {task}")
        else:
            raise ValueError(f"Unsupported version: {version}. Supported versions: yolov5, yolov5u, yolov8, yolo11")
        return replace

    def _get_classes_from_module(self, module_path):
        """
        Extract all class definitions from a module and return their full qualified names.
        
        This method imports a module and collects all class objects, creating a mapping
        from class name to its fully qualified module path (e.g., 'DetectV5' -> 'nxva.yolo.nn.modules.head.DetectV5').
        
        Args:
            module_path (str): Dot-separated module path (e.g., 'nxva.yolo.nn.modules')
            
        Returns:
            dict: Mapping from class name to fully qualified class path
                Format: {class_name: 'module.path.ClassName'}
                Returns empty dict if module cannot be imported
        """
        try:
            mod = importlib.import_module(module_path)
            # Extract all classes from module and create qualified name mapping
            return {cls.__name__: f"{cls.__module__}.{cls.__qualname__}" for cls in mod.__dict__.values() if isinstance(cls, type)}
        except ImportError:
            return {}

    def _open_file(self, name_or_buffer, mode='rb'):
        """
        Open a file or return the buffer if it's already a file-like object.
        
        Args:
            name_or_buffer (str or file-like): File path string or file buffer object
            mode (str): File opening mode. Default: 'rb' (read binary)
            
        Returns:
            file-like object: Opened file or the original buffer
        """
        if isinstance(name_or_buffer, str):
            return open(name_or_buffer, mode)
        else:
            return name_or_buffer

    def _get_torch_version(self):
        """
        Get PyTorch version in major.minor format.
        
        Returns:
            str: PyTorch version in 'major.minor' format (e.g., '1.10', '1.13', '2.0')
        """
        full_version = torch.__version__
        return ".".join(full_version.split(".")[:2])

    def _get_restore_location(self, map_location, version='1.10'):
        """
        Create a restore_location function for tensor storage based on PyTorch version.
        
        The restore_location function determines where tensor storages should be loaded
        (CPU, CUDA device, etc.) based on the map_location parameter. Different PyTorch
        versions handle device mapping differently, so this method provides version-specific
        implementations.
        
        Args:
            map_location (str, dict, torch.device, callable, or None): 
                - str: Device string (e.g., 'cpu', 'cuda:0')
                - dict: Mapping from storage location to target device
                - torch.device: Target device object
                - callable: Custom function(storage, location) -> storage
                - None: Use default behavior
            version (str): PyTorch version in major.minor format. Default: '1.10'
            
        Returns:
            callable: Function that takes (storage, location) and returns mapped storage
        """
        _string_classes = (str, bytes)  # String types for isinstance checks
        default_restore_location = torch.serialization.default_restore_location

        # PyTorch 1.10 and 1.11 use default_restore_location for all cases
        if version in ['1.10', '1.11']:
            if map_location is None:
                # Use default PyTorch restore location
                restore_location = default_restore_location
            elif isinstance(map_location, dict):
                # Dictionary mapping: map storage location to target device
                def restore_location(storage, location):
                    location = map_location.get(location, location)
                    return default_restore_location(storage, location)
            elif isinstance(map_location, _string_classes):
                # String device: map all storages to the specified device
                def restore_location(storage, location):
                    return default_restore_location(storage, map_location)
            elif isinstance(map_location, torch.device):
                # torch.device object: map all storages to the device
                def restore_location(storage, location):
                    return default_restore_location(storage, str(map_location))
            else:
                # Callable: use custom mapping function with fallback
                def restore_location(storage, location):
                    result = map_location(storage, location)
                    if result is None:
                        result = default_restore_location(storage, location)
                    return result
        else:
            # PyTorch 1.13+ uses different storage handling
            if map_location is None:
                # No mapping: return storage as-is
                def restore_location(storage, location):
                    return storage
            elif isinstance(map_location, _string_classes):
                # String device: handle CUDA device mapping with version-specific logic
                def restore_location(storage, location):
                    from packaging import version  # Required for version comparison
                    target = str(map_location)
                    if target.startswith('cuda'):
                        device = torch.device(target)
                        # PyTorch 2.2.0+ requires device index instead of device object
                        if version.parse(torch.__version__) > version.parse("2.2.0"):
                            device = device.index
                        return storage.cuda(device)
                    return storage.cpu()
            elif isinstance(map_location, torch.device):
                # torch.device object: map to CUDA or CPU
                def restore_location(storage, location):
                    if map_location.type == 'cuda':
                        return storage.cuda(map_location)
                    return storage.cpu()
            else:
                # Callable: use custom mapping function
                def restore_location(storage, location):
                    result = map_location(storage, location)
                    return result if result is not None else storage
        return restore_location

    # ---------------- version-specific tensor loading ----------------
    def _load_tensor_1_13(self, dtype, numel, key, location, opened_zipfile):
        """
        Load a tensor from PyTorch checkpoint file (PyTorch 1.13+ format).
        
        PyTorch 1.13+ uses UntypedStorage and requires explicit dtype wrapping.
        This method loads the storage from the zipfile and wraps it in TypedStorage.
        
        Args:
            dtype (torch.dtype): Data type of the tensor
            numel (int): Number of bytes (not elements) in the storage
            key (str): Unique identifier for the tensor storage
            location (str): Device location string (e.g., 'cpu', 'cuda:0')
            opened_zipfile: PyTorch file reader object
        """
        name = f'data/{key}'
        # Load untyped storage from zipfile and convert to untyped storage
        storage = opened_zipfile.get_storage_from_record(name, numel, torch.UntypedStorage).storage().untyped()
        # Wrap in TypedStorage with proper dtype and device mapping
        self.loaded_storages[key] = torch.storage.TypedStorage(
            wrap_storage=self.restore_location(storage, location),
            dtype=dtype
        )

    def _persistent_load_1_13(self, saved_id, opened_zipfile):
        """
        Persistent loader for PyTorch 1.13+ checkpoint format.
        
        This is called by pickle to load tensor storages. It handles the new
        storage format introduced in PyTorch 1.13+ which uses UntypedStorage.
        
        Args:
            saved_id (tuple): Tuple containing (typename, storage_type, key, location, numel)
            opened_zipfile: PyTorch file reader object
            
        Returns:
            torch.storage.TypedStorage: Loaded and cached tensor storage
        """
        assert isinstance(saved_id, tuple)
        # Decode typename if it's bytes
        typename = saved_id[0].decode('ascii') if isinstance(saved_id[0], bytes) else saved_id[0]
        storage_type, key, location, numel = saved_id[1:]

        # Determine dtype: uint8 for UntypedStorage, otherwise use storage_type's dtype
        dtype = torch.uint8 if storage_type is torch.UntypedStorage else storage_type.dtype
        # Only load if not already cached
        if key not in self.loaded_storages:
            location = location.decode('ascii') if isinstance(location, bytes) else location
            # Calculate number of bytes (numel is already bytes in 1.13+ format)
            nbytes = numel * torch._utils._element_size(dtype)
            self._load_tensor_1_13(dtype, nbytes, key, location, opened_zipfile)
        return self.loaded_storages[key]

    def _load_tensor_1_10(self, data_type, size, key, location, opened_zipfile):
        """
        Load a tensor from PyTorch checkpoint file (PyTorch 1.10/1.11 format).
        
        PyTorch 1.10/1.11 uses typed storage directly. This method loads the storage
        from the zipfile with the specified dtype and applies device mapping.
        
        Args:
            data_type (type): PyTorch tensor type class (e.g., torch.FloatTensor)
            size (int): Number of elements in the tensor
            key (str): Unique identifier for the tensor storage
            location (str): Device location string (e.g., 'cpu', 'cuda:0')
            opened_zipfile: PyTorch file reader object
        """
        name = f'data/{key}'
        # Get dtype from tensor type class
        dtype = data_type(0).dtype
        # Load typed storage directly from zipfile
        storage = opened_zipfile.get_storage_from_record(name, size, dtype).storage()
        # Apply device mapping and cache the result
        self.loaded_storages[key] = self.restore_location(storage, location)

    def _persistent_load_1_10(self, saved_id, opened_zipfile):
        """
        Persistent loader for PyTorch 1.10/1.11 checkpoint format.
        
        This is called by pickle to load tensor storages. It handles the older
        storage format used in PyTorch 1.10 and 1.11.
        
        Args:
            saved_id (tuple): Tuple containing (typename, data_type, key, location, size)
            opened_zipfile: PyTorch file reader object
            
        Returns:
            torch.storage: Loaded and cached tensor storage
        """
        assert isinstance(saved_id, tuple)
        # Decode typename if it's bytes
        typename = saved_id[0].decode('ascii') if isinstance(saved_id[0], bytes) else saved_id[0]
        data_type, key, location, size = saved_id[1:]
        # Only load if not already cached
        if key not in self.loaded_storages:
            location = location.decode('ascii') if isinstance(location, bytes) else location
            self._load_tensor_1_10(data_type, size, key, location, opened_zipfile)
        return self.loaded_storages[key]

    # ---------------- main load method ------------------
    def load(self):
        """
        Load the PyTorch model checkpoint from file.
        
        This is the main entry point for loading a model. It:
        1. Opens the checkpoint file and creates a PyTorch file reader
        2. Builds a module mapping dictionary for class name remapping
        3. Creates a custom unpickler with class name remapping support
        4. Loads tensors using version-specific persistent loaders
        5. Validates and returns the checkpoint dictionary
        
        Returns:
            dict: Checkpoint dictionary containing model state and metadata
                Typically includes keys like 'model', 'optimizer', 'epoch', etc.
        """
        with self._open_file(self.path, 'rb') as opened_file:
            # Create PyTorch file reader for the checkpoint zipfile
            opened_zipfile = torch._C.PyTorchFileReader(opened_file)
            
            # Build module dictionary: map class names to their full qualified paths
            modules_dict = {}
            modules_dict.update(self._get_classes_from_module("nxva.yolo.nn.modules"))
            modules_dict.update(self._get_classes_from_module("nxva.yolo.nn.models"))
            
            # Apply replacement mapping: remap original class names to new class names
            for k, v in self.replace.items():
                if v in modules_dict:
                    modules_dict[k] = modules_dict[v]

            class UnpicklerWrapper(pickle.Unpickler):
                """
                Custom unpickler that remaps class names during deserialization.
                
                This wrapper intercepts class lookups and redirects them to the
                correct module paths based on the modules_dict mapping.
                """
                def find_class(inner_self, mod_name, name):
                    # Check if this class name needs remapping
                    if name in modules_dict:
                        target = modules_dict[name]
                        # Extract module path and class name from qualified name
                        mod_name_new = '.'.join(target.split('.')[:-1])
                        name_new = target.split('.')[-1]
                        try:
                            # Try to load from the remapped location
                            return super(UnpicklerWrapper, inner_self).find_class(mod_name_new, name_new)
                        except Exception:
                            # Fall back to original if remapping fails
                            pass
                    # Fall back to original module/name lookup
                    return super(UnpicklerWrapper, inner_self).find_class(mod_name, name)

            # Select appropriate persistent loader based on PyTorch version
            if self.torch_verson in ['1.10', '1.11']:
                persistent_loader = lambda sid: self._persistent_load_1_10(sid, opened_zipfile)
            else:
                persistent_loader = lambda sid: self._persistent_load_1_13(sid, opened_zipfile)

            # Load the pickled data from the checkpoint
            data_file = io.BytesIO(opened_zipfile.get_record('data.pkl'))
            # PyTorch 1.13 requires encoding argument for unpickler
            unpickler = UnpicklerWrapper(data_file, **self.pickle_load_args) if self.torch_verson == '1.13' else UnpicklerWrapper(data_file)
            unpickler.persistent_load = persistent_loader

            # Deserialize the checkpoint
            ckpt = unpickler.load()
            # Validate sparse tensors (PyTorch internal validation)
            torch._utils._validate_loaded_sparse_tensors()
            return ckpt

def load_config(config: Union[str, dict]) -> dict:
    """
    Load configuration from YAML file or dictionary.
    
    This function loads configuration settings from either a YAML file path
    or a dictionary. It also performs special handling for certain configuration
    fields that need type conversion (e.g., kpt_shape, None values).
    
    Args:
        config (str or dict): 
            - str: Path to YAML configuration file (must end with .yaml or .yml)
            - dict: Configuration dictionary (will be copied)
            
    Returns:
        dict: Configuration dictionary with processed values
        
    Raises:
        ValueError: If config type is unsupported or file loading fails
        
    Special Handling:
        - kpt_shape: Converts list to tuple, or extracts numbers from string
        - 'None' strings: Converts string 'None' to Python None value
    """
    # Load from YAML file if string path is provided
    if isinstance(config, str) and config.endswith(('yaml', 'yml')):
        try:
            with open(config, 'r') as f:
                setting = yaml.safe_load(f)
        except Exception as e:
            raise ValueError(f"Error loading config: {e}")
    # Use dictionary directly if already a dict
    elif isinstance(config, dict):
        setting = config.copy()
    else:
        raise ValueError(f"Unsupported config type: {type(config)}")
    
    # Special handling: convert kpt_shape from list to tuple
    # kpt_shape (keypoint shape) is used in pose estimation tasks
    if 'kpt_shape' in setting:
        if isinstance(setting['kpt_shape'], list):
            # Convert list to tuple (required format)
            setting['kpt_shape'] = tuple(setting['kpt_shape'])
        elif isinstance(setting['kpt_shape'], str):
            # Extract numbers from string (e.g., "(17, 3)" -> (17, 3))
            setting['kpt_shape'] = tuple(map(int, re.findall(r'\d+', setting['kpt_shape'])))

    # Special handling: convert string 'None' to Python None
    # YAML files may contain 'None' as a string, which should be converted to None
    for key, value in setting.items():
        if setting[key] == 'None':
            setting[key] = None
        
    return setting