"""
Secure random number generator.

Uses Python's secrets module for cryptographically strong random numbers.

Reference: src/util/SecureRandom.ts (sm-js-bc)
          java.security.SecureRandom
"""

import secrets
from typing import Union


class SecureRandom:
    """
    Cryptographically strong random number generator.
    
    Uses Python's secrets module which provides access to the most secure
    source of randomness that the operating system provides.
    """
    
    def next_bytes(self, data: Union[bytearray, memoryview]) -> None:
        """
        Fill the specified byte array with random bytes.
        
        Args:
            data: The byte array to fill with random bytes
            
        Note:
            This method modifies the input array in-place, matching the
            behavior of Java's SecureRandom.nextBytes() and JS implementation.
        """
        random_bytes = secrets.token_bytes(len(data))
        data[:] = random_bytes
    
    def generate_seed(self, length: int) -> bytearray:
        """
        Generate a seed of random bytes.
        
        Args:
            length: The number of random bytes to generate
            
        Returns:
            A bytearray containing the random bytes
        """
        return bytearray(secrets.token_bytes(length))
    
    def next_int(self) -> int:
        """
        Returns a random 32-bit integer.
        
        Returns:
            A random integer in the range [0, 2^32)
        """
        return int.from_bytes(secrets.token_bytes(4), 'big')
