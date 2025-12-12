"""Pytest fixtures for SDK tests."""
import pytest
from unittest.mock import MagicMock
import requests_mock

from openquantum_sdk.clients import SchedulerClient, ManagementClient


@pytest.fixture
def mock_scheduler():
    """Mock SchedulerClient with requests_mock."""
    with requests_mock.Mocker() as m:
        m.post("https://scheduler.dev.quantumrings.com/v1/jobs/prepare", json={"id": "prep-123"})
        m.get("https://scheduler.dev.quantumrings.com/v1/jobs/prepare/prep-123", json={
            "status": "Completed",
            "quote": [{"execution_plan_id": "plan-1", "name": "Plan A", "price": 10.0, "queue_priorities": [{"queue_priority_id": "prio-1", "name": "Default", "price_increase": 0.0}]}]
        })
        m.post("https://scheduler.dev.quantumrings.com/v1/jobs", json={"id": "job-123", "status": "Created"})
        m.get("https://scheduler.dev.quantumrings.com/v1/jobs/job-123", json={"id": "job-123", "status": "Completed"})

        client = SchedulerClient(token="mock-token")
        client._request = MagicMock()
        yield client
        client.close()


@pytest.fixture
def mock_management():
    """Mock ManagementClient."""
    with requests_mock.Mocker() as m:
        m.get("https://management.dev.quantumrings.com/v1/users/organizations", json={
            "organizations": [{"id": "org-123", "name": "Test Org"}]
        })
        m.get("https://management.dev.quantumrings.com/v1/backend/classes", json={
            "backend_classes": [{"id": "backend-123", "name": "Test Backend", "type": "QPU", "queue_depth": 0, "status": "Online", "accepting_jobs": True}]
        })

        client = ManagementClient(token="mock-token")
        yield client
        client.close()
