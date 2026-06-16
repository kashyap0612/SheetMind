from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base


class QueryUsage(Base):
    __tablename__ = "query_usage"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    chat_session_id: Mapped[int | None] = mapped_column(ForeignKey("chat_sessions.id", ondelete="SET NULL"))
    provider: Mapped[str] = mapped_column(String(32))
    prompt_tokens: Mapped[int] = mapped_column(Integer, default=0)
    completion_tokens: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
