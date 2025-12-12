"""
Utility functions for GCM mode.
Implements Galois field arithmetic for GCM authentication.
"""
from sm_bc.util.pack import Pack


class GCMUtil:
    """Utility functions for GCM mode"""
    
    BLOCK_SIZE = 16
    E1 = 0xe1000000
    
    @staticmethod
    def xor(block: bytearray, val: bytes) -> None:
        """XOR two blocks in-place"""
        for i in range(16):
            block[i] ^= val[i]
    
    @staticmethod
    def as_longs(x: bytes) -> tuple[int, int]:
        """Convert bytes to two 64-bit integers (big-endian)"""
        x0 = Pack.big_endian_to_long(x, 0)
        x1 = Pack.big_endian_to_long(x, 8)
        return (x0, x1)
    
    @staticmethod
    def from_longs(x0: int, x1: int) -> bytes:
        """Convert two 64-bit integers to bytes (big-endian)"""
        result = bytearray(16)
        Pack.long_to_big_endian(x0, result, 0)
        Pack.long_to_big_endian(x1, result, 8)
        return bytes(result)
    
    @staticmethod
    def multiply(x_bytes: bytes, y_bytes: bytes) -> bytes:
        """
        Galois field multiplication in GF(2^128).
        Multiplies two 128-bit blocks.
        """
        # Convert to 32-bit int arrays (4 ints = 128 bits)
        x = [0] * 4
        y = [0] * 4
        
        for i in range(4):
            offset = i * 4
            x[i] = (x_bytes[offset] << 24) | (x_bytes[offset + 1] << 16) | \
                   (x_bytes[offset + 2] << 8) | x_bytes[offset + 3]
            y[i] = (y_bytes[offset] << 24) | (y_bytes[offset + 1] << 16) | \
                   (y_bytes[offset + 2] << 8) | y_bytes[offset + 3]
        
        y0, y1, y2, y3 = y[0], y[1], y[2], y[3]
        z0, z1, z2, z3 = 0, 0, 0, 0
        
        # Process each bit of x
        for i in range(4):
            bits = x[i]
            for j in range(32):
                # Arithmetic shift: -1 if MSB set, 0 otherwise
                m1 = -1 if (bits & 0x80000000) else 0
                bits = (bits << 1) & 0xffffffff
                z0 ^= (y0 & m1) & 0xffffffff
                z1 ^= (y1 & m1) & 0xffffffff
                z2 ^= (y2 & m1) & 0xffffffff
                z3 ^= (y3 & m1) & 0xffffffff
                
                # Shift y right with reduction polynomial
                m2 = ((y3 << 31) >> 8) & 0xffffffff
                y3 = ((y3 >> 1) | (y2 << 31)) & 0xffffffff
                y2 = ((y2 >> 1) | (y1 << 31)) & 0xffffffff
                y1 = ((y1 >> 1) | (y0 << 31)) & 0xffffffff
                y0 = ((y0 >> 1) ^ (m2 & GCMUtil.E1)) & 0xffffffff
        
        # Convert result back to bytes
        result = bytearray(16)
        for i in range(4):
            val = [z0, z1, z2, z3][i]
            offset = i * 4
            result[offset] = (val >> 24) & 0xff
            result[offset + 1] = (val >> 16) & 0xff
            result[offset + 2] = (val >> 8) & 0xff
            result[offset + 3] = val & 0xff
        
        return bytes(result)
    
    @staticmethod
    def increment(counter: bytearray) -> None:
        """Increment the rightmost 32 bits of a counter block"""
        c = 1
        for i in range(15, 11, -1):
            c += counter[i] & 0xff
            counter[i] = c & 0xff
            c >>= 8
