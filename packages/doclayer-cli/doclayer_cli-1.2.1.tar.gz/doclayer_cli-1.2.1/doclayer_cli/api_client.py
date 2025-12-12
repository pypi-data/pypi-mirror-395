from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional

import httpx


DEFAULT_TIMEOUT_SECONDS = 30.0


class APIError(RuntimeError):
    """API error with user-friendly formatting."""
    
    def __init__(self, status_code: int, message: str, code: str | None = None) -> None:
        self.status_code = status_code
        self.code = code
        self.message = message
        super().__init__(self._format_message())
    
    def _format_message(self) -> str:
        """Format error message for display."""
        # For auth errors, provide a clear actionable message
        if self.status_code == 401 or self.code == "UNAUTHORIZED":
            return "Authentication required. Run 'doclayer auth login' or set DOCLAYER_API_KEY."
        if self.status_code == 403 or self.code == "FORBIDDEN":
            return "Access denied. Check your permissions or API key."
        if self.status_code == 404:
            return f"Not found: {self.message}"
        if self.status_code == 429:
            return "Rate limit exceeded. Please wait and try again."
        if self.status_code >= 500:
            return f"Server error ({self.status_code}). Please try again later."
        # Default: show the message without raw JSON
        return self.message
    
    def is_auth_error(self) -> bool:
        """Check if this is an authentication error."""
        return self.status_code == 401 or self.code == "UNAUTHORIZED"


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

            # Handle nested error structure: {"error": {"code": ..., "message": ...}}
            error_data = data.get("error", data)
            message = error_data.get("message") or data.get("message") or "API error"
            code = error_data.get("code") or data.get("code")
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
