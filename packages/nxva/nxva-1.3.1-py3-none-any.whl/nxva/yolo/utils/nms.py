import numpy as np

def box_iou_batch(
    boxes_a: np.ndarray, 
    boxes_b: np.ndarray
) -> np.ndarray:

    def box_area(box):
        return (box[2] - box[0]) * (box[3] - box[1])

    area_a = box_area(boxes_a.T)
    area_b = box_area(boxes_b.T)

    top_left = np.maximum(boxes_a[:, None, :2], boxes_b[:, :2])
    bottom_right = np.minimum(boxes_a[:, None, 2:], boxes_b[:, 2:])

    area_inter = np.prod(
        np.clip(bottom_right - top_left, a_min=0, a_max=None), axis=2)
        
    # Add small epsilon to prevent division by zero
    return area_inter / (area_a[:, None] + area_b - area_inter +  1e-7)


def nms_np(
   predictions: np.ndarray, iou_threshold: float = 0.5
) -> np.ndarray:
    rows, columns = predictions.shape

    sort_index = np.flip(predictions[:, 4].argsort())
    predictions = predictions[sort_index]

    boxes = predictions[:, :4]
    categories = predictions[:, 5]
    ious = box_iou_batch(boxes, boxes)
    ious = ious - np.eye(rows)

    keep = np.ones(rows, dtype=bool)

    for index, (iou, category) in enumerate(zip(ious, categories)):
        if not keep[index]:
            continue

        condition = (iou > iou_threshold) & (categories == category)
        keep = keep & ~condition

    return keep[sort_index.argsort()]

def nms(
    boxes: np.ndarray, 
    scores: np.ndarray, 
    iou_threshold: float = 0.5
) -> np.ndarray:
    #nms_np_agnostic
    rows, columns = boxes.shape
    sort_index = np.argsort(-scores)
    boxes = boxes[sort_index]
    ious = box_iou_batch(boxes, boxes) 
    ious = ious - np.eye(rows)
    ious = ious > iou_threshold
    conditions = ious # mxm
    keep = np.ones(rows, dtype=bool)
    for index, condition in enumerate(~conditions):
        if not keep[index]:
            continue
        keep = keep & condition
    return keep[sort_index.argsort()]