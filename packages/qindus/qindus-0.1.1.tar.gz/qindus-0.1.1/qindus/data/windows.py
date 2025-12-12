from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, List
import numpy as np


@dataclass
class WindowConfig:
    """Configuración de extracción de ventanas sobre una serie temporal."""
    window_size: int
    step: int
    normalize: bool = True


def create_windows(
    series: Iterable[float],
    config: WindowConfig,
) -> np.ndarray:
    """Convierte una serie [x1, x2, ...] en ventanas solapadas.

    Devuelve un array de shape (num_ventanas, window_size).
    """
    arr = np.asarray(series, dtype=float)
    windows: List[np.ndarray] = []
    for start in range(0, len(arr) - config.window_size + 1, config.step):
        w = arr[start:start + config.window_size].copy()
        if config.normalize:
            std = w.std() or 1.0
            w = (w - w.mean()) / std
        windows.append(w)
    if not windows:
        return np.empty((0, config.window_size))
    return np.stack(windows, axis=0)
