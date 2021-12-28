from flask import Flask, redirect, url_for, render_template, request
from database.implementations.postgres_db import AccountDatabasePostgres
from account.account import Account
from transaction.transaction import Transaction
from uuid import uuid4, UUID
from datetime import datetime

app = Flask(__name__)

connection_str = "dbname=test user=postgres port=5432 password=Malstrem_Nautilus host=localhost"
database = AccountDatabasePostgres(connection=connection_str)

@app.route("/", methods = ["POST", "GET"])
def home():
    if request.method == "POST":
        currency = request.form.get("select_currency")
        new_account = Account(id = uuid4(), balance = 0, currency = currency)
        database.save(new_account)
        accounts = database.get_object(table='accounts', filters="")
        return render_template("main_page.html", accounts = accounts)
    else:
        accounts = database.get_object(table='accounts', filters="")
        return render_template("main_page.html", accounts = accounts)

@app.route("/<id>", methods = ["POST", "GET"])
def account_home(id):
    account = database.get_object(table='accounts', filters=f"where id = '{id}'")
    if request.method == "POST":
        operation = request.form.get("select_operation")
        currency = request.form.get("select_currency")
        amount = request.form.get("balance")
        target = request.form.get("target")
        target_account = database.get_object(table = 'accounts', filters = f"where id = '{target}'")
        new_transaction = Transaction(id = uuid4(), source_account = account[0], target_account = target_account[0], amount = int(amount), currency = currency, date = str(datetime.now()), operation = operation)
        if operation == "Перевод":
            new_transaction.transfer()
            database.save(account[0])
            database.save(target_account[0])
        elif operation == "Пополнение":
            new_transaction.replenishment()
            database.save(account[0])
        database.save(new_transaction)
        transactions = database.get_object(table='transactions', filters=f"where source_account = '{id}'")
        return render_template("account_page.html", account = account[0], transactions = transactions)
    elif request.method == "GET":
        transactions = database.get_object(table='transactions', filters=f"where source_account = '{id}'")
        return render_template("account_page.html", account = account[0], transactions = transactions)


if __name__ == "__main__":
    app.run(debug = True)
