from typing import List
from uuid import UUID, uuid4
from account.account import Account
from database.database import AccountDatabase



class AccountDatabaseRAM(AccountDatabase):
    def __init__(self):
        self.BUFFER = []

    def filter(self, arr, filters):
        tmp = []
        for fltr in filters:
            if getattr(self.BUFFER[account], key) == value:
                return self.BUFFER[account]



    def save(self, *argv: Account) -> None:
        for arg in argv:
            if arg.id is None:
                account.id = uuid4()
            self.BUFFER.append(arg)

    def get_objects(self) -> List[Account]:
        return self.BUFFER

    def get_object(self, **kwargs):
        for key, value in kwargs.items():
            for account in range(len(self.BUFFER)):
                if getattr(self.BUFFER[account], key) == value:
                    return self.BUFFER[account]

    def delete_objects(self):
        self.BUFFER.clear()

    def delete_object(self, **kwargs):
        for key, value in kwargs.items():
            for account in range(len(self.BUFFER)):
                if getattr(self.BUFFER[account], key) == value:
                    self.BUFFER.remove(account)
