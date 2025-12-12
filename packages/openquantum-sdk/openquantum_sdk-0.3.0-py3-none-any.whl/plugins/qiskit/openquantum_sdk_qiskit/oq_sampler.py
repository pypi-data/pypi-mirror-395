from __future__ import annotations

from typing import Iterable, Optional, List, Dict, Any

from qiskit.primitives import (
    BaseSamplerV2,
    SamplerPubLike,
    PrimitiveResult,
    SamplerPubResult,
)
from qiskit.primitives.primitive_job import PrimitiveJob
from qiskit.providers import BackendV2
from qiskit.primitives.containers import DataBin, BitArray
from qiskit.primitives.containers.sampler_pub import SamplerPub
from ._qasm import export_circuit_to_qasm

from openquantum_sdk.clients import SchedulerClient, JobSubmissionConfig


class OQSampler(BaseSamplerV2):
    """OpenQuantum Sampler.

    This implementation submits pubs via the platform's scheduler and
    returns results using Qiskit's primitives containers (DataBin,
    SamplerPubResult, PrimitiveResult).
    """

    def __init__(
        self,
        *,
        backend: BackendV2,
        options: Optional[dict] = None,
        scheduler: Optional[SchedulerClient] = None,
        config: Optional[Dict[str, Any]] = None,
        export_format: str = "qasm3",
    ):
        self._backend = backend
        self._options = options or {}
        self._scheduler = scheduler
        self._config = config or {}
        fmt = (export_format or "qasm3").lower()
        if fmt not in {"qasm2", "qasm3"}:
            raise ValueError("export_format must be 'qasm2' or 'qasm3'")
        self._export_format = fmt

    @property
    def backend(self) -> BackendV2:
        return self._backend

    @property
    def options(self):
        return self._options

    def run(self,
            pubs: Iterable[SamplerPubLike],
            *,
            shots: int | None = None,
            export_format: Optional[str] = None,
            ) -> PrimitiveJob[PrimitiveResult[SamplerPubResult]]:
        """Execute sampler pubs and return a Qiskit PrimitiveJob."""
        if shots is None:
            shots = 100

        coerced_pubs = [SamplerPub.coerce(pub, shots) for pub in pubs]

        if not self._scheduler:
            raise RuntimeError(
                "Scheduler submission is required: provide scheduler and config when constructing OQSampler."
            )

        required = ("backend_class_id", "job_subcategory_id")
        missing = [k for k in required if not self._config.get(k)]
        if missing:
            raise ValueError(f"Missing config keys: {', '.join(missing)}")

        fmt = (export_format or self._export_format).lower()
        if fmt not in {"qasm2", "qasm3"}:
            raise ValueError("export_format must be 'qasm2' or 'qasm3'")

        def _job_fn(bound_pubs: List[SamplerPub]) -> PrimitiveResult[SamplerPubResult]:
            return self._run_via_scheduler(bound_pubs, export_fmt=fmt)

        job: PrimitiveJob[PrimitiveResult[SamplerPubResult]]
        job = PrimitiveJob(_job_fn, coerced_pubs)
        job.metadata["export_format"] = fmt
        job._submit()
        return job

    def _run_via_scheduler(self, pubs: List[SamplerPub], *, export_fmt: str) -> PrimitiveResult[SamplerPubResult]:
        """Submit pubs via scheduler and adapt results to Qiskit containers."""
        sub_id = str(self._config["job_subcategory_id"])

        pub_results: List[SamplerPubResult] = []
        for idx, pub in enumerate(pubs):
            circuit = pub.circuit
            pub_shots = pub.shots
            all_samples: List[str] = []

            flat_bindings = pub.parameter_values.ravel()

            for i in range(flat_bindings.size):
                binds = {}
                for params_tuple, val_array in flat_bindings.data.items():
                    values = val_array[i]
                    for param_name, param_val in zip(params_tuple, values):
                        binds[param_name] = param_val

                bound_circuit = circuit
                if binds:
                    bound_circuit = circuit.assign_parameters(binds)

                qasm_bytes = export_circuit_to_qasm(bound_circuit, export_fmt)

                job_config = JobSubmissionConfig(
                    organization_id=self._config.get("organization_id"),
                    backend_class_id=self._config["backend_class_id"],
                    name=self._config.get("name", f"OQ Sampler Pub {idx} Sample {i}"),
                    job_subcategory_id=sub_id,
                    shots=pub_shots,
                    configuration_data=self._config.get("configuration_data", {}),
                )

                job = self._scheduler.submit_job(job_config, file_content=qasm_bytes)
                counts: Dict[str, int] = self._scheduler.download_job_output(job)
                samples = self._counts_to_samples(counts)
                if len(samples) != pub_shots:
                    if len(samples) < pub_shots:
                        samples.extend(["0" * bound_circuit.num_clbits] * (pub_shots - len(samples)))
                    else:
                        samples = samples[:pub_shots]

                all_samples.extend(samples)

            num_bits = circuit.num_clbits if circuit.num_clbits > 0 else max(len(s) for s in all_samples)
            ba = BitArray.from_samples(all_samples, num_bits)
            expected_shape = pub.parameter_values.shape + (pub_shots,)
            ba = ba.reshape(expected_shape)

            meas_container = DataBin(m=ba, shape=pub.parameter_values.shape)
            pub_results.append(
                SamplerPubResult(
                    meas_container,
                    metadata={
                        "shots": pub_shots,
                        "circuit_metadata": getattr(circuit, "metadata", None),
                    },
                )
            )

        return PrimitiveResult(pub_results, metadata={"version": 2})

    def _counts_to_samples(self, counts: Dict[str, int]) -> List[str]:
        samples: List[str] = []
        for bitstr, c in counts.items():
            samples.extend([bitstr] * int(c))
        return samples
