from __future__ import annotations

from pathlib import Path
from typing import Optional, List

from ..http import HttpClient, parse_api_response_json
from ..models import JobSummary, JobDetails, job_summary_from_api
from .base import BaseJobClient
from .sms_parser import parse_sms_schedule_from_zip_bytes


class SingleMachineSchedulingClient(BaseJobClient):
    """
    Client for the single-machine scheduling tool (sms).
    """

    _SUBMIT_PATH = '/jobs/tsp'
    
    def __init__(self, http: HttpClient) -> None:
        super().__init__(http=http)

    def submit(
        self,
        file_path: str | Path,
        description: Optional[str] = None,
    ) -> JobSummary:
        """
        Submit an sms job.

        Validates that the file exists and looks like an Excel file.
        Later we can add content validation here.
        """
        path = Path(file_path)

        if not path.is_file():
            raise ValueError(f"Input file does not exist: {path}")

        # Basic extension-level validation for Excel files.
        # Extend this list if you support more formats.
        allowed_ext = {".xls", ".xlsx"}
        if path.suffix.lower() not in allowed_ext:
            raise ValueError(
                f"Expected an Excel file with one of extensions {sorted(allowed_ext)}, "
                f"got {path.suffix!r}"
            )

        fields = {}
        if description is not None:
            fields["description"] = description

        # Placeholder for future content validation of the Excel file

        with path.open("rb") as f:
            files = {
                "file": (path.name, f, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
            }
            resp = self._http.post(
                self._SUBMIT_PATH,
                files=files,
                data=fields,
            )

        data = parse_api_response_json(resp)
        return job_summary_from_api(data)

    def get(self, job_id: str) -> JobDetails:
        """
        Get sms job details.
        """
        return self.get_job(job_id)

    def wait(
        self,
        job_id: str,
        poll_interval: float = 2.0,
        timeout: Optional[float] = None,
    ) -> JobDetails:
        """
        Wait for an sms job to complete.
        """
        return self.wait_for_completion(
            job_id=job_id,
            poll_interval=poll_interval,
            timeout=timeout,
        )
        
    def run(
        self,
        file_path: str | Path,
        description: Optional[str] = None,
        poll_interval: float = 2.0,
        timeout: Optional[float] = None,
    ) -> List[str]:
        """
        High-level convenience method for SMS:

        1. validate + submit job
        2. wait for completion
        3. download result ZIP (in memory)
        4. parse output/jobs.txt as a sequence of jobs

        Returns:
            List[str]: schedule of jobs in execution order.
        """
        summary = self.submit(file_path=file_path, description=description)
        job_id = summary.id

        # Ensure the job is completed (or error) before fetching results.
        self.wait(
            job_id=job_id,
            poll_interval=poll_interval,
            timeout=timeout,
        )

        # Download ZIP into memory only.
        resp = self._http.get(f"/jobs/{job_id}/result")
        if resp.status_code != 200:
            snippet = resp.text[:200]
            raise RuntimeError(
                f"Failed to download result for job {job_id} "
                f"(status={resp.status_code}): {snippet!r}"
            )

        zip_bytes = resp.content

        # Parse schedule from ZIP bytes.
        schedule = parse_sms_schedule_from_zip_bytes(zip_bytes)
        return schedule

