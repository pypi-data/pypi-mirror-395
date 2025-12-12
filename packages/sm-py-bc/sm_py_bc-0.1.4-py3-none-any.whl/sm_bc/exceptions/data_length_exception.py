"""Data length exception."""

from .crypto_exception import CryptoException


class DataLengthException(CryptoException):
    """
    Exception raised when input data length is incorrect.
    
    Reference: org.bouncycastle.crypto.DataLengthException
    """
    pass
