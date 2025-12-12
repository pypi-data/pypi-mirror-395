from typing import Union, MutableSequence, List

class Pack:
    """
    Utility class for packing/unpacking bytes to integers.
    Note: Unlike Java/JS, this implementation returns Unsigned Integers by default
    to suit Python's handling of bitwise operations.
    """

    @staticmethod
    def big_endian_to_int(bs: Union[bytes, bytearray, List[int]], off: int) -> int:
        """
        Reads a 32-bit unsigned integer from the byte buffer at the specified offset.
        """
        n = bs[off] << 24
        n |= (bs[off + 1] & 0xff) << 16
        n |= (bs[off + 2] & 0xff) << 8
        n |= (bs[off + 3] & 0xff)
        return n

    @staticmethod
    def int_to_big_endian(val: int, bs: MutableSequence[int], off: int) -> None:
        """
        Writes a 32-bit integer to the byte buffer at the specified offset.
        """
        bs[off] = (val >> 24) & 0xff
        bs[off + 1] = (val >> 16) & 0xff
        bs[off + 2] = (val >> 8) & 0xff
        bs[off + 3] = val & 0xff

    @staticmethod
    def big_endian_to_long(bs: Union[bytes, bytearray, List[int]], off: int) -> int:
        """
        Reads a 64-bit unsigned integer from the byte buffer.
        """
        hi = Pack.big_endian_to_int(bs, off)
        lo = Pack.big_endian_to_int(bs, off + 4)
        return (hi << 32) | (lo & 0xffffffff)

    @staticmethod
    def long_to_big_endian(val: int, bs: MutableSequence[int], off: int) -> None:
        """
        Writes a 64-bit integer to the byte buffer.
        """
        # In Python, right shift of negative numbers behaves differently (arithmetic shift),
        # but for packing we typically deal with the bit pattern.
        # We mask to ensure we get the bits we expect.
        
        # High 32 bits
        hi = (val >> 32) & 0xffffffff
        # Low 32 bits
        lo = val & 0xffffffff
        
        Pack.int_to_big_endian(hi, bs, off)
        Pack.int_to_big_endian(lo, bs, off + 4)
