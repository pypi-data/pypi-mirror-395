from sm_bc.crypto.cipher_parameters import CipherParameters

class AsymmetricKeyParameter(CipherParameters):
    def __init__(self, is_private_key: bool):
        self._is_private = is_private_key
    
    def is_private(self) -> bool:
        """Check if this is a private key parameter."""
        return self._is_private
