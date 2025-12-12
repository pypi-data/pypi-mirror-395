import logging

import httpx

from async_temp_email._app._emailnator._config import EmailnatorConfig
from async_temp_email._app._emailnator._http_clients import (
    EmailnatorAuthHttpClient,
    EmailnatorDefaultHttpClient,
)
from async_temp_email._app._emailnator._polling import EmailnatorPolling
from async_temp_email._app._emailnator._service import EmailnatorService
from async_temp_email._app._emailnator._tokens_provider import EmailnatorTokensProvider
from async_temp_email._core._base_client import TempEmailClient

log = logging.getLogger(__name__)


@TempEmailClient._register('emailnator')
class EmailnatorClient:
    def __init__(self, timeout: int = 30, retries: int = 3):
        log.info('Initializing EmailnatorClient (timeout=%s, retries=%s)', timeout, retries)

        self._client = httpx.AsyncClient(
            base_url=EmailnatorConfig.base_url,
            headers=EmailnatorConfig.base_headers,
            timeout=timeout,
            transport=httpx.AsyncHTTPTransport(retries=retries),
            http2=EmailnatorConfig.http2,
            event_hooks={
                'response': [self._log_response],
            },
        )

        default_http = EmailnatorDefaultHttpClient(self._client)
        self._tokens_provider = EmailnatorTokensProvider(default_http)  # type: ignore
        auth_http = EmailnatorAuthHttpClient(self._client, self._tokens_provider)  # type: ignore

        self.service = EmailnatorService(auth_http)  # type: ignore
        self.polling = EmailnatorPolling(self.service)

        self._closed = False

    async def _log_response(self, response: httpx.Response):
        request = response.request
        log.debug('→ %s %s | ← %s %s', request.method, request.url, response.status_code, response.reason_phrase)

    async def __aenter__(self) -> 'EmailnatorClient':
        log.debug('Entering EmailnatorClient context')
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        log.debug('Exiting EmailnatorClient context')
        await self.close()

    async def close(self) -> None:
        if not self._closed:
            log.info('Closing EmailnatorClient HTTP session')
            await self._client.aclose()
            self._closed = True
