from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    clerk_user_id: str
    email: str | None
    name: str | None
    free_queries_remaining: int

    model_config = {"from_attributes": True}
