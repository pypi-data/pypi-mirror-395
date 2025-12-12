from typing import Callable

from async_temp_email._core._interfaces import Client


class TempEmailClient:
    """
    Factory class responsible for constructing concrete temporary email clients.

    This class acts as a registry-based factory: individual provider clients
    (e.g., Emailnator, TempMail, MailGW) register themselves using the
    :meth:`register` decorator, after which they can be instantiated by name.

    Supported providers out of the box:
        - "emailnator"

    Example:
        @TempEmailClient.register("emailnator")
        class EmailnatorClient:
            ...

        client = TempEmailClient.create("emailnator", timeout=20)

        async with TempEmailClient.create("emailnator") as client:
            ...
    """

    _clients: dict[str, type[Client]] = {}

    @classmethod
    def create(cls, source: str, *, timeout: int = 30, retries: int = 3) -> Client:
        """
        Create a new client instance for the specified temporary email provider.

        Officially supported sources:
            - "emailnator"

        Args:
            source: Provider name. Must match a previously registered client.
            timeout: Default request timeout (seconds).
            retries: Number of retry attempts for network operations.

        Returns:
            Client: An instance of the registered provider client.

        Raises:
            ValueError: If the provider name is not registered.

        Example:
            client = TempEmailClient.create("emailnator", timeout=15, retries=5)
        """
        source = source.lower()

        try:
            client_class = cls._clients[source]
        except KeyError:
            available = ', '.join(map(repr, cls._clients)) or 'none'
            raise ValueError(f'Unknown client: {source!r}.\nRegistered: {available}\n')

        return client_class(timeout, retries)

    @classmethod
    def _register(cls, source: str) -> Callable[[type[Client]], type[Client]]:
        """
        Register a new temporary email client implementation.

        This method is used as a class decorator. When applied, it adds the
        given class to the internal registry so that it can later be created
        using :class:`TempEmailClient`.

        Args:
            source: Provider name under which the client will be registered.
                Case-insensitive.
                Officially supported sources:
                    - "emailnator"

        Returns:
            Callable: A decorator that registers the given class.

        Example:
            @TempEmailClient.register("emailnator")
            class EmailnatorClient:
                ...
        """

        def decorator(client_class: type[Client]) -> type[Client]:
            """
            Register the provided client class in the factory.

            Args:
                client_class: The concrete client class implementing the
                    :class:`Client` protocol.

            Returns:
                type[Client]: The same class, unmodified.
            """
            cls._clients[source.lower()] = client_class
            return client_class

        return decorator
