import cv2, math, time

import numpy as np
from .nms import nms


def empty_like(x):
    """
    Create an empty NumPy array with the same shape as the input and dtype float32.
    
    Function:
        Create empty container with same shape as input for improved memory allocation efficiency.
    
    Input:
        x : array-like
            Reference array defining the target shape.
    
    Output:
        Empty array with the same shape as `x` and dtype float32.
    
    Examples
        --------
        >>> arr = np.random.rand(2, 3, 4)
        >>> out = empty_like(arr)
        >>> out.shape
        (2, 3, 4)
    """
    return np.empty_like(x, dtype=np.float32)


def xywh2xyxy(x):
    """
    Convert bounding box coordinates from (x, y, width, height) format to (x1, y1, x2, y2) format.
    
    Function:
        Convert center point coordinates and width/height format to top-left and bottom-right format
        where (x1, y1) is the top-left corner and (x2, y2) is the bottom-right corner.
    
    Input:
        x : np.ndarray, shape (..., 4)
            Bounding boxes in (center_x, center_y, width, height) format.
    
    Output:
        np.ndarray, shape (..., 4)
            Bounding boxes in (x1, y1, x2, y2) format, where
            (x1, y1) is the top-left corner and (x2, y2) the bottom-right.
    
    Example:
        >>> boxes = np.array([[100, 100, 50, 30]], dtype=np.float32)
        >>> xyxy_boxes = xywh2xyxy(boxes)
        >>> xyxy_boxes
        array([[ 75.,  85., 125., 115.]], dtype=float32)
    """
    assert x.shape[-1] == 4, f"expected (...,4), got {x.shape}"
    y = empty_like(x)  # faster than clone/copy
    xy = x[..., :2]  # centers
    wh = x[..., 2:] / 2  # half width-height
    y[..., :2] = xy - wh  # top left xy
    y[..., 2:] = xy + wh  # bottom right xy
    return y

def xyxy2xywh(x):
    """
    Convert bounding box coordinates from (x1, y1, x2, y2) format to (x, y, width, height) format where (x1, y1) is the
    top-left corner and (x2, y2) is the bottom-right corner.

    Args:
        x : np.ndarray, shape (..., 4)
            Bounding boxes in (x1, y1, x2, y2) format, where
            (x1, y1) is the top-left corner and (x2, y2) the bottom-right.

    Returns:
        np.ndarray, shape (..., 4)
            Bounding boxes in (center_x, center_y, width, height) format.
    """
    assert x.shape[-1] == 4, f"input shape last dimension expected 4 but input shape is {x.shape}"
    y = empty_like(x)  # faster than clone/copy
    y[..., 0] = (x[..., 0] + x[..., 2]) / 2.0  # x center
    y[..., 1] = (x[..., 1] + x[..., 3]) / 2.0  # y center
    y[..., 2] = x[..., 2] - x[..., 0]  # width
    y[..., 3] = x[..., 3] - x[..., 1]  # height
    return y
    

def xywhr2xyxyxyxy(x):
    """
    Convert batched Oriented Bounding Boxes (OBB) from [xywh, rotation] to [xy1, xy2, xy3, xy4] format.

    Args:
        x : np.ndarray, shape (..., 5)
            Oriented bounding boxes in format (center_x, center_y, width, height, angle).
            The angle is in radians, measured counter-clockwise.

    Returns:
        np.ndarray, shape (..., 4, 2)
            Corner points of the oriented boxes in order [pt1, pt2, pt3, pt4].
    """
    ctr = x[..., :2]
    w = x[..., 2:3]
    h = x[..., 3:4]
    angle = x[..., 4:5]

    cos_value = np.cos(angle)
    sin_value = np.sin(angle)

    vec1 = [w / 2 * cos_value, w / 2 * sin_value]
    vec2 = [-h / 2 * sin_value, h / 2 * cos_value]

    vec1 = np.concatenate(vec1, -1)
    vec2 = np.concatenate(vec2, -1)

    pt1 = ctr + vec1 + vec2
    pt2 = ctr + vec1 - vec2
    pt3 = ctr - vec1 - vec2
    pt4 = ctr - vec1 + vec2

    return np.stack([pt1, pt2, pt3, pt4], -2)


