from typing import List, Tuple, Union, Any

import numpy as np


def _sigmoid(x: np.ndarray) -> np.ndarray:
    """Apply sigmoid activation function with numerical stability."""
    return 1.0 / (1.0 + np.exp(-np.clip(x, -500, 500)))

def _softmax(x: np.ndarray, axis: int) -> np.ndarray:
    """Apply softmax activation function along specified axis."""
    x = x - np.max(x, axis=axis, keepdims=True)
    ex = np.exp(x)
    return ex / np.sum(ex, axis=axis, keepdims=True)

def _transform_feat(feat: List[np.ndarray], na: int, no: int) -> np.ndarray:
    """Transform feature maps to concatenated format."""
    x_feats = []
    B = feat[0].shape[0]
    for i, xi in enumerate(feat):
        *_, H, W = xi.shape
        # (B, na, no, H, W) => (B, na, H, W, no) => (B, -1, no)
        xi = xi.reshape(B, na, no, H, W).transpose(0, 1, 3, 4, 2).reshape(B, -1, no)  # if error occur, maybe is nc problem, check the nc in the config
        

        x_feats.append(xi)  # (B,na*H*W,no)
    return np.concatenate(x_feats, axis=1)  # (B, sum(na*H*W), no)


class DecodeHead:
    """
    Factory Class: Returns corresponding decoder instance based on version and task.
    Uses __new__ method to directly return concrete decoder instance, avoiding an extra layer of proxy object.
    """

    # Use string names to avoid reference issues caused by class definition order
    DECODE_CLASS_MAP = {
        ('yolov5', 'detect'): 'DecodeDetectV5',
        ('yolov5', 'face'): 'DecodeDetectFaceV5',
        ('yolov5', 'pose'): 'DecodePoseV5',
        ('yolov5', 'classify'): 'DecodeClassify',
        ('yolov8', 'detect'): 'DecodeDetectV11',
        ('yolov8', 'pose'): 'DecodePoseV11',
        ('yolo11', 'detect'): 'DecodeDetectV11',
        ('yolo11', 'pose'): 'DecodePoseV11',
        ('yolo11', 'classify'): 'DecodeClassify',
    }

    def __new__(cls, version: str, task: str, nc: int = 80, **kwargs) -> Any:
        """
        Create and return corresponding decoder instance based on version and task.

        Args:
            version (str): Supported 'yolov5' | 'yolov8' | 'yolo11'
            task (str): Supported 'detect' | 'pose'
            nc (int): Number of classes
            **kwargs: Additional parameters passed to concrete decoder
                     Note: kpt_shape is only used for 'pose' task and will be removed for other tasks

        Returns:
            object: Corresponding decoder instance
        """

        # Create key
        key = (version, task)
        class_name = cls.DECODE_CLASS_MAP.get(key)

        if class_name is None:
            raise ValueError(f"Unsupported version-task combination: {version}-{task}")

        # Filter kwargs: only pose task should receive kpt_shape parameter
        # Remove kpt_shape from kwargs if task is not 'pose' to avoid passing wrong parameters
        filtered_kwargs = kwargs.copy()
        if task != 'pose' and 'kpt_shape' in filtered_kwargs:
            filtered_kwargs.pop('kpt_shape')

        # Get actual class from global namespace to avoid definition order issues
        decoder_class = globals().get(class_name)
        if decoder_class is None:
            raise RuntimeError(f"Decoder class '{class_name}' not found")

        # Return concrete decoder instance
        return decoder_class(nc=nc, **filtered_kwargs)


