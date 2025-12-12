from __future__ import annotations
from typing import Sequence
import numpy as np


def angle_encoder(
    window: Sequence[float],
    n_qubits: int,
) -> np.ndarray:
    """Codifica una ventana en ángulos para Ry usando normalización.

    - Escala la ventana a [-π/2, π/2] o similar.
    - Si hay más qubits que elementos, rellena con ceros.
    - Si hay más elementos que qubits, hace un downsampling sencillo.
    """
    x = np.asarray(window, dtype=float)
    if x.size == 0:
        return np.zeros(n_qubits, dtype=float)

    # Normalización robusta
    x = (x - x.mean()) / (x.std() or 1.0)
    x = np.clip(x, -3, 3)  # evitar outliers extremos
    x = (x / 3.0) * (np.pi / 2.0)

    if x.size == n_qubits:
        return x
    elif x.size > n_qubits:
        idx = np.linspace(0, x.size - 1, n_qubits).astype(int)
        return x[idx]
    else:
        padded = np.zeros(n_qubits, dtype=float)
        padded[:x.size] = x
        return padded
