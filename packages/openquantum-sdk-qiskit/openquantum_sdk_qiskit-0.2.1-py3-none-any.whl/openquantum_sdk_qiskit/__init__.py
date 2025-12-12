from __future__ import annotations

from .oq_service import OpenQuantumService
from .oq_backend import OpenQuantumBackend
from .oq_sampler import OQSampler
from .oq_estimator import OQEstimator

SamplerV2 = OQSampler
EstimatorV2 = OQEstimator

__version__ = "0.2.0"
__all__ = [
    "OpenQuantumService",
    "OpenQuantumBackend",
    "OQSampler",
    "SamplerV2",
    "OQEstimator",
    "EstimatorV2",
]
