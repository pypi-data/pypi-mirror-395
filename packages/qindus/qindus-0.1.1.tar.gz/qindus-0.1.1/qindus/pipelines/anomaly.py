from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, Tuple
import numpy as np

from ..data.windows import WindowConfig, create_windows
from ..quantum.models import QuantumAnomalyDetector
from ..utils.metrics import threshold_from_quantile


@dataclass
class IndustrialAnomalyPipeline:
    """Pipeline end-to-end para detección de anomalías.

    - Recibe una serie temporal (por ejemplo tamaños de paquetes).
    - La trocea en ventanas.
    - Usa el modelo cuántico para obtener un score por ventana.
    - Define un umbral basado en un cuantil del histórico 'normal'.
    """

    window_config: WindowConfig
    model: QuantumAnomalyDetector
    quantile: float = 0.99  # umbral muy exigente por defecto

    _threshold: float | None = None

    def fit(
        self,
        normal_series: Iterable[float],
        shots: int = 512,
    ) -> float:
        """Ajusta el umbral a partir de datos históricos 'normales'."""
        windows = create_windows(normal_series, self.window_config)
        if windows.shape[0] == 0:
            raise ValueError("No hay suficientes datos para crear ventanas.")
        scores = self.model.score_multiple(windows, shots=shots)
        self._threshold = threshold_from_quantile(scores, self.quantile)
        return self._threshold

    def detect(
        self,
        series: Iterable[float],
        shots: int = 512,
    ) -> Tuple[np.ndarray, np.ndarray, float]:
        """Aplica la detección sobre una serie nueva.

        Devuelve:
        - scores: array de scores por ventana.
        - flags: array bool de si cada ventana es anómala.
        - threshold: umbral usado.
        """
        if self._threshold is None:
            raise RuntimeError(
                "Pipeline no entrenada. Llama primero a fit() con datos normales."
            )

        windows = create_windows(series, self.window_config)
        if windows.shape[0] == 0:
            raise ValueError("No hay suficientes datos para crear ventanas.")
        scores = self.model.score_multiple(windows, shots=shots)
        flags = scores >= self._threshold
        return scores, flags, self._threshold
