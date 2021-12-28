from uuid import UUID
from typing import List
from dataclasses import dataclass



@dataclass
class Customer:
    id: UUID
    age: int
    first_name: str
    last_name: str
    accounts: List[UUID]