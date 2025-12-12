"""
Radar band utilities for the Zeta Collapse Model (ZCM).

These functions implement the basic deterministic "band" logic used by ZCM.
They are intentionally kept simple and numeric so they can be reused in
many different domains (tokens, numbers, indices, etc.).
"""

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class RadarBand:
    center: float
    radius: float

    @property
    def lower(self) -> float:
        return self.center - self.radius

    @property
    def upper(self) -> float:
        return self.center + self.radius


def make_radar_band(center: float, radius: float) -> RadarBand:
    """
    Create a radar band around a given center value.

    This is a pure math helper and does not depend on any database or engine.
    """
    return RadarBand(center=center, radius=radius)


def in_radar_band(value: float, band: RadarBand) -> bool:
    """
    Return True if `value` lies inside the closed interval [lower, upper]
    of the given radar band.
    """
    return band.lower <= value <= band.upper


def filter_by_radar_band(values: Iterable[float], band: RadarBand) -> list[float]:
    """
    Filter an iterable of numeric values, returning only those inside the band.
    """
    return [v for v in values if in_radar_band(v, band)]
