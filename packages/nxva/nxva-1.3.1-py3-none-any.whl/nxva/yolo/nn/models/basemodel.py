import torch.nn as nn
from ..modules import DWConv, Conv
from ...utils.torch_utils import model_info, fuse_conv_and_bn


class BaseModel(nn.Module):
    def forward(self, x):
        return self._forward_once(x)

    def _forward_once(self, x):
        y = []
        for i, m in enumerate(self.model):
            if m.f != -1:
                x = y[m.f] if isinstance(m.f, int) else [x if j == -1 else y[j] for j in m.f]
            
            x = m(x)
            
            y.append(x if m.i in self.save else None)
        return x

    def info(self, verbose=False, img_size=320):
        """Prints model information given verbosity and image size, e.g., `info(verbose=True, img_size=640)`."""
        model_info(self, verbose, img_size)

    def fuse(self):
        """Fuses Conv2d() and BatchNorm2d() layers in the model to improve inference speed."""
        for m in self.model.modules():
            if isinstance(m, (Conv, DWConv)) and hasattr(m, "bn"):
                m.conv = fuse_conv_and_bn(m.conv, m.bn)  # update conv
                delattr(m, "bn")  # remove batchnorm
                m.forward = m.forward_fuse  # update forward
        self.info()
        return self


class ClassificationModel(BaseModel):
    def __init__(self, cfg=None, ch=3, nc=None):
        super().__init__()

    def forward(self, x):
        return self._forward_once(x)


class DetectionModel(BaseModel):
    def __init__(self, cfg=None, ch=3, nc=None, anchors=None):
        super().__init__()

    def forward(self, x):
        return self._forward_once(x)


class PoseModel(DetectionModel):
    def __init__(self, cfg=None, ch=3, nc=None):
        super().__init__(cfg=cfg, ch=ch, nc=nc)


class SegmentationModel(DetectionModel):
    def __init__(self, cfg=None, ch=3, nc=None):
        super().__init__(cfg=cfg, ch=ch, nc=nc)