def clip_boxes(boxes, shape):
    """
    Clip bounding boxes to image boundaries to prevent exceeding image bounds.
    
    Function:
        Restrict bounding box coordinates within image bounds [0, width] and [0, height]
        to ensure boxes don't exceed image boundaries.
    
    Input:
        boxes : np.ndarray, shape (..., 4)
            Bounding boxes in (x1, y1, x2, y2) format.
        shape : tuple of int
            Image shape given as (height, width).
    
    Output:
        np.ndarray
            Clipped bounding boxes with coordinates restricted to image bounds.
    
    Example:
        >>> boxes = np.array([[-10, -5, 650, 480]], dtype=np.float32)
        >>> shape = (480, 640)
        >>> clip_boxes(boxes, shape)
        array([[  0.,   0., 640., 480.]], dtype=float32)
    """
    boxes[..., [0, 2]] = boxes[..., [0, 2]].clip(0, shape[1])  # x1, x2
    boxes[..., [1, 3]] = boxes[..., [1, 3]].clip(0, shape[0])  # y1, y2

    return boxes


def scale_boxes(img1_shape, boxes, img0_shape, ratio_pad=None, padding=True, xywh=False):
    """
    Scale bounding boxes from one image size to another image size.
    
    Function:
        Scale bounding box coordinates from processed image size back to original image size.
        Supports YOLO-style padding and different bounding box formats.
    
    Input:
        img1_shape (tuple): Image shape corresponding to bounding boxes (height, width)
        boxes (np.ndarray): Bounding box coordinates in (x1, y1, x2, y2) format
        img0_shape (tuple): Target image shape (height, width)
        ratio_pad (tuple, optional): Scale ratio and padding (ratio, pad), auto-calculated if not provided
        padding (bool): Whether to consider YOLO-style padding, default True
        xywh (bool): Whether bounding box format is xywh, default False
    
    Output:
        numpy.ndarray: Scaled bounding boxes in (x1, y1, x2, y2) format
    
    Example:
        >>> img1_shape = (640, 640)  # processed image size
        >>> boxes = np.array([[100, 100, 200, 200]], dtype=np.float32)
        >>> img0_shape = (480, 640)  # original image size
        >>> scaled_boxes = scale_boxes(img1_shape, boxes, img0_shape)
    """
    if ratio_pad is None:  # calculate from img0_shape
        gain = min(img1_shape[0] / img0_shape[0], img1_shape[1] / img0_shape[1])  # gain  = old / new
        pad = (
            round((img1_shape[1] - img0_shape[1] * gain) / 2 - 0.1),
            round((img1_shape[0] - img0_shape[0] * gain) / 2 - 0.1),
        )  # wh padding
    else:
        gain = ratio_pad[0][0] if isinstance(ratio_pad[0], (list, tuple, np.ndarray)) else ratio_pad[0]
        pad = ratio_pad[1]

    if padding:
        boxes[..., 0] -= pad[0]  # x padding
        boxes[..., 1] -= pad[1]  # y padding
        if not xywh:
            boxes[..., 2] -= pad[0]  # x padding
            boxes[..., 3] -= pad[1]  # y padding
    boxes[..., :4] /= gain
    return clip_boxes(boxes, img0_shape)


