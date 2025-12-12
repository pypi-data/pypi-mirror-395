"""Resource classes for Lenco API"""

from typing import Any

from lenco.types import (
    Account,
    AccountBalance,
    Bank,
    Collection,
    CollectionCustomer,
    EncryptionKey,
    MobileMoneyOperator,
    Recipient,
    ResolvedBankAccount,
    ResolvedLencoMerchant,
    ResolvedLencoMoney,
    ResolvedMobileMoney,
    Settlement,
    Transaction,
    Transfer,
)


class AccountsResource:
    """Accounts API resource"""

    def __init__(self, http: Any) -> None:
        self._http = http

    def list(self, page: int | None = None) -> list[Account]:
        """List all accounts"""
        data = self._http.get("/accounts", params={"page": page})
        return [Account.model_validate(item) for item in data]

    def get(self, account_id: str) -> Account:
        """Get account by ID"""
        data = self._http.get(f"/accounts/{account_id}")
        return Account.model_validate(data)

    def get_balance(self, account_id: str) -> AccountBalance:
        """Get account balance"""
        data = self._http.get(f"/accounts/{account_id}/balance")
        return AccountBalance.model_validate(data)


class AsyncAccountsResource:
    """Async Accounts API resource"""

    def __init__(self, http: Any) -> None:
        self._http = http

    async def list(self, page: int | None = None) -> list[Account]:
        """List all accounts"""
        data = await self._http.get("/accounts", params={"page": page})
        return [Account.model_validate(item) for item in data]

    async def get(self, account_id: str) -> Account:
        """Get account by ID"""
        data = await self._http.get(f"/accounts/{account_id}")
        return Account.model_validate(data)

    async def get_balance(self, account_id: str) -> AccountBalance:
        """Get account balance"""
        data = await self._http.get(f"/accounts/{account_id}/balance")
        return AccountBalance.model_validate(data)


class BanksResource:
    """Banks API resource"""

    def __init__(self, http: Any) -> None:
        self._http = http

    def list(self, country: str | None = None) -> list[Bank]:
        """List all banks"""
        data = self._http.get("/banks", params={"country": country})
        return [Bank.model_validate(item) for item in data]

    def resolve_bank_account(
        self, account_number: str, bank_id: str
    ) -> ResolvedBankAccount:
        """Resolve a bank account"""
        data = self._http.post(
            "/banks/resolve",
            json={"accountNumber": account_number, "bankId": bank_id},
        )
        return ResolvedBankAccount.model_validate(data)

    def resolve_mobile_money(
        self, phone: str, operator: MobileMoneyOperator, country: str
    ) -> ResolvedMobileMoney:
        """Resolve a mobile money account"""
        data = self._http.post(
            "/banks/resolve/mobile-money",
            json={"phone": phone, "operator": operator.value, "country": country},
        )
        return ResolvedMobileMoney.model_validate(data)

    def resolve_lenco_money(self, phone: str) -> ResolvedLencoMoney:
        """Resolve a Lenco Money account"""
        data = self._http.post("/banks/resolve/lenco-money", json={"phone": phone})
        return ResolvedLencoMoney.model_validate(data)

    def resolve_lenco_merchant(self, merchant_id: str) -> ResolvedLencoMerchant:
        """Resolve a Lenco Merchant"""
        data = self._http.post(
            "/banks/resolve/lenco-merchant", json={"merchantId": merchant_id}
        )
        return ResolvedLencoMerchant.model_validate(data)


