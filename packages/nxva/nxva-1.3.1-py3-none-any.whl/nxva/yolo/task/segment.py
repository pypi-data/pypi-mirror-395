from typing import List, Dict, Any, Tuple, Union

import cv2
import numpy as np

from .detect import DetectionPredictor
from ..utils import np_ops


class SegmentationPredictor(DetectionPredictor):
    """
    A class extending the DetectionPredictor class for prediction based on a segmentation model.
    """
    def __init__(self, config: dict) -> None:
        super().__init__(config)
        self.weight_type = self.config['weights'].split('.')[-1]

    def postprocess(
        self, 
        preds: Union[List[np.ndarray], Tuple[np.ndarray, ...]], 
        orig_imgs: List[np.ndarray]
    ) -> List[Dict[str, Any]]:
        """
        Applies non-max suppression and processes detections for each image in an input batch.
        """
        if self.weight_type == 'engine':
            preds[0], preds[1] = preds[1], preds[0]
        proto = preds[1][None, ...] if preds[1].ndim == 3 else preds[1]

        preds = np_ops.non_max_suppression(
            preds[0],
            conf_threshold=self.conf,
            iou_threshold=self.iou,
            nc=self.nc,
            classes=self.classes,
            agnostic=self.agnostic,
            version=self.version
        )
        results = []
        for i, (pred, orig_img) in enumerate(zip(preds, orig_imgs)):
            if len(pred) == 0:
                results.append({'boxes': np.empty((0, 6)), 'mask': None})
                continue

            masks = np_ops.process_mask(proto[i], pred[:, 6:], pred[:, :4], self.input_shape, upsample=True)  # HWC
            pred[:, :4] = np_ops.scale_boxes(self.input_shape, pred[:, :4], orig_img.shape)
            results.append({'boxes': pred[:, :6], 'mask': masks})
        return results