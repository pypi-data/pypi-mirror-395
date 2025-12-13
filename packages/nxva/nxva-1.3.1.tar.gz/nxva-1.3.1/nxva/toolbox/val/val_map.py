import sys
sys.path.insert(0, '/mnt/hailo_pi5/test_space/nxva')

import os
from nxva.yolo.yolo import YOLO
from nxva.toolbox.val_speed import Profile, SpeedCalculator
from nxva.yolo.utils.loader import LoadImages
from ultralytics.utils.metrics import DetMetrics
import numpy as np

def _np_box_iou(box1, box2):
    """
    NumPy version of IoU between two sets of boxes.
    box1: (N, 4) [x1, y1, x2, y2]
    box2: (M, 4) [x1, y1, x2, y2]
    return: (N, M) IoU matrix
    """
    area1 = (box1[:, 2] - box1[:, 0]) * (box1[:, 3] - box1[:, 1])  # (N,)
    area2 = (box2[:, 2] - box2[:, 0]) * (box2[:, 3] - box2[:, 1])  # (M,)

    inter_x1 = np.maximum(box1[:, None, 0], box2[:, 0])
    inter_y1 = np.maximum(box1[:, None, 1], box2[:, 1])
    inter_x2 = np.minimum(box1[:, None, 2], box2[:, 2])
    inter_y2 = np.minimum(box1[:, None, 3], box2[:, 3])

    inter_w = np.clip(inter_x2 - inter_x1, a_min=0, a_max=None)
    inter_h = np.clip(inter_y2 - inter_y1, a_min=0, a_max=None)
    inter_area = inter_w * inter_h

    union = area1[:, None] + area2 - inter_area
    return inter_area / (union + 1e-6)


def compute_tp_for_map(labels_boxes, labels_class_ids, pred_scaled_boxes, pred_confs, pred_class_ids):
    """
    Compute true positive flags for each prediction across different IoU thresholds,
    which is used to calculate mean Average Precision (mAP).

    Args:
        labels_boxes (np.ndarray): Ground truth bounding boxes, shape (n_labels, 4).
        labels_class_ids (np.ndarray): Ground truth class IDs, shape (n_labels,).
        pred_scaled_boxes (np.ndarray): Predicted bounding boxes (already scaled back to original image), shape (n_preds, 4).
        pred_confs (np.ndarray): Confidence scores for predicted boxes, shape (n_preds,).
        pred_class_ids (np.ndarray): Predicted class IDs, shape (n_preds,).

    Returns:
        Tuple:
            tp (np.ndarray): Boolean array of shape (n_preds, 10), where each element indicates
                whether the prediction is a true positive at IoU thresholds from 0.5 to 0.95.
            confs (np.ndarray): Confidence scores of predictions, shape (n_preds,).
            pred_classes (np.ndarray): Predicted class indices, shape (n_preds,).
            target_classes (np.ndarray): Ground truth class indices, shape (n_labels,).
    """

    preds = np.concatenate([pred_scaled_boxes, pred_confs[:, None], pred_class_ids[:, None]], axis=1)

    ious = _np_box_iou(pred_scaled_boxes, labels_boxes)
    pred_classes = preds[:, 5].astype(int)
    target_classes = labels_class_ids.astype(int)

    iou_thresholds = np.linspace(0.5, 0.95, 10)
    n_preds = len(preds)
    tp = np.zeros((n_preds, len(iou_thresholds)), dtype=bool)

    for i, thresh in enumerate(iou_thresholds):
        iou_max = ious.max(axis=1)
        iou_idx = ious.argmax(axis=1)
        matched_gt_classes = target_classes[iou_idx]
        correct = (iou_max > thresh) & (pred_classes == matched_gt_classes)
        tp[:, i] = correct

    return tp, preds[:, 4], pred_classes, target_classes


def val_map(model, images):
    total_time_all  = 0
    tp_list = []
    conf_list = []
    pred_cls_list = []
    target_cls_list = []

    metrics = DetMetrics(save_dir="")
    speed_calculator = SpeedCalculator()
    profiles = [Profile() for _ in range(3)]
    for im in images:
        with profiles[0]:
            pre_imgs, imgs = model._predictor.preprocess(imgs)
        with profiles[1]:
            results = model._predictor.infer(pre_imgs)
        with profiles[2]:
            dets = model._predictor.postprocess(results, pre_imgs, imgs)
        scaled_boxes, confs, class_ids = dets
        speed_calculator.update(len(im), profiles)

        label_path = img_path.replace('images', 'labels').replace('.jpg', '.txt')
        if not os.path.exists(label_path):
            labels = np.zeros((0, 5))
        else:
            labels = []
            with open(label_path, 'r') as f:
                for line in f.readlines():
                    try:
                        cls, xc, yc, w, h = map(float, line.strip().split())
                    except ValueError:
                        continue  # 忽略這一行
                    x1 = (xc - w / 2) * img.shape[1]
                    y1 = (yc - h / 2) * img.shape[0]
                    x2 = (xc + w / 2) * img.shape[1]
                    y2 = (yc + h / 2) * img.shape[0]
                    labels.append([x1, y1, x2, y2, cls])
            labels = np.array(labels)
        if labels.shape[0] == 0:
            continue
        else:
            labels_boxes = labels[:, :4]
            labels_class_ids = labels[:, 4].astype(int)
            tp, pred_confs, pred_classes, target_classes = compute_tp_for_map(labels_boxes, labels_class_ids, scaled_boxes, confs, class_ids)
            tp_list.append(tp)
            conf_list.append(pred_confs)
            pred_cls_list.append(pred_classes)
            target_cls_list.append(target_classes)    
    return speed_calculator.compute()

