from io import BytesIO
from pathlib import Path
import pandas as pd

ALLOWED_EXTENSIONS = {".csv", ".xlsx"}
ALLOWED_MIME_TYPES = {
    "text/csv",
    "application/csv",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
}


def validate_upload(filename: str, mime_type: str, size_bytes: int, max_mb: int) -> str:
    extension = Path(filename).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError("Only CSV and XLSX files are supported")
    if mime_type not in ALLOWED_MIME_TYPES:
        raise ValueError("Unsupported MIME type")
    if size_bytes > max_mb * 1024 * 1024:
        raise ValueError(f"File exceeds {max_mb} MB limit")
    return extension.removeprefix(".")


def _column_metadata(df: pd.DataFrame) -> list[dict]:
    metadata = []
    for column in df.columns:
        series = df[column]
        metadata.append(
            {
                "name": str(column),
                "dtype": str(series.dtype),
                "nullable": bool(series.isna().any()),
                "sample_values": series.dropna().head(5).astype(object).where(series.notna(), None).tolist(),
            }
        )
    return metadata


def parse_spreadsheet(filename: str, data: bytes) -> dict:
    extension = Path(filename).suffix.lower()
    if extension == ".csv":
        df = pd.read_csv(BytesIO(data))
        sheets = [("Sheet1", df)]
    elif extension == ".xlsx":
        workbook = pd.read_excel(BytesIO(data), sheet_name=None, engine="openpyxl")
        sheets = list(workbook.items())
    else:
        raise ValueError("Unsupported spreadsheet extension")
    sheet_payloads = []
    total_rows = 0
    max_columns = 0
    first_sample: list[dict] = []
    for name, df in sheets:
        df = df.rename(columns=lambda value: str(value).strip())
        total_rows += len(df)
        max_columns = max(max_columns, len(df.columns))
        sample = df.head(20).where(pd.notna(df), None).to_dict(orient="records")
        if not first_sample:
            first_sample = sample[:5]
        sheet_payloads.append(
            {
                "name": str(name),
                "row_count": int(len(df)),
                "column_count": int(len(df.columns)),
                "columns": _column_metadata(df),
                "sample_rows": sample[:10],
            }
        )
    return {"row_count": total_rows, "column_count": max_columns, "sample_rows": first_sample, "sheets": sheet_payloads}


def read_first_sheet(filename: str, data: bytes) -> pd.DataFrame:
    if filename.lower().endswith(".csv"):
        return pd.read_csv(BytesIO(data))
    workbook = pd.read_excel(BytesIO(data), sheet_name=None, engine="openpyxl")
    return next(iter(workbook.values()))
