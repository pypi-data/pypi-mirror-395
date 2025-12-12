from sm_bc.crypto.params.asymmetric_key_parameter import AsymmetricKeyParameter
from sm_bc.crypto.params.ec_domain_parameters import ECDomainParameters

class ECKeyParameters(AsymmetricKeyParameter):
    def __init__(self, is_private: bool, parameters: ECDomainParameters):
        super().__init__(is_private)
        self.parameters = parameters
    
    def get_parameters(self) -> ECDomainParameters:
        """Get the domain parameters."""
        return self.parameters
