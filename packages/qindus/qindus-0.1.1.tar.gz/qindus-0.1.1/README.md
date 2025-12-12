# QINDUS – Quantum Industrial Detection System

Quantum-enhanced anomaly detection for OT and industrial networks  
Autor: **José Israel Nadal Vidal**

---

## Descripción general

QINDUS (Quantum Industrial Detection System) es una librería de Python para la detección de anomalías en tráfico industrial y redes OT (SCADA, PLC, HMI, etc.) utilizando modelos cuánticos variacionales simulados con Qiskit.

A partir de un fichero PCAP, QINDUS:

1. Extrae una serie temporal (por ejemplo, tamaños de paquetes).
2. Fragmenta la serie en ventanas temporales.
3. Codifica cada ventana en un circuito cuántico parametrizado.
4. Calcula un valor de anomalía (*anomaly score*) en el rango `[0, 1]`.
5. Marca como sospechosas las ventanas cuyo comportamiento no se ajusta al tráfico considerado normal.

Este enfoque permite detectar cambios sutiles en el comportamiento de sistemas industriales que difícilmente se identifican con técnicas clásicas.

---

## Índice

- [Características principales](#características-principales)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso rápido desde línea de comandos](#uso-rápido-desde-línea-de-comandos)
- [Uso como librería](#uso-como-librería)
- [Arquitectura de QINDUS](#arquitectura-de-qindus)
- [Testing](#testing)
- [Documentación](#documentación)
- [Hoja de ruta](#hoja-de-ruta)
- [Autor y cita](#autor-y-cita)
- [Licencia](#licencia)

---

## Características principales

1. **Modelo cuántico variacional (VQC)**  
   - Backend cuántico basado en Qiskit Aer (simulador).  
   - Codificación de ventanas mediante rotaciones en qubits.  
   - La probabilidad de medición del estado `|1⟩` se interpreta como *anomaly score*.

2. **Enfoque específico para redes OT e industria**  
   - Diseñado para tráfico determinista típico de entornos industriales.  
   - Adecuado para analizar patrones cíclicos de PLC, SCADA y sistemas de control.

3. **Pipeline completo de anomalías**  
   - PCAP → serie temporal → ventanas → modelo cuántico → umbral → anomalías.  
   - Incluye un script de análisis con generación de informe interpretativo.

4. **Umbral de anomalía autoaprendido**  
   - La primera parte del tráfico se considera referencia “normal”.  
   - El umbral se define como un cuantil configurable (por defecto, 0.99).  
   - No requiere reglas fijas ni calibraciones manuales complejas.

5. **Arquitectura modular y extensible**  
   - Módulos separados para carga de datos, ventanas, backends cuánticos, modelos y pipelines.  
   - Posibilidad de ampliar con nuevas características, backends o integraciones (SIEM, Wazuh, etc.).

---

## Requisitos

- Python 3.10 o superior.
- Dependencias principales:
  - `numpy`
  - `scapy`
  - `qiskit`
  - `qiskit-aer`

---

## Instalación

### Instalación desde PyPI (cuando el paquete esté publicado)

```bash
pip install qindus