class DecodeDetectV11:
    def __init__(self, nc: int = 80, reg_max: int = 16):
        self.reg_max = reg_max
        self.no = nc + reg_max*4

        self.strides = np.array([8., 16., 32.])

    def __call__(self, x: List[np.ndarray]) -> np.ndarray:
        """Process feature maps and return decoded bounding boxes and class predictions."""
        B = x[0].shape[0]

        #1. cat aligned feature maps
        x_cat = np.concatenate([xi.reshape(B, self.no, -1) for xi in x], axis=2)

        #2. make anchors and strides
        self.anchors_grid, self.strides_grid = self._make_anchors(x, self.strides, grid_cell_offset=0.5)

        #3. split x_cat into box and cls
        box, cls = np.split(x_cat, [self.reg_max * 4], axis=1)

        #4. dfl
        box = self.dfl(box)
        cls = _sigmoid(cls)
        # 5. decode bbox
        dbox = self.decode_bboxes(box, self.anchors_grid) * self.strides_grid
        return np.concatenate([dbox, cls], axis=1)

    def _make_anchors(
        self, 
        feats: List[np.ndarray], 
        strides: Union[List[float], np.ndarray], 
        grid_cell_offset: float = 0.5
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Use NumPy to generate anchors."""
        anchor_points, stride_tensor = [], []

        assert feats is not None
        for i, stride in enumerate(strides):
            if isinstance(feats, list):
                h, w = feats[i].shape[2:]  # (B, C, H, W)
            else:
                h, w = int(feats[i][0]), int(feats[i][1])

            # create grid coordinates
            sx = np.arange(w, dtype=np.float32) + grid_cell_offset
            sy = np.arange(h, dtype=np.float32) + grid_cell_offset
            sy, sx = np.meshgrid(sy, sx, indexing="ij")  # shape: (h, w)

            # stack coordinate points
            points = np.stack((sx, sy), axis=-1).reshape(-1, 2)  # shape: (h * w, 2)
            anchor_points.append(points)

            # each anchor assigned a stride value
            stride_arr = np.full((h * w, 1), stride, dtype=np.float32)
            stride_tensor.append(stride_arr)
        return np.concatenate(anchor_points, axis=0).transpose(1, 0).reshape(1, 2, -1), np.concatenate(stride_tensor, axis=0).reshape(1, 1, -1)

    def dfl(self, feat: np.ndarray) -> np.ndarray:
        """Distribution Focal Loss decoding."""
        b, _, fn = feat.shape  # batch size, feature channel and feature number
        bins = np.arange(self.reg_max).reshape(1, 1, self.reg_max, 1)
        bins = np.broadcast_to(bins, (b, 4, self.reg_max, fn))
        feat = feat.reshape(b, 4, self.reg_max, fn)
        feat = _softmax(feat, axis=2)
        ltrb = (feat * bins).sum(axis=2) 
        return ltrb
    
    def decode_bboxes(self, box: np.ndarray, anchors: np.ndarray) -> np.ndarray:
        """Decode bounding boxes from predictions."""
        return self._dist2bbox(box, anchors, dim=1)

    def _dist2bbox(self, distance: np.ndarray, anchor_points: np.ndarray, dim: int = 1) -> np.ndarray:
        """Transform distance(ltrb) to box(xywh or xyxy)."""
        lt, rb = np.split(distance, 2, axis=dim)
        x1y1 = anchor_points - lt
        x2y2 = anchor_points + rb
        c_xy = (x1y1 + x2y2) / 2
        wh = x2y2 - x1y1
        return np.concatenate((c_xy, wh), axis=dim)  # xywh bbox


class DecodePoseV11(DecodeDetectV11):
    def __init__(self, nc: int = 1, kpt_shape: Tuple[int, int] = (17, 3)):
        super().__init__(nc=nc)
        self.nc = nc
        self.kpt_shape = kpt_shape
        self.nk = kpt_shape[0] * kpt_shape[1]
    
    def __call__(self, x: Tuple[List[np.ndarray], List[np.ndarray]]) -> np.ndarray:
        """Process bounding box and keypoint feature maps and return decoded results."""
        bbox_heads, kpt_heads = x
        B = bbox_heads[0].shape[0]
        x_cat = np.concatenate([xi.reshape(B, self.nk, -1) for xi in kpt_heads], axis=-1)
        bbox = DecodeDetectV11.__call__(self, bbox_heads)
        pred_kpt = self.decode_kpts(x_cat)
        return np.concatenate((bbox, pred_kpt), axis=1)
    
    def decode_kpts(self, kpts: np.ndarray) -> np.ndarray:
        """Decode keypoints from predictions."""
        ndim = self.kpt_shape[1]
        if ndim == 3:
            kpts[:, 2::ndim] = _sigmoid(kpts[:, 2::ndim])
        kpts[:, 0::ndim] = (kpts[:, 0::ndim] * 2.0 + (self.anchors_grid[:, 0:1, :] - 0.5)) * self.strides_grid
        kpts[:, 1::ndim] = (kpts[:, 1::ndim] * 2.0 + (self.anchors_grid[:, 1:2, :] - 0.5)) * self.strides_grid
        return kpts

class DecodeSegmentV11(DecodeDetectV11):
    def __init__(self, nc: int = 80) -> None:
        super().__init__(nc=nc)
    
    def __call__(self, x: Tuple[List[np.ndarray], List[np.ndarray], np.ndarray]) -> Tuple[np.ndarray, np.ndarray]:
        """Process segmentation, detection features and mask coefficients, return decoded results."""
        segment_feat, detect_feat, mask_coeffs = x
        x = DecodeDetectV11.__call__(self, detect_feat)
        return (np.concatenate((x[0], mask_coeffs), axis=1), segment_feat)


class DecodeDetectV5:
    anchors = np.array([
        [[10, 13],  [16, 30],  [33, 23]],
        [[30, 61],  [62, 45],  [59, 119]],
        [[116, 90], [156, 198], [373, 326]]
    ], dtype=np.float32)
    strides = np.array([8., 16., 32.])
    
    def __init__(self, nc: int = 80):
        self.na = len(self.anchors[0])
        self.no = nc + 5
        self.anchor_grid, self.strides_grid = None, None

    def __call__(self, x: List[np.ndarray]) -> np.ndarray:
        """Process feature maps and return decoded bounding boxes."""
        #1. cat aligned feature maps
        x_cat = _transform_feat(x, self.na, self.no)
        
        #2. make anchors and strides
        if self.anchor_grid is None:
            self._make_anchorsV5(x, self.na, self.anchors, self.strides)

        # 4. decode bbox
        return self.decode_bboxes(x_cat)

    def decode_bboxes(self, boxes: np.ndarray) -> np.ndarray:
        """Decode bounding boxes from predictions."""
        return self._dist2bbox(boxes)
    
    def _dist2bbox(self, boxes: np.ndarray) -> np.ndarray:
        """Transform xy(ltrb) to box(xywh or xyxy)."""
        xy, wh, conf = np.split(_sigmoid(boxes), [2, 4], axis=2)
        xy = (xy * 2 + self.grid) * self.strides_grid
        wh = (wh * 2) ** 2 * self.anchor_grid
        return np.concatenate((xy, wh, conf), axis=-1)

    def _make_anchorsV5(
        self, 
        feats: List[np.ndarray], 
        na: int, 
        anchors: np.ndarray, 
        strides: Union[List[float], np.ndarray], 
        grid_cell_offset: float = -0.5
    ) -> None:
        """Use NumPy to generate anchors."""
        grids, anchor_grids, strides_grids = [], [], []
        for i, stride in enumerate(strides):
            *_, h, w = feats[i].shape
            # create grid coordinates
            sx = np.arange(w, dtype=np.float32) + grid_cell_offset
            sy = np.arange(h, dtype=np.float32) + grid_cell_offset
            sy, sx = np.meshgrid(sy, sx, indexing="ij")  # shape: (h, w)

            # stack coordinate points
            points = np.stack((sx, sy), axis=-1).reshape(1, 1, -1, 2)  # shape: (h * w, 2)
            points = np.repeat(points, na, axis=1).reshape(1, -1, 2)
            grids.append(points)

            # make anchor grids
            anchor = anchors[i]
            anchor = anchor.reshape(1, na, 1, 1, 2) + np.zeros((1,1,h,w,1), dtype=anchors.dtype)
            anchor = anchor.reshape(1, -1, 2)
            anchor_grids.append(anchor)

            # make stride grids
            strides = np.full((1, na * h * w, 1), stride, dtype=np.float32)
            strides_grids.append(strides)
        self.grid = np.concatenate(grids, axis=1)
        self.anchor_grid = np.concatenate(anchor_grids, axis=1)
        self.strides_grid = np.concatenate(strides_grids, axis=1)
        

class DecodePoseV5(DecodeDetectV5):
    def __init__(self, nc: int = 1, kpt_shape: Tuple[int, int] = (17, 3)) -> None:
        self.strides = np.array([8., 16., 32., 64.])
        self.anchors = np.array([
               [[ 19.,  27.],
                [ 44.,  40.],
                [ 38.,  94.]],

               [[ 96.,  68.],
                [ 86., 152.],
                [180., 137.]],

               [[140., 301.],
                [303., 264.],
                [238., 542.]],

               [[436., 615.],
                [739., 380.],
                [925., 792.]]])
        self.nc = 1
        self.no = nc + 5
        self.na = len(self.anchors[0])
        self.kpt_shape = kpt_shape
        self.nk = kpt_shape[0] * kpt_shape[1]    
        self.anchor_grid, self.strides_grid = None, None    

    def __call__(self, x: List[np.ndarray]) -> np.ndarray:
        """Process feature maps and return decoded bounding boxes and keypoints."""
        #feature transform
        feats = _transform_feat(x, self.na, self.nk+self.no)

        #split feats to boxes, kpts
        boxes, kpts = np.split(feats, [6], axis=-1)

        # make grid and anchor
        if self.anchor_grid is None:
            self._make_anchorsV5(x, self.na, self.anchors, self.strides)
        
        #process boxes
        pred_boxes = self.decode_bboxes(boxes)

        #process kpts
        pred_kpt = self.decode_kpts(kpts)
        
        #concat outputs
        return np.concatenate([pred_boxes, pred_kpt], axis=-1)
    
    def decode_kpts(self, kpts: np.ndarray) -> np.ndarray:
        """Decode keypoints from predictions."""
        return self._dist2kpts(kpts)

    def _dist2kpts(self, kpts: np.ndarray) -> np.ndarray:
        """Transform keypoint distances to coordinates."""
        x = (kpts[..., 0::3] * 2.0 + self.grid[..., 0:1]) * self.strides_grid
        y = (kpts[..., 1::3] * 2.0 + self.grid[..., 1:2]) * self.strides_grid
        conf = _sigmoid(kpts[..., 2::3])
        return np.stack((x, y, conf), axis=-1).reshape(kpts.shape) 


class DecodeSegmentV5(DecodeDetectV5):
    def __init__(self, nc: int = 80) -> None:
        super().__init__(nc=nc)

    def __call__(self, x: Tuple[List[np.ndarray], List[np.ndarray]]) -> Tuple[np.ndarray, np.ndarray]:
        """Process segmentation and detection features and return decoded results."""
        segment_feat, detect_feat = x
        x = DecodeDetectV5.__call__(self, detect_feat)
        return (x[0], segment_feat)
        

class DecodeClassify:
    def __init__(self, nc: int = 80) -> None:
        pass
    
    def __call__(self, x: np.ndarray) -> np.ndarray:
        """Process classification predictions and return probabilities."""
        return x