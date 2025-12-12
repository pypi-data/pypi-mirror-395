from unittest.mock import MagicMock
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from openquantum_sdk_qiskit import SamplerV2


def test_sampler_parameter_binding():
    backend = MagicMock()
    scheduler = MagicMock()
    scheduler.download_job_output.return_value = {"0": 100}
    mock_job = MagicMock()
    scheduler.submit_job.return_value = mock_job

    config = {
        "organization_id": "org-1",
        "backend_class_id": "backend-1",
        "job_subcategory_id": "phys:hds"
    }

    sampler = SamplerV2(backend=backend, scheduler=scheduler, config=config)

    theta = Parameter('theta')
    qc = QuantumCircuit(1)
    qc.rx(theta, 0)
    qc.measure_all()

    # PUB with parameter value
    pub = (qc, [3.14], 100)

    job = sampler.run([pub])
    job.result()

    assert scheduler.submit_job.called

    call_args = scheduler.submit_job.call_args
    config = call_args[0][0]
    assert config.job_subcategory_id == "phys:hds"

    file_content = call_args[1]['file_content']
    qasm_str = file_content.decode('utf-8')
    assert "rx(3.14" in qasm_str


def test_sampler_no_params():
    backend = MagicMock()
    scheduler = MagicMock()
    scheduler.download_job_output.return_value = {"0": 100}
    scheduler.submit_job.return_value = MagicMock()

    config = {
        "organization_id": "org-1",
        "backend_class_id": "backend-1",
        "job_subcategory_id": "phys:hds"
    }

    sampler = SamplerV2(backend=backend, scheduler=scheduler, config=config)

    qc = QuantumCircuit(1)
    qc.x(0)
    qc.measure_all()

    pub = (qc, None, 100)
    job = sampler.run([pub])
    job.result()

    assert scheduler.submit_job.called
    call_args = scheduler.submit_job.call_args
    config = call_args[0][0]
    assert config.job_subcategory_id == "phys:hds"

    file_content = call_args[1]['file_content']
    qasm_str = file_content.decode('utf-8')
    assert "x q[0];" in qasm_str or "x q0;" in qasm_str
