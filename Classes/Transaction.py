from QIWI_API.LinkParts import CURRENCY


class Transaction:
    def __init__(self, transaction_data):
        self.title = transaction_data["view"]["title"]
        self.account = transaction_data["view"]["account"]
        self.date = transaction_data["date"]
        self.status = transaction_data["status"]
        self.error = transaction_data["error"]
        self.txnId = transaction_data["txnId"]

        # TODO: rework this calls
        self.commission = str(transaction_data["commission"]["amount"]) + " " + CURRENCY[transaction_data["commission"]["currency"]]
        self.total = str(transaction_data["total"]["amount"]) + " " + CURRENCY[transaction_data["total"]["currency"]]

    def get_dict(self) -> dict:
        transaction_form = dict()
        transaction_form["Title"] = self.title
        transaction_form["Account"] = self.account
        transaction_form["Date"] = self.date
        transaction_form["Status"] = self.status
        transaction_form["Error"] = self.error
        transaction_form["txnId"] = self.txnId
        transaction_form["Commission"] = self.commission
        transaction_form["Total"] = self.total

        return transaction_form

