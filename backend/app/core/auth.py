from functools import lru_cache
from fastapi import Depends, Header, HTTPException, status
from jose import jwt
from jose.exceptions import JWTError
from sqlalchemy.orm import Session
import httpx
from app.core.config import get_settings
from app.db.session import get_db
from app.models.user import User


@lru_cache(maxsize=1)
def _jwks() -> dict:
    settings = get_settings()
    if not settings.clerk_jwks_url:
        return {}
    return httpx.get(settings.clerk_jwks_url, timeout=10).json()


def get_current_user(authorization: str = Header(default=""), db: Session = Depends(get_db)) -> User:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")
    token = authorization.removeprefix("Bearer ")
    settings = get_settings()
    try:
        if settings.environment == "development" and token.startswith("dev:"):
            claims = {"sub": token.removeprefix("dev:"), "email": "dev@sheetmind.local", "name": "Dev User"}
        else:
            claims = jwt.decode(token, _jwks(), algorithms=["RS256"], issuer=settings.clerk_issuer)
    except JWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc
    clerk_id = claims.get("sub")
    if not clerk_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid subject")
    user = db.query(User).filter(User.clerk_user_id == clerk_id).one_or_none()
    if user is None:
        user = User(
            clerk_user_id=clerk_id,
            email=claims.get("email") or claims.get("primary_email_address"),
            name=claims.get("name"),
            free_queries_remaining=settings.free_query_limit,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user
