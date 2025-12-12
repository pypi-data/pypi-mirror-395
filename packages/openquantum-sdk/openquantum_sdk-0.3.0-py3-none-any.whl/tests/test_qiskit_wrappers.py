"""Tests for openquantum_sdk.qiskit wrapper functions."""
from __future__ import annotations

from unittest.mock import MagicMock


def test_list_backends_passes_name_filter():
    """Test that list_backends passes the name parameter to service.backends()."""
    mock_service = MagicMock()
    mock_service.backends.return_value = [{"id": "bk-1", "name": "Ankaa-3"}]

    from openquantum_sdk.qiskit import list_backends

    result = list_backends(service=mock_service, name="ankaa")

    mock_service.backends.assert_called_once_with(
        name="ankaa",
        online=None,
        device_type=None,
        vendor_id=None,
        min_num_qubits=None,
        limit=50,
    )
    assert result == [{"id": "bk-1", "name": "Ankaa-3"}]


def test_list_backends_passes_all_filters():
    """Test that list_backends passes all filter parameters correctly."""
    mock_service = MagicMock()
    mock_service.backends.return_value = []

    from openquantum_sdk.qiskit import list_backends

    list_backends(
        service=mock_service,
        name="test",
        online=True,
        device_type="QPU",
        vendor_id="vendor-123",
        min_num_qubits=10,
        limit=25,
    )

    mock_service.backends.assert_called_once_with(
        name="test",
        online=True,
        device_type="QPU",
        vendor_id="vendor-123",
        min_num_qubits=10,
        limit=25,
    )


def test_list_backends_name_none_by_default():
    """Test that name defaults to None when not provided."""
    mock_service = MagicMock()
    mock_service.backends.return_value = []

    from openquantum_sdk.qiskit import list_backends

    list_backends(service=mock_service)

    call_kwargs = mock_service.backends.call_args.kwargs
    assert call_kwargs["name"] is None


def test_list_backends_does_not_close_provided_service():
    """Test that list_backends doesn't close a service passed by the caller."""
    mock_service = MagicMock()
    mock_service.backends.return_value = []

    from openquantum_sdk.qiskit import list_backends

    list_backends(service=mock_service, name="test")

    mock_service.close.assert_not_called()
