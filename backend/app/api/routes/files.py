from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from sqlalchemy.orm import Session
from app.core.auth import get_current_user
from app.core.config import get_settings
from app.db.session import get_db
from app.models.enums import FileStatus
from app.models.file import UploadedFile
from app.models.sheet import Sheet
from app.models.user import User
from app.repositories.files import FileRepository
from app.schemas.file import FileResponse
from app.services.spreadsheet import parse_spreadsheet, validate_upload
from app.services.storage import R2StorageService

router = APIRouter(prefix="/files", tags=["files"])


@router.get("", response_model=list[FileResponse])
def list_files(search: str | None = Query(default=None), user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return FileRepository(db).list_owned(user.id, search)


@router.post("", response_model=FileResponse, status_code=201)
async def upload_file(upload: UploadFile = File(...), user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    data = await upload.read()
    try:
        extension = validate_upload(upload.filename or "", upload.content_type or "", len(data), get_settings().max_upload_mb)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc
    storage_key = R2StorageService().put(user.id, upload.filename or "spreadsheet", data, upload.content_type or "application/octet-stream")
    record = UploadedFile(owner_id=user.id, original_filename=upload.filename or "spreadsheet", storage_key=storage_key, mime_type=upload.content_type or "", extension=extension, size_bytes=len(data), status=FileStatus.uploading)
    db.add(record)
    db.commit()
    db.refresh(record)
    try:
        metadata = parse_spreadsheet(record.original_filename, data)
        record.row_count = metadata["row_count"]
        record.column_count = metadata["column_count"]
        record.sample_rows = metadata["sample_rows"]
        record.status = FileStatus.ready
        for sheet in metadata["sheets"]:
            db.add(Sheet(file_id=record.id, **sheet))
        db.commit()
        db.refresh(record)
    except Exception as exc:  # noqa: BLE001 - persisted for user-visible processing diagnostics
        record.status = FileStatus.failed
        record.error_message = str(exc)
        db.commit()
        raise HTTPException(status_code=500, detail="File uploaded but parsing failed") from exc
    return record


@router.get("/{file_id}", response_model=FileResponse)
def get_file(file_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    record = FileRepository(db).get_owned(file_id, user.id)
    if record is None:
        raise HTTPException(status_code=404, detail="File not found")
    return record
