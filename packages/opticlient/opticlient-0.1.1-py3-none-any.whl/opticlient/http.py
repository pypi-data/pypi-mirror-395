from __future__ import annotations

from typing import Any, Dict, Optional

import httpx


class HttpClient:
    """
    Thin wrapper around httpx.Client that handles:
    - base URL
    - API key header (X-Api-Key)
    """

    def __init__(
        self,
        base_url: str,
        api_token: Optional[str] = None,
        timeout: float = 30.0,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_token = api_token
        self._client = httpx.Client(
            base_url=self.base_url,
            timeout=timeout,
        )

    def _auth_headers(self) -> Dict[str, str]:
        """
        Build authentication headers using X-Api-Key.
        """
        if not self.api_token:
            return {}
        return {
            "X-Api-Key": self.api_token,
            "Accept": "application/json",
        }

    def request(self, method: str, path: str, **kwargs: Any) -> httpx.Response:
        headers = kwargs.pop("headers", {})
        merged_headers = {**headers, **self._auth_headers()}

        response = self._client.request(
            method=method,
            url=path,
            headers=merged_headers,
            **kwargs,
        )
        return response

    def get(self, path: str, **kwargs: Any) -> httpx.Response:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> httpx.Response:
        return self.request("POST", path, **kwargs)

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "HttpClient":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()


def parse_api_response_json(response: httpx.Response) -> Any:
    """
    Parse the standard ApiResponse envelope used by the backend.

    Expected shape:
    {
        "ok": true/false,
        "data": ...,
        "error": {
            "code": "SOME_CODE",
            "message": "Human readable",
            "details": {...}  # optional
        }
    }

    On ok == True: returns the 'data' value.
    On ok == False or non-2xx status: raises RuntimeError with status, code, and message.
    """
    try:
        payload = response.json()
    except ValueError:
        raise RuntimeError(f"Unexpected non-JSON response (status={response.status_code})")

    if not isinstance(payload, dict):
        raise RuntimeError(f"Unexpected JSON structure (status={response.status_code})")

    ok = payload.get("ok")
    data = payload.get("data")
    error = payload.get("error") or {}

    # If HTTP status suggests error, treat it as error even if ok is True/missing
    if response.status_code < 200 or response.status_code >= 300:
        code = error.get("code")
        message = error.get("message") or "HTTP error from API"
        raise RuntimeError(
            f"API error (status={response.status_code}, code={code!r}): {message}"
        )

    if ok is True:
        return data

    # ok is False or missing but status is 2xx -> application-level error
    code = error.get("code")
    message = error.get("message") or "Unknown API error"
    raise RuntimeError(
        f"API error (status={response.status_code}, code={code!r}): {message}"
    )