def scale_coords(img1_shape, coords, img0_shape, ratio_pad=None, normalize: bool = False, padding: bool = True):
    """
    Scale segmentation coordinates from one image size to another image size.
    
    Function:
        Scale segmentation coordinates from processed image size back to original image size.
        Supports coordinate normalization and YOLO-style padding handling.
    
    Input:
        img1_shape (tuple): Source image shape (height, width)
        coords (np.ndarray): Coordinates to scale with shape (N, 2)
        img0_shape (tuple): Target image shape (height, width)
        ratio_pad (tuple, optional): Scale ratio and padding values ((ratio_h, ratio_w), (pad_h, pad_w))
        normalize (bool): Whether to normalize coordinates to range [0, 1], default False
        padding (bool): Whether coordinates are based on YOLO-style padded images, default True
    
    Output:
        np.ndarray: Scaled coordinates
    
    Example:
        >>> img1_shape = (640, 640)  # processed image size
        >>> coords = np.ndarray([[100, 100], [200, 200]])
        >>> img0_shape = (480, 640)  # original image size
        >>> scaled_coords = scale_coords(img1_shape, coords, img0_shape)
    """
    if coords.shape[0] == 0:
        return np.zeros((17, 3), dtype=np.float32)
    if ratio_pad is None:  # calculate from img0_shape
        gain = min(img1_shape[0] / img0_shape[0], img1_shape[1] / img0_shape[1])  # gain  = old / new
        pad = (img1_shape[1] - img0_shape[1] * gain) / 2, (img1_shape[0] - img0_shape[0] * gain) / 2  # wh padding
    else:
        gain = ratio_pad[0]
        pad = ratio_pad[1]

    if padding:
        coords[..., 0] -= pad[0]  # x padding
        coords[..., 1] -= pad[1]  # y padding
    coords[..., 0] /= gain
    coords[..., 1] /= gain
    coords = clip_coords(coords, img0_shape)
    if normalize:
        coords[..., 0] /= img0_shape[1]  # width
        coords[..., 1] /= img0_shape[0]  # height
    return coords


def clip_coords(coords, shape):
    """
    Clip line coordinates to the image boundaries.
    
    Function:
        Restrict coordinates within image bounds [0, width] and [0, height]
        to prevent coordinates from exceeding image boundaries.
    
    Input:
        coords (numpy.ndarray): Line coordinates list with shape (..., 2)
        shape (tuple): Image dimensions (height, width)
    
    Output:
        numpy.ndarray: Clipped coordinates with same type as input
    
    Example:
        >>> coords = np.array([[-10, -5], [650, 480]])  # coordinates exceeding boundaries
        >>> shape = (480, 640)  # image dimensions
        >>> clipped = clip_coords(coords, shape)
        >>> print(clipped)  # [[0, 0], [640, 480]]
    """
    coords[..., 0] = coords[..., 0].clip(0, shape[1])  # x
    coords[..., 1] = coords[..., 1].clip(0, shape[0])  # y

    return coords


def scale_coordsV5(img1_shape, coords, img0_shape, ratio_pad=None):
    """
    YOLOv5 version coordinate scaling function.
    
    Function:
        Specialized coordinate scaling implementation for YOLOv5.
        Scale coordinates from processed image size back to original image size.
    
    Input:
        img1_shape (tuple): Source image shape (height, width)
        coords (np.ndarray): Coordinates to scale with shape (N, 2)
        img0_shape (tuple): Target image shape (height, width)
        ratio_pad (tuple, optional): Scale ratio and padding values, auto-calculated if not provided
    
    Output:
        np.ndarray: Scaled coordinates, rounded to nearest integer
    
    Example:
        >>> img1_shape = (640, 640)  # processed image size
        >>> coords = np.array([[100, 100], [200, 200]])
        >>> img0_shape = (480, 640)  # original image size
        >>> scaled_coords = scale_coordsV5(img1_shape, coords, img0_shape)
    """
    def _clip_coords(boxes, img_shape, step=2):
        # Clip bounding xyxy bounding boxes to image shape (height, width)
        boxes[:, 0::step].clip(0, img_shape[1])  # x1
        boxes[:, 1::step].clip(0, img_shape[0])  # y1
        
    step=1
    # Rescale coords (xyxy) from img1_shape to img0_shape
    if ratio_pad is None:  # calculate from img0_shape
        gain = min(img1_shape[0] / img0_shape[0], img1_shape[1] / img0_shape[1])  # gain  = old / new
        pad = (img1_shape[1] - img0_shape[1] * gain) / 2, (img1_shape[0] - img0_shape[0] * gain) / 2  # wh padding
    else:
        gain = ratio_pad[0]
        pad = ratio_pad[1]
    if isinstance(gain, (list, tuple)):
        gain = gain[0]
    coords[:, 0::step] -= pad[0]  # x padding
    coords[:, 1::step] -= pad[1]  # y padding
    coords[:, 0::step] /= gain
    coords[:, 1::step] /= gain

    _clip_coords(coords, img0_shape, step=step)
    coords = np.round(coords).astype(np.float32)
    return coords


