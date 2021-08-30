import requests
from time import time
from json import dumps

from QIWI_API.Exceptions import *
from QIWI_API.Tools import run_the_query, write_file, found_id
from QIWI_API.LinkParts import HEADERS, FUNCTIONS


from QIWI_API.Classes.User import User
from QIWI_API.Classes.Transaction import Transaction
from QIWI_API.Classes.Balances import Balances


class Qiwi:
    def __init__(self, token: str):
        self.user = User("-1")
        self.headers = HEADERS.copy()

        self.change_token(token)
        self.user_data_update()

    def update(self, new_token: str) -> None:
        self.change_token(new_token)
        self.user_data_update()

    def change_token(self, new_token: str) -> None:
        if not self.check_token(new_token):
            raise TokenError

        self.user.update_token(new_token)

    def check_token(self, token: str) -> bool:
        self.headers["Authorization"] = HEADERS["Authorization"].format(token)

        if not run_the_query(self.headers, FUNCTIONS["Profile"][0]):
            return False

        return True

    def user_data_update(self):
        try:
            answer = run_the_query(self.headers, FUNCTIONS["Profile"][0])
            self.user.update_data(answer)

        except Exception as err:
            print(err)
            raise QiwiError

    def get_balance(self) -> Balances:
        try:
            answer = run_the_query(self.headers, FUNCTIONS["Balance"][0])["accounts"]
            return Balances(answer)

        except Exception as err:
            print(err)
            raise QiwiError

    def get_last_transactions(self, transactions_number: int = 10) -> list:
        try:
            answer = run_the_query(self.headers, FUNCTIONS["Transactions"][0].format(self.user.get_id(), transactions_number))
            return self.create_transactions_list(answer["data"])

        except Exception as err:
            print(err)
            raise TransactionNotFound

    @staticmethod
    def create_transactions_list(answer: dict) -> list:
        transactions = []

        for transaction_data in answer:
            transactions.append(Transaction(transaction_data))

        return transactions

    def get_transaction(self, transaction_id: str) -> Transaction:
        try:
            answer = run_the_query(self.headers, FUNCTIONS["Transaction"][0].format(transaction_id))
            return Transaction(answer)

        except Exception as err:
            print(err)
            raise TransactionNotFound

    def download_receipt(self, transaction_id, file_name="check.jpg"):
        # TODO: rework this method
        answer = run_the_query(self.headers, FUNCTIONS["Transaction"][0].format(transaction_id))

        if not answer:
            raise TransactionNotFound

        typ = answer['type']
        write = write_file(self.headers, FUNCTIONS["Check"][0].format(transaction_id, "file", typ, "&format=JPEG"),
                           file_name)

        if not write:
            raise CheckError

    def send_check_email(self, transaction_id: str, email=None) -> None:
        answer = run_the_query(self.headers, FUNCTIONS["Transaction"][0].format(transaction_id))

        if not answer:
            raise TransactionNotFound

        typ = answer['type']
        email = {"email": self.user.get_email() if email is None else email}
        request = requests.post(FUNCTIONS["Check"][0].format(transaction_id, "send", typ, ''),
                                data=dumps(email),
                                headers=self.headers)
        if not request:
            raise WrongEmail

    def transaction_telephone(self, amount, number=None):
        if number is None:
            number = str(self.user.get_id())

        number_id = found_id(number)

        if not number_id:
            raise WrongNumber

        number = number[1:]

        try:
            amount = round(float(amount), 2)

        except TypeError:
            raise WalletError

        data = {"id": str(int(time() * 1000)),
                "sum": {"amount": amount,
                        "currency": "643"},
                "paymentMethod": {"type": "Account",
                                  "accountId": "643"},
                "fields": {"account": number}}

        try:
            request = requests.post(FUNCTIONS["Phone pay"][0].format(number_id), data=dumps(data),
                                    headers=self.headers)
            if request:
                answer = request.json()
                return "Successfully. Transaction ID: {}".format(answer["transaction"]["id"])

            else:
                raise TransactionError

        except Exception as err:
            print(err)
            raise TransactionError

    def transaction_qiwi(self, account_id, amount):
        try:
            amount = round(float(amount), 2)

        except ValueError:
            raise WalletError

        data = {"id": str(int(time() * 1000)),
                "sum": {"amount": amount,
                        "currency": "643"},
                "paymentMethod": {"type": "Account",
                                  "accountId": "643"},
                "comment": "test",
                "fields": {"account": account_id}}

        try:
            request = requests.post(FUNCTIONS["Qiwi pay"][0], data=dumps(data), headers=self.headers)

            if request:
                answer = request.json()

                return "Successfully. Transaction ID: {}".format(answer["transaction"]["id"])

            else:
                raise TransactionError

        except Exception as err:
            print(err)
            raise TransactionError

    def get_current_user(self) -> User:
        return self.user
