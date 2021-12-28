import json
import random
from typing import Optional
from decimal import Decimal
from uuid import UUID, uuid4
from dataclasses import dataclass



@dataclass
class Account:
    id: Optional[UUID]
    currency: str
    balance: Decimal

    def to_json(self) -> dict:
        return {
            "id": str(self.id),
            "currency": self.currency,
            "balance": float(self.balance),
        }

    @classmethod
    def random(cls) -> "Account":
        return cls(
            id=uuid4(),
            currency="KZT",
            balance=float(random.randint(1, 1000)),
        )
