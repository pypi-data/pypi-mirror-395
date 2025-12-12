from __future__ import annotations
import threading
import time
from dataclasses import dataclass
from typing import Optional, Dict
import requests
from urllib.parse import urljoin


@dataclass
class ClientCredentials:
    client_id: str
    client_secret: str


class ClientCredentialsAuth:
    """
    Keycloak client-credentials OAuth2 helper with local, thread-safe token cache.
    - Fetches token from: {keycloak_base}/realms/{realm}/protocol/openid-connect/token
    - Auto refreshes when within leeway of expiry
    - Retries once on 401
    """
    def __init__(
        self,
        creds: ClientCredentials,
        keycloak_base: str = "https://id.openquantum.com",
        realm: str = "platform",
        scope: Optional[str] = None,
        leeway_seconds: int = 30,
        session: Optional[requests.Session] = None,
    ):
        self.keycloak_base = keycloak_base.rstrip("/")
        self.realm = realm
        self.creds = creds
        self.scope = scope
        self.leeway = max(leeway_seconds, 0)
        self._session = session or requests.Session()
        self._lock = threading.Lock()
        self._access_token: Optional[str] = None
        self._expires_at: float = 0.0

    @property
    def token_endpoint(self) -> str:
        return urljoin(
            self.keycloak_base + "/",
            f"realms/{self.realm}/protocol/openid-connect/token",
        )

    def _needs_refresh(self) -> bool:
        # refresh if no token or we're within leeway of expiry
        return not self._access_token or (time.time() + self.leeway) >= self._expires_at

    def _fetch_token(self) -> None:
        data = {
            "grant_type": "client_credentials",
            "client_id": self.creds.client_id,
            "client_secret": self.creds.client_secret,
        }
        if self.scope:
            data["scope"] = self.scope

        resp = self._session.post(self.token_endpoint, data=data, timeout=20)
        resp.raise_for_status()
        payload: Dict = resp.json()
        access_token = payload.get("access_token")
        expires_in = payload.get("expires_in", 300)

        if not access_token:
            raise RuntimeError("Keycloak token response missing access_token")

        self._access_token = access_token
        self._expires_at = time.time() + int(expires_in)

    def get_access_token(self, force: bool = False) -> str:
        if force or self._needs_refresh():
            with self._lock:
                if force or self._needs_refresh():
                    self._fetch_token()
        return self._access_token  # type: ignore[str-bytes-safe]

    def apply_auth_header(self, headers: Dict[str, str]) -> Dict[str, str]:
        token = self.get_access_token()
        # don't mutate caller's header dict
        return {**headers, "Authorization": f"Bearer {token}"}
