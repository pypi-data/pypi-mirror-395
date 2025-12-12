import pytest
from unittest.mock import MagicMock
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit.providers import BackendV2
from openquantum_sdk_qiskit.oq_backend import OpenQuantumBackend
from openquantum_sdk_qiskit import OQEstimator


def test_estimator_initialization():
    backend = MagicMock(spec=BackendV2)
    backend.name = "mock_backend"
    estimator = OQEstimator(backend=backend)
    assert estimator.backend == backend
    assert estimator.options is not None


def test_estimator_run_no_scheduler():
    backend = OpenQuantumBackend(name="Rigetti Ankaa-3")
    estimator = OQEstimator(backend=backend)
    qc = QuantumCircuit(1)
    qc.h(0)
    qc.measure_all()
    op = SparsePauliOp("Z")

    with pytest.raises(RuntimeError, match="Scheduler submission is required"):
        estimator.run([(qc, op)]).result()
