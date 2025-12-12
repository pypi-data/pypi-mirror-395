"""Invalid cipher text exception."""

from .crypto_exception import CryptoException


class InvalidCipherTextException(CryptoException):
    """
    Exception raised when decrypting invalid ciphertext.
    
    Reference: org.bouncycastle.crypto.InvalidCipherTextException
    """
    pass
