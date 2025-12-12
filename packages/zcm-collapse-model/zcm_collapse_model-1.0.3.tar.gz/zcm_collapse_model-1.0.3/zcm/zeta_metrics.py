"""
Minimal zeta-related metrics used in ZCM examples.

This file intentionally contains only simple, demonstrative functions.
It does NOT attempt to implement full analytic number theory and does
not expose any database or engine behaviour.
"""

from typing import Iterable
import cmath


def basic_zeta_metric(ts: Iterable[float]) -> float:
    """
    Compute a very simple aggregate metric over zeta(1/2 + i t) values
    for a list of t's.

    This is meant as a toy / illustrative function. In the full model,
    more detailed spectral and fractal analysis is used.
    """
    total = 0.0
    count = 0

    for t in ts:
        s = 0.5 + 1j * t
        # naive, slow zeta approximation – placeholder only
        z = _zeta_naive(s, terms=200)
        total += abs(z)
        count += 1

    return total / count if count else 0.0


def _zeta_naive(s: complex, terms: int = 200) -> complex:
    """
    Very naive implementation of the Dirichlet series for zeta(s),
    for Re(s) > 1/2 and small term counts. This is ONLY for examples,
    not for serious analysis.
    """
    acc = 0 + 0j
    for n in range(1, terms + 1):
        acc += 1 / (n ** s)
    return acc
