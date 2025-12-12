from __future__ import annotations

import time
from pathlib import Path
from typing import Optional

from ..http import HttpClient, parse_api_response_json
from ..models import (
    JobDetails,
    job_details_from_api,
)


class BaseJobClient:
    """
    Shared logic for job-based tools:
    - submit job with file
    - check job status
    - wait for completion
    - download result ZIP
    """

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def get_job(self, job_id: str) -> JobDetails:
        """
        Fetch detailed information for a job.
        """
        resp = self._http.get(f"/jobs/{job_id}")
        data = parse_api_response_json(resp)
        return job_details_from_api(data)

    def wait_for_completion(
        self,
        job_id: str,
        poll_interval: float = 2.0,
        timeout: Optional[float] = None,
    ) -> JobDetails:
        """
        Poll the job until it is completed or failed, or until the timeout is reached.
        """
        start = time.time()

        while True:
            details = self.get_job(job_id)

            if details.status == "completed":
                return details

            if details.status in {"failed", "error"}:
                raise RuntimeError(
                    f"Job {job_id} failed with status={details.status!r}, "
                    f"error={details.error_message!r}"
                )

            if timeout is not None and (time.time() - start) > timeout:
                raise RuntimeError(f"Timed out waiting for job {job_id}")

            time.sleep(poll_interval)

    def download_result_zip(
        self,
        job_id: str,
        output_dir: str | Path,
    ) -> Path:
        """
        Download the result ZIP for a completed job into output_dir.
        Returns the path to the saved ZIP file.
        """
        resp = self._http.get(f"/jobs/{job_id}/result")

        if resp.status_code != 200:
            snippet = resp.text[:200]
            raise RuntimeError(
                f"Failed to download result for job {job_id} "
                f"(status={resp.status_code}): {snippet!r}"
            )

        output_dir_path = Path(output_dir)
        output_dir_path.mkdir(parents=True, exist_ok=True)

        # Try to infer filename from Content-Disposition, otherwise default.
        content_disp = resp.headers.get("Content-Disposition", "")
        filename = f"{job_id}.zip"

        if "filename=" in content_disp:
            part = content_disp.split("filename=", 1)[1].strip()
            if part.startswith('"') or part.startswith("'"):
                part = part[1:-1]
            if part:
                filename = part

        zip_path = output_dir_path / filename
        zip_path.write_bytes(resp.content)
        return zip_path
