import click

from datetime import datetime
import pickle

import settings
from Account import Account


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
@click.option(
    '--since',
    help='from what date to make a bank statement, for example, 2021-01-31 00:00:00',
)
@click.option(
    '--till',
    help='to what date to make a bank statement, for example, 2021-12-31 00:00:00',
)
def main(command, client, amount, description, since, till):
    amount = 0 if amount is None else float(amount)
    description = "" if description is None else str(description)

    with open(settings.pickle_file, 'rb') as f:
        bank = pickle.load(f)

    if bank.get_account(client):
        client_acc = bank.get_account(client)
    else:
        client_acc = Account(client)
        bank.add_account(client_acc)

    if command == settings.deposit_comm:
        command_deposit(bank, client, client_acc, amount, description)
    elif command == settings.withdraw_comm:
        command_withdraw(bank, client, client_acc, amount, description)
    elif command == settings.show_comm:
        command_show(client_acc, since, till)


def command_deposit(bank, client, client_account, amount, description):
    if amount > 0:
        client_account.deposit(amount, description)
        bank.update_account(client, client_account)

    with open(settings.pickle_file, 'wb') as f:
        pickle.dump(bank, f)


def command_withdraw(bank, client, client_account, amount, description):
    if amount > 0:
        client_account.withdraw(amount, description)
        bank.update_account(client, client_account)

    with open(settings.pickle_file, 'wb') as f:
        pickle.dump(bank, f)


def command_show(client_account, since=None, till=None):
    if since is None:
        since_date = None
    else:
        since_date = datetime.strptime(since, "%Y-%m-%d %H:%M:%S")

    if till is None:
        till_date = None
    else:
        till_date = datetime.strptime(till, "%Y-%m-%d %H:%M:%S")

    account_table = client_account.get_bank_statement(date_from=since_date, date_to=till_date)
    print(account_table)


# deposit --client="John Jones" --amount=100 --description="ATM Deposit"
# withdraw --client="John Jones" --amount=100 --description="ATM Withdrawal"
# show_bank_statement --client="John Jones" --since="2021-01-01 00:00:00" --till="2021-02-01 00:00:00"
if __name__ == "__main__":
    main()
