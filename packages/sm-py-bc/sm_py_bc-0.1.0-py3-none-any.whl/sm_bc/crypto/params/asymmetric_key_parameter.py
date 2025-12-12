from sm_bc.crypto.cipher_parameters import CipherParameters

class AsymmetricKeyParameter(CipherParameters):
    def __init__(self, is_private: bool):
        self.is_private = is_private
