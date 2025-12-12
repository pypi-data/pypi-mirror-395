from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Sequence

import numpy as np

try:
    from qiskit import QuantumCircuit
    from qiskit_aer import AerSimulator
except Exception:  # pragma: no cover - qiskit puede no estar instalado
    QuantumCircuit = None
    AerSimulator = None


class BaseQuantumBackend(ABC):
    """Interfaz genérica para backends cuánticos."""

    @abstractmethod
    def run_anomaly_circuit(
        self,
        angles: Sequence[float],
        params: Sequence[float],
        shots: int = 1024,
    ) -> float:
        """Devuelve un 'anomaly score' en [0,1] a partir de un circuito."""


class QiskitBackend(BaseQuantumBackend):
    """Backend basado en Qiskit (simulador).

    - Codifica la ventana en rotaciones Ry.
    - Aplica capas de Rz+Ry parametrizadas.
    - El score es la probabilidad media de medir '1' en el último qubit.
    """

    def __init__(self, n_qubits: int, depth: int = 1) -> None:
        if QuantumCircuit is None or AerSimulator is None:
            raise RuntimeError(
                "Qiskit y qiskit-aer son necesarios para QiskitBackend. "
                "Instala con `pip install qiskit qiskit-aer`."
            )
        self.n_qubits = n_qubits
        self.depth = depth
        self.sim = AerSimulator()

    def run_anomaly_circuit(
        self,
        angles: Sequence[float],
        params: Sequence[float],
        shots: int = 1024,
    ) -> float:
        import math

        if len(angles) != self.n_qubits:
            raise ValueError(
                f"Se esperaban {self.n_qubits} ángulos, recibido {len(angles)}"
            )

        qc = QuantumCircuit(self.n_qubits, 1)

        # Encoding: Ry(angles[i]) sobre cada qubit
        for i, a in enumerate(angles):
            qc.ry(float(a), i)

        # Variational layers
        idx = 0
        for _ in range(self.depth):
            for q in range(self.n_qubits):
                qc.rz(float(params[idx % len(params)]), q)
                idx += 1
            for q in range(self.n_qubits):
                qc.ry(float(params[idx % len(params)]), q)
                idx += 1
            # Cadenas de CNOT tipo ring
            for q in range(self.n_qubits - 1):
                qc.cx(q, q + 1)

        # Medimos solo el último qubit como "anomaly qubit"
        qc.measure(self.n_qubits - 1, 0)

        job = self.sim.run(qc, shots=shots)
        result = job.result()
        counts = result.get_counts()
        # Probabilidad de resultado "1" (anómalo)
        p1 = counts.get("1", 0) / shots
        return float(p1)
