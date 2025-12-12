"""
Parameters for AEAD (Authenticated Encryption with Associated Data) modes.
Used with modes like GCM that provide both encryption and authentication.

@see BouncyCastle AEADParameters.java
"""

from ..cipher_parameters import CipherParameters
from .key_parameter import KeyParameter


class AEADParameters(CipherParameters):
    """Parameters for AEAD modes like GCM."""
    
    def __init__(self, key: KeyParameter, mac_size: int, nonce: bytes, 
                 associated_text: bytes = None):
        """
        Create AEAD parameters.
        
        Args:
            key: The cipher key
            mac_size: The MAC/tag size in bits (must be multiple of 8)
            nonce: The nonce/IV
            associated_text: Optional additional authenticated data (AAD)
        """
        self._key = key
        self._nonce = nonce
        self._mac_size = mac_size
        self._associated_text = associated_text
    
    def get_key(self) -> KeyParameter:
        """Get the cipher key."""
        return self._key
    
    def get_mac_size(self) -> int:
        """Get the MAC size in bits."""
        return self._mac_size
    
    def get_nonce(self) -> bytes:
        """Get the nonce/IV."""
        return self._nonce
    
    def get_associated_text(self) -> bytes:
        """Get the associated text (additional authenticated data)."""
        return self._associated_text
