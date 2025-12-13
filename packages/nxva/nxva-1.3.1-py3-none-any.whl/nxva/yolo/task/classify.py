from typing import List, Tuple, Optional
from PIL import Image

import numpy as np
import cv2

from .base_predictor import BasePredictor
from ..utils import np_ops


class ClassificationPredictor(BasePredictor):
    def __init__(self, config: dict) -> None:
        super().__init__(config)
        
        self.transforms = np_ops.classify_transforms(size=self.input_shape)

    def preprocess(self, imgs: List[np.ndarray]) -> Tuple[np.ndarray, List[np.ndarray]]:
        """Preprocess images for classification."""
        img_stack = np.stack(
            [self.transforms(Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))) for im in imgs]
        )
        return img_stack, imgs

    def postprocess(
        self, 
        preds: np.ndarray, 
        orig_imgs: Optional[List[np.ndarray]] = None
    ) -> Tuple[np.ndarray, Tuple[np.ndarray, np.ndarray]]:
        preds = preds[0] if isinstance(preds, (list, tuple)) else preds
        top5_idx = np.argsort(preds, axis=1)[:, -5:][:, ::-1]
        top5 = np.take_along_axis(preds, top5_idx, axis=1)
        return preds, (top5, top5_idx)