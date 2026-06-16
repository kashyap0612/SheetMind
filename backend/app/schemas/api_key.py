from datetime import datetime
from pydantic import BaseModel, Field
from app.models.enums import ApiProvider


class ApiKeyUpsert(BaseModel):
    provider: ApiProvider
    api_key: str = Field(min_length=8, max_length=4096)


class ApiKeyResponse(BaseModel):
    provider: ApiProvider
    key_hint: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