class AsyncBanksResource:
    """Async Banks API resource"""

    def __init__(self, http: Any) -> None:
        self._http = http

    async def list(self, country: str | None = None) -> list[Bank]:
        """List all banks"""
        data = await self._http.get("/banks", params={"country": country})
        return [Bank.model_validate(item) for item in data]

    async def resolve_bank_account(
        self, account_number: str, bank_id: str
    ) -> ResolvedBankAccount:
        """Resolve a bank account"""
        data = await self._http.post(
            "/banks/resolve",
            json={"accountNumber": account_number, "bankId": bank_id},
        )
        return ResolvedBankAccount.model_validate(data)

    async def resolve_mobile_money(
        self, phone: str, operator: MobileMoneyOperator, country: str
    ) -> ResolvedMobileMoney:
        """Resolve a mobile money account"""
        data = await self._http.post(
            "/banks/resolve/mobile-money",
            json={"phone": phone, "operator": operator.value, "country": country},
        )
        return ResolvedMobileMoney.model_validate(data)

    async def resolve_lenco_money(self, phone: str) -> ResolvedLencoMoney:
        """Resolve a Lenco Money account"""
        data = await self._http.post("/banks/resolve/lenco-money", json={"phone": phone})
        return ResolvedLencoMoney.model_validate(data)

    async def resolve_lenco_merchant(self, merchant_id: str) -> ResolvedLencoMerchant:
        """Resolve a Lenco Merchant"""
        data = await self._http.post(
            "/banks/resolve/lenco-merchant", json={"merchantId": merchant_id}
        )
        return ResolvedLencoMerchant.model_validate(data)


class RecipientsResource:
    """Recipients API resource"""

    def __init__(self, http: Any) -> None:
        self._http = http

    def list(self, page: int | None = None) -> list[Recipient]:
        """List all recipients"""
        data = self._http.get("/transfer-recipients", params={"page": page})
        return [Recipient.model_validate(item) for item in data]

    def get(self, recipient_id: str) -> Recipient:
        """Get recipient by ID"""
        data = self._http.get(f"/transfer-recipients/{recipient_id}")
        return Recipient.model_validate(data)

    def create_bank_account(
        self, name: str, account_number: str, bank_id: str
    ) -> Recipient:
        """Create a bank account recipient"""
        data = self._http.post(
            "/transfer-recipients/bank-account",
            json={"name": name, "accountNumber": account_number, "bankId": bank_id},
        )
        return Recipient.model_validate(data)

    def create_mobile_money(
        self, name: str, phone: str, operator: MobileMoneyOperator, country: str
    ) -> Recipient:
        """Create a mobile money recipient"""
        data = self._http.post(
            "/transfer-recipients/mobile-money",
            json={
                "name": name,
                "phone": phone,
                "operator": operator.value,
                "country": country,
            },
        )
        return Recipient.model_validate(data)

    def create_lenco_money(self, name: str, phone: str) -> Recipient:
        """Create a Lenco Money recipient"""
        data = self._http.post(
            "/transfer-recipients/lenco-money",
            json={"name": name, "phone": phone},
        )
        return Recipient.model_validate(data)

    def create_lenco_merchant(self, merchant_id: str) -> Recipient:
        """Create a Lenco Merchant recipient"""
        data = self._http.post(
            "/transfer-recipients/lenco-merchant",
            json={"merchantId": merchant_id},
        )
        return Recipient.model_validate(data)


class AsyncRecipientsResource:
    """Async Recipients API resource"""

    def __init__(self, http: Any) -> None:
        self._http = http

    async def list(self, page: int | None = None) -> list[Recipient]:
        """List all recipients"""
        data = await self._http.get("/transfer-recipients", params={"page": page})
        return [Recipient.model_validate(item) for item in data]

    async def get(self, recipient_id: str) -> Recipient:
        """Get recipient by ID"""
        data = await self._http.get(f"/transfer-recipients/{recipient_id}")
        return Recipient.model_validate(data)

    async def create_bank_account(
        self, name: str, account_number: str, bank_id: str
    ) -> Recipient:
        """Create a bank account recipient"""
        data = await self._http.post(
            "/transfer-recipients/bank-account",
            json={"name": name, "accountNumber": account_number, "bankId": bank_id},
        )
        return Recipient.model_validate(data)

    async def create_mobile_money(
        self, name: str, phone: str, operator: MobileMoneyOperator, country: str
    ) -> Recipient:
        """Create a mobile money recipient"""
        data = await self._http.post(
            "/transfer-recipients/mobile-money",
            json={
                "name": name,
                "phone": phone,
                "operator": operator.value,
                "country": country,
            },
        )
        return Recipient.model_validate(data)

    async def create_lenco_money(self, name: str, phone: str) -> Recipient:
        """Create a Lenco Money recipient"""
        data = await self._http.post(
            "/transfer-recipients/lenco-money",
            json={"name": name, "phone": phone},
        )
        return Recipient.model_validate(data)

    async def create_lenco_merchant(self, merchant_id: str) -> Recipient:
        """Create a Lenco Merchant recipient"""
        data = await self._http.post(
            "/transfer-recipients/lenco-merchant",
            json={"merchantId": merchant_id},
        )
        return Recipient.model_validate(data)


