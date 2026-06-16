from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.auth import get_current_user
from app.db.session import get_db
from app.models.enums import ApiProvider
from app.models.user import User
from app.schemas.api_key import ApiKeyResponse, ApiKeyUpsert
from app.services.api_keys import ApiKeyService

router = APIRouter(prefix="/api-keys", tags=["api keys"])


@router.get("", response_model=list[ApiKeyResponse])
def list_keys(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return ApiKeyService(db).list(user)


@router.put("", response_model=ApiKeyResponse)
async def upsert_key(payload: ApiKeyUpsert, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        return await ApiKeyService(db).upsert(user, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc


@router.delete("/{provider}", status_code=204)
def delete_key(provider: ApiProvider, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    ApiKeyService(db).delete(user, provider)
