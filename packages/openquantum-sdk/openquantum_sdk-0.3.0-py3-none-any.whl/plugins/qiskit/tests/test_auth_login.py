from __future__ import annotations

from typing import Any, Dict  # noqa: F401

from openquantum_sdk.qiskit import OpenQuantumService
from openquantum_sdk.auth import ClientCredentials


def test_service_login_token_saves_and_active_account(tmp_path):
    path = tmp_path / "accounts.json"
    svc = OpenQuantumService.login(
        token="tok_abcdefgh123456",
        save=True,
        name="dev",
        filename=str(path),
        scheduler_url="https://scheduler.example.com",
        management_url="https://management.example.com",
    )
    assert svc.active_account["auth_mode"] == "token"

    saved = OpenQuantumService.saved_accounts(filename=str(path))
    assert "dev" in saved
    assert saved["dev"]["token"].endswith("…3456")


def test_client_credentials_auth_applies_header_and_caches(monkeypatch):
    calls: Dict[str, Any] = {"n": 0}

    class _Resp:
        status_code = 200

        def json(self):
            return {"access_token": "abc123", "expires_in": 300}

        def raise_for_status(self):
            return None

    def _fake_post(self, url, data=None, timeout=None, **kwargs):
        calls["n"] += 1
        return _Resp()

    import requests

    monkeypatch.setattr(requests.Session, "post", _fake_post, raising=False)

    svc = OpenQuantumService(
        creds=ClientCredentials(client_id="cid", client_secret="secret"),
        keycloak_base="https://id.example.com",
        realm="platform",
    )

    headers1 = svc.management._authorized_headers({})
    assert headers1.get("Authorization") == "Bearer abc123"
    assert calls["n"] == 1

    headers2 = svc.management._authorized_headers({})
    assert headers2.get("Authorization") == "Bearer abc123"
    assert calls["n"] == 1
