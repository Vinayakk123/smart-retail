from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from database import replace_transactions
from schemas import UploadResponse
from services.analytics import add_financial_metrics
from services.data_cleaning import clean_retail_data
from services.file_handler import (
    build_preview,
    cleanup_temp_file,
    read_uploaded_dataframe,
    save_upload_file,
)
from utils.helpers import standardize_input_columns

router = APIRouter(tags=["upload"])
TEMP_UPLOAD_DIR = Path(__file__).resolve().parent.parent / "tmp_uploads"


@router.post("/upload", response_model=UploadResponse, status_code=status.HTTP_200_OK)
async def upload_retail_data(file: UploadFile = File(...)) -> UploadResponse:
    temp_file_path: Path | None = None

    try:
        temp_file_path = await save_upload_file(file=file, destination_dir=TEMP_UPLOAD_DIR)
        raw_df = read_uploaded_dataframe(temp_file_path)
        standardized_df = standardize_input_columns(raw_df)
        cleaned_df, cleaning_summary = clean_retail_data(standardized_df)
        enriched_df = add_financial_metrics(cleaned_df)

        replace_transactions(enriched_df)

        return UploadResponse(
            preview=build_preview(enriched_df, limit=10),
            total_rows=int(cleaning_summary["input_rows"]),
            cleaned_rows=int(cleaning_summary["cleaned_rows"]),
            dropped_rows=int(cleaning_summary["dropped_rows"]),
            warnings=list(cleaning_summary.get("warnings", [])),
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Upload failed: {error}") from error
    finally:
        cleanup_temp_file(temp_file_path)
