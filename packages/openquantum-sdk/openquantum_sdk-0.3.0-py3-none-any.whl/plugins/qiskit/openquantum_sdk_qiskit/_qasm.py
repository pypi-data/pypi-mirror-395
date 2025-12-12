from __future__ import annotations

from typing import Any


def export_circuit_to_qasm(circuit: Any, fmt: str) -> bytes:
    f = (fmt or "qasm3").lower()
    if f == "qasm3":
        try:
            import qiskit.qasm3 as qasm3
        except Exception as e:
            raise RuntimeError(
                "Qiskit qasm3 exporter is required. Install: pip install 'openquantum-sdk[qiskit]'"
            ) from e
        qasm = qasm3.dumps(circuit)
        return qasm.encode("utf-8")
    if f == "qasm2":
        try:
            from qiskit import qasm2

            qasm = qasm2.dumps(circuit)
            return qasm.encode("utf-8")
        except Exception:
            try:
                qasm = circuit.qasm()
                return qasm.encode("utf-8")
            except Exception as e:
                raise RuntimeError("Failed to export circuit to OpenQASM 2.") from e
    raise ValueError("export_format must be 'qasm2' or 'qasm3'")
