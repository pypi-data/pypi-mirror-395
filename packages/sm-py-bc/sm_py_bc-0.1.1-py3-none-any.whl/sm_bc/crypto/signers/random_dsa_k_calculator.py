"""
Random k calculator for DSA-style signatures.

This implementation generates cryptographically secure random k values
for each signature operation. Each k value is uniformly distributed
in the range [1, n-1] where n is the curve order.

Based on: org.bouncycastle.crypto.signers.RandomDSAKCalculator
"""

from typing import Optional
from .dsa_k_calculator import DSAKCalculator
from ...util.secure_random import SecureRandom
from ...util.big_integers import BigIntegers


class RandomDSAKCalculator(DSAKCalculator):
    """Random DSA k value calculator."""
    
    def __init__(self):
        self._q: Optional[int] = None
        self._random: Optional[SecureRandom] = None
    
    def init(self, n: int, random: SecureRandom) -> None:
        """
        Initialize with curve order and random source.
        
        Args:
            n: Order of the curve
            random: Secure random number generator
            
        Raises:
            ValueError: If n <= 1
        """
        if n <= 1:
            raise ValueError('Order must be greater than 1')
        
        self._q = n
        self._random = random
    
    def next_k(self) -> int:
        """
        Generate next random k value.
        
        Returns:
            Random k value in range [1, q-1]
            
        Raises:
            RuntimeError: If calculator not initialized
        """
        if self._q is None or self._random is None:
            raise RuntimeError('Calculator not initialized')
        
        bit_length = self._get_bit_length(self._q)
        
        # Generate random k in range [1, q-1]
        k = 0
        while True:
            k = BigIntegers.create_random_big_integer(bit_length - 1, self._random)
            # Ensure k is in the correct range
            if k == 0:
                k = 1
            if k < self._q:
                break
        
        return k
    
    def is_deterministic(self) -> bool:
        """
        This is a non-deterministic (random) calculator.
        
        Returns:
            False (this calculator is non-deterministic)
        """
        return False
    
    def _get_bit_length(self, value: int) -> int:
        """
        Calculate bit length of an integer.
        
        Args:
            value: Integer value
            
        Returns:
            Number of bits needed to represent value
        """
        if value == 0:
            return 0
        
        bit_length = 0
        temp = value
        while temp > 0:
            bit_length += 1
            temp = temp >> 1
        
        return bit_length
