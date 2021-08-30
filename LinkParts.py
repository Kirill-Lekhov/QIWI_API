MAIN_URL = "https://edge.qiwi.com/"

HEADERS = {"Accept": "application/json", "Content-Type": "application/json", "Authorization": "Bearer {}"}

FUNCTIONS = {"Profile": (MAIN_URL+"person-profile/v1/profile/current?", ["authInfoEnabled", "contractInfoEnabled", "userInfoEnabled"]),
             "Balance": (MAIN_URL+"funding-sources/v1/accounts/current", None),
             "Transactions": (MAIN_URL+"payment-history/v2/persons/{}/payments?rows={}", None),
             "Transaction": (MAIN_URL+"payment-history/v2/transactions/{}", None),
             "Check": (MAIN_URL+"payment-history/v1/transactions/{}/cheque/{}?type={}{}", None),
             "Phone pay": (MAIN_URL+"sinap/api/v2/terms/{}/payments", None),
             "Qiwi pay": (MAIN_URL+"sinap/api/v2/terms/99/payments", None)}

CURRENCY = {398: "KZT", 643: "RUB", 840: "USD", 978: "EUR", "Not Stated": "Not Stated"}

IDENTIFICATION = {"ANONYMOUS": "без идентификации",
                  "SIMPLE": "упрощенная идентификация (SIMPLE)",
                  "VERIFIED": "упрощенная идентификация (VERIFIED)",
                  "FULL": "полная идентификация",
                  "Not Stated": "Not Stated"}
