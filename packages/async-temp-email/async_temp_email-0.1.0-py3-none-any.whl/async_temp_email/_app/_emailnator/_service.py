import logging

from bs4 import BeautifulSoup, NavigableString
from pydantic import EmailStr

from async_temp_email._app._emailnator._config import EmailnatorConfig
from async_temp_email._app._emailnator._schemas import (
    EmailnatorMessageSchema,
    EmailnatorMessagesSchema,
    GenerateEmailBodySchema,
    GenerateEmailResponseSchema,
)
from async_temp_email._core._interfaces import HttpClient
from async_temp_email._core._schemas import Message

log = logging.getLogger(__name__)


class EmailnatorService:
    def __init__(self, client: HttpClient):
        self._client = client

    async def get_email(
        self,
        domain: bool = True,
        plus_gmail: bool = True,
        dot_gmail: bool = True,
        google_mail: bool = True,
    ) -> EmailStr:
        log.debug(
            'Generating new temporary email with options: domain=%s, plus_gmail=%s, dot_gmail=%s, google_mail=%s',
            domain,
            plus_gmail,
            dot_gmail,
            google_mail,
        )

        body = GenerateEmailBodySchema(
            domain=domain,
            plus_gmail=plus_gmail,
            dot_gmail=dot_gmail,
            google_mail=google_mail,
            email_types=[],
        )
        payload = {'email': body.email_types}

        response = await self._client.post(EmailnatorConfig.generate_email_endpoint, json=payload)
        email = GenerateEmailResponseSchema(**response.json()).email[0]

        log.info('Generated temporary email: %s', email)
        return email

    async def get_messages(self, email: EmailStr) -> list[Message]:
        log.debug('Fetching message list for %s', email)
        response = await self._client.post(EmailnatorConfig.message_list, json={'email': str(email)})
        data = response.json()
        schema = EmailnatorMessagesSchema(**data)

        messages = schema.to_messages_list()
        log.info('Retrieved %d message(s) for %s', len(messages), email)
        return messages

    async def get_message(self, email: EmailStr, message_id: str) -> Message:
        log.debug('Fetching message %s for %s', message_id, email)
        response = await self._client.post(
            EmailnatorConfig.message_list,
            json={'email': str(email), 'messageID': str(message_id)},
        )

        html = response.content.decode('utf-8', errors='replace')
        message_from, message_subject, message_time = self._extract_data_from_html(html)

        if not all((message_from, message_subject)):
            log.warning('Failed to parse some header fields for message %s (email: %s)', message_id, email)

        message = EmailnatorMessageSchema(
            message_id=message_id,
            message_from=message_from,
            message_subject=message_subject,
            message_content=html,
            message_time=message_time or 'unknown',
        ).to_message()

        log.info('Retrieved message %s from %s: %s', message_id, email, message.message_subject)
        return message

    @staticmethod
    def _extract_data_from_html(html: str) -> tuple[str | None, str | None, str | None]:
        soup = BeautifulSoup(html, 'html.parser')
        header = soup.find(id='subject-header')

        if not header:
            log.warning("HTML structure changed: <div id='subject-header'> not found")
            return None, None, None

        needed = {'from', 'subject', 'time'}
        result = {}

        for b in header.find_all('b'):
            key_raw = b.get_text(strip=True).rstrip(':').lower()
            if key_raw not in needed:
                continue

            sibling = b.next_sibling
            while sibling and (not isinstance(sibling, NavigableString) or not sibling.strip()):
                sibling = sibling.next_sibling

            value = sibling.strip() if sibling and isinstance(sibling, NavigableString) else None
            result[key_raw] = value

        return result.get('from'), result.get('subject'), result.get('time')
