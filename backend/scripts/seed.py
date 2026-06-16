from app.core.config import get_settings
from app.db.session import Base, engine, SessionLocal
from app.models.user import User

Base.metadata.create_all(bind=engine)
with SessionLocal() as db:
    if db.query(User).filter_by(clerk_user_id="dev-user").count() == 0:
        db.add(User(clerk_user_id="dev-user", email="dev@sheetmind.local", name="Dev User", free_queries_remaining=get_settings().free_query_limit))
        db.commit()
print("Seeded development user. Use Authorization: Bearer dev:dev-user in development.")