class TransfersResource:
    """Transfers API resource"""

    def __init__(self, http: Any) -> None:
        self._http = http

    def list(
        self,
        page: int | None = None,
        per_page: int | None = None,
        account_id: str | None = None,
        status: str | None = None,
        type: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> list[Transfer]:
        """List all transfers"""
        data = self._http.get(
            "/transfers",
            params={
                "page": page,
                "perPage": per_page,
                "accountId": account_id,
                "status": status,
                "type": type,
                "startDate": start_date,
                "endDate": end_date,
            },
        )
        return [Transfer.model_validate(item) for item in data]

    def get(self, transfer_id: str) -> Transfer:
        """Get transfer by ID"""
        data = self._http.get(f"/transfers/{transfer_id}")
        return Transfer.model_validate(data)

    def get_by_reference(self, reference: str) -> Transfer:
        """Get transfer by reference"""
        data = self._http.get(f"/transfers/reference/{reference}")
        return Transfer.model_validate(data)

    def to_bank_account(
        self,
        account_id: str,
        account_number: str,
        bank_id: str,
        amount: int,
        reference: str,
        narration: str | None = None,
    ) -> Transfer:
        """Transfer to a bank account"""
        data = self._http.post(
            "/transfers/bank-account",
            json={
                "accountId": account_id,
                "accountNumber": account_number,
                "bankId": bank_id,
                "amount": amount,
                "reference": reference,
                "narration": narration,
            },
        )
        return Transfer.model_validate(data)

    def to_mobile_money(
        self,
        account_id: str,
        phone: str,
        operator: MobileMoneyOperator,
        country: str,
        amount: int,
        reference: str,
        narration: str | None = None,
    ) -> Transfer:
        """Transfer to mobile money"""
        data = self._http.post(
            "/transfers/mobile-money",
            json={
                "accountId": account_id,
                "phone": phone,
                "operator": operator.value,
                "country": country,
                "amount": amount,
                "reference": reference,
                "narration": narration,
            },
        )
        return Transfer.model_validate(data)

    def to_lenco_money(
        self,
        account_id: str,
        phone: str,
        amount: int,
        reference: str,
        narration: str | None = None,
    ) -> Transfer:
        """Transfer to Lenco Money"""
        data = self._http.post(
            "/transfers/lenco-money",
            json={
                "accountId": account_id,
                "phone": phone,
                "amount": amount,
                "reference": reference,
                "narration": narration,
            },
        )
        return Transfer.model_validate(data)

    def to_lenco_merchant(
        self,
        account_id: str,
        merchant_id: str,
        amount: int,
        reference: str,
        narration: str | None = None,
    ) -> Transfer:
        """Transfer to Lenco Merchant"""
        data = self._http.post(
            "/transfers/lenco-merchant",
            json={
                "accountId": account_id,
                "merchantId": merchant_id,
                "amount": amount,
                "reference": reference,
                "narration": narration,
            },
        )
        return Transfer.model_validate(data)

    def to_recipient(
        self,
        account_id: str,
        recipient_id: str,
        amount: int,
        reference: str,
        narration: str | None = None,
    ) -> Transfer:
        """Transfer to a saved recipient"""
        data = self._http.post(
            "/transfers/account",
            json={
                "accountId": account_id,
                "recipientId": recipient_id,
                "amount": amount,
                "reference": reference,
                "narration": narration,
            },
        )
        return Transfer.model_validate(data)


class AsyncTransfersResource:
    """Async Transfers API resource"""

    def __init__(self, http: Any) -> None:
        self._http = http

    async def list(
        self,
        page: int | None = None,
        per_page: int | None = None,
        account_id: str | None = None,
        status: str | None = None,
        type: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> list[Transfer]:
        """List all transfers"""
        data = await self._http.get(
            "/transfers",
            params={
                "page": page,
                "perPage": per_page,
                "accountId": account_id,
                "status": status,
                "type": type,
                "startDate": start_date,
                "endDate": end_date,
            },
        )
        return [Transfer.model_validate(item) for item in data]

    async def get(self, transfer_id: str) -> Transfer:
        """Get transfer by ID"""
        data = await self._http.get(f"/transfers/{transfer_id}")
        return Transfer.model_validate(data)

    async def get_by_reference(self, reference: str) -> Transfer:
        """Get transfer by reference"""
        data = await self._http.get(f"/transfers/reference/{reference}")
        return Transfer.model_validate(data)

    async def to_bank_account(
        self,
        account_id: str,
        account_number: str,
        bank_id: str,
        amount: int,
        reference: str,
        narration: str | None = None,
    ) -> Transfer:
        """Transfer to a bank account"""
        data = await self._http.post(
            "/transfers/bank-account",
            json={
                "accountId": account_id,
                "accountNumber": account_number,
                "bankId": bank_id,
                "amount": amount,
                "reference": reference,
                "narration": narration,
            },
        )
        return Transfer.model_validate(data)

    async def to_mobile_money(
        self,
        account_id: str,
        phone: str,
        operator: MobileMoneyOperator,
        country: str,
        amount: int,
        reference: str,
        narration: str | None = None,
    ) -> Transfer:
        """Transfer to mobile money"""
        data = await self._http.post(
            "/transfers/mobile-money",
            json={
                "accountId": account_id,
                "phone": phone,
                "operator": operator.value,
                "country": country,
                "amount": amount,
                "reference": reference,
                "narration": narration,
            },
        )
        return Transfer.model_validate(data)

    async def to_lenco_money(
        self,
        account_id: str,
        phone: str,
        amount: int,
        reference: str,
        narration: str | None = None,
    ) -> Transfer:
        """Transfer to Lenco Money"""
        data = await self._http.post(
            "/transfers/lenco-money",
            json={
                "accountId": account_id,
                "phone": phone,
                "amount": amount,
                "reference": reference,
                "narration": narration,
            },
        )
        return Transfer.model_validate(data)

    async def to_lenco_merchant(
        self,
        account_id: str,
        merchant_id: str,
        amount: int,
        reference: str,
        narration: str | None = None,
    ) -> Transfer:
        """Transfer to Lenco Merchant"""
        data = await self._http.post(
            "/transfers/lenco-merchant",
            json={
                "accountId": account_id,
                "merchantId": merchant_id,
                "amount": amount,
                "reference": reference,
                "narration": narration,
            },
        )
        return Transfer.model_validate(data)

    async def to_recipient(
        self,
        account_id: str,
        recipient_id: str,
        amount: int,
        reference: str,
        narration: str | None = None,
    ) -> Transfer:
        """Transfer to a saved recipient"""
        data = await self._http.post(
            "/transfers/account",
            json={
                "accountId": account_id,
                "recipientId": recipient_id,
                "amount": amount,
                "reference": reference,
                "narration": narration,
            },
        )
        return Transfer.model_validate(data)


class CollectionsResource:
    """Collections API resource"""

    def __init__(self, http: Any) -> None:
        self._http = http

    def list(
        self,
        page: int | None = None,
        per_page: int | None = None,
        status: str | None = None,
        type: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> list[Collection]:
        """List all collections"""
        data = self._http.get(
            "/collections",
            params={
                "page": page,
                "perPage": per_page,
                "status": status,
                "type": type,
                "startDate": start_date,
                "endDate": end_date,
            },
        )
        return [Collection.model_validate(item) for item in data]

    def get(self, collection_id: str) -> Collection:
        """Get collection by ID"""
        data = self._http.get(f"/collections/{collection_id}")
        return Collection.model_validate(data)

    def get_by_reference(self, reference: str) -> Collection:
        """Get collection by reference"""
        data = self._http.get(f"/collections/status/{reference}")
        return Collection.model_validate(data)

    def from_mobile_money(
        self,
        amount: int,
        reference: str,
        phone: str,
        operator: MobileMoneyOperator,
        country: str,
        customer: CollectionCustomer | None = None,
    ) -> Collection:
        """Collect from mobile money"""
        payload: dict[str, Any] = {
            "amount": amount,
            "reference": reference,
            "phone": phone,
            "operator": operator.value,
            "country": country,
        }
        if customer:
            payload["customer"] = customer.model_dump(by_alias=True, exclude_none=True)

        data = self._http.post("/collections/mobile-money", json=payload)
        return Collection.model_validate(data)

    def from_card(
        self,
        amount: int,
        reference: str,
        currency: str,
        encrypted_card: str,
        customer: CollectionCustomer,
        callback_url: str | None = None,
    ) -> Collection:
        """Collect from card"""
        payload: dict[str, Any] = {
            "amount": amount,
            "reference": reference,
            "currency": currency,
            "encryptedCard": encrypted_card,
            "customer": customer.model_dump(by_alias=True, exclude_none=True),
        }
        if callback_url:
            payload["callbackUrl"] = callback_url

        data = self._http.post("/collections/card", json=payload)
        return Collection.model_validate(data)


class AsyncCollectionsResource:
    """Async Collections API resource"""

    def __init__(self, http: Any) -> None:
        self._http = http

    async def list(
        self,
        page: int | None = None,
        per_page: int | None = None,
        status: str | None = None,
        type: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> list[Collection]:
        """List all collections"""
        data = await self._http.get(
            "/collections",
            params={
                "page": page,
                "perPage": per_page,
                "status": status,
                "type": type,
                "startDate": start_date,
                "endDate": end_date,
            },
        )
        return [Collection.model_validate(item) for item in data]

    async def get(self, collection_id: str) -> Collection:
        """Get collection by ID"""
        data = await self._http.get(f"/collections/{collection_id}")
        return Collection.model_validate(data)

    async def get_by_reference(self, reference: str) -> Collection:
        """Get collection by reference"""
        data = await self._http.get(f"/collections/status/{reference}")
        return Collection.model_validate(data)

    async def from_mobile_money(
        self,
        amount: int,
        reference: str,
        phone: str,
        operator: MobileMoneyOperator,
        country: str,
        customer: CollectionCustomer | None = None,
    ) -> Collection:
        """Collect from mobile money"""
        payload: dict[str, Any] = {
            "amount": amount,
            "reference": reference,
            "phone": phone,
            "operator": operator.value,
            "country": country,
        }
        if customer:
            payload["customer"] = customer.model_dump(by_alias=True, exclude_none=True)

        data = await self._http.post("/collections/mobile-money", json=payload)
        return Collection.model_validate(data)

    async def from_card(
        self,
        amount: int,
        reference: str,
        currency: str,
        encrypted_card: str,
        customer: CollectionCustomer,
        callback_url: str | None = None,
    ) -> Collection:
        """Collect from card"""
        payload: dict[str, Any] = {
            "amount": amount,
            "reference": reference,
            "currency": currency,
            "encryptedCard": encrypted_card,
            "customer": customer.model_dump(by_alias=True, exclude_none=True),
        }
        if callback_url:
            payload["callbackUrl"] = callback_url

        data = await self._http.post("/collections/card", json=payload)
        return Collection.model_validate(data)


class SettlementsResource:
    """Settlements API resource"""

    def __init__(self, http: Any) -> None:
        self._http = http

    def list(
        self,
        page: int | None = None,
        per_page: int | None = None,
        status: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> list[Settlement]:
        """List all settlements"""
        data = self._http.get(
            "/settlements",
            params={
                "page": page,
                "perPage": per_page,
                "status": status,
                "startDate": start_date,
                "endDate": end_date,
            },
        )
        return [Settlement.model_validate(item) for item in data]

    def get(self, settlement_id: str) -> Settlement:
        """Get settlement by ID"""
        data = self._http.get(f"/settlements/{settlement_id}")
        return Settlement.model_validate(data)


class AsyncSettlementsResource:
    """Async Settlements API resource"""

    def __init__(self, http: Any) -> None:
        self._http = http

    async def list(
        self,
        page: int | None = None,
        per_page: int | None = None,
        status: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> list[Settlement]:
        """List all settlements"""
        data = await self._http.get(
            "/settlements",
            params={
                "page": page,
                "perPage": per_page,
                "status": status,
                "startDate": start_date,
                "endDate": end_date,
            },
        )
        return [Settlement.model_validate(item) for item in data]

    async def get(self, settlement_id: str) -> Settlement:
        """Get settlement by ID"""
        data = await self._http.get(f"/settlements/{settlement_id}")
        return Settlement.model_validate(data)


class TransactionsResource:
    """Transactions API resource"""

    def __init__(self, http: Any) -> None:
        self._http = http

    def list(
        self,
        page: int | None = None,
        per_page: int | None = None,
        account_id: str | None = None,
        type: str | None = None,
        category: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> list[Transaction]:
        """List all transactions"""
        data = self._http.get(
            "/transactions",
            params={
                "page": page,
                "perPage": per_page,
                "accountId": account_id,
                "type": type,
                "category": category,
                "startDate": start_date,
                "endDate": end_date,
            },
        )
        return [Transaction.model_validate(item) for item in data]

    def get(self, transaction_id: str) -> Transaction:
        """Get transaction by ID"""
        data = self._http.get(f"/transactions/{transaction_id}")
        return Transaction.model_validate(data)


class AsyncTransactionsResource:
    """Async Transactions API resource"""

    def __init__(self, http: Any) -> None:
        self._http = http

    async def list(
        self,
        page: int | None = None,
        per_page: int | None = None,
        account_id: str | None = None,
        type: str | None = None,
        category: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> list[Transaction]:
        """List all transactions"""
        data = await self._http.get(
            "/transactions",
            params={
                "page": page,
                "perPage": per_page,
                "accountId": account_id,
                "type": type,
                "category": category,
                "startDate": start_date,
                "endDate": end_date,
            },
        )
        return [Transaction.model_validate(item) for item in data]

    async def get(self, transaction_id: str) -> Transaction:
        """Get transaction by ID"""
        data = await self._http.get(f"/transactions/{transaction_id}")
        return Transaction.model_validate(data)


class EncryptionResource:
    """Encryption API resource"""

    def __init__(self, http: Any) -> None:
        self._http = http

    def get_key(self) -> EncryptionKey:
        """Get encryption key for card data"""
        data = self._http.get("/collections/encryption-key")
        return EncryptionKey.model_validate(data)


class AsyncEncryptionResource:
    """Async Encryption API resource"""

    def __init__(self, http: Any) -> None:
        self._http = http

    async def get_key(self) -> EncryptionKey:
        """Get encryption key for card data"""
        data = await self._http.get("/collections/encryption-key")
        return EncryptionKey.model_validate(data)
