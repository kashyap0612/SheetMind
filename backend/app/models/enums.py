from enum import StrEnum


class ApiProvider(StrEnum):
    openai = "openai"
    gemini = "gemini"
    anthropic = "anthropic"


class FileStatus(StrEnum):
    uploading = "uploading"
    ready = "ready"
    failed = "failed"


class MessageRole(StrEnum):
    user = "user"
    assistant = "assistant"
    system = "system"
