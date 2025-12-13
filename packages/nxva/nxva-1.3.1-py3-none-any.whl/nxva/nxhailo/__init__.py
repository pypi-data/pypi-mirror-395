import warnings

try:
    from .inference import HefInference
    from .feat_process import HailoFeatPostFactory, HailoFeatPreFactory
except Exception as e:
    print(e)
    warnings.warn(f"⚠️ Hailort not install: {e}")
