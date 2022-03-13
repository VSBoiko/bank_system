from prettytable import PrettyTable

from datetime import datetime


class Account:
    deposit_text = "deposit"
    deposit_text_success = "Deposit operation was successful!"

    withdraw_text = "withdraw"
    withdraw_text_success = "Withdrawal operation was successful!"

    currency_text = "$"

    def __init__(self, client: str):
        self._client = client
        self._operation_list = list()
        self._balance = 0

        self._create_account()

    def get_bank_statement(self, date_from=None, date_to=None):
        table = PrettyTable()
        table.field_names = [
            "Date",
            "Description",
            "Withdrawals",
            "Deposits",
            "Balance"
        ]

        operations = self._filter_operations_by_date(date_from, date_to)
        table = self._add_operations_rows(table, operations)
        table = self._add_total_row(table, operations)

        return table

    def deposit(self, amount: float, description: str = ""):
        self._balance += amount
        self._add_operation(Account.deposit_text, amount, description)
        print(Account.deposit_text_success)

    def withdraw(self, amount: float, description: str = ""):
        self._balance -= amount
        self._add_operation(Account.withdraw_text, amount, description)
        print(Account.withdraw_text_success)

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
        }
        self._operation_list.append(new_operation)

    def _add_operations_rows(self, table, operations=None):
        if operations is None:
            operations = self.get_operation_list()

        balance = 0
        for operation in operations:
            new_row = [
                operation["date"].strftime("%Y-%m-%d %H:%M:%S"),
                operation["description"],
            ]

            str_amount = self._get_monetary_str(operation["amount"])
            if operation["type"] == Account.withdraw_text:
                new_row.append(str_amount)
                new_row.append("")
                balance -= operation["amount"]
            elif operation["type"] == Account.deposit_text:
                new_row.append("")
                new_row.append(str_amount)
                balance += operation["amount"]
            else:
                new_row.append("")
                new_row.append("")

            str_balance = self._get_monetary_str(balance)
            new_row.append(str_balance)

            table.add_row(new_row)
            new_row.clear()

        return table

    def _add_total_row(self, table, operations):
        withdrawals = 0
        deposits = 0
        for operation in operations:
            if operation["type"] == Account.withdraw_text:
                withdrawals += operation["amount"]
            elif operation["type"] == Account.deposit_text:
                deposits += operation["amount"]
        withdrawals_text = self._get_monetary_str(withdrawals)
        deposits_text = self._get_monetary_str(deposits)
        balance = self._get_monetary_str(deposits - withdrawals)

        total_row = [
            "",
            "Totals",
            withdrawals_text,
            deposits_text,
            balance
        ]
        table.add_row(total_row)

        return table

    def _create_account(self):
        self._add_operation("create_account", 0, "account created")

    def _filter_operations_by_date(self, date_from=None, date_to=None):
        all_operations = self.get_operation_list()

        if date_from is None and date_to is None:
            return all_operations

        if date_from is None:
            date_from = all_operations[0]["date"]
        if date_to is None:
            date_to = all_operations[-1]["date"]

        filtered = list()
        for operation in all_operations:
            date = operation["date"]
            if date_from <= date <= date_to:
                filtered.append(operation)

        return filtered

    def _get_monetary_str(self, amount: float):
        return Account.currency_text + str(round(amount, 2))