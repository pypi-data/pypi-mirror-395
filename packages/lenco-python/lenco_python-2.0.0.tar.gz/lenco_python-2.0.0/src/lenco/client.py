"""Lenco API client"""

from lenco.http import AsyncHttpClient, HttpClient
from lenco.resources import (
    AccountsResource,
    AsyncAccountsResource,
    AsyncBanksResource,
    AsyncCollectionsResource,
    AsyncEncryptionResource,
    AsyncRecipientsResource,
    AsyncSettlementsResource,
    AsyncTransactionsResource,
    AsyncTransfersResource,
    BanksResource,
    CollectionsResource,
    EncryptionResource,
    RecipientsResource,
    SettlementsResource,
    TransactionsResource,
    TransfersResource,
)
from lenco.types import Environment


class Lenco:
    """Synchronous Lenco API client"""

    def __init__(
        self,
        api_key: str,
        environment: str = "production",
        timeout: float = 30.0,
        max_retries: int = 3,
        debug: bool = False,
    ) -> None:
        if not api_key:
            raise ValueError("API key is required")

        env = Environment(environment)
        self._http = HttpClient(
            api_key=api_key,
            environment=env,
            timeout=timeout,
            max_retries=max_retries,
            debug=debug,
        )

        self.accounts = AccountsResource(self._http)
        self.banks = BanksResource(self._http)
        self.recipients = RecipientsResource(self._http)
        self.transfers = TransfersResource(self._http)
        self.collections = CollectionsResource(self._http)
        self.settlements = SettlementsResource(self._http)
        self.transactions = TransactionsResource(self._http)
        self.encryption = EncryptionResource(self._http)

    def close(self) -> None:
        """Close the HTTP client"""
        self._http.close()

    def __enter__(self) -> "Lenco":
        return self

    def __exit__(self, *args: object) -> None:
        self.close()


class AsyncLenco:
    """Asynchronous Lenco API client"""

    def __init__(
        self,
        api_key: str,
        environment: str = "production",
        timeout: float = 30.0,
        max_retries: int = 3,
        debug: bool = False,
    ) -> None:
        if not api_key:
            raise ValueError("API key is required")

        env = Environment(environment)
        self._http = AsyncHttpClient(
            api_key=api_key,
            environment=env,
            timeout=timeout,
            max_retries=max_retries,
            debug=debug,
        )

        self.accounts = AsyncAccountsResource(self._http)
        self.banks = AsyncBanksResource(self._http)
        self.recipients = AsyncRecipientsResource(self._http)
        self.transfers = AsyncTransfersResource(self._http)
        self.collections = AsyncCollectionsResource(self._http)
        self.settlements = AsyncSettlementsResource(self._http)
        self.transactions = AsyncTransactionsResource(self._http)
        self.encryption = AsyncEncryptionResource(self._http)

    async def close(self) -> None:
        """Close the HTTP client"""
        await self._http.close()

    async def __aenter__(self) -> "AsyncLenco":
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()