def box_area(box):
    """
    Calculate the area of bounding boxes.
    
    Function:
        Calculate area based on top-left and bottom-right coordinates of bounding boxes.
        Uses formula: area = width × height
    
    Input:
        box (np.ndarray): Bounding box coordinates in (x1, y1, x2, y2) format
                           with shape (4,) or (4, n)
    
    Output:
        np.ndarray: Bounding box area
    
    Example:
        >>> box = np.array([10, 10, 50, 30])  # (x1, y1, x2, y2)
        >>> area = box_area(box)
        >>> print(area)  # 800 (width=40 × height=20)
    """
    
    return (box[:, 2] - box[:, 0]) * (box[:, 3] - box[:, 1])


def box_iou(box1, box2, eps=1e-7):
    """
    Calculate Intersection over Union (IoU) values between bounding boxes.
    
    Function:
        Calculate IoU (Intersection over Union) values between two sets of bounding boxes.
        Also known as Jaccard index, used to measure the overlap between two bounding boxes.
    
    Input:
        box1 (np.ndarray): First set of bounding boxes with shape (N, 4) in (x1, y1, x2, y2) format
        box2 (np.ndarray): Second set of bounding boxes with shape (M, 4) in (x1, y1, x2, y2) format
        eps (float): Small value to prevent division by zero, default 1e-7
    
    Output:
        np.ndarray: IoU matrix with shape (N, M)
                     containing IoU values for each pair of bounding boxes from box1 and box2
    
    Example:
        >>> box1 = np.ndarray([[0, 0, 10, 10]])  # one bounding box
        >>> box2 = np.ndarray([[5, 5, 15, 15]])  # another bounding box
        >>> iou = box_iou(box1, box2)
        >>> print(iou)  # [[0.1429]] (intersection area 25 / union area 175)
    """
    # https://github.com/pytorch/vision/blob/master/torchvision/ops/boxes.py

    # inter(N,M) = (rb(N,M,2) - lt(N,M,2)).clamp(0).prod(2)
    
    a1, a2 = np.split(box1[:, None, :], 2, axis=2)  # (N,1,2), (N,1,2)
    b1, b2 = np.split(box2[None, :, :], 2, axis=2)  # (1,M,2), (1,M,2)
    
    inter_wh = np.clip(np.minimum(a2, b2) - np.maximum(a1, b1), a_min=0, a_max=None)
    inter = inter_wh[..., 0] * inter_wh[..., 1]

    area1 = box_area(box1)  # (N,)
    area2 = box_area(box2)

    # IoU = inter / (area1 + area2 - inter)
    return inter / (area1[:, None] + area2[None, :] - inter + eps)
    

def non_max_suppression(
    prediction,
    conf_threshold=0.25,
    iou_threshold=0.7,
    classes=None,
    agnostic=False,
    max_det=300,
    nc=0,
    version='yolo11',
    task=None
):
    """
    Non-Maximum Suppression (   ) processing on inference results to remove overlapping detections.
    
    Function:
        Apply Non-Maximum Suppression to YOLO model inference results.
        Remove low-confidence and high-overlap detection boxes, retaining the best detections.
        Supports multiple YOLO versions (yolov5, yolov8, yolo11, etc.).
    
    Input:
        prediction (numpy.ndarray): Model inference results
        conf_thres (float): Confidence threshold, default 0.25
        iou_thres (float): IoU threshold, default 0.7
        classes (list, optional): Specific class indices to keep
        agnostic (bool): Whether to perform class-agnostic NMS, default False
        max_det (int): Maximum number of detections per image, default 300
        nc (int): Number of classes, default 0 (auto-calculate)
        version (str): YOLO version, default 'yolov11'
    
    Output:
        list: List of detection results for each image
        Each element is a tensor with raw_img_shape (n, 6) in format [x1, y1, x2, y2, conf, cls]
    """

    max_wh = 7680  # large offset for class-agnostic
    multiplier = 0 if agnostic else max_wh
    num_bbox_conf = 5 if version == "yolov5" else 4
    bs, _, num_feat = prediction.shape
    nc = nc or (num_feat - num_bbox_conf)  # infer num_classes
    mi = num_bbox_conf + nc
    time_limit = 0.5 + 0.05 * bs  # seconds to quit after

    # Pre-determine version-specific flags (moved outside loop)
    is_yolov5 = (version == "yolov5")
    apply_pose_multiplier = is_yolov5 and (task != "pose")
    if version not in ["yolov5", "yolov5u", "yolov8", "yolo11"]:
        raise ValueError(f"Unsupported YOLO version: {version}")

    outputs = [np.zeros((0, 6), dtype=np.float32)] * bs
    t = time.time()
    for xi, x in enumerate(prediction):
        if is_yolov5:
            xc = x[..., 4] > conf_threshold
            if apply_pose_multiplier:
                x[..., 5:] *= x[..., 4:5]
        else:
            x = x.transpose(1, 0)  # (num_boxes, num_features)
            xc = x[..., 4:mi].max(-1) > conf_threshold

        x = x[xc]  # filter by conf
        if not x.shape[0]:
            continue

        boxes = xywh2xyxy(x[..., :4])
        cls_scores = x[:, num_bbox_conf:num_bbox_conf + nc]
        mask = x[:, num_bbox_conf + nc:]

        conf = cls_scores.max(1)
        j = cls_scores.argmax(1)
        x = np.concatenate([boxes, conf[:, None], j[:, None].astype(np.float32), mask], axis=1)
        x = x[conf > conf_threshold]

        if classes is not None:
            x = x[np.isin(x[:, 5].astype(int), classes)]

        if not x.shape[0]:
            continue
        
        i = nms(x[..., :4] + x[..., 5:6] * multiplier, x[..., 4], iou_threshold=iou_threshold)[:max_det] # NMS 
        outputs[xi] = x[:max_det][i] if len(i) > 0 else np.zeros((0, x.shape[1]), dtype=np.float32)
        # Ensure indices are valid for the current x array
        if (time.time() - t) > time_limit:
            break  # time limit exceeded
    return outputs


