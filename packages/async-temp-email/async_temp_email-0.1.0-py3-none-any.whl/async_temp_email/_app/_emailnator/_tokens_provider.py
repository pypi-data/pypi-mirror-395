import asyncio
import logging

from async_temp_email._core._interfaces import HttpClient

log = logging.getLogger(__name__)


class EmailnatorTokensProvider:
    def __init__(self, client: HttpClient):
        self._client = client

        self._xsrf_token: str | None = None
        self._gmailnator_session: str | None = None

        self._lock = asyncio.Lock()

    async def get_tokens(self) -> dict[str, str]:
        if self._xsrf_token is None or self._gmailnator_session is None:
            async with self._lock:
                if self._xsrf_token is None or self._gmailnator_session is None:
                    await self._update_tokens()

        log.debug(
            'Tokens retrieved: XSRF-TOKEN=%s..., session=%s...',
            self._xsrf_token[:8] if self._xsrf_token else None,
            self._gmailnator_session[:8] if self._gmailnator_session else None,
        )

        return {
            'xsrf_token': self._xsrf_token,
            'gmailnator_session': self._gmailnator_session,
        }

    async def _update_tokens(self) -> None:
        log.debug('Fetching fresh tokens from homepage...')
        await self._client.get('')

        cookies = self._client.get_cookies()
        self._xsrf_token = cookies.get('XSRF-TOKEN')
        self._gmailnator_session = cookies.get('gmailnator_session')

        if not self._xsrf_token or not self._gmailnator_session:
            log.warning(
                'Failed to extract one or both tokens. XSRF=%s, session=%s', self._xsrf_token, self._gmailnator_session
            )
        else:
            log.info('Successfully updated Emailnator session tokens')
