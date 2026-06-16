from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base


class Sheet(Base):
    __tablename__ = "sheets"

    id: Mapped[int] = mapped_column(primary_key=True)
    file_id: Mapped[int] = mapped_column(ForeignKey("files.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(255))
    row_count: Mapped[int] = mapped_column(Integer)
    column_count: Mapped[int] = mapped_column(Integer)
    columns: Mapped[list[dict]] = mapped_column(JSON)
    sample_rows: Mapped[list[dict]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    file = relationship("UploadedFile", back_populates="sheets")