def letterbox(img, new_shape=(640, 640), color=(114, 114, 114)):
    """
    Resize image to specified dimensions while maintaining aspect ratio and padding borders.
    
    Function:
        Resize input image to specified new dimensions while maintaining original aspect ratio.
        Fill empty areas with specified color, ensuring image is a multiple of 32 pixels.
    
    Input:
        img (numpy.ndarray): Input image with shape (height, width, channels)
        new_shape (tuple | int): Target dimensions, default (640, 640)
        color (tuple): Padding color (R, G, B), default (114, 114, 114)
    
    Output:
        numpy.ndarray: Resized image with dimensions new_shape
    
    Example:
        >>> img = cv2.imread('image.jpg')  # shape (480, 640, 3)
        >>> resized = letterbox(img, new_shape=(416, 416))
        >>> print(resized.shape)  # (416, 416, 3)
    """
    # Resize image to a 32-pixel-multiple rectangle https://github.com/ultralytics/yolov3/issues/232
    shape = img.shape[:2]  # current shape [height, width]
    # Scale ratio (new / old)
    r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
    # Compute padding
    new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
    dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding
    dw /= 2  # divide padding into 2 sides
    dh /= 2
    
    if shape[::-1] != new_unpad:  # resize
        img = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)
    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
    img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border
    return img

