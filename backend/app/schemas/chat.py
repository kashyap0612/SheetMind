from datetime import datetime
from typing import Any, Literal
from pydantic import BaseModel, Field

Operation = Literal["count", "average", "sum", "min", "max", "filter", "sort", "groupby", "top_n", "unique", "null_analysis"]


class FilterSpec(BaseModel):
    column: str
    value: str | int | float | bool | None


class ActionSpec(BaseModel):
    operation: Operation
    target_column: str | None = None
    metric: str | None = None
    filter: FilterSpec | None = None
    groupby_column: str | None = None
    sort_direction: Literal["asc", "desc"] = "desc"
    limit: int = Field(default=10, ge=1, le=100)


class QueryRequest(BaseModel):
    file_id: int
    question: str = Field(min_length=2, max_length=2000)
    provider: Literal["openai", "gemini", "anthropic"] = "openai"
    session_id: int | None = None


class QueryResponse(BaseModel):
    session_id: int
    answer: str
    action: ActionSpec
    execution_plan: list[str]
    result: dict[str, Any]
    free_queries_remaining: int


class ChatMessageResponse(BaseModel):
    id: int
    role: str
    content: str
    execution_plan: list | None
    result: dict | None
    created_at: datetime

    model_config = {"from_attributes": True}
