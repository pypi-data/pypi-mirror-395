from .ec_key_parameters import ECKeyParameters
from .ec_domain_parameters import ECDomainParameters
from ...math.ec_point import ECPoint

class ECPublicKeyParameters(ECKeyParameters):
    def __init__(self, q: ECPoint, parameters: ECDomainParameters):
        super().__init__(False, parameters)
        self.q = self.validate(q)

    def validate(self, q: ECPoint) -> ECPoint:
        # BC checks if q is valid on curve
        if not q.is_valid():
             raise ValueError("Point not on curve")
        return q
    
    def get_Q(self) -> ECPoint:
        """Get the public key point Q."""
        return self.q
