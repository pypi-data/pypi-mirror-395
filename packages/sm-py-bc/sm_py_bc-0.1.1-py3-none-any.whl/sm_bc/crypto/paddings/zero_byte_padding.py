"""
Zero Byte Padding implementation.

Reference: org.bouncycastle.crypto.paddings.ZeroBytePadding
"""

from typing import Union


class ZeroBytePadding:
    """
    Zero byte padding - pads with zero bytes.
    
    Note: This is ambiguous if data naturally ends with zeros.
    
    Reference: org.bouncycastle.crypto.paddings.ZeroBytePadding
    """
    
    def __init__(self):
        """Initialize Zero Byte Padding."""
        pass
    
    def add_padding(self, data: Union[bytes, bytearray], block_size: int) -> bytearray:
        """
        Add zero byte padding to data.
        
        Args:
            data: The data to pad
            block_size: The block size in bytes
            
        Returns:
            Padded data
            
        Raises:
            ValueError: If block_size is invalid
        """
        if block_size < 1:
            raise ValueError(f'Invalid block size: {block_size}')
        
        # Calculate padding length
        padding_length = block_size - (len(data) % block_size)
        
        # Create padded data
        padded = bytearray(data)
        
        # Add zero bytes (only if not already block-aligned)
        if padding_length < block_size:
            padded.extend(bytes(padding_length))
        
        return padded
    
    def remove_padding(self, data: Union[bytes, bytearray], block_size: int) -> bytearray:
        """
        Remove zero byte padding from data.
        
        Args:
            data: The padded data
            block_size: The block size in bytes
            
        Returns:
            Unpadded data
            
        Raises:
            ValueError: If block_size is invalid
        """
        if block_size < 1:
            raise ValueError(f'Invalid block size: {block_size}')
        
        if len(data) == 0:
            return bytearray()
        
        if len(data) % block_size != 0:
            raise ValueError('Data length is not a multiple of block size')
        
        # Find last non-zero byte
        last_nonzero = len(data) - 1
        while last_nonzero >= 0 and data[last_nonzero] == 0x00:
            last_nonzero -= 1
        
        # Remove padding
        return bytearray(data[:last_nonzero + 1])
    
    def get_padded_length(self, data_length: int, block_size: int) -> int:
        """
        Calculate the length after padding.
        
        Args:
            data_length: The original data length
            block_size: The block size in bytes
            
        Returns:
            Length after padding
        """
        # Zero byte padding doesn't add padding if already block-aligned
        if data_length % block_size == 0:
            return data_length
        padding_length = block_size - (data_length % block_size)
        return data_length + padding_length
