from __future__ import annotations
from typing import Sequence
import numpy as np

try:
    from scapy.all import rdpcap
except Exception:  # pragma: no cover - scapy puede no estar instalado
    rdpcap = None


def pcap_lengths_series(path: str) -> np.ndarray:
    """Carga un PCAP y devuelve una serie temporal simple de tamaños de paquetes.

    Esta función está pensada como ejemplo educativo:
    - Cada muestra es la longitud de un paquete en bytes.
    - Puedes extenderla para agrupar por flujo, tiempos, etc.
    """
    if rdpcap is None:
        raise RuntimeError(
            "scapy no está disponible. Instala con `pip install scapy`."
        )
    pkts = rdpcap(path)
    lengths = [len(pkt) for pkt in pkts]
    return np.asarray(lengths, dtype=float)