#==========================================
# Classification
#==========================================
DEFAULT_MEAN = (0.0, 0.0, 0.0)
DEFAULT_STD = (1.0, 1.0, 1.0)
DEFAULT_CROP_FRACTION = 1.0
def classify_transforms(
    size=224,
    mean=DEFAULT_MEAN,
    std=DEFAULT_STD,
    interpolation="BILINEAR",
    crop_fraction: float = DEFAULT_CROP_FRACTION,
):
    """
    Create a composition of image transforms for classification tasks.
    
    Function:
        Generate image preprocessing transform sequence suitable for classification models.
        Includes resizing, center cropping, tensor conversion, and normalization.
    
    Input:
        size (int | tuple): Target image size
                          If integer, represents shortest edge length
                          If tuple, represents (height, width)
        mean (tuple): RGB channel mean values for normalization
        std (tuple): RGB channel standard deviation values for normalization
        interpolation (str): Interpolation method, options: 'NEAREST', 'BILINEAR', or 'BICUBIC'
        crop_fraction (float): Crop fraction, default DEFAULT_CROP_FRACTION
    
    Output:
        torchvision.transforms.Compose: Composition of image transforms
    
    Example:
        >>> transforms = classify_transforms(size=224)
        >>> img = Image.open("path/to/image.jpg")
        >>> transformed_img = transforms(img)
        >>> print(transformed_img.shape)  # torch.Size([3, 224, 224])
    """
    import torchvision.transforms as T  # scope for faster 'import ultralytics'
    import torch
    if isinstance(size, (tuple, list)):
        assert len(size) == 2, f"'size' tuples must be length 2, not length {len(size)}"
        scale_size = tuple(math.floor(x / crop_fraction) for x in size)
    else:
        scale_size = math.floor(size / crop_fraction)
        scale_size = (scale_size, scale_size)

    # Aspect ratio is preserved, crops center within image, no borders are added, image is lost
    if scale_size[0] == scale_size[1]:
        # Simple case, use torchvision built-in Resize with the shortest edge mode (scalar size arg)
        tfl = [T.Resize(scale_size[0], interpolation=getattr(T.InterpolationMode, interpolation))]
    else:
        # Resize the shortest edge to matching target dim for non-square target
        tfl = [T.Resize(scale_size)]
    tfl.extend(
        [
            T.CenterCrop(size),
            T.ToTensor(),
            T.Normalize(mean=torch.tensor(mean), std=torch.tensor(std)),
        ]
    )
    return T.Compose(tfl)

def classify_transforms_numpy(
    img,
    size=224,
    mean=DEFAULT_MEAN,
    std=DEFAULT_STD,
    crop_fraction: float = DEFAULT_CROP_FRACTION,
):
    """
    Preprocess image for classification (NumPy version).
    Suitable for ONNX / TensorRT pipelines.

    Parameters
    ----------
    img : np.ndarray
        Input image in HWC format, uint8 [0,255].
    size : int or tuple
        Output size (height, width).
    mean : tuple of float
        Channel mean for normalization.
    std : tuple of float
        Channel std for normalization.
    crop_fraction : float
        Fraction for center crop before resize.

    Returns
    -------
    np.ndarray
        Preprocessed image in CHW format, float32.

    Example:
        img_np = cv2.imread("cat.jpg")[:, :, ::-1]  # BGR->RGB
        img_trt = classify_transforms_numpy(img_np, size=224)  # np.ndarray, shape (3,224,224)
    """
    if isinstance(size, int):
        size = (size, size)

    h, w = img.shape[:2]
    scale = min(size[0] / h, size[1] / w)
    new_w, new_h = int(w * scale), int(h * scale)
    resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

    # optional center crop
    if crop_fraction < 1.0:
        crop_w, crop_h = int(size[1] * crop_fraction), int(size[0] * crop_fraction)
        start_x = (new_w - crop_w) // 2
        start_y = (new_h - crop_h) // 2
        resized = resized[start_y:start_y+crop_h, start_x:start_x+crop_w]

    # final resize to match target
    resized = cv2.resize(resized, (size[1], size[0]), interpolation=cv2.INTER_LINEAR)

    # normalize
    img_np = resized.astype(np.float32) / 255.0
    img_np = (img_np - mean) / std

    return np.transpose(img_np, (2, 0, 1))  # HWC -> CHW

#==========================================
# Mask
#==========================================
def process_mask(protos, masks_in, bboxes, shape, upsample=False, version='yolo11'):
    """
    Apply masks to bounding boxes using the output of the mask head.
    
    Function:
        Combine prototype masks and mask coefficients to generate final segmentation masks.
        Supports different YOLO model versions and optional upsampling.
    
    Input:
        protos (np.ndarray): Prototype mask tensor with shape [mask_dim, mask_h, mask_w]
        masks_in (np.ndarray): Mask coefficients tensor with shape [n, mask_dim]
                                where n is the number of masks after NMS
        bboxes (np.ndarray): Bounding box tensor with shape [n, 4]
        shape (tuple): Input image dimensions (h, w)
        upsample (bool): Whether to upsample masks to original image size, default False
        version (str): YOLO version, default 'yolo11'
    
    Output:
        np.ndarray: Binary mask tensor with shape [n, h, w]
                     where n is the number of masks after NMS
    """
    c, mh, mw = protos.shape  # CHW
    ih, iw = shape

    if masks_in.shape[0] == 0:
        return np.zeros((0, mh, mw))

    masks = (masks_in @ protos.reshape(c, -1)).reshape(-1, mh, mw)  # CHW
    width_ratio = mw / iw
    height_ratio = mh / ih

    bboxes = bboxes.copy().astype(np.float32)
    bboxes[:, 0] *= width_ratio
    bboxes[:, 2] *= width_ratio
    bboxes[:, 3] *= height_ratio
    bboxes[:, 1] *= height_ratio

    masks = crop_mask(masks, bboxes)  # CHW
    if upsample:
        masks = np.stack([cv2.resize(m, (iw, ih), interpolation=cv2.INTER_LINEAR) for m in masks])  # CHW
    if version in ['yolov8', 'yolo11']:
        threshold = 0.0
    elif version == 'yolov5':
        threshold = 0.5
    else:
        raise ValueError(f"Invalid version: {version}")
    return (masks > threshold)


