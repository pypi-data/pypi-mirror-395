from typing import List
import numpy as np

from .base_predictor import BasePredictor
from ..utils import np_ops


class DetectionPredictor(BasePredictor):
    def __init__(self, config: dict) -> None:
        super().__init__(config)
                
    def postprocess(
        self, 
        preds: List[np.ndarray], 
        orig_imgs: List[np.ndarray]
    ) -> List[np.ndarray]:
        """Post-processes predictions for an image and returns them.""" 
        pred = np_ops.non_max_suppression(
            preds[0],
            conf_threshold=self.conf,
            iou_threshold=self.iou,
            nc=self.nc,
            classes=self.classes,
            agnostic=self.agnostic,
            version=self.version
        )
        results = []
        for i, det in enumerate(pred):
            if len(det):
                det[:, :4] = np_ops.scale_boxes(self.input_shape, det[:, :4], orig_imgs[i].shape).round()
                det = det[np.argsort(det[:, 0])]
            else:
                det = np.zeros((0, 6), dtype=np.float32)
            results.append(det)
        return results