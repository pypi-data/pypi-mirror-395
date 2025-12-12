from sm_bc.crypto.cipher_parameters import CipherParameters
from sm_bc.math.ec_curve import ECCurve
from sm_bc.math.ec_point import ECPoint
from typing import Union, List

class ECDomainParameters(CipherParameters):
    def __init__(self, curve: ECCurve, g: ECPoint, n: int, h: int = 1, seed: Union[bytes, bytearray, List[int]] = None):
        self.curve = curve
        self.g = g
        self.n = n
        self.h = h
        self.seed = seed
    
    def get_curve(self) -> ECCurve:
        """Get the elliptic curve."""
        return self.curve
    
    def get_G(self) -> ECPoint:
        """Get the base point G."""
        return self.g
    
    def get_n(self) -> int:
        """Get the order n of the base point."""
        return self.n
    
    def get_h(self) -> int:
        """Get the cofactor h."""
        return self.h
    
    def get_seed(self) -> Union[bytes, bytearray, List[int], None]:
        """Get the seed (if any)."""
        return self.seed
    
    def equals(self, other: 'ECDomainParameters') -> bool:
        """Check if two domain parameters are equal."""
        if not isinstance(other, ECDomainParameters):
            return False
        return (self.curve.equals(other.curve) if hasattr(self.curve, 'equals') else self.curve == other.curve) and \
               (self.g.equals(other.g) if hasattr(self.g, 'equals') else self.g == other.g) and \
               self.n == other.n and \
               self.h == other.h
    
    def hash_code(self) -> int:
        """Compute hash code for the domain parameters."""
        try:
            h = hash(self.curve)
        except TypeError:
            h = id(self.curve)
        
        try:
            h ^= hash(self.g)
        except TypeError:
            h ^= id(self.g)
        
        h ^= hash(self.n)
        h ^= hash(self.h)
        return h
