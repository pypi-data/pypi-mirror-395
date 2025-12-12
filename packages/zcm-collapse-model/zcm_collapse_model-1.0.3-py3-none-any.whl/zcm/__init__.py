"""
Zeta Collapse Model (ZCM) - Math Library

This package exposes the public math-only API for the ZCM collapse model.
System architecture, databases, and engines are intentionally excluded.
"""

from .collapse import collapse_by_radar_band
from .radar_bands import make_radar_band, in_radar_band
from .zeta_metrics import basic_zeta_metric

__all__ = [
    "collapse_by_radar_band",
    "make_radar_band",
    "in_radar_band",
    "basic_zeta_metric",
]
