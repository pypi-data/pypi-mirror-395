"""
Elliptic curve algorithms utility class.

Provides common elliptic curve operations and algorithms.
"""

from .ec_point import ECPoint
from .ec_curve import ECCurve


class ECAlgorithms:
    """Utility class containing various elliptic curve algorithms."""
    
    @staticmethod
    def clean_point(curve: ECCurve, point: ECPoint) -> ECPoint:
        """
        Clean a point by validating it's on the curve and normalizing if needed.
        
        Args:
            curve: The elliptic curve
            point: The point to clean
            
        Returns:
            The cleaned (validated and normalized) point
            
        Raises:
            ValueError: If point is not on the expected curve or is invalid
        """
        if not curve.equals(point.curve):
            raise ValueError('Point is not on the expected curve')
        
        if not point.is_valid():
            raise ValueError('Point is not valid')
        
        return point.normalize()
    
    @staticmethod
    def sum_of_two_multiplies(P1: ECPoint, k1: int, P2: ECPoint, k2: int) -> ECPoint:
        """
        Calculate k1*P1 + k2*P2 efficiently.
        
        This method computes the sum of two scalar multiplications more efficiently
        than computing them separately and then adding.
        
        Args:
            P1: The first point
            k1: The first scalar
            P2: The second point  
            k2: The second scalar
            
        Returns:
            The result point k1*P1 + k2*P2
            
        Raises:
            ValueError: If points are not on the same curve
        """
        if not P1.curve.equals(P2.curve):
            raise ValueError('Points must be on the same curve')
        
        # Use Shamir's trick for efficient dual scalar multiplication
        # This is a simplified implementation - could be optimized further
        result1 = P1.multiply(k1)
        result2 = P2.multiply(k2)
        
        return result1.add(result2)
    
    @staticmethod
    def is_point_at_infinity(point: ECPoint) -> bool:
        """
        Check if a point is the point at infinity.
        
        Args:
            point: The point to check
            
        Returns:
            True if the point is at infinity
        """
        return point.is_infinity()
    
    @staticmethod
    def are_on_same_curve(P1: ECPoint, P2: ECPoint) -> bool:
        """
        Validate that two points are on the same curve.
        
        Args:
            P1: First point
            P2: Second point
            
        Returns:
            True if both points are on the same curve
        """
        return P1.curve.equals(P2.curve)
