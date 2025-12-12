import httpx

from opticlient.http import parse_api_response_json
from opticlient.models import job_summary_from_api, job_details_from_api


def test_parse_api_response_ok_and_job_summary():
    # Simulate a normal "create job" response
    resp = httpx.Response(
        status_code=201,
        json={
            "ok": True,
            "data": {
                "id": "123",
                "tool_code": "sms",
                "filename": "input.xlsx",
                "status": "pending",
                "created_at": "2025-01-01T12:00:00+00:00",
            },
            "error": None,
        },
    )

    data = parse_api_response_json(resp)
    summary = job_summary_from_api(data)

    assert summary.id == "123"
    assert summary.tool == "sms"
    assert summary.filename == "input.xlsx"
    assert summary.status == "pending"
    assert summary.created_at.startswith("2025-01-01")


def test_parse_api_response_ok_and_job_details():
    resp = httpx.Response(
        status_code=200,
        json={
            "ok": True,
            "data": {
                "id": "123",
                "tool_code": "sms",
                "filename": "input.xlsx",
                "status": "completed",
                "created_at": "2025-01-01T12:00:00+00:00",
                "error_message": None,
                "resultAvailable": True,
                "input_params": {"description": "test job"},
                "input_bytes": 100,
                "result_bytes": 2048,
                "started_at": "2025-01-01T12:00:01+00:00",
                "finished_at": "2025-01-01T12:00:10+00:00",
                "wall_time_seconds": 9.0,
                "cpu_time_seconds": 8.5,
                "max_memory_mb": 256.0,
            },
            "error": None,
        },
    )

    data = parse_api_response_json(resp)
    details = job_details_from_api(data)

    assert details.id == "123"
    assert details.tool == "sms"
    assert details.result_available is True
    assert details.input_params == {"description": "test job"}
    assert details.result_bytes == 2048
    assert details.wall_time_seconds == 9.0


def test_parse_api_response_error():
    resp = httpx.Response(
        status_code=400,
        json={
            "ok": False,
            "data": None,
            "error": {
                "code": "INVALID_TOKEN",
                "message": "Invalid API Token!",
            },
        },
    )

    try:
        parse_api_response_json(resp)
    except RuntimeError as exc:
        msg = str(exc)
        assert "status=400" in msg
        assert "INVALID_TOKEN" in msg
        assert "Invalid API Token!" in msg
    else:
        raise AssertionError("Expected RuntimeError for API error response")
