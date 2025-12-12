from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional

import httpx


DEFAULT_TIMEOUT_SECONDS = 30.0


class APIError(RuntimeError):
    def __init__(self, status_code: int, message: str, code: str | None = None) -> None:
        super().__init__(
            f"{code + ': ' if code else ''}{message} (status {status_code})"
        )
        self.status_code = status_code
        self.code = code
        self.message = message


@dataclass
class APIClient:
    base_url: str
    api_key: str | None = None
    token: str | None = None
    tenant_id: str | None = None

    def _build_headers(
        self, extra: Optional[Mapping[str, str]] = None
    ) -> Dict[str, str]:
        headers: Dict[str, str] = {
            "Accept": "application/json",
        }
        if self.api_key:
            headers["X-API-Key"] = self.api_key
        elif self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        if self.tenant_id:
            headers["X-Tenant-ID"] = self.tenant_id
            # Some endpoints (like ingest-service) expect lowercase "tenant" header
            # Send both for compatibility
            headers["tenant"] = self.tenant_id
        if extra:
            headers.update(extra)
        return headers

    def request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Mapping[str, Any]] = None,
        json_body: Any | None = None,
        headers: Optional[Mapping[str, str]] = None,
        timeout: float = DEFAULT_TIMEOUT_SECONDS,
    ) -> Any:
        url = self.base_url.rstrip("/") + path
        final_headers = self._build_headers(headers)

        with httpx.Client(timeout=timeout) as client:
            resp = client.request(
                method, url, params=params, json=json_body, headers=final_headers
            )

        if resp.status_code >= 400:
            try:
                data = resp.json()
            except json.JSONDecodeError:
                raise APIError(resp.status_code, resp.text or "API error")

            message = data.get("message") or resp.text or "API error"
            code = data.get("code")
            raise APIError(resp.status_code, message, code=code)

        if not resp.content:
            return None

        try:
            return resp.json()
        except json.JSONDecodeError:
            return resp.text

    def fetch_extraction_traces(
        self,
        *,
        tenant_id: Optional[str] = None,
        job_id: Optional[str] = None,
        checksum: Optional[str] = None,
        status: Optional[str] = None,
        field_name: Optional[str] = None,
        limit: int = 50,
    ) -> Any:
        params: Dict[str, Any] = {"limit": str(limit)}
        tenant = tenant_id or self.tenant_id
        if tenant:
            params["tenant_id"] = tenant
        if job_id:
            params["job_id"] = job_id
        if checksum:
            params["checksum"] = checksum
        if status:
            params["status"] = status
        if field_name:
            params["field_name"] = field_name
        return self.request("GET", "/api/v4/extractions/traces", params=params)
