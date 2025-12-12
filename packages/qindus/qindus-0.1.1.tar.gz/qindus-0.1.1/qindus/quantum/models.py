from __future__ import annotations
from dataclasses import dataclass, field
from typing import Iterable, Sequence
import numpy as np

from .backends import BaseQuantumBackend
from .encoders import angle_encoder


@dataclass
class QuantumAnomalyDetector:
    """Modelo cuántico simple para scoring de anomalías.

    No implementamos un entrenamiento completo, pero sí:
    - inicialización aleatoria de parámetros
    - posibilidad de ajustarlos
    - método score() para obtener el anomaly score de una ventana
    """

    backend: BaseQuantumBackend
    n_params: int = 16
    params: np.ndarray = field(default_factory=lambda: np.array([]))

    def __post_init__(self) -> None:
        if self.params.size == 0:
            # Inicialización aleatoria pequeña
            self.params = 0.1 * np.random.randn(self.n_params)

    def set_params(self, params: Sequence[float]) -> None:
        params = np.asarray(params, dtype=float)
        if params.size != self.n_params:
            raise ValueError(
                f"Se esperaban {self.n_params} parámetros, recibido {params.size}"
            )
        self.params = params

    def score(
        self,
        window: Sequence[float],
        shots: int = 1024,
    ) -> float:
        """Devuelve un score de anomalía en [0,1] para una ventana."""
        angles = angle_encoder(window, n_qubits=self.backend.n_qubits)
        return self.backend.run_anomaly_circuit(
            angles=angles,
            params=self.params,
            shots=shots,
        )

    def score_multiple(
        self,
        windows: Iterable[Sequence[float]],
        shots: int = 1024,
    ) -> np.ndarray:
        scores = [self.score(w, shots=shots) for w in windows]
        return np.asarray(scores, dtype=float)
