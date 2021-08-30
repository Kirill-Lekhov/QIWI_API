from QIWI_API.LinkParts import IDENTIFICATION


class User:
    def __init__(self, token: str):
        self.token = token
        self.data = {}

    def update_token(self, new_token: str) -> None:
        self.token = new_token

    def update_data(self, new_data: dict) -> None:
        self.data["boundEmail"] = new_data["authInfo"]['boundEmail']
        self.data["ip"] = new_data["authInfo"]['ip']
        self.data["lastLoginDate"] = new_data["authInfo"]['lastLoginDate']
        self.data["lastMobilePinChange"] = new_data["authInfo"]['mobilePinInfo']['lastMobilePinChange']
        self.data["nextMobilePinChange"] = new_data["authInfo"]['mobilePinInfo']['nextMobilePinChange']
        self.data["lastPassChange"] = new_data["authInfo"]['passInfo']['lastPassChange']
        self.data["nextPassChange"] = new_data["authInfo"]['passInfo']['nextPassChange']
        self.data["personId"] = new_data["authInfo"]['personId']
        self.data["registrationDate"] = new_data["authInfo"]['registrationDate']
        self.data["blocked"] = new_data["contractInfo"]["blocked"]

        # TODO: Rework this line
        self.data["identificationInfo"] = self.create_identifications(new_data)

        self.data["defaultPayAccountAlias"] = new_data['userInfo']['defaultPayAccountAlias']
        self.data["defaultPayCurrency"] = new_data['userInfo']['defaultPayCurrency']
        self.data["firstTxnId"] = new_data['userInfo']['firstTxnId']
        self.data["operator"] = new_data['userInfo']['operator']

    @staticmethod
    def create_identifications(answer: dict) -> tuple:
        # TODO: Rework this method
        return tuple(map(lambda x: (x["bankAlias"], IDENTIFICATION[x["identificationLevel"]]),
                         answer["contractInfo"]["identificationInfo"]))

    def get_id(self) -> str:
        return self.data["personId"]

    def get_email(self) -> str:
        return self.data["boundEmail"]

    def get_token(self) -> str:
        return self.token

    def get_data(self) -> dict:
        return self.data
