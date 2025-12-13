import os
import random
import cv2
import numpy as np
from PIL import Image


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
    if isinstance(new_shape, int):
        new_shape = (new_shape, new_shape)
    elif isinstance(new_shape, tuple):
        new_shape = new_shape
    else:
        raise TypeError(f"Unsupported type for new_shape: {type(new_shape)}")
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


def make_quant_dataset(dataset_path, img_size=320, ch=3, max_num=5000, output_dir='./'):
    """Create quantization dataset"""
    os.makedirs(output_dir, exist_ok=True)
    # images_list = [img_name for img_name in os.listdir(dataset_path) 
    #               if os.path.splitext(img_name)[1] == ".jpg"]
    import glob
    images_list = []
    if isinstance(dataset_path, list):
        for p in dataset_path:
            images_list.extend(glob.glob(p))
    else:
        images_list = glob.glob(dataset_path)

    random.shuffle(images_list)

    images_list = images_list[:max_num]
    
    calib_dataset = np.zeros((len(images_list), img_size, img_size, ch))
    error_count = 0
    error_path_list = []
    for idx, img_name in enumerate(sorted(images_list)):
        img = np.array(Image.open(img_name))
        if img.shape[-1] == 3:
            img_preproc = letterbox(img, new_shape=(img_size, img_size))
            calib_dataset[idx, :, :, :] = img_preproc
        else:
            error_path_list.append(img_name)
            error_count += 1
    print(f"error_count: {error_count}")
    print(f"error_path_list: {error_path_list}")
    
    save_data_path = os.path.join(output_dir, "calib_set.npy")
    np.save(save_data_path, calib_dataset)
    return calib_dataset