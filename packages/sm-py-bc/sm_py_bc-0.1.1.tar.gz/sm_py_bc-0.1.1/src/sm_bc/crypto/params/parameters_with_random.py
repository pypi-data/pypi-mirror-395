from sm_bc.crypto.cipher_parameters import CipherParameters
from sm_bc.util.secure_random import SecureRandom

class ParametersWithRandom(CipherParameters):
    def __init__(self, parameters: CipherParameters, random: SecureRandom = None):
        self.parameters = parameters
        self.random = random if random is not None else SecureRandom()
