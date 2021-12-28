import pytest
from typing import Type, Any
from database.database import AccountDatabase
from database.implementations.ram import AccountDatabaseRAM
from database.implementations.postgres_db import AccountDatabasePostgres


@pytest.fixture()
def connection_string(request: Any) -> str:
    return "dbname=test user=postgres port=5432 password=Malstrem_Nautilus host=localhost"


@pytest.fixture(
    params=[
    AccountDatabaseRAM,
    AccountDatabasePostgres,
    ])
def database_implementation(request: Any) -> Type[AccountDatabase]:
    implementation = request.param
    return implementation


@pytest.fixture()
def database_connected(
        request: Any,
        database_implementation: Type[AccountDatabase],
        connection_string: str,
) -> AccountDatabase:
    if database_implementation == AccountDatabasePostgres:
        return AccountDatabasePostgres(connection=connection_string)
    return database_implementation()
