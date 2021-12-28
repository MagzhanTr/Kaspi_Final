from uuid import UUID
from decimal import Decimal
from dataclasses import dataclass
from account.account import Account
from currency_converter import CurrencyConverter



c = CurrencyConverter()


@dataclass
class Transaction:
    id: UUID
    source_account: Account
    target_account: Account
    amount: Decimal
    currency: str
    date: str
    operation: str

    def transfer(self):
        if self.source_account.balance < Decimal(c.convert(self.amount, self.currency, self.source_account.currency)):
            raise ValueError("Insufficient funds in the account!")
        else:
            self.source_account.balance = self.source_account.balance - Decimal(c.convert(self.amount, self.currency, self.source_account.currency))
            self.target_account.balance = self.target_account.balance + Decimal(c.convert(self.amount, self.currency, self.target_account.currency))

    def replenishment(self):
        self.source_account.balance = self.source_account.balance + Decimal(c.convert(self.amount, self.currency, self.source_account.currency))