def crop_mask(masks, boxes):
    """
    Crop predicted masks to bounding box regions.
    
    Function:
        Set mask pixels outside bounding boxes to zero, retaining masks within bounding boxes.
        Uses vectorized operations for improved efficiency.
    
    Input:
        masks (np.ndarray): Mask tensor with shape [n, h, w]
        boxes (np.ndarray): Bounding box coordinate tensor with shape [n, 4]
                             in relative coordinate format (x1, y1, x2, y2)
    
    Output:
        np.ndarray: Cropped masks with shape [n, h, w]
    """
    n, h, w = masks.shape
    y = np.arange(h)[:, None]  # shape (h,1)
    x = np.arange(w)[None, :]  # shape (1,w)

    out = np.zeros_like(masks)
    for i in range(n):
        x1, y1, x2, y2 = boxes[i].astype(int)
        crop = np.zeros((h, w), dtype=masks.dtype)
        crop[y1:y2, x1:x2] = 1
        out[i] = masks[i] * crop
    return out


def scale_masks(masks, shape, padding: bool = True):
    """
    Rescale segmentation masks to target shape.
    
    Function:
        Scale masks from one size to another size.
        Supports YOLO-style padding handling.
    
    Input:
        masks (np.ndarray): Mask tensor with shape (N, C, H, W)
        shape (tuple): Target height and width (height, width)
        padding (bool): Whether masks are based on YOLO-style padded images, default True
    
    Output:
        np.ndarray: Rescaled masks
    """
    n, c, mh, mw = masks.shape
    gain = min(mh / shape[0], mw / shape[1])
    pad = [mw - shape[1] * gain, mh - shape[0] * gain]
    if padding:
        pad[0] /= 2
        pad[1] /= 2
    top, left = int(round(pad[1] - 0.1)), int(round(pad[0] - 0.1))
    bottom, right = mh - int(round(pad[1] + 0.1)), mw - int(round(pad[0] + 0.1))

    cropped = masks[..., top:bottom, left:right]

    resized = np.zeros((n, c, shape[0], shape[1]), dtype=np.float32)
    for i in range(n):
        for j in range(c):
            resized[i, j] = cv2.resize(cropped[i, j], (shape[1], shape[0]), interpolation=cv2.INTER_LINEAR)
    return resized
    

def scale_image(masks, im0_shape, ratio_pad=None):
    """
    Scale masks or images to original image dimensions.
    
    Function:
        Scale resized and padded masks or images back to original image dimensions.
        Remove padding and adjust to correct dimensions.
    
    Input:
        masks (np.ndarray): Resized and padded masks/images
                           with shape [h, w, num] or [h, w, 3]
        im0_shape (tuple): Original image shape (height, width)
        ratio_pad (tuple, optional): Padding ratio and padding values
                                   in format (ratio, pad)
    
    Output:
        np.ndarray: Scaled masks with shape [h, w, num]
    
    Example:
        >>> masks = np.random.rand(640, 640, 3)  # padded image
        >>> im0_shape = (480, 640)  # original image size
        >>> scaled = scale_image(masks, im0_shape)
        >>> print(scaled.shape)  # (480, 640, 3)
    """
    # Rescale coordinates (xyxy) from im1_shape to im0_shape
    im1_shape = masks.shape
    if im1_shape[:2] == im0_shape[:2]:
        return masks
    if ratio_pad is None:  # calculate from im0_shape
        gain = min(im1_shape[0] / im0_shape[0], im1_shape[1] / im0_shape[1])  # gain  = old / new
        pad = (im1_shape[1] - im0_shape[1] * gain) / 2, (im1_shape[0] - im0_shape[0] * gain) / 2  # wh padding
    else:
        # gain = ratio_pad[0][0]
        pad = ratio_pad[1]
    top, left = int(pad[1]), int(pad[0])  # y, x
    bottom, right = int(im1_shape[0] - pad[1]), int(im1_shape[1] - pad[0])

    if len(masks.shape) < 2:
        raise ValueError(f'"len of masks shape" should be 2 or 3, but got {len(masks.shape)}')
    masks = masks[top:bottom, left:right]
    masks = cv2.resize(masks, (im0_shape[1], im0_shape[0]))
    if len(masks.shape) == 2:
        masks = masks[:, :, None]
    return masks

