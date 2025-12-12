from typing import Protocol
from sm_bc.math.ec_point import ECPoint

class ECMultiplier(Protocol):
    def multiply(self, p: ECPoint, k: int) -> ECPoint:
        ...

class AbstractECMultiplier(ECMultiplier):
    def multiply(self, p: ECPoint, k: int) -> ECPoint:
        if p.is_infinity or k == 0:
            return p.curve.get_infinity()
        
        if k < 0:
            p = p.negate()
            k = -k
            
        return self.multiply_positive(p, k)

    def multiply_positive(self, p: ECPoint, k: int) -> ECPoint:
        raise NotImplementedError
        
class SimpleMultiplier(AbstractECMultiplier):
    def multiply_positive(self, p: ECPoint, k: int) -> ECPoint:
        return p.multiply(k)


class FixedPointCombMultiplier(AbstractECMultiplier):
    """
    Fixed-point comb multiplier for efficient scalar multiplication.
    This is an optimized multiplier that uses precomputation for fixed points.
    For now, it uses the standard multiplication algorithm.
    """
    
    def multiply_positive(self, p: ECPoint, k: int) -> ECPoint:
        """
        Multiply point p by scalar k using comb method.
        
        Args:
            p: The point to multiply
            k: The scalar multiplier (positive)
            
        Returns:
            The result point k*p
        """
        # For now, use standard multiplication
        # TODO: Implement actual comb method with precomputation
        return p.multiply(k)
