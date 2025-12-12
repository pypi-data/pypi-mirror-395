from typing import Protocol

from pydantic import EmailStr

from async_temp_email._core._schemas import Message
from async_temp_email._core._types import _Cookies, _HttpResponse, _Tokens


class HttpClient(Protocol):
    """
    Protocol for an asynchronous HTTP client used internally by the library.

    Implementations must provide minimal `GET` and `POST` methods that return
    provider-compatible HTTP responses. This allows the library to remain
    backend-agnostic and work with different HTTP libraries (httpx, aiohttp, etc.).

    Typical usage with a client implementation::

        response = await http_client.get('https://example.com')
        data = response.json()
    """

    async def get(self, url: str, **kwargs) -> _HttpResponse:
        """
        Send an asynchronous HTTP GET request.

        Args:
            url: The endpoint URL.
            **kwargs: Extra request arguments (headers, params, timeout, etc.).

        Returns:
            _HttpResponse: Provider-specific HTTP response wrapper.

        Example:
            response = await client.get(url, headers={"User-Agent": "TempEmail"})
        """
        ...

    async def post(self, url: str, **kwargs) -> _HttpResponse:
        """
        Send an asynchronous HTTP POST request.

        Args:
            url: The endpoint URL.
            **kwargs: Extra request arguments (headers, JSON body, timeout, etc.).

        Returns:
            _HttpResponse: Provider-specific HTTP response wrapper.

        Example:
            response = await client.post(url, json={"email": "test@example.com"})
        """
        ...

    def get_cookies(self, *args, **kwargs) -> _Cookies:
        """
        Retrieve cookies from the temporary email provider.

        This method is used to obtain session or authentication cookies that may
        be required for subsequent API requests. It is typically asynchronous
        when implemented with an async HTTP client.

        Args:
            *args: Provider-specific positional arguments.
            **kwargs: Provider-specific keyword arguments, such as headers,
                query parameters, timeout, etc.

        Returns:
            _Cookies: A container holding cookies returned by the provider.

        Example:
            cookies = client.get_cookies(headers={"User-Agent": "TempEmail"})
        """
        ...


class TokensProvider(Protocol):
    """
    Protocol describing a component responsible for retrieving authentication
    or session tokens required by a temporary email provider.

    The provider may require CSRF tokens, API keys, session cookies or other
    authorization information. Implementations encapsulate the logic needed to
    acquire such tokens before performing API requests.
    """

    async def get_tokens(self, *args, **kwargs) -> _Tokens:
        """
        Fetch authentication/session tokens for a provider.

        Args:
            *args: Provider-specific arguments.
            **kwargs: Provider-specific configuration.

        Returns:
            _Tokens: Token container used by the provider.

        Example:
            tokens = await provider.get_tokens()
        """
        ...


class Service(Protocol):
    """
    Protocol defining high-level API operations for a temporary email provider.

    A concrete implementation encapsulates provider-specific logic for:
    - generating or retrieving temporary email addresses,
    - retrieving mailbox message lists,
    - getting detailed message contents.

    All methods are asynchronous and operate with validated email types and
    structured message objects.
    """

    async def get_email(
        self,
        domain: bool = True,
        plus_gmail: bool = True,
        dot_gmail: bool = True,
        google_mail: bool = True,
    ) -> EmailStr:
        """
        Request or generate a temporary email address.

        Args:
            domain: Allow provider-generated domain-based emails.
            plus_gmail: Allow Gmail aliasing with "+".
            dot_gmail: Allow Gmail dot variations.
            google_mail: Allow base @gmail.com addresses.

        Returns:
            EmailStr: A validated temporary email address.

        Example:
            email = await client.service.get_email()
        """
        ...

    async def get_messages(self, email: EmailStr) -> list[Message]:
        """
        Fetch a list of messages for a given temporary email address.

        Args:
            email: Target email address.

        Returns:
            list[Message]: Parsed list of messages from the provider.

        Example:
            messages = await service.get_messages(email)\n
            for msg in messages:
                print(msg.subject)
        """
        ...

    async def get_message(self, email: EmailStr, message_id: str) -> Message:
        """
        Fetch a specific message by its provider-defined ID.

        Args:
            email: Email whose mailbox is queried.
            message_id: Provider-specific message identifier.

        Returns:
            Message: Parsed message object.

        Example:
            message = await service.get_message(email, "abc123")
        """
        ...


class Polling(Protocol):
    """
    Protocol providing real-time message polling for a temporary email provider.

    A Polling implementation continuously queries the API for new incoming
    messages and yields them via asynchronous iteration.

    Features:
        - async context management
        - async iteration (``async for message in poller``)
        - dynamic configuration through ``__call__``

    Example:
        async with client.polling(email, skip_existing=False) as poller:
            async for message in poller:
                print(message)
    """

    def __init__(self, service: Service) -> None:
        """
        Initialize a polling instance for a temporary email provider.

        The Polling instance is responsible for continuously querying the
        provider for new messages and making them available via asynchronous
        iteration.

        Args:
            service: An instance implementing the :class:`Service` protocol.
                This service is used to fetch email addresses and messages
                from the provider.

        Example:
            poller = EmailnatorPolling(service)
            async with poller(email="test@example.com") as p:
                async for message in p:
                    print(message.subject)
        """
        ...

    async def __aenter__(self) -> 'Polling':
        """
        Start the internal polling loop upon entering async context.

        Returns:
            Polling: Self.

        Example:
            async with poller(email) as p:
                ...
        """
        ...

    async def __aexit__(self, exc_type, exc, tb) -> None:
        """
        Stop polling and clean up resources when leaving async context.

        Args:
            exc_type: Exception type if raised during context execution.
            exc: The exception instance.
            tb: Traceback for the exception.

        Returns:
            None
        """
        ...

    def __aiter__(self) -> 'Polling':
        """
        Return asynchronous iterator for message retrieval.

        Returns:
            Polling: Self, yielding :class:`Message` objects.

        Example:
            async for message in poller:
                print(message)
        """
        ...

    async def __anext__(self) -> Message:
        """
        Retrieve the next available message.

        Returns:
            Message: Newly received message.

        Raises:
            StopAsyncIteration: If polling has stopped and queue is empty.

        Example:
            msg = await poller.__anext__()
        """
        ...

    def __call__(
        self,
        email: EmailStr,
        poll_interval: float = 10,
        skip_existing: bool = True,
    ) -> 'Polling':
        """
        Configure polling parameters for a mailbox.

        Args:
            email: Email address to poll.
            poll_interval: Delay between provider API checks (seconds).
            skip_existing: Whether to ignore already existing messages
                during the first poll iteration.

        Returns:
            Polling: Configured poller instance.

        Example:
            poller = client.polling(email, poll_interval=5)
        """
        ...


class Client(Protocol):
    """
    Protocol representing the main high-level temporary email client.

    A concrete implementation must expose:
        - ``service`` — direct email/message management API;
        - ``polling`` — real-time mailbox polling capability.

    This is the primary interface end users interact with.

    Example:
        client = Emailnator(timeout=30, retries=3)
        email = await client.service.get_email()
        async for msg in client.polling(email):
            print(msg.subject)
    """

    service: Service
    polling: Polling

    def __init__(self, timeout: int, retries: int):
        """
        Initialize client with HTTP/network configuration.

        Args:
            timeout: HTTP request timeout in seconds.
            retries: Number of retry attempts on failure.

        Returns:
            None
        """
        ...
