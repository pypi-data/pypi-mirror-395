"""
Neural Scaling Probe: Predict scaling laws from data geometry.

Predict β_D (data scaling exponent) before expensive training runs
using intrinsic dimension measurement.

Usage:
    from scaling_law_probe import predict_beta

    beta, id_estimate = predict_beta(texts, encoder="minilm")
    print(f"Predicted β_D: {beta:.3f}, ID: {id_estimate:.1f}")
"""

__version__ = "0.1.0"

from .probe import predict_beta, measure_id, ScalingProbe
from .probes.twonn import twonn_id

__all__ = ["predict_beta", "measure_id", "twonn_id", "ScalingProbe", "__version__"]
