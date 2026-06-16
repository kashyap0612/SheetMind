from datetime import datetime
from pydantic import BaseModel
from app.models.enums import FileStatus


class ColumnMetadata(BaseModel):
    name: str
    dtype: str
    nullable: bool
    sample_values: list[str | int | float | bool | None]


class SheetMetadata(BaseModel):
    id: int
    name: str
    row_count: int
    column_count: int
    columns: list[ColumnMetadata]
    sample_rows: list[dict]

    model_config = {"from_attributes": True}


class FileResponse(BaseModel):
    id: int
    original_filename: str
    mime_type: str
    extension: str
    size_bytes: int
    status: FileStatus
    row_count: int | None
    column_count: int | None
    sample_rows: list | None
    created_at: datetime
    sheets: list[SheetMetadata] = []

    model_config = {"from_attributes": True}
