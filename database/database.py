from uuid import UUID
from typing import List
from dataclasses import dataclass
from abc import ABC, abstractmethod
from account.account import Account


@dataclass
class AccountDatabase(ABC):
    @abstractmethod
    def save(self) -> None:
        pass

    @abstractmethod
    def get_object(self) -> List[Account]:
        pass

    @abstractmethod
    def delete_object(self):
        pass