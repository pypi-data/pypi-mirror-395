from __future__ import annotations
from typing import Any, Optional
import requests

class BaseClient:
    def __init__(self, *, base_url: str, license_key: str, session: Optional[requests.Session] = None, timeout: float = 10.0):
        if not license_key:
            raise ValueError("license_key is required")
        self.base_url = base_url.rstrip("/")
        self.license_key = license_key
        self.session = session or requests.Session()
        self.timeout = timeout

    def _request(self, *, path: str, params: dict[str, Any] | None = None) -> Any:
        params = dict(params or {})
        params["LicenseKey"] = self.license_key

        url = f"{self.base_url}/{path.lstrip('/')}"
        resp = self.session.get(url, params=params, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()