def min_index(arr1, arr2):
    """
    Find a pair of indexes with the shortest distance between two arrays of 2D points.

    Args:
        arr1 (np.ndarray): A NumPy array of shape (N, 2) representing N 2D points.
        arr2 (np.ndarray): A NumPy array of shape (M, 2) representing M 2D points.

    Returns:
        (tuple): A tuple containing the indexes of the points with the shortest distance in arr1 and arr2 respectively.
    """
    dis = ((arr1[:, None, :] - arr2[None, :, :]) ** 2).sum(-1)
    return np.unravel_index(np.argmin(dis, axis=None), dis.shape)

def merge_multi_segment(segments):
    """
    Merge multiple segments into one list by connecting the coordinates with the minimum distance between each segment.
    This function connects these coordinates with a thin line to merge all segments into one.

    Args:
        segments (List[List]): Original segmentations in COCO's JSON file.
                               Each element is a list of coordinates, like [segmentation1, segmentation2,...].

    Returns:
        s (List[np.ndarray]): A list of connected segments represented as NumPy arrays.
    """
    s = []
    segments = [np.array(i).reshape(-1, 2) for i in segments]
    idx_list = [[] for _ in range(len(segments))]

    # Record the indexes with min distance between each segment
    for i in range(1, len(segments)):
        idx1, idx2 = min_index(segments[i - 1], segments[i])
        idx_list[i - 1].append(idx1)
        idx_list[i].append(idx2)

    # Use two round to connect all the segments
    for k in range(2):
        # Forward connection
        if k == 0:
            for i, idx in enumerate(idx_list):
                # Middle segments have two indexes, reverse the index of middle segments
                if len(idx) == 2 and idx[0] > idx[1]:
                    idx = idx[::-1]
                    segments[i] = segments[i][::-1, :]

                segments[i] = np.roll(segments[i], -idx[0], axis=0)
                segments[i] = np.concatenate([segments[i], segments[i][:1]])
                # Deal with the first segment and the last one
                if i in {0, len(idx_list) - 1}:
                    s.append(segments[i])
                else:
                    idx = [0, idx[1] - idx[0]]
                    s.append(segments[i][idx[0] : idx[1] + 1])

        else:
            for i in range(len(idx_list) - 1, -1, -1):
                if i not in {0, len(idx_list) - 1}:
                    idx = idx_list[i]
                    nidx = abs(idx[1] - idx[0])
                    s.append(segments[i][nidx:])
    return s

def masks2segments(masks, strategy: str = "all"):
    """
    Convert masks to segments using contour detection.

    Args:
        masks (np.ndarray): Binary masks with shape (batch_size, 160, 160).
        strategy (str): Segmentation strategy, either 'all' or 'largest'.

    Returns:
        (list): List of segment masks as float32 arrays.
    """
    segments = []
    for x in masks.astype("uint8"):
        c, _ = cv2.findContours(x, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(c) > 0:
            if strategy == "all":
                if len(c) > 1:
                    c = np.concatenate([cnt.reshape(-1, 2) for cnt in c])
                else:
                    c = c[0].reshape(-1, 2)
            elif strategy == "largest":
                c = max(c, key=lambda a: len(a)).reshape(-1, 2)
        else:
            c = np.zeros((0, 2), dtype=np.float32)
        segments.append(c.astype(np.float32))
    return segments