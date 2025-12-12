"""
BigIntegers utility class.

Reference: org.bouncycastle.util.BigIntegers (BC-Java)
           src/util/BigIntegers.ts (sm-js-bc)
"""

from typing import Protocol


class RandomProvider(Protocol):
    """Protocol for random number generators."""
    def next_bytes(self, length: int) -> bytes:
        ...


class BigIntegers:
    """Utility methods for BigInt operations."""
    
    @staticmethod
    def as_unsigned_byte_array(length: int, value: int) -> bytes:
        """
        Convert BigInt to unsigned byte array (big-endian) with specified length.
        
        Args:
            length: Byte array length
            value: BigInt value
            
        Returns:
            Byte array representation
        """
        # Convert to bytes (big-endian)
        byte_length = (value.bit_length() + 7) // 8
        if byte_length > length:
            # Truncate if too long
            value_bytes = value.to_bytes(byte_length, 'big')
            return value_bytes[-length:]
        else:
            # Pad with zeros if too short
            return value.to_bytes(length, 'big')
    
    @staticmethod
    def from_unsigned_byte_array(data: bytes) -> int:
        """
        Convert unsigned byte array (big-endian) to BigInt.
        
        Args:
            data: Byte array
            
        Returns:
            BigInt value
        """
        return int.from_bytes(data, 'big')
    
    @staticmethod
    def create_random_big_integer(bit_length: int, random) -> int:
        """
        Create random BigInt with specified bit length.
        
        Args:
            bit_length: Bit length
            random: Random number generator (must have generate_seed method)
            
        Returns:
            Random BigInt
        """
        byte_length = (bit_length + 7) // 8
        random_bytes = random.generate_seed(byte_length)
        
        # Clear excess bits
        excess_bits = byte_length * 8 - bit_length
        if excess_bits > 0:
            mask = (1 << (8 - excess_bits)) - 1
            random_bytes = bytes([random_bytes[0] & mask]) + random_bytes[1:]
        
        return BigIntegers.from_unsigned_byte_array(random_bytes)
    
    @staticmethod
    def bit_length(value: int) -> int:
        """
        Get bit length of BigInt (position of highest 1-bit + 1).
        
        Args:
            value: BigInt value
            
        Returns:
            Bit length
        """
        if value == 0:
            return 0
        if value < 0:
            value = -value
        return value.bit_length()
