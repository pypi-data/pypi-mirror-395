"""
Cipher parameters with an initialization vector.

Reference: org.bouncycastle.crypto.params.ParametersWithIV
"""

from sm_bc.crypto.cipher_parameters import CipherParameters


class ParametersWithIV(CipherParameters):
    """
    Cipher parameters with an initialization vector (IV).
    
    Used for block cipher modes that require an IV such as CBC, CTR, etc.
    """
    
    def __init__(self, parameters: CipherParameters, iv: bytes):
        """
        Create parameters with IV.
        
        Args:
            parameters: The underlying cipher parameters (e.g., KeyParameter)
            iv: The initialization vector
        """
        self.parameters = parameters
        self.iv = bytes(iv)
    
    def get_iv(self) -> bytes:
        """
        Get the initialization vector.
        
        Returns:
            The IV bytes
        """
        return self.iv
    
    def get_parameters(self) -> CipherParameters:
        """
        Get the underlying parameters.
        
        Returns:
            The underlying cipher parameters
        """
        return self.parameters
