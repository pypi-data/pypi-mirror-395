import logging

from httpx import AsyncClient, Response

from async_temp_email._core._interfaces import TokensProvider

log = logging.getLogger(__name__)


class EmailnatorDefaultHttpClient:
    def __init__(self, client: AsyncClient):
        self._client = client

    async def get(self, url: str, **kwargs) -> Response:
        log.debug('GET | payload keys: %s', list(kwargs.get('params', {}).keys()))
        response = await self._client.get(url, **kwargs)
        response.raise_for_status()
        return response

    async def post(self, url: str, **kwargs) -> Response:
        log.debug('POST | payload keys: %s', list(kwargs.get('json', {}).keys()))
        response = await self._client.post(url, **kwargs)
        response.raise_for_status()
        return response

    def get_cookies(self) -> dict:
        return dict(self._client.cookies)


class EmailnatorAuthHttpClient:
    def __init__(self, client: AsyncClient, tokens_provider: TokensProvider):
        self._client = client
        self._tokens_provider = tokens_provider

    async def get(self, url: str, **kwargs) -> Response:
        log.debug('GET | payload keys: %s', list(kwargs.get('params', {}).keys()))
        kwargs = await self._add_tokens_to_headers(kwargs)
        response = await self._client.get(url, **kwargs)
        response.raise_for_status()
        return response

    async def post(self, url: str, **kwargs) -> Response:
        log.debug('POST | payload keys: %s', list(kwargs.get('json', {}).keys()))
        kwargs = await self._add_tokens_to_headers(kwargs)
        response = await self._client.post(url, **kwargs)
        response.raise_for_status()
        return response

    def get_cookies(self) -> dict:
        return dict(self._client.cookies)

    async def _add_tokens_to_headers(self, kwargs: dict) -> dict:
        tokens = await self._tokens_provider.get_tokens()

        kwargs = kwargs.copy()
        kwargs['headers'] = {
            'X-Xsrf-Token': tokens['xsrf_token'].replace('%3D', '='),
            'Cookie': f'XSRF-TOKEN={tokens["xsrf_token"]}; gmailnator_session={tokens["gmailnator_session"]}',
        } | kwargs.get('headers', {})

        return kwargs
