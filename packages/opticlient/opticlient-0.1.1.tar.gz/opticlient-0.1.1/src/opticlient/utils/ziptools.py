from __future__ import annotations

import zipfile
from pathlib import Path
from typing import List


def extract_zip(zip_path: str | Path, dest_dir: str | Path) -> List[Path]:
    """
    Extract a ZIP file into dest_dir.
    Returns a list of extracted file paths.
    """
    zip_path = Path(zip_path)
    dest_dir = Path(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)

    extracted: List[Path] = []

    with zipfile.ZipFile(zip_path, "r") as z:
        for name in z.namelist():
            target = dest_dir / name
            if name.endswith("/"):  # folder
                target.mkdir(parents=True, exist_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                with target.open("wb") as f:
                    f.write(z.read(name))
                extracted.append(target)

    return extracted
