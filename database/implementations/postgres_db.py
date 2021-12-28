import psycopg2
from uuid import UUID, uuid4
from typing import List, Optional
from account.account import Account
from psycopg2.extras import DictCursor
from database.database import AccountDatabase
from transaction.transaction import Transaction



class AccountDatabasePostgres(AccountDatabase):
    def __init__(self, connection=str):
        self.conn = psycopg2.connect(connection)
        cursor = self.conn.cursor(cursor_factory=DictCursor)
        cursor.execute("""
            create table if not exists accounts(
                id varchar primary key,
                currency varchar,
                balance decimal
                );

            create table if not exists transactions(
                id varchar primary key,
                source_account varchar not null references accounts (id),
                target_account varchar not null references accounts (id),
                amount decimal not null check (amount > 0),
                date varchar not null,
                currency varchar not null,
                operation varchar not null
                )""")
        self.conn.commit()


    def save(self, arg) -> None:
        cursor = self.conn.cursor(cursor_factory=DictCursor)
        if isinstance(arg, Account):
            if arg.id is None:
                arg.id = uuid4()
            cursor.execute("""
                insert into accounts values (%s, %s, %s)
                on conflict (id) do
                update set currency = excluded.currency, balance = excluded.balance
            """,
            (str(arg.id), arg.currency, arg.balance))
        elif isinstance(arg, Transaction):
            if arg.id is None:
                arg.id = uuid4()
            cursor.execute("""
                insert into transactions values (%s, %s, %s, %s, %s, %s, %s)
            """,
            (str(arg.id), str(arg.source_account.id), str(arg.target_account.id), arg.amount, arg.date, arg.currency, arg.operation))
        else:
            print("Not Account or Transaction objects!")
        self.conn.commit()


    def to_Account(self, arg) -> Account:
        return Account(
            id = UUID(arg["id"]),
            currency = arg["currency"],
            balance = arg["balance"],
            )


    def to_Transaction(self, arg) -> Transaction:
        return Transaction(
            id = UUID(arg["id"]),
            source_account = self.get_object(table="accounts", filters = f"where id = '{arg['source_account']}'"),
            target_account = self.get_object(table="accounts", filters = f"where id = '{arg['target_account']}'"),
            amount = arg["amount"],
            currency = arg["currency"],
            date = arg["date"],
            operation = arg["operation"]
            )


    def get_object(self, table=str, filters=str):
        cursor = self.conn.cursor(cursor_factory=DictCursor)
        cursor.execute(""" select * from %s %s""" % (table, filters))
        data = cursor.fetchall()
        if table == "accounts":
            return [self.to_Account(x) for x in data]
        elif table == "transactions":
            if len(data) == 0:
                print ("No transactions!")
            return [self.to_Transaction(x) for x in data]


    def delete_object(self, table=str, filters=str):
        cursor = self.conn.cursor(cursor_factory=DictCursor)
        cursor.execute(""" delete * from %s %s""" % (table, filters))
        self.conn.commit()


    def close_connection(self):
        self.conn.close()