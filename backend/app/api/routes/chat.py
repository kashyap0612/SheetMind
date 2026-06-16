from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.auth import get_current_user
from app.db.session import get_db
from app.models.api_key import ApiKey
from app.models.chat import ChatMessage, ChatSession
from app.models.enums import FileStatus, MessageRole
from app.models.usage import QueryUsage
from app.models.user import User
from app.repositories.files import FileRepository
from app.schemas.chat import QueryRequest, QueryResponse
from app.services.action_engine import execute_action
from app.services.llm import LLMPlanner
from app.services.spreadsheet import read_first_sheet
from app.services.storage import R2StorageService

router = APIRouter(prefix="/chat", tags=["chat"])


def _has_key(db: Session, user: User, provider: str) -> bool:
    return db.query(ApiKey).filter(ApiKey.owner_id == user.id, ApiKey.provider == provider).count() > 0


@router.post("/query", response_model=QueryResponse)
def query(payload: QueryRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    record = FileRepository(db).get_owned(payload.file_id, user.id)
    if record is None or record.status != FileStatus.ready:
        raise HTTPException(status_code=404, detail="Ready file not found")
    if user.free_queries_remaining <= 0 and not _has_key(db, user, payload.provider):
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail="Add your API key to continue querying")
    data = R2StorageService().get(record.storage_key)
    df = read_first_sheet(record.original_filename, data)
    planner = LLMPlanner()
    try:
        action = planner.plan(payload.question, [str(column) for column in df.columns])
        execution = execute_action(action, df)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    session = db.get(ChatSession, payload.session_id) if payload.session_id else None
    if session is None:
        session = ChatSession(owner_id=user.id, file_id=record.id, title=payload.question[:120])
        db.add(session)
        db.flush()
    answer = planner.explain(action, execution.result, execution.steps)
    db.add(ChatMessage(session_id=session.id, role=MessageRole.user, content=payload.question))
    db.add(ChatMessage(session_id=session.id, role=MessageRole.assistant, content=answer, execution_plan=execution.steps, result=execution.result))
    if user.free_queries_remaining > 0:
        user.free_queries_remaining -= 1
    db.add(QueryUsage(owner_id=user.id, chat_session_id=session.id, provider=payload.provider))
    db.commit()
    return QueryResponse(session_id=session.id, answer=answer, action=action, execution_plan=execution.steps, result=execution.result, free_queries_remaining=user.free_queries_remaining)
