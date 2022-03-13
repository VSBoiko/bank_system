from datetime import datetime
import pickle

from prettytable import PrettyTable
import click

from settings import pickle_file


class Account:
    deposit_text = "deposit"
    withdraw_text = "withdraw"
    currency_text = "$"

    def __init__(self, client: str):
        self._client = client
        self._operation_list = list()
        self._total_deposit = 0
        self._total_withdraw = 0
        self._balance = 0

        self._create_account()

    def get_bank_statement(self, date_from=None, date_to=None):
        if (date_from is not None) or (date_to is not None):
            pass

        table = PrettyTable()
        table.field_names = [
            "Date",
            "Description",
            "Withdrawals",
            "Deposits",
            "Balance"
        ]

        table = self._add_operations_rows(table)
        table = self._add_total_row(table)

        return table

    def deposit(self, amount: float, description: str = ""):
        self._total_deposit += amount
        self._balance += amount
        self._add_operation(Account.deposit_text, amount, description)

    def withdraw(self, amount: float, description: str = ""):
        self._total_withdraw += amount
        self._balance -= amount
        self._add_operation(Account.withdraw_text, amount, description)

    def get_client(self):
        return self._client

    def get_operation_list(self):
        return self._operation_list

    def get_balance(self):
        return self._balance

    def _add_operation(self, operation: str, amount: float, description: str = ""):
        new_operation = {
            "type": operation,
            "date": datetime.now(),
            "amount": amount,
            "description": description,
            "balance": self._balance,
        }
        self._operation_list.append(new_operation)

    def _add_operations_rows(self, table, operations=None):
        if operations is None:
            operations = self._operation_list

        for operation in operations:
            new_row = [
                operation["date"].strftime("%Y-%m-%d %H:%M:%S"),
                operation["description"],
            ]

            str_amount = self._get_monetary_str(operation["amount"])
            if operation["type"] == Account.withdraw_text:
                new_row.append(str_amount)
                new_row.append("")
            elif operation["type"] == Account.deposit_text:
                new_row.append("")
                new_row.append(str_amount)
            else:
                new_row.append("")
                new_row.append("")

            str_balance = self._get_monetary_str(operation["balance"])
            new_row.append(str_balance)

            table.add_row(new_row)
            new_row.clear()

        return table

    def _add_total_row(self, table):
        withdrawals = self._get_monetary_str(self._total_withdraw)
        deposits = self._get_monetary_str(self._total_deposit)
        balance = self._get_monetary_str(self.get_balance())

        total_row = [
            "",
            "Totals",
            withdrawals,
            deposits,
            balance
        ]
        table.add_row(total_row)

        return table

    def _create_account(self):
        self._add_operation("create_account", 0, "account created")

    def _get_monetary_str(self, amount):
        return Account.currency_text + str(round(amount, 2))


class Bank:
    def __init__(self):
        self._accounts = dict()

    def add_account(self, new_account: Account):
        account_name = new_account.get_client()
        self._accounts[account_name] = new_account

    def get_account(self, account_name: str):
        return self._accounts.get(account_name)

    def update_account(self, account_name: str, new_account):
        if self._accounts.get(account_name):
            self._accounts[account_name] = new_account


@click.command()
@click.argument('command')
@click.option(
    '--client',
    help='account holder`s name',
)
@click.option(
    '--amount',
    help='the amount of money to deposit or withdraw',
)
@click.option(
    '--description',
    help='description of the operation',
)
def main(command, client, amount, description):
    amount = 0 if amount is None else float(amount)
    description = "" if description is None else str(description)

    with open(pickle_file, 'rb') as f:
        bank = pickle.load(f)

    if bank.get_account(client):
        client_acc = bank.get_account(client)
    else:
        client_acc = Account(client)
        bank.add_account(client_acc)

    if command == Account.deposit_text:
        if amount > 0:
            client_acc.deposit(amount, description)
            bank.update_account(client, client_acc)

        with open(pickle_file, 'wb') as f:
            pickle.dump(bank, f)
    elif command == Account.withdraw_text:
        if amount > 0:
            client_acc.withdraw(amount, description)
            bank.update_account(client, client_acc)

        with open(pickle_file, 'wb') as f:
            pickle.dump(bank, f)
    elif command == "show_bank_statement":
        acc_table = client_acc.get_bank_statement()
        print(acc_table)


if __name__ == "__main__":
    main()
