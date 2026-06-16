import httpx
from sqlalchemy.orm import Session
from app.models.api_key import ApiKey
from app.models.enums import ApiProvider
from app.models.user import User
from app.schemas.api_key import ApiKeyUpsert
from app.utils.crypto import encrypt_secret, key_hint


class ApiKeyService:
    def __init__(self, db: Session) -> None:
        self.db = db

    async def validate(self, provider: ApiProvider, api_key: str) -> None:
        if provider == ApiProvider.openai and not api_key.startswith("sk-"):
            raise ValueError("OpenAI keys should start with sk-")
        if provider == ApiProvider.anthropic and not api_key.startswith("sk-ant-"):
            raise ValueError("Anthropic keys should start with sk-ant-")
        if provider == ApiProvider.gemini and len(api_key) < 20:
            raise ValueError("Gemini API key is too short")
        # Keep validation lightweight for local MVP; production can enable provider health probes.

    async def upsert(self, user: User, payload: ApiKeyUpsert) -> ApiKey:
        await self.validate(payload.provider, payload.api_key)
        encrypted, nonce = encrypt_secret(payload.api_key)
        record = self.db.query(ApiKey).filter(ApiKey.owner_id == user.id, ApiKey.provider == payload.provider).one_or_none()
        if record is None:
            record = ApiKey(owner_id=user.id, provider=payload.provider, encrypted_key=encrypted, nonce=nonce, key_hint=key_hint(payload.api_key))
            self.db.add(record)
        else:
            record.encrypted_key = encrypted
            record.nonce = nonce
            record.key_hint = key_hint(payload.api_key)
        self.db.commit()
        self.db.refresh(record)
        return record

    def delete(self, user: User, provider: ApiProvider) -> None:
        record = self.db.query(ApiKey).filter(ApiKey.owner_id == user.id, ApiKey.provider == provider).one_or_none()
        if record:
            self.db.delete(record)
            self.db.commit()

    def list(self, user: User) -> list[ApiKey]:
        return self.db.query(ApiKey).filter(ApiKey.owner_id == user.id).order_by(ApiKey.provider).all()
