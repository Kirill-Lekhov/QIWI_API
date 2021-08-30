from QIWI_API.LinkParts import CURRENCY


class Balances:
    def __init__(self, balance_data):
        self.balances = dict()

        for account in balance_data:
            self.balances[account["alias"]] = dict()

            if account["balance"]:
                self.balances[account["alias"]]["amount"] = account["balance"]["amount"]
                self.balances[account["alias"]]["currency"] = CURRENCY[account["balance"]["currency"]]

            else:
                self.balances[account["alias"]]["amount"] = -1
                self.balances[account["alias"]]["amount"] = 0

    def __getitem__(self, item: str) -> dict:
        return self.balances[item]

    def get_dict(self) -> dict:
        return self.balances
