from datetime import datetime
from sqlalchemy import DateTime, Enum, ForeignKey, LargeBinary, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base
from app.models.enums import ApiProvider


class ApiKey(Base):
    __tablename__ = "api_keys"
    __table_args__ = (UniqueConstraint("owner_id", "provider", name="uq_api_key_owner_provider"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    provider: Mapped[ApiProvider] = mapped_column(Enum(ApiProvider))
    encrypted_key: Mapped[bytes] = mapped_column(LargeBinary)
    nonce: Mapped[bytes] = mapped_column(LargeBinary)
    key_hint: Mapped[str] = mapped_column(String(16))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    owner = relationship("User", back_populates="api_keys")
