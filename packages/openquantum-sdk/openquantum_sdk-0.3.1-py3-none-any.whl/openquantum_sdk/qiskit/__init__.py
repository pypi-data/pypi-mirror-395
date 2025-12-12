"""
OpenQuantum SDK - Qiskit Integration
"""
import os
from typing import Any, Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from openquantum_sdk_qiskit import (
        OpenQuantumService,
        OQSampler,
        SamplerV2,
        OQEstimator,
        EstimatorV2,
    )

try:
    from openquantum_sdk.auth import ClientCredentials
except ImportError:
    ClientCredentials = None


def __getattr__(name):
    if name in {
        "OpenQuantumService",
        "OQSampler",
        "SamplerV2",
        "OQEstimator",
        "EstimatorV2",
    }:
        try:
            import openquantum_sdk_qiskit
        except ImportError as e:
            raise ImportError(
                "The 'openquantum-sdk-qiskit' plugin is required for this functionality.\n"
                "Please install it with: pip install \"openquantum-sdk[qiskit]\""
            ) from e

        if name == "OpenQuantumService":
            return openquantum_sdk_qiskit.OpenQuantumService
        elif name in {"OQSampler", "SamplerV2"}:
            return openquantum_sdk_qiskit.OQSampler
        elif name in {"OQEstimator", "EstimatorV2"}:
            return openquantum_sdk_qiskit.OQEstimator

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def list_backends(
    *,
    service: Optional["OpenQuantumService"] = None,
    name: Optional[str] = None,
    online: Optional[bool] = None,
    device_type: Optional[str] = None,
    vendor_id: Optional[str] = None,
    min_num_qubits: Optional[int] = None,
    limit: int = 50,
    **svc_kwargs: Any,
) -> List[Dict[str, Any]]:
    """
    List available backends with optional filtering.

    Args:
        service: Optional OpenQuantumService instance. If None, one is created.
        name: Filter by name or short_code.
        online: Filter for online backends.
        device_type: Filter by device type (e.g. "QPU", "SIMULATOR").
        vendor_id: Filter by vendor ID.
        min_num_qubits: Filter by minimum number of qubits.
        limit: Maximum number of results.
        **svc_kwargs: Arguments passed to OpenQuantumService constructor if service is None.
    """
    own = False
    if service is None:
        try:
            from openquantum_sdk_qiskit import OpenQuantumService
            service = OpenQuantumService(**svc_kwargs)
            own = True
        except ImportError as e:
            raise ImportError(
                "The 'openquantum-sdk-qiskit' plugin is required for this functionality.\n"
                "Please install it with: pip install \"openquantum-sdk[qiskit]\""
            ) from e

    try:
        return service.backends(
            name=name,
            online=online,
            device_type=device_type,
            vendor_id=vendor_id,
            min_num_qubits=min_num_qubits,
            limit=limit,
        )
    finally:
        if own and hasattr(service, "close"):
            service.close()


def get_backend(
    ref: str,
    *,
    service: Optional["OpenQuantumService"] = None,
    organization_id: Optional[str] = None,
    job_subcategory_id: Optional[str] = None,
    backend_class_id: Optional[str] = None,
    capabilities_source: Optional[str] = None,
    export_format: str = "qasm3",
    **svc_kwargs: Any,
):
    """
    Get a backend instance by name or ID.

    Args:
        ref: Name or ID of the backend.
        service: Optional OpenQuantumService instance.
        organization_id: Organization ID (overrides env var OQ_ORG_ID).
        job_subcategory_id: Job subcategory ID (overrides env var OQ_SUBCATEGORY_ID).
        backend_class_id: Backend class ID (defaults to ref).
        capabilities_source: URL or path to capabilities (overrides env var OQ_CAPS_URL).
        export_format: "qasm2" or "qasm3".
        **svc_kwargs: Arguments passed to OpenQuantumService constructor if service is None.
    """
    own = False
    if service is None:
        try:
            from openquantum_sdk_qiskit import OpenQuantumService
            service = OpenQuantumService(**svc_kwargs)
            own = True
        except ImportError as e:
            raise ImportError(
                "The 'openquantum-sdk-qiskit' plugin is required for this functionality.\n"
                "Please install it with: pip install \"openquantum-sdk[qiskit]\""
            ) from e

    try:
        organization_id = organization_id or os.getenv("OQ_ORG_ID")
        job_subcategory_id = job_subcategory_id or os.getenv("OQ_SUBCATEGORY_ID")
        capabilities_source = capabilities_source or os.getenv("OQ_CAPS_URL")

        config = {}
        if organization_id:
            config["organization_id"] = organization_id
        if backend_class_id or ref:
            config["backend_class_id"] = backend_class_id or ref
        if job_subcategory_id:
            config["job_subcategory_id"] = job_subcategory_id

        backend = service.return_backend(
            name=ref,
            capabilities_source=capabilities_source,
            config=config,
            export_format=export_format,
        )
        return backend
    finally:
        if own and hasattr(service, "close"):
            service.close()


__all__ = [
    "OpenQuantumService",
    "SamplerV2",
    "OQSampler",
    "EstimatorV2",
    "OQEstimator",
    "list_backends",
    "get_backend",
    "ClientCredentials",
]
