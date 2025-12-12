# (C) Copyright IBM 2017, 2018.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.
#
# Copyright 2024 IonQ, Inc. (www.ionq.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Portions of this file (IonQ gate definitions and equivalences) are derived
# from qiskit-ionq: https://github.com/qiskit-community/qiskit-ionq

"""Build Qiskit Target from backend capabilities."""

from __future__ import annotations

from typing import Any, Dict, Iterable, Tuple


def build_target_from_capabilities(cap: Dict[str, Any]):
    """build Qiskit Target from a capabilities dict.

    Expects:
      - n_qubits: int
      - timing: { dt: float|None, durations: [{op, qubits, value_s}] }
      - native_ops: [{name, arity}]
      - topology: { directed_edges: bool, coupling_map: [[int,int], ...] }
      - noise: { gate_error: [{op, qubits, prob}] }
    """
    from qiskit.transpiler import Target, InstructionProperties
    from qiskit.circuit import Gate
    from qiskit.circuit.library import (
        XGate, YGate, ZGate, HGate, SXGate, SXdgGate, TGate, TdgGate, SGate, SdgGate,
        RXGate, RYGate, RZGate, PhaseGate,
        CXGate, CZGate, SwapGate, iSwapGate, ECRGate,
        CCXGate, CSwapGate, CPhaseGate, CYGate,
        RXXGate, RYYGate, RZZGate,
        Measure
    )

    n_qubits = int(cap.get("n_qubits", 0))
    dt = (cap.get("timing", {}) or {}).get("dt")
    target = Target(num_qubits=n_qubits, dt=dt)

    durations = {}
    for d in (cap.get("timing", {}) or {}).get("durations", []) or []:
        try:
            key = (str(d["op"]).lower(), tuple(int(q) for q in d["qubits"]))
            durations[key] = float(d["value_s"])
        except Exception:
            continue

    errors = {}
    for e in (cap.get("noise", {}) or {}).get("gate_error", []) or []:
        try:
            key = (str(e["op"]).lower(), tuple(int(q) for q in e["qubits"]))
            errors[key] = float(e["prob"])
        except Exception:
            continue

    def props_for(op_name: str, qs: Iterable[int]):
        key = (op_name.lower(), tuple(qs))
        dur_s = durations.get(key)
        dur_dt = (dur_s / dt) if (dur_s is not None and dt) else None
        err = errors.get(key)
        if dur_dt is None and err is None:
            return None
        return InstructionProperties(duration=dur_dt, error=err)

    directed = bool((cap.get("topology", {}) or {}).get("directed_edges", False))
    coupling = [tuple(map(int, pair)) for pair in ((cap.get("topology", {}) or {}).get("coupling_map", []) or [])]

    class PRXGate(Gate):
        """Phased RX gate: R(theta, phi)"""

        def __init__(self, theta, phi):
            super().__init__("prx", 1, [theta, phi])

        def _define(self):
            from qiskit.circuit.library import RZGate, RXGate
            from qiskit.circuit import QuantumCircuit
            qc = QuantumCircuit(1)
            qc.append(RZGate(self.params[1]), [0])
            qc.append(RXGate(self.params[0]), [0])
            qc.append(RZGate(-self.params[1]), [0])
            self.definition = qc

    class GPIGate(Gate):
        """IonQ GPI gate"""

        def __init__(self, phi):
            super().__init__("gpi", 1, [phi])

        def _define(self):
            import numpy as np
            from qiskit.circuit import QuantumCircuit

            phi = self.params[0]

            unitary = np.array([
                [0, np.exp(-1j * 2 * np.pi * phi)],
                [np.exp(1j * 2 * np.pi * phi), 0]
            ])

            qc = QuantumCircuit(1)
            qc.unitary(unitary, [0], label='gpi')
            self.definition = qc

    class GPI2Gate(Gate):
        """IonQ GPI2 gate."""

        def __init__(self, phi):
            super().__init__("gpi2", 1, [phi])

        def _define(self):
            import numpy as np
            from qiskit.circuit import QuantumCircuit

            phi = self.params[0]

            unitary = (1 / np.sqrt(2)) * np.array([
                [1, -1j * np.exp(-1j * 2 * np.pi * phi)],
                [-1j * np.exp(1j * 2 * np.pi * phi), 1]
            ])

            qc = QuantumCircuit(1)
            qc.unitary(unitary, [0], label='gpi2')
            self.definition = qc

    class MSGate(Gate):
        """IonQ Mølmer-Sørensen gate."""

        def __init__(self, phi0, phi1, theta=0.25):
            super().__init__("ms", 2, [phi0, phi1, theta])

        def _define(self):
            import numpy as np
            from qiskit.circuit import QuantumCircuit

            phi0, phi1, theta = self.params

            diag = np.cos(np.pi * theta)
            sin = np.sin(np.pi * theta)

            unitary = np.array([
                [diag, 0, 0, -1j * sin * np.exp(-1j * 2 * np.pi * (phi0 + phi1))],
                [0, diag, -1j * sin * np.exp(-1j * 2 * np.pi * (phi0 - phi1)), 0],
                [0, -1j * sin * np.exp(1j * 2 * np.pi * (phi0 - phi1)), diag, 0],
                [-1j * sin * np.exp(1j * 2 * np.pi * (phi0 + phi1)), 0, 0, diag],
            ])

            qc = QuantumCircuit(2)
            qc.unitary(unitary, [0, 1], label='ms')
            self.definition = qc

    from qiskit.circuit.equivalence_library import SessionEquivalenceLibrary as SELib
    from qiskit.circuit.library import (  # noqa: F811
        RGate, RXGate, RYGate, RZGate, HGate, CXGate, CZGate
    )
    from qiskit.circuit import QuantumCircuit, Parameter
    import numpy as np

    theta = Parameter("theta")
    phi = Parameter("phi")

    # PRX(θ,φ) = RZ(φ) · RX(θ) · RZ(-φ)
    qc_prx_equiv = QuantumCircuit(1)
    qc_prx_equiv.rz(phi, 0)
    qc_prx_equiv.rx(theta, 0)
    qc_prx_equiv.rz(-phi, 0)
    SELib.add_equivalence(PRXGate(theta, phi), qc_prx_equiv)

    # R(θ,φ) = PRX(θ,φ)
    qc_r = QuantumCircuit(1)
    qc_r.append(PRXGate(theta, phi), [0])
    SELib.add_equivalence(RGate(theta, phi), qc_r)

    # RX(θ) = PRX(θ,0)
    qc_rx = QuantumCircuit(1)
    qc_rx.append(PRXGate(theta, 0.0), [0])
    SELib.add_equivalence(RXGate(theta), qc_rx)

    # RY(θ) = PRX(θ,π/2)
    qc_ry = QuantumCircuit(1)
    qc_ry.append(PRXGate(theta, np.pi / 2), [0])
    SELib.add_equivalence(RYGate(theta), qc_ry)

    # IonQ GPI/GPI2/MS equivalences
    # Derived from qiskit-ionq (Copyright 2024 IonQ, Apache 2.0)
    # https://github.com/qiskit-community/qiskit-ionq
    from qiskit.circuit.library import UGate
    lam = Parameter("lam")

    # GPI(φ)
    qc_gpi_equiv = QuantumCircuit(1)
    qc_gpi_equiv.x(0)
    qc_gpi_equiv.rz(4 * np.pi * phi, 0)
    SELib.add_equivalence(GPIGate(phi), qc_gpi_equiv)

    # GPI2(φ)
    qc_gpi2_equiv = QuantumCircuit(1)
    qc_gpi2_equiv.rz(-2 * np.pi * phi, 0)
    qc_gpi2_equiv.rx(np.pi / 2, 0)
    qc_gpi2_equiv.rz(2 * np.pi * phi, 0)
    SELib.add_equivalence(GPI2Gate(phi), qc_gpi2_equiv)

    # U(θ,φ,λ)
    qc_u_equiv = QuantumCircuit(1)
    qc_u_equiv.append(GPI2Gate(1/2 - lam / (2 * np.pi)), [0])
    qc_u_equiv.append(GPIGate(theta / (4 * np.pi) + phi / (4 * np.pi) - lam / (4 * np.pi)), [0])
    qc_u_equiv.append(GPI2Gate(1/2 + phi / (2 * np.pi)), [0])
    SELib.add_equivalence(UGate(theta, phi, lam), qc_u_equiv)

    # CX
    qc_cx_equiv = QuantumCircuit(2)
    qc_cx_equiv.append(GPI2Gate(1/4), [0])
    qc_cx_equiv.append(MSGate(0, 0, 1/4), [0, 1])
    qc_cx_equiv.append(GPI2Gate(1/2), [0])
    qc_cx_equiv.append(GPI2Gate(1/2), [1])
    qc_cx_equiv.append(GPI2Gate(-1/4), [0])
    SELib.add_equivalence(CXGate(), qc_cx_equiv)

    _lib_map = {
        "x": lambda: XGate(),
        "y": lambda: YGate(),
        "z": lambda: ZGate(),
        "h": lambda: HGate(),
        "s": lambda: SGate(),
        "si": lambda: SdgGate(),
        "sdg": lambda: SdgGate(),
        "t": lambda: TGate(),
        "ti": lambda: TdgGate(),
        "tdg": lambda: TdgGate(),
        "v": lambda: SXGate(),
        "vi": lambda: SXdgGate(),
        "sx": lambda: SXGate(),
        "sxdg": lambda: SXdgGate(),

        "rx": lambda: RXGate(0.0),
        "ry": lambda: RYGate(0.0),
        "rz": lambda: RZGate(0.0),
        "phaseshift": lambda: PhaseGate(0.0),
        "p": lambda: PhaseGate(0.0),

        "cx": lambda: CXGate(),
        "cnot": lambda: CXGate(),
        "cz": lambda: CZGate(),
        "cy": lambda: CYGate(),
        "swap": lambda: SwapGate(),
        "iswap": lambda: iSwapGate(),
        "ecr": lambda: ECRGate(),
        "pswap": lambda: SwapGate(),

        "ccnot": lambda: CCXGate(),
        "ccx": lambda: CCXGate(),
        "cswap": lambda: CSwapGate(),
        "cphaseshift": lambda: CPhaseGate(0.0),
        "cp": lambda: CPhaseGate(0.0),

        "rxx": lambda: RXXGate(0.0),
        "xx": lambda: RXXGate(0.0),
        "ms": lambda: MSGate(0.0, 0.0),
        "ryy": lambda: RYYGate(0.0),
        "yy": lambda: RYYGate(0.0),
        "rzz": lambda: RZZGate(0.0),
        "zz": lambda: RZZGate(0.0),

        "measure": lambda: Measure(),
        "measure_ff": lambda: Measure(),

        # custom gates
        "prx": lambda: PRXGate(0.0, 0.0),
        "gpi": lambda: GPIGate(0.0),
        "gpi2": lambda: GPI2Gate(0.0),
    }

    all_ops = cap.get("native_ops", []) or []

    seen_ops = set()
    unique_ops = []
    for op in all_ops:
        name = str(op.get("name"))
        if name not in seen_ops:
            seen_ops.add(name)
            unique_ops.append(op)

    added_qiskit_names = set()

    for op in unique_ops:
        name = str(op.get("name"))
        arity = int(op.get("arity", 1))
        name_l = name.lower()

        try:
            if name_l in _lib_map:
                gate = _lib_map[name_l]()
            else:
                gate = Gate(name, arity, [])
        except Exception:
            gate = Gate(name, arity, [])

        if gate.name in added_qiskit_names:
            continue

        if arity == 1:
            mapping: Dict[Tuple[int], Any] = {}
            for q in range(n_qubits):
                ip = props_for(name, [q])
                mapping[(q,)] = ip
            if mapping:
                target.add_instruction(gate, mapping)
                added_qiskit_names.add(gate.name)
        elif arity == 2:
            mapping2: Dict[Tuple[int, int], Any] = {}
            for a, b in coupling:
                ip = props_for(name, [a, b])
                mapping2[(a, b)] = ip
                if not directed:
                    ip2 = props_for(name, [b, a])
                    mapping2[(b, a)] = ip2
            if mapping2:
                target.add_instruction(gate, mapping2)
                added_qiskit_names.add(gate.name)
    return target
