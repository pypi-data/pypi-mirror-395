from __future__ import annotations

import httpx
from pathlib import Path

from opticlient.tools.sms import SingleMachineSchedulingClient


class FakeHttp:
    """
    Minimal HTTP fake used for tests.
    """
    def __init__(self, responses):
        self._responses = list(responses)
        self.calls = []

    def post(self, path, **kwargs):
        self.calls.append(("POST", path))
        return self._responses.pop(0)

    def get(self, path, **kwargs):
        self.calls.append(("GET", path))
        return self._responses.pop(0)


def make_zip_with_jobs_txt(tmp_path: Path) -> Path:
    """
    Create a ZIP with output/jobs.txt for testing.
    Each line is a job in the schedule.
    """
    zip_path = tmp_path / "result.zip"

    from zipfile import ZipFile

    with ZipFile(zip_path, "w") as z:
        z.writestr("output/jobs.txt", "job_a\njob_b\njob_c\n")

    return zip_path



def test_sms_run_end_to_end(tmp_path):
    """
    Submits → waits → downloads → parses schedule from ZIP bytes.
    Completely fakes backend HTTP responses.
    """
    # 1. Create fake Excel input file
    xlsx = tmp_path / "input.xlsx"
    xlsx.write_bytes(b"dummy")

    # 2. Mock responses

    # submit → JobSummary
    resp_submit = httpx.Response(
        status_code=201,
        json={
            "ok": True,
            "data": {
                "id": "job-42",
                "tool_code": "sms",
                "filename": "input.xlsx",
                "status": "pending",
                "created_at": "2025-01-01T00:00:00Z",
            },
            "error": None,
        },
    )

    # poll #1 → still pending
    resp_pending = httpx.Response(
        status_code=200,
        json={
            "ok": True,
            "data": {
                "id": "job-42",
                "tool_code": "sms",
                "filename": "input.xlsx",
                "status": "pending",
                "created_at": "2025-01-01T00:00:00Z",
                "resultAvailable": False,
                "error_message": None,
            },
            "error": None,
        },
    )

    # poll #2 → completed
    resp_completed = httpx.Response(
        status_code=200,
        json={
            "ok": True,
            "data": {
                "id": "job-42",
                "tool_code": "sms",
                "filename": "input.xlsx",
                "status": "completed",
                "created_at": "2025-01-01T00:00:00Z",
                "resultAvailable": True,
                "error_message": None,
            },
            "error": None,
        },
    )

    # download result.zip (with schedule lines)
    zip_path = make_zip_with_jobs_txt(tmp_path)
    resp_zip = httpx.Response(
        status_code=200,
        content=zip_path.read_bytes(),
        headers={"Content-Disposition": 'attachment; filename="job-42.zip"'},
    )

    fake_http = FakeHttp([
        resp_submit,
        resp_pending,
        resp_completed,
        resp_zip,
    ])

    # disable sleep
    import opticlient.tools.base as base_mod
    base_mod.time.sleep = lambda _: None

    client = SingleMachineSchedulingClient(fake_http)  # type: ignore[arg-type]

    schedule = client.run(
        file_path=xlsx,
        description="test-run",
        poll_interval=0.0,
        timeout=5.0,
    )

    assert schedule == ["job_a", "job_b", "job_c"]
