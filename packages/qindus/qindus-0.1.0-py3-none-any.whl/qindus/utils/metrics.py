from __future__ import annotations
import numpy as np


def threshold_from_quantile(scores, q: float = 0.95) -> float:
    """Umbral basado en cuantil (por ejemplo 0.95)."""
    scores = np.asarray(scores, dtype=float)
    if scores.size == 0:
        return 1.0
    return float(np.quantile(scores, q))
