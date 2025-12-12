from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional, Dict, Any  # noqa: F401
from openquantum_sdk.qiskit import OpenQuantumService
from openquantum_sdk.models import (
    BackendClassRead,
    PaginatedBackendClasses,
    PaginationInfo,
)


@dataclass
class _Page:
    backend_classes: List[BackendClassRead]
    pagination: PaginationInfo


def _bk(idx: int, **kw) -> BackendClassRead:
    return BackendClassRead(
        id=f"bk-{idx}",
        name=f"Backend {idx}",
        description="",
        type=kw.get("type", "QPU"),
        provider_id=kw.get("provider_id", "prov-1"),
        short_code=kw.get("short_code", f"sc-{idx}"),
        queue_depth=kw.get("queue_depth", 0),
        accepting_jobs=kw.get("accepting_jobs", True),
        status=kw.get("status", "Online"),
    )


def test_service_backends_filters_and_pagination(monkeypatch):
    svc = OpenQuantumService()

    pages = [
        _Page(
            backend_classes=[_bk(1), _bk(2, type="SIMULATOR")],
            pagination=PaginationInfo(next_cursor="cursor-2"),
        ),
        _Page(
            backend_classes=[_bk(3, accepting_jobs=False, status="Offline"), _bk(4)],
            pagination=PaginationInfo(next_cursor=None),
        ),
    ]
    calls: Dict[str, Any] = {"i": 0}

    def _list_backend_classes(limit: int = 50, cursor: Optional[str] = None):
        i = calls["i"]
        calls["i"] = i + 1
        p = pages[i]
        return PaginatedBackendClasses(backend_classes=p.backend_classes, pagination=p.pagination)

    monkeypatch.setattr(svc.management, "list_backend_classes", _list_backend_classes)

    out = svc.backends(online=True, device_type="QPU")
    ids = {b["id"] for b in out}
    assert ids == {"bk-1", "bk-4"}


def test_service_account_save_load(tmp_path):
    path = tmp_path / "accounts.json"
    OpenQuantumService.save_account(
        name="dev",
        token="tok_abcdefgh123456",
        filename=str(path),
        scheduler_url="https://scheduler.example.com",
        management_url="https://management.example.com",
    )
    saved = OpenQuantumService.saved_accounts(filename=str(path))
    assert "dev" in saved
    assert saved["dev"]["token"].endswith("…3456")
    svc = OpenQuantumService.from_saved_account(name="dev", filename=str(path))
    assert svc.scheduler.base_url == "https://scheduler.example.com"
    assert svc.management.base_url == "https://management.example.com"
