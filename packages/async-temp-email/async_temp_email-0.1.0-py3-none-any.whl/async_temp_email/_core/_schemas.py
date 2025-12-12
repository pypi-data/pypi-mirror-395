import datetime

from pydantic import BaseModel, Field


class Message(BaseModel):
    message_id: str | None = Field(default=None)
    message_from: str | None = Field(default=None)
    message_subject: str | None = Field(default=None)
    message_content: str | None = Field(default=None)
    message_time: datetime.datetime | None = Field(default=None)
