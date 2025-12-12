"""Unit tests for OpenQuantum SDK clients."""
from __future__ import annotations
from typing import Any, Dict, List
import pytest
import requests_mock
from dataclasses import dataclass
import requests

from openquantum_sdk.clients import (
    SchedulerClient,
    ManagementClient,
    JobSubmissionConfig,
)
from openquantum_sdk.enums import ExecutionPlanType, QueuePriorityType
from openquantum_sdk.models import (
    QuotePlan,
    QueuePriority,
    JobPreparationCreate,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture
def mock_scheduler():
    with requests_mock.Mocker() as m:
        m.post(
            "https://scheduler.openquantum.com/v1/jobs/prepare",
            json={"id": "prep-123"},
        )
        m.post(
            "https://scheduler.openquantum.com/v1/jobs",
            json={
                "id": "job-123",
                "status": "Running",
                "job_preparation_id": "prep-123",
                "execution_plan_id": "plan-1",
                "queue_priority_id": "prio-1",
                "input_data_url": "https://input.example.com/job-123",
                "output_data_url": None,
                "transaction_id": None,
                "submitted_at": "2025-04-05T12:00:00Z",
            },
        )
        m.get(
            "https://scheduler.openquantum.com/v1/jobs/job-123",
            json={
                "id": "job-123",
                "status": "Completed",
                "job_preparation_id": "prep-123",
                "execution_plan_id": "plan-1",
                "queue_priority_id": "prio-1",
                "input_data_url": "https://input.example.com/job-123",
                "output_data_url": "https://output.example.com/result-123",
                "transaction_id": "tx-789",
                "submitted_at": "2025-04-05T12:00:00Z",
            },
        )
        client = SchedulerClient()
        client.session.mocker = m
        client.management.session.mocker = m
        yield client


@pytest.fixture
def mock_management():
    with requests_mock.Mocker() as m:
        m.get(
            "https://management.openquantum.com/v1/users/organizations?limit=20",
            json={
                "organizations": [{"id": "org-123", "name": "Quantum Labs Inc."}],
                "pagination": {"next_cursor": None},
            },
        )
        m.get(
            "https://management.openquantum.com/v1/backends/classes?limit=20",
            json={
                "backend_classes": [
                    {
                        "id": "bc-123",
                        "name": "IonQ Harmony",
                        "description": "High-fidelity trapped-ion QPU",
                        "type": "QPU",
                        "provider_id": "prov-456",
                        "queue_depth": 5,
                        "accepting_jobs": True,
                        "status": "Online",
                    }
                ],
                "pagination": {"next_cursor": None},
            },
        )
        client = ManagementClient()
        client.session.mocker = m
        yield client


@pytest.fixture
def mock_management_with_providers():
    with requests_mock.Mocker() as m:
        m.get(
            "https://management.openquantum.com/v1/backends/providers?limit=20",
            json={
                "providers": [
                    {
                        "id": "prov-001",
                        "name": "IonQ",
                        "description": "Trapped-ion quantum computers",
                        "short_code": "ionq",
                    },
                    {
                        "id": "prov-002",
                        "name": "Rigetti",
                        "description": "Superconducting quantum processors",
                        "short_code": "rigetti",
                    },
                ],
                "pagination": {"next_cursor": None},
            },
        )
        client = ManagementClient()
        client.session.mocker = m
        yield client


# ---------------------------------------------------------------------------
# submit_job flow
# ---------------------------------------------------------------------------
@dataclass
class _JobStore:
    exec_id: str = ExecutionPlanType.PUBLIC.value
    prio_id: str = QueuePriorityType.STANDARD.value


def _create_job_callback(store: _JobStore):
    def cb(request, context):
        payload = request.json()
        store.exec_id = payload.get("execution_plan_id")
        store.prio_id = payload.get("queue_priority_id")
        context.status_code = 200
        return {
            "id": "job-999",
            "status": "Running",
            "job_preparation_id": payload.get("job_preparation_id"),
            "execution_plan_id": store.exec_id,
            "queue_priority_id": store.prio_id,
            "input_data_url": "https://input.example.com/job-999",
            "output_data_url": None,
            "transaction_id": None,
            "submitted_at": "2025-04-05T12:00:00Z",
        }
    return cb


def _poll_job_callback(store: _JobStore):
    def cb(request, context):
        return {
            "id": "job-999",
            "status": "Completed",
            "job_preparation_id": "prep-999",
            "execution_plan_id": store.exec_id,
            "queue_priority_id": store.prio_id,
            "input_data_url": "https://input.example.com/job-999",
            "output_data_url": "https://output.example.com/result-999",
            "transaction_id": "tx-999",
            "submitted_at": "2025-04-05T12:00:00Z",
        }
    return cb


@pytest.fixture
def mock_submit_flow():
    store = _JobStore()
    with requests_mock.Mocker() as m:
        m.post("https://scheduler.openquantum.com/v1/jobs/upload", json={"id": "upload-999", "url": "https://upload.example.com/put"})
        m.put(requests_mock.ANY, status_code=200)
        m.post("https://scheduler.openquantum.com/v1/jobs/prepare", json={"id": "prep-999"})
        m.get("https://scheduler.openquantum.com/v1/jobs/prepare/prep-999", json={})
        m.post("https://scheduler.openquantum.com/v1/jobs", json=_create_job_callback(store))
        m.get("https://scheduler.openquantum.com/v1/jobs/job-999", json=_poll_job_callback(store))

        client = SchedulerClient()
        client.session.mocker = m
        client.management.session.mocker = m
        client._store = store
        yield client


# ---------------------------------------------------------------------------
# Quote helpers
# ---------------------------------------------------------------------------
def make_priority(
    name: str,
    price_increase: int,
    queue_priority_id: str,
    description: str = "",
) -> QueuePriority:
    return QueuePriority(
        name=name,
        description=description or f"{name} description",
        price_increase=price_increase,
        queue_priority_id=queue_priority_id,
    )


def make_plan(
    name: str,
    price: int,
    execution_plan_id: str,
    priorities: List[QueuePriority],
    description: str = "",
) -> QuotePlan:
    return QuotePlan(
        name=name,
        price=price,
        description=description or f"{name} description",
        execution_plan_id=execution_plan_id,
        queue_priorities=priorities,
    )


def _preparation_result_obj(quote_plans: List[QuotePlan]) -> Dict[str, Any]:
    def plan_to_dict(plan: QuotePlan):
        return {
            "name": plan.name,
            "price": plan.price,
            "description": plan.description,
            "execution_plan_id": plan.execution_plan_id,
            "queue_priorities": [
                {
                    "name": qp.name,
                    "description": qp.description,
                    "price_increase": qp.price_increase,
                    "queue_priority_id": qp.queue_priority_id,
                }
                for qp in plan.queue_priorities
            ],
        }

    return {
        "status": "Completed",
        "message": None,
        "quote": [plan_to_dict(p) for p in quote_plans],
        "organization_id": "org-123",
        "backend_class_id": "bc-123",
        "name": "Test Job",
        "input_data_url": "https://input.example.com/prep-999",
        "job_category_id": "cat-001",
        "job_subcategory_id": "sub-001",
        "shots": 1024,
        "configuration_data": {},
    }


# ---------------------------------------------------------------------------
# ManagementClient Tests
# ---------------------------------------------------------------------------
def test_list_providers_basic(mock_management_with_providers):
    result = mock_management_with_providers.list_providers()
    assert len(result.providers) == 2
    assert result.providers[0].name == "IonQ"


def test_list_providers_pagination(mock_management_with_providers):
    mock_management_with_providers.session.mocker.get(
        "https://management.openquantum.com/v1/backends/providers?limit=1",
        json={
            "providers": [
                {"id": "prov-001", "name": "IonQ", "description": "test", "short_code": "ionq"}
            ],
            "pagination": {"next_cursor": "cursor-abc123"},
        },
    )
    result = mock_management_with_providers.list_providers(limit=1)
    assert result.pagination.next_cursor == "cursor-abc123"


def test_list_providers_with_cursor(mock_management_with_providers):
    mock_management_with_providers.session.mocker.get(
        "https://management.openquantum.com/v1/backends/providers?limit=1",
        json={
            "providers": [
                {"id": "prov-001", "name": "IonQ", "description": "test", "short_code": "ionq"}
            ],
            "pagination": {"next_cursor": "next-123"},
        },
    )
    mock_management_with_providers.session.mocker.get(
        "https://management.openquantum.com/v1/backends/providers?limit=1&cursor=next-123",
        json={
            "providers": [
                {"id": "prov-002", "name": "Rigetti", "description": "test", "short_code": "rigetti"}
            ],
            "pagination": {"next_cursor": None},
        },
    )
    page1 = mock_management_with_providers.list_providers(limit=1)
    page2 = mock_management_with_providers.list_providers(limit=1, cursor="next-123")
    assert page1.providers[0].id == "prov-001"
    assert page2.providers[0].id == "prov-002"


def test_list_backend_classes(mock_management):
    result = mock_management.list_backend_classes()
    assert len(result.backend_classes) == 1
    bc = result.backend_classes[0]
    assert bc.name == "IonQ Harmony"
    assert bc.type == "QPU"


def test_list_backend_classes_with_provider_filter(mock_management_with_providers):
    mock_management_with_providers.session.mocker.get(
        "https://management.openquantum.com/v1/backends/classes?limit=20&provider_id=prov-001",
        json={
            "backend_classes": [
                {
                    "id": "bc-ionq",
                    "name": "IonQ Aria",
                    "description": "test",
                    "type": "QPU",
                    "short_code": "ionq:aria-1",
                    "provider_id": "prov-001",
                }
            ],
            "pagination": {"next_cursor": None},
        },
    )
    result = mock_management_with_providers.list_backend_classes(provider_id="prov-001")
    assert result.backend_classes[0].short_code == "ionq:aria-1"


def test_list_user_organizations_pagination(mock_management):
    mock_management.session.mocker.get(
        "https://management.openquantum.com/v1/users/organizations?limit=1",
        json={
            "organizations": [{"id": "org-1", "name": "Org One"}],
            "pagination": {"next_cursor": "cursor-xyz"},
        },
    )
    result = mock_management.list_user_organizations(limit=1)
    assert result.pagination.next_cursor == "cursor-xyz"


# ---------------------------------------------------------------------------
# High-level submit_job tests (all pass unchanged)
# ---------------------------------------------------------------------------
def test_submit_job_free_auto_approve(mock_submit_flow):
    plan = make_plan(
        name="Public Plan",
        price=0,
        execution_plan_id=ExecutionPlanType.PUBLIC.value,
        priorities=[make_priority("Standard Queue", 0, QueuePriorityType.STANDARD.value)],
    )
    mock_submit_flow.session.mocker.get(
        "https://scheduler.openquantum.com/v1/jobs/prepare/prep-999",
        json=_preparation_result_obj([plan]),
    )
    cfg = JobSubmissionConfig(
        organization_id="org-123",
        backend_class_id="bc-123",
        name="Free Test",
        job_subcategory_id="sub-001",
        shots=1024,
        execution_plan="auto",
        queue_priority="auto",
        auto_approve_quote=False,
        verbose=False,
    )
    job = mock_submit_flow.submit_job(cfg, file_content=b"OPENQASM 2.0;")
    assert job.id == "job-999"


# ---------------------------------------------------------------------------
# download_job_output tests
# ---------------------------------------------------------------------------
def test_download_job_output_success(mock_scheduler):
    job = mock_scheduler.get_job("job-123")
    mock_scheduler.session.mocker.get(
        "https://output.example.com/result-123",
        text='{"histogram": {"00": 512, "11": 512}}',
    )
    output = mock_scheduler.download_job_output(job)
    assert output["histogram"]["00"] == 512


def test_download_job_output_no_url(mock_scheduler):
    mock_scheduler.session.mocker.get(
        "https://scheduler.openquantum.com/v1/jobs/job-123",
        json={
            "id": "job-123",
            "status": "Completed",
            "job_preparation_id": "prep-123",
            "execution_plan_id": "plan-1",
            "queue_priority_id": "prio-1",
            "input_data_url": "https://input.example.com/job-123",
            "output_data_url": None,  # ← critical
            "transaction_id": "tx-789",
            "submitted_at": "2025-04-05T12:00:00Z",
        },
    )
    job = mock_scheduler.get_job("job-123")
    with pytest.raises(RuntimeError, match=r"Job job-123 has no output_data_url"):
        mock_scheduler.download_job_output(job)


def test_download_job_output_non_json(mock_scheduler):
    job = mock_scheduler.get_job("job-123")
    mock_scheduler.session.mocker.get(
        "https://output.example.com/result-123",
        text="not json",
    )
    with pytest.raises(ValueError):
        mock_scheduler.download_job_output(job)


def test_download_job_output_http_error(mock_scheduler):
    job = mock_scheduler.get_job("job-123")
    mock_scheduler.session.mocker.get(
        "https://output.example.com/result-123",
        status_code=404,
        text="Not Found",
    )
    with pytest.raises(requests.HTTPError):
        mock_scheduler.download_job_output(job)


# ---------------------------------------------------------------------------
# Categories & Listing
# ---------------------------------------------------------------------------
def test_get_job_categories(mock_scheduler):
    mock_scheduler.session.mocker.get(
        "https://scheduler.openquantum.com/v1/jobs/categories?limit=20",
        json={
            "categories": [{"id": "cat-001", "name": "Finance", "short_code": "finance"}],
            "pagination": {"next_cursor": None},
        },
    )
    result = mock_scheduler.get_job_categories()
    assert result.categories[0].name == "Finance"


def test_get_job_subcategories(mock_scheduler):
    mock_scheduler.session.mocker.get(
        "https://scheduler.openquantum.com/v1/jobs/categories/cat-001/subcategories?limit=20",
        json={
            "categories": [{"id": "sub-001", "name": "Option Pricing"}],
            "pagination": {"next_cursor": None},
        },
    )
    result = mock_scheduler.get_job_subcategories("cat-001")
    assert result.categories[0].name == "Option Pricing"


def test_list_jobs(mock_scheduler):
    mock_scheduler.session.mocker.get(
        "https://scheduler.openquantum.com/v1/organizations/org-123/jobs?limit=20",
        json={
            "jobs": [{
                "id": "job-001",
                "backend_class_id": "bc-123",
                "name": "Test Job",
                "status": "Completed",
                "submitted_at": "2025-01-01T00:00:00Z",
            }],
            "pagination": {"next_cursor": None},
        },
    )
    result = mock_scheduler.list_jobs(organization_id="org-123")
    assert result.jobs[0].id == "job-001"


def test_list_jobs_with_status_filter(mock_scheduler):
    mock_scheduler.session.mocker.get(
        "https://scheduler.openquantum.com/v1/organizations/org-123/jobs?limit=20&status=running",  # <-- lowercase!
        json={"jobs": [], "pagination": {"next_cursor": None}},
    )
    mock_scheduler.list_jobs(organization_id="org-123", status="Running")
    assert mock_scheduler.session.mocker.last_request.query == "limit=20&status=running"  # <-- matches reality


def test_list_jobs_no_org_id(mock_scheduler):
    # Mock the management client call that _resolve_organization_id will make
    mock_scheduler.management.session.mocker.get(
        "https://management.openquantum.com/v1/users/organizations?limit=1",
        json={
            "organizations": [{"id": "org-auto-resolved", "name": "Auto-Resolved Org"}],
            "pagination": {"next_cursor": None},
        },
    )
    mock_scheduler.session.mocker.get(
        "https://scheduler.openquantum.com/v1/organizations/org-auto-resolved/jobs?limit=20",
        json={
            "jobs": [{"id": "job-resolved", "backend_class_id": "bc-123", "name": "Resolved Job", "status": "Completed"}],
            "pagination": {"next_cursor": None},
        },
    )

    # Call list_jobs without organization_id
    result = mock_scheduler.list_jobs()

    assert len(result.jobs) == 1
    assert result.jobs[0].id == "job-resolved"


# ---------------------------------------------------------------------------
# upload + prepare
# ---------------------------------------------------------------------------
def test_upload_job_input_file_path(tmp_path):
    file = tmp_path / "circuit.qasm"
    file.write_bytes(b"OPENQASM 2.0;")
    with requests_mock.Mocker() as m:
        m.post("https://scheduler.openquantum.com/v1/jobs/upload", json={"id": "up-123", "url": "https://upload.example.com/put"})
        m.put("https://upload.example.com/put", status_code=200)
        client = SchedulerClient()
        client.session.mocker = m
        upload_id = client.upload_job_input(file_path=str(file))
        assert upload_id == "up-123"


def test_prepare_job_and_get_result(mock_scheduler):
    mock_scheduler.session.mocker.post(
        "https://scheduler.openquantum.com/v1/jobs/prepare",
        json={"id": "prep-direct"},
    )
    mock_scheduler.session.mocker.get(
        "https://scheduler.openquantum.com/v1/jobs/prepare/prep-direct",
        json=_preparation_result_obj([
            make_plan("Test Plan", 0, "plan-test", [make_priority("Std", 0, "prio-std")])
        ]),
    )
    prep = JobPreparationCreate(
        organization_id="org-123",
        backend_class_id="bc-123",
        name="Direct Prep",
        upload_endpoint_id="up-123",
        job_subcategory_id="sub-001",
        shots=100,
    )
    resp = mock_scheduler.prepare_job(prep)
    assert resp.id == "prep-direct"
    result = mock_scheduler.get_preparation_result("prep-direct")
    assert result.status == "Completed"


def test_submit_job_no_org_id(mock_submit_flow):
    # Mock the management client call that _resolve_organization_id will make
    mock_submit_flow.management.session.mocker.get(
        "https://management.openquantum.com/v1/users/organizations?limit=1",
        json={
            "organizations": [{"id": "org-auto-resolved", "name": "Auto-Resolved Org"}],
            "pagination": {"next_cursor": None},
        },
    )
    plan = make_plan("Free Plan", 0, ExecutionPlanType.PUBLIC.value, [make_priority("Std", 0, QueuePriorityType.STANDARD.value)])
    mock_submit_flow.session.mocker.get(
        "https://scheduler.openquantum.com/v1/jobs/prepare/prep-999",
        json=_preparation_result_obj([plan]),
    )
    cfg = JobSubmissionConfig(
        organization_id=None,  # Explicitly None
        backend_class_id="bc-123",
        name="No Org ID Test",
        job_subcategory_id="sub-001",
        shots=1,
        verbose=False,
    )
    job = mock_submit_flow.submit_job(cfg, file_content=b"test")
    assert job.id == "job-999"
