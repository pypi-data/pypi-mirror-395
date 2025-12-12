import dateparser
from pydantic import BaseModel, EmailStr, Field, field_validator
from pydantic_core.core_schema import ValidationInfo

from async_temp_email._core._schemas import Message


class GenerateEmailBodySchema(BaseModel):
    domain: bool
    plus_gmail: bool
    dot_gmail: bool
    google_mail: bool

    email_types: list[str]

    @field_validator('email_types', mode='before')
    def validate_email_types(cls, _: list[str] | None, values: ValidationInfo) -> list[str]:
        email_types = []

        if values.data.get('domain'):
            email_types.append('domain')
        if values.data.get('plus_gmail'):
            email_types.append('plusGmail')
        if values.data.get('dot_gmail'):
            email_types.append('dotGmail')
        if values.data.get('google_mail'):
            email_types.append('googleMail')

        return email_types


class GenerateEmailResponseSchema(BaseModel):
    email: list[EmailStr]


class EmailnatorMessageSchema(BaseModel):
    message_id: str = Field(alias='messageID')
    message_from: str = Field(alias='from')
    message_subject: str = Field(alias='subject')
    message_content: str | None = Field(alias='text', default=None)
    message_time: str = Field(alias='time')

    model_config = {
        'populate_by_name': True,
    }

    def to_message(self) -> Message:
        time_text = self.message_time
        if time_text.lower() == 'just now':
            time_text = '0 seconds ago'

        message_time = dateparser.parse(time_text)

        return Message(
            message_id=self.message_id,
            message_from=self.message_from,
            message_subject=self.message_subject,
            message_content=self.message_content,
            message_time=message_time,
        )


class EmailnatorMessagesSchema(BaseModel):
    message_data: list[EmailnatorMessageSchema] = Field(alias='messageData')

    def to_messages_list(self) -> list[Message]:
        return [message.to_message() for message in self.message_data]
