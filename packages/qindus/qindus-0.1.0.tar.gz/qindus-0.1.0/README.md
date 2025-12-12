# qindus

Librería de ejemplo para detección de anomalías en tráfico industrial usando un modelo cuántico
(simulado con Qiskit) sobre series temporales derivadas de un PCAP.

## Instalación (entorno virtual recomendado)

```bash
pip install -e .
```

Necesitas además:

```bash
pip install qiskit qiskit-aer scapy
```

## Uso rápido con un PCAP

```bash
python run_pcap_analysis.py ruta_al_fichero.pcap
```

El script:
- Carga el PCAP.
- Extrae una serie temporal de tamaños de paquetes.
- Usa la primera mitad como "normal" para aprender un umbral.
- Analiza la segunda mitad y marca ventanas sospechosas.
