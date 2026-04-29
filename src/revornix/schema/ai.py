from pydantic import BaseModel, Field


class ChatItem(BaseModel):
    chat_id: str
    content: str
    role: str
    images: list[str] = Field(default_factory=list)
