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
                     "Balance": ("https://edge.qiwi.com/funding-sources/v1/accounts/current", None)}

        self.currency = {643: "RUB",
                         840: "USD",
                         978: "EUR",
                         "Not Stated": "Not Stated"}
        self.identification = {"ANONYMOUS": "без идентификации",
                               "SIMPLE": "упрощенная идентификация (SIMPLE)",
                               "VERIFIED": "упрощенная идентификация (VERIFIED)",
                               "FULL": "полная идентификация",
                               "Not Stated": "Not Stated"}

        if not run_the_query(self.headers, self.urls["Profile"][0]):
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

    def get_info(self):
        answer = run_the_query(self.headers, self.urls["Profile"][0])

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
            prepared_date = {}
            for i in comands_info:
                if comands_info[i] is None or comands_info[i] == 'null' or not comands_info[i]:
                    prepared_date[i] = 'Not Stated'
                else:
                    prepared_date[i] = comands_info[i]
        except:
            raise QIWI_ERROR

        return "User: {} {}\nEmail: {}\nRegistration date: {}\nStatus: {}\nLast ip: {}\nLast change password: {}\n" \
               "Last change mobile pin: {}\nNext change password: {}\nNext change mobile pin: {}\n" \
               "Ident info: \n--{}\nDefault alias: {}\nDefault currency: {}\n" \
               "First transaction: {}".format(prepared_date['id'], prepared_date['operator'], prepared_date['email'],
                                              prepared_date['reg_date'], prepared_date['status'],
                                              prepared_date['last_ip'], prepared_date['last_pass_ch'],
                                              prepared_date['last_mob_pin_ch'], prepared_date['next_pass_ch'],
                                              prepared_date['next_mob_pin_ch'],
                                              "\n--".join(map(lambda x: ": ".join(x), prepared_date['ident_info'])),
                                              prepared_date['default_alias'],
                                              self.currency[prepared_date['default_cur']],
                                              prepared_date['first_tr_id'])

