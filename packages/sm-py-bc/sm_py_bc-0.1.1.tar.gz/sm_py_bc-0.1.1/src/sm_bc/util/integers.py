"""
Utility functions for integer operations.

Provides bit manipulation and other integer utilities similar to Java's Integer class.
All operations treat integers as 32-bit signed values.

Reference: src/util/Integers.ts (sm-js-bc)
"""


class Integers:
    """
    Integer utility functions for bit manipulation.
    
    All methods treat integers as 32-bit signed values, matching Java/TypeScript behavior.
    """
    
    @staticmethod
    def _to_int32(i: int) -> int:
        """Convert Python int to 32-bit signed integer."""
        # Mask to 32 bits and interpret as signed
        i = i & 0xFFFFFFFF
        if i >= 0x80000000:
            i -= 0x100000000
        return i
    
    @staticmethod
    def number_of_leading_zeros(i: int) -> int:
        """
        Returns the number of zero bits preceding the highest-order one-bit.
        Returns 32 if the number is zero.
        
        Args:
            i: The value whose number of leading zero bits to compute
            
        Returns:
            The number of zero bits preceding the highest-order one-bit (0-32)
        """
        # Convert to 32-bit integer
        i = Integers._to_int32(i)
        
        if i == 0:
            return 32
        
        # Handle negative numbers (MSB is set)
        if i < 0:
            return 0
        
        n = 1
        if (i >> 16) == 0:
            n += 16
            i <<= 16
        if (i >> 24) == 0:
            n += 8
            i <<= 8
        if (i >> 28) == 0:
            n += 4
            i <<= 4
        if (i >> 30) == 0:
            n += 2
            i <<= 2
        n -= (i >> 31) & 1
        
        return n
    
    @staticmethod
    def bit_count(i: int) -> int:
        """
        Returns the number of one-bits in the two's complement binary representation.
        
        Args:
            i: The value whose bits to count
            
        Returns:
            The number of one-bits
        """
        # Convert to 32-bit integer
        i = Integers._to_int32(i)
        # Make unsigned for bit operations
        i = i & 0xFFFFFFFF
        
        # Brian Kernighan's algorithm
        i = i - ((i >> 1) & 0x55555555)
        i = (i & 0x33333333) + ((i >> 2) & 0x33333333)
        i = (i + (i >> 4)) & 0x0F0F0F0F
        i = i + (i >> 8)
        i = i + (i >> 16)
        return i & 0x3F
    
    @staticmethod
    def rotate_left(i: int, distance: int) -> int:
        """
        Returns the value obtained by rotating left by the specified number of bits.
        
        Args:
            i: The value whose bits to rotate left
            distance: The number of bit positions to rotate by
            
        Returns:
            The value obtained by rotating left
        """
        # Convert to 32-bit integer
        i = Integers._to_int32(i)
        i = i & 0xFFFFFFFF  # Make unsigned
        distance = distance & 31  # Only use lower 5 bits
        
        result = ((i << distance) | (i >> (32 - distance))) & 0xFFFFFFFF
        return Integers._to_int32(result)
    
    @staticmethod
    def rotate_right(i: int, distance: int) -> int:
        """
        Returns the value obtained by rotating right by the specified number of bits.
        
        Args:
            i: The value whose bits to rotate right
            distance: The number of bit positions to rotate by
            
        Returns:
            The value obtained by rotating right
        """
        # Convert to 32-bit integer
        i = Integers._to_int32(i)
        i = i & 0xFFFFFFFF  # Make unsigned
        distance = distance & 31  # Only use lower 5 bits
        
        result = ((i >> distance) | (i << (32 - distance))) & 0xFFFFFFFF
        return Integers._to_int32(result)
    
    @staticmethod
    def number_of_trailing_zeros(i: int) -> int:
        """
        Returns the number of zero bits following the lowest-order one-bit.
        Returns 32 if the number is zero.
        
        Args:
            i: The value whose number of trailing zero bits to compute
            
        Returns:
            The number of zero bits following the lowest-order one-bit (0-32)
        """
        # Convert to 32-bit integer
        i = Integers._to_int32(i)
        
        if i == 0:
            return 32
        
        # Count trailing zeros using bit manipulation
        # Isolate the rightmost 1-bit: i & -i
        # Count position of that bit
        count = 0
        i_unsigned = i & 0xFFFFFFFF
        
        if (i_unsigned & 0xFFFF) == 0:
            count += 16
            i_unsigned >>= 16
        if (i_unsigned & 0xFF) == 0:
            count += 8
            i_unsigned >>= 8
        if (i_unsigned & 0xF) == 0:
            count += 4
            i_unsigned >>= 4
        if (i_unsigned & 0x3) == 0:
            count += 2
            i_unsigned >>= 2
        if (i_unsigned & 0x1) == 0:
            count += 1
        
        return count
    
    @staticmethod
    def highest_one_bit(i: int) -> int:
        """
        Returns the highest one bit of the specified number.
        
        Args:
            i: The value whose highest one bit to compute
            
        Returns:
            The highest one bit, or 0 if i is 0
        """
        # Convert to 32-bit integer
        i = Integers._to_int32(i)
        i = i & 0xFFFFFFFF  # Make unsigned
        
        i |= (i >> 1)
        i |= (i >> 2)
        i |= (i >> 4)
        i |= (i >> 8)
        i |= (i >> 16)
        result = (i - (i >> 1)) & 0xFFFFFFFF
        return Integers._to_int32(result)
    
    @staticmethod
    def lowest_one_bit(i: int) -> int:
        """
        Returns the lowest one bit of the specified number.
        
        Args:
            i: The value whose lowest one bit to compute
            
        Returns:
            The lowest one bit, or 0 if i is 0
        """
        # Convert to 32-bit integer
        i = Integers._to_int32(i)
        
        # Two's complement trick: i & -i isolates lowest bit
        result = (i & -i) & 0xFFFFFFFF
        return Integers._to_int32(result)
