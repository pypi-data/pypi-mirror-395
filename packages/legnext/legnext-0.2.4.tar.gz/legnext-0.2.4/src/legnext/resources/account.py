"""Account management resources."""

from legnext._internal.http_client import AsyncHTTPClient, HTTPClient
from legnext.types.responses import BalanceResponse


class AccountResource:
    """Synchronous account management resource."""

    def __init__(self, http: HTTPClient) -> None:
        """Initialize the account resource."""
        self._http = http

    def balance(self) -> BalanceResponse:
        """Get account balance (GET /account/balance).

        Returns:
            Balance response with account balance information

        Example:
            ```python
            balance = client.account.balance()
            print(f"Balance: {balance.balance} {balance.currency}")
            ```
        """
        data = self._http.request("GET", "/account/balance")
        return BalanceResponse.model_validate(data)


class AsyncAccountResource:
    """Asynchronous account management resource."""

    def __init__(self, http: AsyncHTTPClient) -> None:
        """Initialize the async account resource."""
        self._http = http

    async def balance(self) -> BalanceResponse:
        """Get account balance (GET /account/balance) - async.

        Returns:
            Balance response with account balance information

        Example:
            ```python
            balance = await client.account.balance()
            print(f"Balance: {balance.balance} {balance.currency}")
            ```
        """
        data = await self._http.request("GET", "/account/balance")
        return BalanceResponse.model_validate(data)
