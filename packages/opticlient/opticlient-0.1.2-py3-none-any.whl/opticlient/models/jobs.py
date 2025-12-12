from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class JobSummary:
    """
    Lightweight view of a job as returned when a job is created
    or listed.
    """
    id: str
    tool: str
    filename: Optional[str]
    status: str
    created_at: str


@dataclass
class JobDetails:
    """
    Detailed view of a job, including execution metrics and
    whether a result is available.
    """
    id: str
    tool: str
    filename: Optional[str]
    status: str
    created_at: str

    error_message: Optional[str]
    result_available: bool

    input_params: Optional[Dict[str, Any]]
    input_bytes: Optional[int]
    result_bytes: Optional[int]

    started_at: Optional[str]
    finished_at: Optional[str]
    wall_time_seconds: Optional[float]
    cpu_time_seconds: Optional[float]
    max_memory_mb: Optional[float]


def job_summary_from_api(data: Dict[str, Any]) -> JobSummary:
    """
    Build a JobSummary from the backend JSON 'data' payload.

    We intentionally normalize some field names (e.g. tool_code -> tool).
    """
    return JobSummary(
        id=str(data.get("id", "")),
        tool=str(data.get("tool_code") or data.get("tool") or ""),
        filename=data.get("filename"),
        status=str(data.get("status", "")),
        created_at=str(data.get("created_at", "")),
    )


def job_details_from_api(data: Dict[str, Any]) -> JobDetails:
    """
    Build a JobDetails from the backend JSON 'data' payload.

    Handles the mixture of snake_case and camelCase used by the API.
    """
    return JobDetails(
        id=str(data.get("id", "")),
        tool=str(data.get("tool_code") or data.get("tool") or ""),
        filename=data.get("filename"),
        status=str(data.get("status", "")),
        created_at=str(data.get("created_at", "")),

        error_message=data.get("error_message"),
        result_available=bool(
            data.get("resultAvailable")
            if "resultAvailable" in data
            else data.get("result_available", False)
        ),

        input_params=data.get("input_params"),
        input_bytes=data.get("input_bytes"),
        result_bytes=data.get("result_bytes"),

        started_at=data.get("started_at"),
        finished_at=data.get("finished_at"),
        wall_time_seconds=data.get("wall_time_seconds"),
        cpu_time_seconds=data.get("cpu_time_seconds"),
        max_memory_mb=data.get("max_memory_mb"),
    )
