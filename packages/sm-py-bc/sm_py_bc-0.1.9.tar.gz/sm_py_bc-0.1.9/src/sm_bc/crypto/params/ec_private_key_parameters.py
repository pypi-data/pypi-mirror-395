from .ec_key_parameters import ECKeyParameters
from .ec_domain_parameters import ECDomainParameters

class ECPrivateKeyParameters(ECKeyParameters):
    def __init__(self, d: int, parameters: ECDomainParameters):
        super().__init__(True, parameters)
        self.d = d
    
    def get_d(self) -> int:
        """Get the private key scalar d."""
        return self.d
