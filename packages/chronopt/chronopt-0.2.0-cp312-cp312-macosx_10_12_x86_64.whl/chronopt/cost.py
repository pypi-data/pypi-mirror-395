"""Cost metric helpers exposed by the Chronopt Python API."""

from __future__ import annotations

from chronopt._chronopt import RMSE as _RMSE
from chronopt._chronopt import SSE as _SSE
from chronopt._chronopt import CostMetric
from chronopt._chronopt import GaussianNLL as _GaussianNLL


def SSE(weight: float = 1.0) -> CostMetric:
    """Sum of Squared Errors cost metric."""
    return _SSE(weight)


def RMSE(weight: float = 1.0) -> CostMetric:
    """Root Mean Squared Error cost metric."""
    return _RMSE(weight)


def GaussianNLL(variance: float = 1.0, weight: float = 1.0) -> CostMetric:
    """Gaussian Negative Log-Likelihood cost metric.

    A single positional argument is interpreted as the variance. An optional
    second positional argument (or keyword) can be used as a weight
    multiplier on the resulting cost.
    """
    return _GaussianNLL(variance, weight)


__all__ = ["CostMetric", "SSE", "RMSE", "GaussianNLL"]
