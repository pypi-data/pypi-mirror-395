"""Type definitions for Lenco SDK"""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class Environment(str, Enum):
    PRODUCTION = "production"
    SANDBOX = "sandbox"


class MobileMoneyOperator(str, Enum):
    AIRTEL = "airtel"
    MTN = "mtn"
    ZAMTEL = "zamtel"
    TNM = "tnm"


class TransferStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SUCCESSFUL = "successful"
    FAILED = "failed"
    REVERSED = "reversed"


class TransferType(str, Enum):
    BANK_ACCOUNT = "bank-account"
    MOBILE_MONEY = "mobile-money"
    LENCO_MONEY = "lenco-money"
    LENCO_MERCHANT = "lenco-merchant"
    ACCOUNT = "account"


class CollectionStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SUCCESSFUL = "successful"
    FAILED = "failed"
    THREE_DS_AUTH_REQUIRED = "3ds-auth-required"


class CollectionType(str, Enum):
    MOBILE_MONEY = "mobile-money"
    CARD = "card"


class SettlementStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SUCCESSFUL = "successful"
    FAILED = "failed"


class TransactionType(str, Enum):
    CREDIT = "credit"
    DEBIT = "debit"


class TransactionCategory(str, Enum):
    TRANSFER = "transfer"
    COLLECTION = "collection"
    SETTLEMENT = "settlement"
    FEE = "fee"
    REVERSAL = "reversal"


class RecipientType(str, Enum):
    BANK_ACCOUNT = "bank-account"
    MOBILE_MONEY = "mobile-money"
    LENCO_MONEY = "lenco-money"
    LENCO_MERCHANT = "lenco-merchant"


# Response Models


class PaginationMeta(BaseModel):
    total: int
    page: int
    per_page: int = Field(alias="perPage")
    total_pages: int = Field(alias="totalPages")

    model_config = {"populate_by_name": True}


class Account(BaseModel):
    id: str
    name: str
    account_number: str = Field(alias="accountNumber")
    bank_name: str = Field(alias="bankName")
    bank_code: str = Field(alias="bankCode")
    currency: str
    type: str
    status: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")

    model_config = {"populate_by_name": True}


class AccountBalance(BaseModel):
    account_id: str = Field(alias="accountId")
    currency: str
    available_balance: float = Field(alias="availableBalance")
    ledger_balance: float = Field(alias="ledgerBalance")

    model_config = {"populate_by_name": True}


class Bank(BaseModel):
    id: str
    name: str
    code: str
    country: str
    type: str
    logo: str | None = None


class Recipient(BaseModel):
    id: str
    name: str
    type: RecipientType
    account_number: str | None = Field(default=None, alias="accountNumber")
    bank_id: str | None = Field(default=None, alias="bankId")
    bank_name: str | None = Field(default=None, alias="bankName")
    phone: str | None = None
    operator: MobileMoneyOperator | None = None
    country: str | None = None
    created_at: datetime = Field(alias="createdAt")

    model_config = {"populate_by_name": True}


class Transfer(BaseModel):
    id: str
    reference: str
    account_id: str = Field(alias="accountId")
    type: TransferType
    amount: float
    fee: float
    currency: str
    status: TransferStatus
    narration: str | None = None
    recipient: Recipient
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")

    model_config = {"populate_by_name": True}


class CollectionCustomer(BaseModel):
    email: str | None = None
    first_name: str | None = Field(default=None, alias="firstName")
    last_name: str | None = Field(default=None, alias="lastName")
    phone: str | None = None

    model_config = {"populate_by_name": True}


class PaymentDetails(BaseModel):
    operator: MobileMoneyOperator | None = None
    phone: str | None = None
    card_bin: str | None = Field(default=None, alias="cardBin")
    card_last4: str | None = Field(default=None, alias="cardLast4")
    card_brand: str | None = Field(default=None, alias="cardBrand")

    model_config = {"populate_by_name": True}


class Collection3DSAuthMeta(BaseModel):
    redirect_url: str | None = Field(default=None, alias="redirectUrl")

    model_config = {"populate_by_name": True}


class Collection(BaseModel):
    id: str
    reference: str
    type: CollectionType
    amount: float
    fee: float
    currency: str
    status: CollectionStatus
    customer: CollectionCustomer | None = None
    payment_details: PaymentDetails | None = Field(default=None, alias="paymentDetails")
    meta: Collection3DSAuthMeta | None = None
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")

    model_config = {"populate_by_name": True}


class Settlement(BaseModel):
    id: str
    amount: float
    fee: float
    currency: str
    status: SettlementStatus
    settled_at: datetime | None = Field(default=None, alias="settledAt")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")

    model_config = {"populate_by_name": True}


class Transaction(BaseModel):
    id: str
    account_id: str = Field(alias="accountId")
    type: TransactionType
    category: TransactionCategory
    amount: float
    fee: float
    currency: str
    balance_before: float = Field(alias="balanceBefore")
    balance_after: float = Field(alias="balanceAfter")
    reference: str
    narration: str | None = None
    created_at: datetime = Field(alias="createdAt")

    model_config = {"populate_by_name": True}


class ResolvedBankAccount(BaseModel):
    account_number: str = Field(alias="accountNumber")
    account_name: str = Field(alias="accountName")
    bank_id: str = Field(alias="bankId")
    bank_name: str = Field(alias="bankName")

    model_config = {"populate_by_name": True}


class ResolvedMobileMoney(BaseModel):
    phone: str
    name: str
    operator: MobileMoneyOperator
    country: str


class ResolvedLencoMoney(BaseModel):
    phone: str
    name: str
    email: str | None = None


class ResolvedLencoMerchant(BaseModel):
    merchant_id: str = Field(alias="merchantId")
    name: str
    email: str | None = None

    model_config = {"populate_by_name": True}


class EncryptionKey(BaseModel):
    key: str
    expires_at: datetime = Field(alias="expiresAt")

    model_config = {"populate_by_name": True}


class WebhookPayload(BaseModel):
    event: str
    data: dict[str, Any]
    created_at: datetime = Field(alias="createdAt")

    model_config = {"populate_by_name": True}
