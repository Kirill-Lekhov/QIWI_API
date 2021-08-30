from QIWI_API.Qiwi import Qiwi

from pprint import pprint


if __name__ == "__main__":
    qiwi = Qiwi("TOKEN")

    pprint(qiwi.get_current_user().get_data())
    pprint(qiwi.get_balance().get_dict())
    pprint(list(map(lambda transaction: transaction.get_dict(), qiwi.get_last_transactions())))
    pprint(qiwi.get_transaction("21540017664").get_dict())
