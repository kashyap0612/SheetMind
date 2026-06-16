from sqlalchemy.orm import Session
from app.models.file import UploadedFile


class FileRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_owned(self, file_id: int, owner_id: int) -> UploadedFile | None:
        return self.db.query(UploadedFile).filter(UploadedFile.id == file_id, UploadedFile.owner_id == owner_id).one_or_none()

    def list_owned(self, owner_id: int, search: str | None = None) -> list[UploadedFile]:
        query = self.db.query(UploadedFile).filter(UploadedFile.owner_id == owner_id)
        if search:
            query = query.filter(UploadedFile.original_filename.ilike(f"%{search}%"))
        return query.order_by(UploadedFile.created_at.desc()).all()
