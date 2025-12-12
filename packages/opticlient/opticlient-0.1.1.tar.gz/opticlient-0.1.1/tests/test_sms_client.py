from __future__ import annotations

from typing import Any, Dict, List

import httpx

from opticlient.tools.sms import SingleMachineSchedulingClient
from opticlient.tools.base import BaseJobClient


class FakeHttp:
    """
    Minimal fake HttpClient-like object for testing.
    Returns prepared httpx.Response objects from a queue.
    """

    def __init__(self, responses: List[httpx.Response]) -> None:
        self._responses = responses
        self.calls: List[Dict[str, Any]] = []

    def post(self, path: str, **kwargs: Any) -> httpx.Response:
        self.calls.append({"method": "POST", "path": path, "kwargs": kwargs})
        return self._responses.pop(0)

    def get(self, path: str, **kwargs: Any) -> httpx.Response:
        self.calls.append({"method": "GET", "path": path, "kwargs": kwargs})
        return self._responses.pop(0)


def test_sms_submit_uses_correct_path_and_parses_job_summary(tmp_path):
    xlsx = tmp_path / "input.xlsx"
    xlsx.write_bytes(b"dummy")

    response = httpx.Response(
        status_code=201,
        json={
            "ok": True,
            "data": {
                "id": "job-123",
                "tool_code": "sms",
                "filename": "input.xlsx",
                "status": "pending",
                "created_at": "2025-01-01T00:00:00Z",
            },
            "error": None,
        },
    )

    fake_http = FakeHttp([response])
    client = SingleMachineSchedulingClient(fake_http)  # type: ignore[arg-type]

    summary = client.submit(file_path=xlsx, description="test")


    assert summary.id == "job-123"
    assert summary.tool == "sms"
    assert summary.status == "pending"

    assert fake_http.calls[0]["method"] == "POST"
    assert fake_http.calls[0]["path"] == "/jobs/tsp"


def test_base_job_client_wait_for_completion(monkeypatch):
    # First GET: job is pending
    resp_pending = httpx.Response(
        status_code=200,
        json={
            "ok": True,
            "data": {
                "id": "job-123",
                "tool_code": "sms",
                "filename": "input.xlsx",
                "status": "pending",
                "created_at": "2025-01-01T00:00:00Z",
                "error_message": None,
                "resultAvailable": False,
            },
            "error": None,
        },
    )

    # Second GET: job is completed
    resp_completed = httpx.Response(
        status_code=200,
        json={
            "ok": True,
            "data": {
                "id": "job-123",
                "tool_code": "sms",
                "filename": "input.xlsx",
                "status": "completed",
                "created_at": "2025-01-01T00:00:00Z",
                "error_message": None,
                "resultAvailable": True,
            },
            "error": None,
        },
    )

    fake_http = FakeHttp([resp_pending, resp_completed])
    base_client = BaseJobClient(fake_http)  # type: ignore[arg-type]

    # Avoid real sleeping
    monkeypatch.setattr("opticlient.tools.base.time.sleep", lambda _: None)

    details = base_client.wait_for_completion(
        job_id="job-123",
        poll_interval=0.0,
        timeout=5.0,
    )

    assert details.status == "completed"
    assert len(fake_http.calls) == 2
    assert all(call["method"] == "GET" for call in fake_http.calls)
    assert all(call["path"] == "/jobs/job-123" for call in fake_http.calls)


def test_sms_submit_rejects_non_excel(tmp_path):
    wrong = tmp_path / "input.txt"
    wrong.write_text("not excel")

    response = httpx.Response(
        status_code=201,
        json={
            "ok": True,
            "data": {
                "id": "job-123",
                "tool_code": "sms",
                "filename": "input.txt",
                "status": "pending",
                "created_at": "2025-01-01T00:00:00Z",
            },
            "error": None,
        },
    )

    fake_http = FakeHttp([response])
    client = SingleMachineSchedulingClient(fake_http)  # type: ignore[arg-type]

    try:
        client.submit(file_path=wrong, description="test")
    except ValueError as exc:
        msg = str(exc)
        assert "Expected an Excel file" in msg
    else:
        raise AssertionError("Expected ValueError for non-excel file")
