"""initial schema

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-06-03
"""
from alembic import op
import sqlalchemy as sa

revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    api_provider = sa.Enum("openai", "gemini", "anthropic", name="apiprovider")
    file_status = sa.Enum("uploading", "ready", "failed", name="filestatus")
    message_role = sa.Enum("user", "assistant", "system", name="messagerole")
    api_provider.create(op.get_bind(), checkfirst=True)
    file_status.create(op.get_bind(), checkfirst=True)
    message_role.create(op.get_bind(), checkfirst=True)
    op.create_table("users", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("clerk_user_id", sa.String(128), nullable=False), sa.Column("email", sa.String(320)), sa.Column("name", sa.String(255)), sa.Column("free_queries_remaining", sa.Integer(), nullable=False, server_default="10"), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()))
    op.create_index("ix_users_clerk_user_id", "users", ["clerk_user_id"], unique=True)
    op.create_index("ix_users_email", "users", ["email"])
    op.create_table("files", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("owner_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False), sa.Column("original_filename", sa.String(255), nullable=False), sa.Column("storage_key", sa.String(512), nullable=False), sa.Column("mime_type", sa.String(160), nullable=False), sa.Column("extension", sa.String(16), nullable=False), sa.Column("size_bytes", sa.Integer(), nullable=False), sa.Column("status", file_status, nullable=False), sa.Column("row_count", sa.Integer()), sa.Column("column_count", sa.Integer()), sa.Column("sample_rows", sa.JSON()), sa.Column("error_message", sa.Text()), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()))
    op.create_index("ix_files_owner_id", "files", ["owner_id"])
    op.create_index("ix_files_storage_key", "files", ["storage_key"], unique=True)
    op.create_table("sheets", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("file_id", sa.Integer(), sa.ForeignKey("files.id", ondelete="CASCADE"), nullable=False), sa.Column("name", sa.String(255), nullable=False), sa.Column("row_count", sa.Integer(), nullable=False), sa.Column("column_count", sa.Integer(), nullable=False), sa.Column("columns", sa.JSON(), nullable=False), sa.Column("sample_rows", sa.JSON(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()))
    op.create_index("ix_sheets_file_id", "sheets", ["file_id"])
    op.create_table("api_keys", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("owner_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False), sa.Column("provider", api_provider, nullable=False), sa.Column("encrypted_key", sa.LargeBinary(), nullable=False), sa.Column("nonce", sa.LargeBinary(), nullable=False), sa.Column("key_hint", sa.String(16), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()), sa.UniqueConstraint("owner_id", "provider", name="uq_api_key_owner_provider"))
    op.create_index("ix_api_keys_owner_id", "api_keys", ["owner_id"])
    op.create_table("chat_sessions", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("owner_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False), sa.Column("file_id", sa.Integer(), sa.ForeignKey("files.id", ondelete="CASCADE"), nullable=False), sa.Column("title", sa.String(255), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()))
    op.create_index("ix_chat_sessions_owner_id", "chat_sessions", ["owner_id"])
    op.create_index("ix_chat_sessions_file_id", "chat_sessions", ["file_id"])
    op.create_table("chat_messages", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("session_id", sa.Integer(), sa.ForeignKey("chat_sessions.id", ondelete="CASCADE"), nullable=False), sa.Column("role", message_role, nullable=False), sa.Column("content", sa.Text(), nullable=False), sa.Column("execution_plan", sa.JSON()), sa.Column("result", sa.JSON()), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()))
    op.create_index("ix_chat_messages_session_id", "chat_messages", ["session_id"])
    op.create_table("query_usage", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("owner_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False), sa.Column("chat_session_id", sa.Integer(), sa.ForeignKey("chat_sessions.id", ondelete="SET NULL")), sa.Column("provider", sa.String(32), nullable=False), sa.Column("prompt_tokens", sa.Integer(), nullable=False, server_default="0"), sa.Column("completion_tokens", sa.Integer(), nullable=False, server_default="0"), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()))
    op.create_index("ix_query_usage_owner_id", "query_usage", ["owner_id"])


def downgrade() -> None:
    for table in ["query_usage", "chat_messages", "chat_sessions", "api_keys", "sheets", "files", "users"]:
        op.drop_table(table)
    for enum in ["messagerole", "filestatus", "apiprovider"]:
        sa.Enum(name=enum).drop(op.get_bind(), checkfirst=True)
