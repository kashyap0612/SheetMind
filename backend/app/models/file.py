from datetime import datetime
from sqlalchemy import DateTime, Enum, ForeignKey, Integer, JSON, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base
from app.models.enums import FileStatus


class UploadedFile(Base):
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    original_filename: Mapped[str] = mapped_column(String(255))
    storage_key: Mapped[str] = mapped_column(String(512), unique=True)
    mime_type: Mapped[str] = mapped_column(String(160))
    extension: Mapped[str] = mapped_column(String(16))
    size_bytes: Mapped[int] = mapped_column(Integer)
    status: Mapped[FileStatus] = mapped_column(Enum(FileStatus), default=FileStatus.uploading)
    row_count: Mapped[int | None] = mapped_column(Integer)
    column_count: Mapped[int | None] = mapped_column(Integer)
    sample_rows: Mapped[list | None] = mapped_column(JSON)
    error_message: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    owner = relationship("User", back_populates="files")
    sheets = relationship("Sheet", back_populates="file", cascade="all,delete")
