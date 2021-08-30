class QiwiError(Exception):
    pass


class QiwiSyntaxError(QiwiError):
    def __init__(self):
        self.text = "Query execution failed"


class TokenError(QiwiError):
    def __init__(self):
        self.text = "Wrong TOKEN"


class NoRightsError(QiwiError):
    def __init__(self):
        self.text = "No right"


class TransactionNotFound(QiwiError):
    def __init__(self):
        self.text = "Transaction not found or missing payments with specified characteristics"


class WalletError(QiwiError):
    def __init__(self):
        self.text = "Wallet not found"


class HistoryError(QiwiError):
    def __init__(self):
        self.text = "Too many requests, the service is temporarily unavailable"


class MapError(QiwiError):
    def __init__(self):
        self.text = "Map processing errors"


class NotFoundAddress(MapError):
    def __init__(self):
        self.text = "Could not find address"


class CheckError(QiwiError):
    def __init__(self):
        self.text = "Could not get check"


class WrongEmail(CheckError):
    def __init__(self):
        self.text = "Wrong Email address"


class WrongNumber(QiwiError):
    def __init__(self):
        self.text = "Wrong phone number"


class TransactionError(QiwiError):
    def __init__(self):
        self.text = "Failed to carry out the transaction"
