import urllib.request
import json
import pprint
import time


class QIWI_ERROR(Exception):
    pass


class SINTAKSIS_ERROR(QIWI_ERROR):
    def __init__(self):
        self.text = "Query execution failed"


class TOKEN_ERROR(QIWI_ERROR):
    def __init__(self):
        self.text = "Wrong TOKEN"


class NO_RIGHTS_ERROR(QIWI_ERROR):
     def __init__(self):
        self.text = "No right"


class TRANSACTION_NOT_FOUND(QIWI_ERROR):
    def __init__(self):
        self.text = "Transaction not found or missing payments with specified characteristics"


class WALLET_ERROR(QIWI_ERROR):
    def __init__(self):
        self.text = "Wallet not found"


class HISTORY_ERROR(QIWI_ERROR):
    def __init__(self):
        self.text = "Too many requests, the service is temporarily unavailable"


def run_the_query(headers, url):
    try:
        req = urllib.request.Request(url, headers=headers)
        html = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
        return html
    except:
        return False


class UserQiwi:
    def __init__(self, token):
        self.token = token
        self.headers = {"Accept": "application/json",
                        "Content-Type": "application/json",
                        "Authorization": "Bearer {}".format(self.token)}
        self.urls = {"Profile": ("https://edge.qiwi.com/person-profile/v1/profile/current?", ["authInfoEnabled",
                                                                                              "contractInfoEnabled",
                                                                                              "userInfoEnabled"]),
                     "Balance": ("https://edge.qiwi.com/funding-sources/v1/accounts/current", None),
                     "Transactions": ("https://edge.qiwi.com/payment-history/v2/persons/{}/payments?rows={}", None),
                     "Transaction": ("https://edge.qiwi.com/payment-history/v2/transactions/{}", None)}
        self.currency = {643: "RUB",
                         840: "USD",
                         978: "EUR",
                         "Not Stated": "Not Stated"}
        self.identification = {"ANONYMOUS": "без идентификации",
                               "SIMPLE": "упрощенная идентификация (SIMPLE)",
                               "VERIFIED": "упрощенная идентификация (VERIFIED)",
                               "FULL": "полная идентификация",
                               "Not Stated": "Not Stated"}
        self.user_date = None

        try:
            answer = run_the_query(self.headers, self.urls["Profile"][0])
            self.update_info(answer)
        except:
            raise TOKEN_ERROR

    def change_token(self, new_token):
        self.token = new_token

        if not run_the_query(self.headers, self.urls["Profile"][0]):
            raise TOKEN_ERROR

    def get_user_token(self):
        return self.token

    def get_balans(self):
        answer = run_the_query(self.headers, self.urls["Balance"][0])["accounts"]

        report = ["Balance {}\n-----------------------".format(time.asctime())]
        for i in answer:
            if i["balance"]:
                report.append("{}: {} {}".format(i["alias"],
                                                 i["balance"]["amount"],
                                                 self.currency[i["balance"]["currency"]]))
            else:
                report.append("{}: {}".format(i["alias"], "Not Stated"))

        return "\n".join(report)

    def update_info(self, answer):
        try:
            comands_info = {'email': answer["authInfo"]['boundEmail'],
                            'last_ip': answer["authInfo"]['ip'],
                            'last_login': answer["authInfo"]['lastLoginDate'],
                            'last_mob_pin_ch': answer["authInfo"]['mobilePinInfo']['lastMobilePinChange'],
                            'next_mob_pin_ch': answer["authInfo"]['mobilePinInfo']['nextMobilePinChange'],
                            'last_pass_ch': answer["authInfo"]['passInfo']['lastPassChange'],
                            'next_pass_ch': answer["authInfo"]['passInfo']['nextPassChange'],
                            'id': answer["authInfo"]['personId'],
                            'reg_date': answer["authInfo"]['registrationDate'],
                            'status': answer["contractInfo"]["blocked"],
                            'ident_info': tuple(map(lambda x: (x["bankAlias"],
                                                               self.identification[x["identificationLevel"]]),
                                                    answer["contractInfo"]["identificationInfo"])),
                            'default_alias': answer['userInfo']['defaultPayAccountAlias'],
                            'default_cur': answer['userInfo']['defaultPayCurrency'],
                            'first_tr_id': answer['userInfo']['firstTxnId'],
                            'operator': answer['userInfo']['operator']}
            self.user_date = {}
            for i in comands_info:
                if comands_info[i] is None or comands_info[i] == 'null' or not comands_info[i]:
                    self.user_date[i] = 'Not Stated'
                else:
                    self.user_date[i] = comands_info[i]
        except:
            raise QIWI_ERROR

    def get_info(self):
        return "User: {} {}\nEmail: {}\nRegistration date: {}\nStatus: {}\nLast ip: {}\nLast change password: {}\n" \
               "Last change mobile pin: {}\nNext change password: {}\nNext change mobile pin: {}\n" \
               "Ident info: \n--{}\nDefault alias: {}\nDefault currency: {}\n" \
               "First transaction: {}".format(self.user_date['id'], self.user_date['operator'], self.user_date['email'],
                                              self.user_date['reg_date'], self.user_date['status'],
                                              self.user_date['last_ip'], self.user_date['last_pass_ch'],
                                              self.user_date['last_mob_pin_ch'], self.user_date['next_pass_ch'],
                                              self.user_date['next_mob_pin_ch'],
                                              "\n--".join(map(lambda x: ": ".join(x), self.user_date['ident_info'])),
                                              self.user_date['default_alias'],
                                              self.currency[self.user_date['default_cur']],
                                              self.user_date['first_tr_id'])

    def get_last_transactions(self, rows=10):
        transactions = []

        try:
            answer = run_the_query(self.headers, self.urls["Transactions"][0].format(self.user_date["id"], rows))[
                "data"]
            for i in answer:
                transactions.append(["Name: {}".format(i["view"]["title"] + "\n      " + i["view"]["account"]),
                                     "Data: {}".format(i["date"]),
                                     "Status: {}".format(i["status"]),
                                     "Error: {}".format(i["error"]),
                                     "Commission: {} {}".format(i["commission"]["amount"],
                                                                self.currency[i["commission"]["currency"]]),
                                     "Total: {} {}".format(i["total"]["amount"],
                                                           self.currency[i["total"]["currency"]])])
        except:
            raise TRANSACTION_NOT_FOUND

        return "\n------------------------\n".join(["\n".join(i) for i in transactions])

    def get_info_about_transaction(self, transaction_id):
        try:
            answer = run_the_query(self.headers, self.urls["Transaction"][0].format(transaction_id))
            return "\n".join(["Name: {}".format(answer["view"]["title"] + "\n      " + answer["view"]["account"]),
                              "Data: {}".format(answer["date"]),
                              "Status: {}".format(answer["status"]),
                              "Error: {}".format(answer["error"]),
                              "Commission: {} {}".format(answer["commission"]["amount"],
                                                         self.currency[answer["commission"]["currency"]]),
                              "Total: {} {}".format(answer["total"]["amount"],
                                                    self.currency[answer["total"]["currency"]])])
        except:
            raise TRANSACTION_NOT_FOUND
