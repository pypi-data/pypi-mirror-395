from typing import List, Dict, Any

import numpy as np

from .base_predictor import BasePredictor
from ..utils import np_ops


class PosePredictor(BasePredictor):
    def __init__(self, config: dict) -> None:
        super().__init__(config)

    def postprocess(
        self, 
        preds: List[np.ndarray], 
        orig_imgs: List[np.ndarray]
    ) -> List[Dict[str, Any]]:
        preds = np_ops.non_max_suppression(
            preds[0],
            conf_threshold=self.conf,
            iou_threshold=self.iou,
            nc=self.nc,
            classes=self.classes,
            agnostic=self.agnostic,
            version=self.version,
            task=self.task
        )
        results = []
        for pred, orig_img in zip(preds, orig_imgs):
            if len(pred) == 0:
                results.append({'boxes': np.empty((0, 6)), 'keypoints': np.empty((0, *self.kpt_shape))})
                continue
            pred[:, :4] = np_ops.scale_boxes(self.input_shape, pred[:, :4], orig_img.shape).round()
            # len(pred) > 0 is guaranteed here due to continue above
            pred_kpts = pred[:, 6:].reshape((len(pred), *self.kpt_shape))
            pred_kpts = np_ops.scale_coords(self.input_shape, pred_kpts, orig_img.shape)
            results.append({'boxes': pred[:, :6], 'keypoints': pred_kpts})
        return results