from __future__ import annotations

from pathlib import Path
from uuid import uuid4

import pandas as pd
from fastapi import UploadFile

from utils.helpers import dataframe_to_records

SUPPORTED_EXTENSIONS = {".csv", ".xlsx", ".xls"}


async def save_upload_file(file: UploadFile, destination_dir: Path) -> Path:
    extension = Path(file.filename or "").suffix.lower()
    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError("Only CSV, XLS, and XLSX files are supported.")

    destination_dir.mkdir(parents=True, exist_ok=True)
    temp_file_path = destination_dir / f"{uuid4().hex}{extension}"

    file_content = await file.read()
    if not file_content:
        raise ValueError("Uploaded file is empty.")

    temp_file_path.write_bytes(file_content)
    return temp_file_path


def read_uploaded_dataframe(file_path: Path) -> pd.DataFrame:
    suffix = file_path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(file_path)
    return pd.read_excel(file_path)


def build_preview(df: pd.DataFrame, limit: int = 10) -> list[dict[str, object]]:
    return dataframe_to_records(df.head(limit))


def cleanup_temp_file(file_path: Path | None) -> None:
    if file_path and file_path.exists():
        file_path.unlink()
