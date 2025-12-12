from __future__ import annotations

from io import BytesIO
from typing import List
import zipfile


def parse_sms_schedule_from_zip_bytes(zip_bytes: bytes) -> List[str]:
    """
    Read output/jobs.txt from the given ZIP bytes and interpret each
    non-empty, non-comment line as one job in the schedule, in order.

    Returns:
        List of job identifiers as strings.
    """
    try:
        with zipfile.ZipFile(BytesIO(zip_bytes)) as z:
            try:
                with z.open("output/jobs.txt") as f:
                    text = f.read().decode("utf-8")
            except KeyError:
                raise RuntimeError("Missing expected file 'output/jobs.txt' in result ZIP")
    except zipfile.BadZipFile:
        raise RuntimeError("Result is not a valid ZIP file")

    schedule: List[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        schedule.append(stripped)

    return schedule
