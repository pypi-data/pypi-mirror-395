import warnings

import numpy as np

"""
Because the Hailo NPU may cuts off the head and tail of the feature map in the ONNX model, 
we have to restore it.
"""


def post_default(results, m):
    return [results[info.name] for info in m["output_infos"]]

def post_feat_yolov5_detect(results, m):
    return [results[info.name].transpose(0, 3, 1, 2) for info in m["output_infos"]]

def post_feat_yolov5_pose(results, m):
    outputs = [results[info.name].transpose(0, 3, 1, 2) for info in m["output_infos"]]
    return [np.concatenate(outputs[i:i+2], axis=1) for i in range(0, len(outputs), 2)]    

def post_feat_yolo11_detect(results, m):
    outputs = [results[info.name].transpose(0, 3, 1, 2) for info in m["output_infos"]]
    return [np.concatenate(outputs[i:i+2], axis=1) for i in range(0, len(outputs), 2)]

def post_feat_yolo11_pose(results, m):
    outputs = [results[info.name].transpose(0, 3, 1, 2) for info in m["output_infos"]]
    return [outputs[:3], outputs[3:]]

def post_feat_yolo11_classify(results, m):
    return np.array([[results[info.name][0] for info in m["output_infos"]][0]])

def post_feat_embed(results, m):
    outptus = [results[info.name] for info in m["output_infos"]]
    return outputs

def pre_feat_yolov5_pose(input_data):
    key = next(iter(input_data))
    data = input_data[key]
    
    N, H, W, C = data.shape
    
    # 將 2x2 的區塊重新排列，但保持 NHWC 格式
    # 原始: (N, H, W, C) -> 目標: (N, H//2, W//2, 4*C)
    H //= 2
    W //= 2
    
    # 方法1: 直接使用 reshape
    # 將 (N, H*2, W*2, C) reshape 成 (N, H, 2, W, 2, C)
    # 然後 transpose 成 (N, H, W, 2, 2, C)
    # 最後 reshape 成 (N, H, W, 4*C)
    data = data.reshape(N, H, 2, W, 2, C)
    data = data.transpose(0, 1, 3, 2, 4, 5)
    data = data.reshape(N, H, W, 4*C)
    
    input_data[key] = data
    return input_data

def pre_default(input_data):
    return input_data


class HailoFeatPostFactory:
    """
    featFactory
    根據 version 與 task 自動回傳對應的解碼函式。
    如果找不到對應組合，會 warning 並使用 default 函式。
    """

    _MAP = {
        ('yolov5', 'pose'): post_feat_yolov5_pose,
        ('yolov5', 'detect'): post_feat_yolov5_detect,
        ('yolo11', 'detect'): post_feat_yolo11_detect,
        ('yolo11', 'pose'): post_feat_yolo11_pose,
        ('yolo11', 'classify'): post_feat_yolo11_classify,
        ('embed', 'embed'): post_feat_embed,
    }

    _DEFAULT = post_default

    @classmethod
    def create(cls, version, task):
        key = (version, task)
        if key not in cls._MAP:
            warnings.warn(f"⚠️ Unsupported version-task combination: {key}, using default function.")
            return cls._DEFAULT
        return cls._MAP[key]


class HailoFeatPreFactory:
    """
    featFactory
    根據 version 與 task 自動回傳對應的解碼函式。
    - 特殊組合 ('yolov5','pose') 使用 pre_feat_yolov5_pose
    - 其他組合使用 pre_feat_default，並 warning
    """

    _MAP = {
        ('yolov5', 'pose'): pre_feat_yolov5_pose,
    }

    _DEFAULT = pre_default

    @classmethod
    def create(cls, version, task):
        key = (version, task)
        # if key not in cls._MAP:
        #     warnings.warn(f"⚠️ Unsupported version-task combination: {key}, using default function.")
        return cls._MAP.get(key, cls._DEFAULT)


# [array([[8.1031357e-07, 3.6341215e-05, 5.2590476e-10, 9.9996281e-01,2.0658609e-11]], dtype=float32)]