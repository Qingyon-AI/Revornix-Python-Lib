from datetime import datetime

from pydantic import BaseModel


class SectionUserPublicInfo(BaseModel):
    id: int
    avatar: str
    nickname: str
    slogan: str | None = None
    authority: int | None = None
    role: int | None = None
    create_time: datetime
    update_time: datetime | None = None


class UserPublicInfo(BaseModel):
    id: int
    role: int
    avatar: str
    nickname: str
    slogan: str | None = None
    is_followed: bool | None = None
    fans: int | None = None
    follows: int | None = None
