"""
Utility functions for GCM mode.
Implements Galois field arithmetic for GCM authentication.

@see BouncyCastle GCMUtil.java
"""

from ....util.pack import Pack


class GCMUtil:
    """Utility functions for GCM mode authentication."""
    
    BLOCK_SIZE = 16
    E1 = 0xe1000000
    
    @staticmethod
    def xor(block: bytearray, val: bytes) -> None:
        """XOR two blocks in-place."""
        for i in range(16):
            block[i] ^= val[i]
    
    @staticmethod
    def multiply(x_bytes: bytes, y_bytes: bytes) -> bytes:
        """
        Galois field multiplication in GF(2^128).
        Multiplies two 128-bit blocks.
        
        This implements the algorithm from BouncyCastle's GCMUtil.java multiply method.
        Using 32-bit int processing.
        """
        # Convert to 32-bit int arrays (4 ints = 128 bits)
        x = [0] * 4
        y = [0] * 4
        
        for i in range(4):
            offset = i * 4
            x[i] = ((x_bytes[offset] << 24) | (x_bytes[offset + 1] << 16) | 
                   (x_bytes[offset + 2] << 8) | x_bytes[offset + 3])
            y[i] = ((y_bytes[offset] << 24) | (y_bytes[offset + 1] << 16) | 
                   (y_bytes[offset + 2] << 8) | y_bytes[offset + 3])
            
            # Convert to signed 32-bit
            if x[i] & 0x80000000:
                x[i] -= 0x100000000
            if y[i] & 0x80000000:
                y[i] -= 0x100000000
        
        y0, y1, y2, y3 = y[0], y[1], y[2], y[3]
        z0 = z1 = z2 = z3 = 0
        
        # Process each bit of x
        for i in range(4):
            bits = x[i]
            for j in range(32):
                # Arithmetic shift: -1 if MSB set, 0 otherwise
                m1 = bits >> 31
                bits = (bits << 1) & 0xffffffff
                if bits & 0x80000000:
                    bits -= 0x100000000
                
                z0 ^= (y0 & m1)
                z1 ^= (y1 & m1)
                z2 ^= (y2 & m1)
                z3 ^= (y3 & m1)
                
                # Shift y right with reduction polynomial
                m2 = ((y3 << 31) >> 8) & 0xffffffff
                if m2 & 0x80000000:
                    m2 -= 0x100000000
                
                y3 = ((y3 & 0xffffffff) >> 1) | ((y2 << 31) & 0xffffffff)
                y2 = ((y2 & 0xffffffff) >> 1) | ((y1 << 31) & 0xffffffff)
                y1 = ((y1 & 0xffffffff) >> 1) | ((y0 << 31) & 0xffffffff)
                y0 = (((y0 & 0xffffffff) >> 1) ^ (m2 & GCMUtil.E1)) & 0xffffffff
                
                # Convert back to signed if needed
                if y0 & 0x80000000:
                    y0 -= 0x100000000
                if y1 & 0x80000000:
                    y1 -= 0x100000000
                if y2 & 0x80000000:
                    y2 -= 0x100000000
                if y3 & 0x80000000:
                    y3 -= 0x100000000
        
        # Convert result back to bytes
        result = bytearray(16)
        vals = [z0, z1, z2, z3]
        for i in range(4):
            val = vals[i] & 0xffffffff
            offset = i * 4
            result[offset] = (val >> 24) & 0xff
            result[offset + 1] = (val >> 16) & 0xff
            result[offset + 2] = (val >> 8) & 0xff
            result[offset + 3] = val & 0xff
        
        return bytes(result)
    
    @staticmethod
    def increment(counter: bytearray) -> None:
        """Increment the rightmost 32 bits of a counter block."""
        c = 1
        for i in range(15, 11, -1):
            c += counter[i] & 0xff
            counter[i] = c & 0xff
            c >>= 8
